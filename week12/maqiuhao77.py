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
		self.needFields = list(set([t.HIGH,t.VOLUME,t.HIGH,t.MKTCAPFL,t.ADJOPEN]))# 设置需要的字段
	def factor_definition(self):
		s = time.time()
		needData = self.needData  # 计算所需数据
		factor=add(min8(var10(regbeta20(log(needData[t.HIGH]), needData[t.VOLUME]))), sum10(diff2(corr25(cmpmax(needData[t.HIGH], needData[t.MKTCAPFL]), max7(needData[t.ADJOPEN])))))
		print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
		return factor
	def run_factor(self):
		self.run()
fct = Factor()
fct.run_factor()