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
		self.needFields = [t.PDD,t.HIGH,t.NETCASHLYR,t.MKTCAPFL,t.PB,t.SHRFREE]# ������Ҫ���ֶ�
	def factor_definition(self):
		s = time.time()
		needData = self.needData  # ������������
		factor=regalpha10(regbeta5(regalpha10(min7(sum10(needData[t.PDD])), regbeta10(max8(needData[t.HIGH]), decaylinear8(needData[t.NETCASHLYR]))), rank(cmpmax(max8(needData[t.MKTCAPFL]), log(needData[t.PB])))), needData[t.SHRFREE])
		print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
		return factor
	def run_factor(self):
		self.run()
fct = Factor()
fct.run_factor()