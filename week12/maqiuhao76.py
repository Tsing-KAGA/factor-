#!/usr/bin/env Python
# -*- coding:utf-8 -*-
# author: mqh
import time
import numpy as np
import pandas as pd
import math
from FactorModule.FactorBase import FactorBase
from DataReaderModule.Constants import ALIAS_FIELDS as t
from CalculatorModule.OperatorPool import *
class Factor(FactorBase):
	def __init__(self):
		super(Factor, self).__init__()
		self.neutral = True
		self.factorName = __name__.split('.')[-1]
		self.needFields = list(set([t.ADJOPEN,t.AMOUNT,t.HIGH,t.MKTCAPFL,t.AMOUNT]))# 设置需要的字段
	def factor_definition(self):
		s = time.time()
		needData = self.needData  # 计算所需数据
		factor=add(min8(var10(regbeta20(needData[t.ADJOPEN], var30(var30(diff8(needData[t.AMOUNT])))))), sum10(diff2(corr25(cmpmax(needData[t.HIGH], needData[t.MKTCAPFL]), max7(needData[t.AMOUNT])))))
		print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
		return factor
	def run_factor(self):
		self.run()
fct = Factor()
fct.run_factor()