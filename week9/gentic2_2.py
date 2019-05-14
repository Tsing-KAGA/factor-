#!/usr/bin/env Python
# -*- coding:utf-8 -*-
# author: mqh
import time
import numpy as np
import pandas as pd
import math
from FactorModule.mqhBase import FactorBase
from DataReaderModule.Constants import ALIAS_FIELDS as t
from CalculatorModule.OperatorPool import *
class Factor(FactorBase):
	def __init__(self):
		super(Factor, self).__init__()
		self.neutral = False
		self.factorName = __name__.split('.')[-1]
		self.needFields = list(set([t.LOW,t.PCTCHG,t.CLOSE,t.PCTCHG,t.PCTCHG,t.VWAP,t.PCTCHG,t.LOW]))# 设置需要的字段
	def factor_definition(self):
		s = time.time()
		needData = self.needData  # 计算所需数据
		factor=regbeta5(regalpha10(min7(sum10(regbeta10(max8(needData[t.LOW]), decaylinear8(needData[t.PCTCHG])))), cmpmax(max8(min7(log(needData[t.CLOSE]))), sum6(log(regbeta30(needData[t.PCTCHG], needData[t.PCTCHG]))))), sum7(sum5(divide(add(log2(needData[t.VWAP]), max7(needData[t.PCTCHG])), diff10(needData[t.LOW])))))
		print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
		return factor
	def run_factor(self):
		self.run()
fct = Factor()
fct.run_factor()