#思路： 2.21*Rank(Corr((close-open),Delay(volume,1),15))+0.7*Rank(-1*(close-open))+0.73*.Rank(FindRank(Delay(-1*PCTCHG,6),5))+Rank(abs(Corr(vwap,Mean(volume,20),6)))+0.6*Rank((Mean(close,200)-open)*(close-open))
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
        self.needFields = [t.HIGH,t.LOW,t.CLOSE,t.OPEN,t.VOLUME,t.PCTCHG,t.VWAP]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData  # 计算所需数据
        close=needData[t.CLOSE]
        open=needData[t.OPEN]
        vol = needData[t.VOLUME]
        vwap=needData[t.VWAP]
        adv20=self.calculator.Mean(vol,20)
        ret=needData[t.PCTCHG]
        uprange=(close-open)
        beta1=self.calculator.Rank(self.calculator.Corr(uprange,self.calculator.Delay(vol,1),15))
        beta2=self.calculator.Rank(-1*uprange)
        beta3=self.calculator.Rank(self.calculator.FindRank(self.calculator.Delay(-1*ret,6),5))
        beta4=self.calculator.Rank(abs(self.calculator.Corr(vwap,adv20,6)))
        beta5=self.calculator.Rank((self.calculator.Mean(close,200)-open)*(close-open))

        factor = 2.21*beta1+0.7*beta2+0.73*beta3+beta4+0.6*beta5
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()


fct = Factor()
fct.run_factor()
