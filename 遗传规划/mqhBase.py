#coding=utf8
__author__ = 'wangjp'

import os
import time
import numpy as np
import pandas as pd
import gc
from DataReaderModule.DataReaderMat import DataReaderMat
from DataReaderModule.Constants import ALIAS_FIELDS as alf
from DataReaderModule.Constants import ALIAS_RESPONSE as alr
from DataReaderModule.Constants import ALIAS_TABLES as alt
from FactorModule.__update__ import update
from FactorModule.FactorIO import FactorIO
from FactorModule.FactorScore import FactorScores
from FactorModule.FactorTests import FactorTests
from FactorModule.FactorRisks import FactorRisks
from CalculatorModule.CalculatorMatrix import Calculator
from DataReaderModule.Constants import ALIAS_FIELDS as alf
from DataReaderModule.Constants import ALIAS_INDICATORS as ali

class FactorBase:

    dataReader = None
    factorIO = None
    factorRisk = None

    def __init__(self):
        self.needFields = None
        self.needTableFields = None
        self.factorName = None
        self.neutral = False
        self.isRiskFactor = False
        self.scoreObj = FactorScores()
        self.testsObj = FactorTests()
        if FactorBase.factorIO is None:
            FactorBase.factorIO = FactorIO(fctDataPath=update.fctDataPath)
        if FactorBase.dataReader is None:
            FactorBase.dataReader = DataReaderMat()
        if FactorBase.factorRisk is None:
            FactorBase.factorRisk = FactorRisks(fctDataPath=update.fctDataPath, riskFctPath=update.riskDataPath)
        self.headDate = self.dataReader.calendar._calibrate_date(currDate=20070630, currSide='right')
        # self.headDate = self.dataReader.calendar._calibrate_date(currDate=20180101, currSide='right')
        self.tailDate = self.dataReader.calendar._tradeDates[-1]
        self.calculator = Calculator()

    def factor_definition(self):
        raise NotImplementedError

    def run(self):
        """
        完成 因子的 计算，打分，测试，入库 等
        :return:
        """
        start = time.time()

        if not update.startOver:    # 提取因子上次更新日期
            lastUpdt = self.factorIO.factor_last_update(factorName=self.factorName, fromMat=True)
            self.headDate = self.dataReader.calendar.tdaysoffset(1, lastUpdt)
            if lastUpdt == self.headDate:
                print('factor {0} already updated to latest date {1}'.format(self.factorName, lastUpdt))
                return
            else:
                print('factor {0} last updated date {1}'.format(self.factorName, lastUpdt))
        updateDateNum = self.dataReader.calendar.tdayscount(headDate=self.headDate,
                                                            tailDate=self.tailDate,
                                                            selectType='CloseClose')

        print('updating factor {0} from {1} to {2}, {3} days, {4}'.format(self.factorName,
                                                                          self.headDate,
                                                                          self.tailDate,
                                                                          updateDateNum,
                                                                          'start new' if update.startOver else 'update exist'))

        # 注1 ： 因子更新 数据需要部分 日期提前，取决于因子定义 : 目前采取设定一个较长日期 如240天，确保对绝大多数因子都满足
        cutDate = self.dataReader.calendar.tdaysoffset(currDates=self.headDate, num=-update.preDateNum)
        # 注2 ： 风险因子需要更长一点
        if self.isRiskFactor:
            self.headDate = self.dataReader.calendar.tdaysoffset(currDates=self.headDate, num=-20)
        # 注3 ： 因子指标 上一次计算结尾， 最新数据的指标是 nan， 因为未来收益率尚不存在，新数据更新以后需要把这些部分也补上
        respCutDate = self.dataReader.calendar.tdaysoffset(currDates=self.headDate, num=-10)  # 目前最长的收益天数
        ########  提取需要的数据字段  ########
        case1 = alf.TRDSTAT not in self.needFields
        case2 = (self.needTableFields is None) or (alf.TRDSTAT not in self.needTableFields.get(alt.TRAEDINFO, []))
        if case1 and case2:
            self.needFields.append(alf.TRDSTAT)
        needData = self.dataReader.get_data(fields=self.needFields,
                                            tableFields=self.needTableFields,
                                            headDate=cutDate,
                                            tailDate=self.tailDate,
                                            selectType='CloseClose',
                                            useCache=update.useCache)
        self.needData = {}
        for table in needData:
            if (self.needTableFields is not None) and (table in self.needTableFields):
                self.needData[table] = needData[table]        # 明确通过 表名: 字段 字典方式提取的数据不会展开
            for field in needData[table]:
                if self.needData.get(field) is None:
                    self.needData[field] = needData[table][field]
        invalidIdx = self.needData[alf.TRDSTAT].isin([5, 6])        # 把无效交易日对应的数据点设为空值
        for table in self.needData:
            if (self.needTableFields is not None) and (table in self.needTableFields):
                for field in self.needData[table]:
                    self.needData[table][field][invalidIdx] = np.nan
            else:
                if table != alf.TRDSTAT:
                    self.needData[table][invalidIdx] = np.nan
        ####### 因子计算, 及原始因子值处理 ########
        rawFactor = self.factor_definition()
        rawFactor.sort_index(inplace=True)
        # 从respCuteDate 开始
        idx = pd.IndexSlice
        rawFactor = rawFactor.loc[idx[respCutDate:self.tailDate], :]
        # 对风格因子进行 空缺值 填充, 无效交易日，无效因子值处理
        if self.isRiskFactor:
            rawFactor = rawFactor.fillna(method='ffill')
        rawFactor[invalidIdx] = np.nan
        rawFactor[np.isinf(rawFactor)] = np.nan
        riskFactors = os.listdir(update.riskDataPath)       # 提取 风险因子
        if self.neutral and (not self.isRiskFactor):        # 进行 风格中性处理
            rawFactor = self.factorRisk.neutralizeMat(factorData=rawFactor,
                                                      headDate=respCutDate,
                                                      tailDate=self.tailDate,
                                                      riskFactors=riskFactors,
                                                      selectType='CloseClose',
                                                      useCache=True)
            print(self.factorName, ' neutralized')
        # 获取filter X
        filterX = self.dataReader.get_data(headDate=respCutDate,
                                           tailDate=self.tailDate,
                                           selectType='CloseClose',
                                           fields=['FilterX'],
                                           useCache=update.useCache)[alt.XFILTER]['FilterX']
        filterX = filterX.astype(np.int) == 1
        # 因子打分
        factorScores = self.scoreObj.factor_scores_section_mat(factorName=self.factorName,
                                                               rawFactor=rawFactor,
                                                               filterX=filterX)
        # 因子存储
        ifExist = 'replace' if update.startOver else 'append'
        headStart = self.headDate if update.startOver else self.dataReader.calendar.tdaysoffset(num=1, currDates=lastUpdt)

        # 提取收益率
        responseFields = [alr.OC1, alr.OCG1, alr.OCG2, alr.CCG1, alr.CCG2]
        stockResponse = self.dataReader.get_data(headDate=respCutDate,
                                                 tailDate=self.tailDate,
                                                 selectType='CloseClose',
                                                 useCache=update.useCache,
                                                 fields=responseFields)[alt.RESPONSE]
        # 计算因子 统计量
        factorIndicators = self.testsObj.factor_indicators_section_mat(factorName=self.factorName,
                                                                       factorScores=factorScores,
                                                                       stockRets=stockResponse,indicators=[ali.TBDF])
        # 因子统计量 存储
        self.factorIO.write_factor_indcators(factorName=self.factorName,
                                             factorIndicators=factorIndicators,
                                             cutDate=respCutDate,
                                             startNew=update.startOver)
        # 计算因子 截面自相关性
        print('Factor {0} updated from {1} to {2}, {3} days, with {4} seconds \n'.format(self.factorName,
                                                                                      self.headDate,
                                                                                      self.tailDate,
                                                                                      updateDateNum,
                                                                                      time.time() - start))
        idx = pd.IndexSlice
        factorAutocorr = self.testsObj.factor_autocorr_section_mat(factorName=self.factorName,
                                                                   factorZScores=factorScores[
                                                                                     self.factorName + '_zscore'].loc[
                                                                                 idx[respCutDate:self.tailDate], :])
        self.factorIO.write_factor_autocorr(factorName=self.factorName,
                                            factorAutocorr=factorAutocorr,
                                            headDate=headStart,
                                            ifExist=ifExist,
                                            checkExist=True)
        for x in locals().keys():
            del locals()[x]
        gc.collect()