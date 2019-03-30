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
        prevol = self.calculator.Mean(vol,10)
        adjOpen = needData[t.OPEN]*needData[t.ADJFCT]
        adjLow = needData[t.LOW] * needData[t.ADJFCT]
        adjHigh = needData[t.HIGH] * needData[t.ADJFCT]
        adjClose = needData[t.CLOSE] * needData[t.ADJFCT]
        r1 = self.calculator.Rank((close - open) / open)
        r2 = self.calculator.Rank((adjClose-adjOpen)/adjOpen)
        q1 = self.calculator.Rank(r1)
        q2 = self.calculator.Rank(r2)
        corr = self.calculator.Decaylinear(self.calculator.Corr(r1, r2, 20),5)
        factor = (vol>=prevol)*(-1 * corr)+(vol<prevol)*corr
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()


fct = Factor()
fct.run_factor()
