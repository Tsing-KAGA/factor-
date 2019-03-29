# coding=utf8
#该因子通过检验
__author__ = 'mqh'
import time

import numpy as np
import pandas as pd
import math
from FactorModule.FactorBase import FactorBase
from DataReaderModule.Constants import ALIAS_FIELDS as t


class Factor(FactorBase):

    def __init__(self):
        super(Factor, self).__init__()
        self.neutral = False
        self.factorName = __name__.split('.')[-1]
        self.needFields = [t.HIGH,t.LOW]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData  # 计算所需数据
        high=needData[t.HIGH]
        low=needData[t.LOW]
        weightnow=self.calculator.RegBeta(high,low,10)
        weightlist=self.calculator.RegBeta(high,low,18)
        weightmean=self.calculator.Mean(weightlist,600)
        weightstd=self.calculator.Std(weightlist,600)
        zscore=(weightnow-weightmean)/weightstd

        factor = zscore
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()


fct = Factor()
fct.run_factor()
