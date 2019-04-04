#思路： (2*close-high-low)/(high-low)-self.calculator.Delay((2*close-high-low)/(high-low),9)
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
        self.neutral = False
        self.factorName = __name__.split('.')[-1]
        self.needFields = [t.HIGH,t.CLOSE,t.LOW]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        length = 5;
        needData = self.needData# 计算所需数据
        high = needData[t.HIGH]
        close=needData[t.CLOSE]
        low=needData[t.LOW]
        r1 = (2*close-high-low)/(high-low)
        r2 = self.calculator.Delay(r1,9)
        factor = r1-r2

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()
