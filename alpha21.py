# coding=utf8
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
        self.needFields = [t.CLOSE, t.OPEN, t.VOLUME,t.HIGH,t.LOW,t.ADJFCT]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        length = 5
        needData = self.needData  # 计算所需数据
        close = needData[t.CLOSE]
        open = needData[t.OPEN]
        vol = needData[t.VOLUME]
        high=needData[t.HIGH]
        high20=self.calculator.Mean(high,20)
        adv20 = self.calculator.Mean(vol, 20)
        factor=(high20<high)*(-1*self.calculator.Diff(high,2))+(high20>=high)*(self.calculator.Diff(high,20))
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()


fct = Factor()
fct.run_factor()
