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
		self.needFields = [t.VOLUME,t.HIGH]# 设置需要的字段
	def factor_definition(self):
		s = time.time()
		needData = self.needData  # 计算所需数据
		element1=needData[t.HIGH]
		element2=needData[t.VOLUME]
		s1=self.calculator.Rank(self.calculator.Mean(self.calculator.Delay(element1,5),20))
		s2=self.calculator.Corr(element1,element2,2)
		s3=self.calculator.Rank(self.calculator.Corr(self.calculator.Sum(element1,5),self.calculator.Sum(element1,20),2))
		zscore=-1*s1*s2*s3
		factor=self.calculator.Decaylinear(zscore,8)
		print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
		return factor
	def run_factor(self):
		self.run()
fct = Factor()
fct.run_factor()