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
		self.needFields = list(set([t.VWAP,t.PCTCHG,t.PRCCHG,t.PRCCHG,t.VOLUME]))# 设置需要的字段
	def factor_definition(self):
		s = time.time()
		needData = self.needData  # 计算所需数据
		factor=add(sin(max8(corr5(decaylinear5(needData[t.VWAP]), delay7(needData[t.PCTCHG])))), regalpha30(divide(min7(decaylinear8(needData[t.PRCCHG])), log2(max6(needData[t.PRCCHG]))), delay7(needData[t.VOLUME])))
		print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
		return factor
	def run_factor(self):
		self.run()
fct = Factor()
fct.run_factor()