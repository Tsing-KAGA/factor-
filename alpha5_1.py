#!/usr/bin/env Python
# -*- coding:utf-8 -*-
# author: mqh
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
        self.needFields = [t.VWAP, t.CLOSE,t.OPEN]  # 设置需要的字段

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
        vwap = needData[t.VWAP]
        mvwap = self.calculator.Mean(vwap,10)
        r1 = self.calculator.Rank(open-mvwap)
        #r1 = self.calculator.Decaylinear(r1,5)
        r2 = -1*self.calculator.Rank(close-vwap)
        #r2 = self.calculator.Decaylinear(r2,5)

        factor = self.calculator.Decaylinear(r1*r2,5)
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()


fct = Factor()
fct.run_factor()
