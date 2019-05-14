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
		self.needFields = [t.PDD,t.HIGH,t.NETCASHLYR,t.MKTCAPFL,t.PSTTM,t.PRCCHG,t.OPERREVTTM,t.PSTTM,t.VWAP]# 设置需要的字段
	def factor_definition(self):
		s = time.time()
		needData = self.needData  # 计算所需数据
		factor=multiply(regbeta20(multiply(min5(sum10(needData[t.PDD])), regalpha5(max6(needData[t.HIGH]), decaylinear7(needData[t.NETCASHLYR]))), minus(arcsin(max6(needData[t.MKTCAPFL])), divide(diff5(needData[t.PSTTM]), sum6(needData[t.PRCCHG])))), regbeta15(minus(rank(sum7(needData[t.OPERREVTTM])), diff9(max10(needData[t.PSTTM]))), max5(min5(tsmin5(needData[t.VWAP])))))
		print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
		return factor
	def run_factor(self):
		self.run()
fct = Factor()
fct.run_factor()