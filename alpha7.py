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
        self.needFields = [t.VOLUME, t.CLOSE]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        length = 5
        needData = self.needData  # 计算所需数据
        close = needData[t.CLOSE]
        vol=needData[t.VOLUME]
        adv20=self.calculator.Mean(vol,20)
        declose=self.calculator.Diff(close,7).applymap(lambda x:abs(x))
        siclose=self.calculator.Diff(close,7).applymap(lambda x:np.sign(x))
        r1=-1*self.calculator.Rank(declose,60)
        factor =(adv20<vol)*(r1*siclose)+(adv20>=vol)*close.applymap(lambda x:1)
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()


fct = Factor()
fct.run_factor()
