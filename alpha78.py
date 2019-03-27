# coding=utf8
__author__ = 'mqh'
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
        self.needFields = [t.HIGH,t.LOW]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        length=5
        needData = self.needData# 计算所需数据
        high=needData[t.HIGH];low=needData[t.LOW]
        [m,n]=high.shape;factor=pd.DataFrame(index=high.index,columns=high.columns)
        for i in range(m):
            for j in range(n):
                sta=max(0,i-length);fin=max(0,i-1)+1
                temp1=high.iloc[sta:fin,j].sort_values(ascending=False)
                temp2=low.iloc[sta:fin,j].sort_values(ascending=False)
                if len(temp1)==1 or len(temp2)==1:
                    continue
                if temp1.isnull().any() or temp2.isnull().any():
                    continue
                factor.iloc[i,j]=temp1.corr(temp2)


        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()