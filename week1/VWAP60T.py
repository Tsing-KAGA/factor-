#!/usr/bin/env Python
# -*- coding:utf-8 -*-
# author: mqh
import time

import numpy as np
import pandas as pd
from FactorModule.FactorBase import FactorBase
from DataReaderModule.Constants import ALIAS_FIELDS as t

class Factor(FactorBase):

    def __init__(self):
        super(Factor,self).__init__()
        self.neutral = True
        self.factorName = __name__.split('.')[-1]
        self.needFields = [t.CLOSE,t.VOLUME]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        length = 60;
        needData = self.needData# 计算所需数据
        close = needData[t.CLOSE]
        vol = needData[t.VOLUME]
        closelist = [close];vollist=[vol]
        for i in range(length-1):
            closelist.append(self.calculator.Delay(close,i+1))
            vollist.append(self.calculator.Delay(vol,i + 1))
        s=0
        for i in range(length):
            s += closelist[i]*vollist[i]
        factor=sum(closelist)/s

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()
