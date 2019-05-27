# coding=utf8
__author__ = 'wangjp'

import time

import numpy as np
import pandas as pd
from FactorModule.FactorBase import FactorBase
from DataReaderModule.Constants import ALIAS_FIELDS as t

class Factor(FactorBase):

    def __init__(self):
        super(Factor,self).__init__()
        self.neutral = False
        self.factorName = __name__.split('.')[-1]
        self.needFields = [t.VALUE_DIFF_INSTITUTE_ACT_MONEYFVALUE_DIFF_LARGE_TRADER_PCT_VALUE, t.VALUE_DIFF_LARGE_TRADER, t.VALUE_DIFF_INSTITUTE_ACT, t.ADJFCT, t.TRDSTAT]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据

        adjLow = needData[t.VALUE_DIFF_LARGE_TRADER] * needData[t.ADJFCT]
        adjHigh = needData[t.VALUE_DIFF_INSTITUTE_ACT_MONEYFVALUE_DIFF_LARGE_TRADER_PCT_VALUE] * needData[t.ADJFCT]
        adjClose = needData[t.VALUE_DIFF_INSTITUTE_ACT] * needData[t.ADJFCT]
        preClose = self.calculator.Delay(x=adjClose, num=1)
        distrib = (adjClose >= preClose)*(adjClose - self.calculator.cmpMin(preClose, adjLow)) + (adjClose < preClose)*(adjClose - self.calculator.cmpMax(preClose, adjHigh))
        factor = -self.calculator.Sum(x=distrib, num=5) / adjClose

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()