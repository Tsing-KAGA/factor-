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
		self.neutral = True
		self.factorName = __name__.split('.')[-1]
		self.needFields = [t.CLOSE]# 设置需要的字段
	def factor_definition(self):
		s = time.time()
		needData = self.needData  # 计算所需数据
		length=27
		s1=0
		s2=0
		close=needData[t.CLOSE]
		for i in range(length):
			close1 = self.calculator.Delay(close, i + 1)
			close2 = self.calculator.Delay(close, i)
			s1+=(close2>=close1)*((close2 - close1) / close1)
			s2+=(close2<close1)*((close2 - close1) / close1)
		s1 /= length
		s2 /= length
		factor=self.calculator.Decaylinear((1/np.pi)*np.arctan(s1/(s1 + s2)),5)
		print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
		return factor
	def run_factor(self):
		self.run()
fct = Factor()
fct.run_factor()