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
		self.needFields = [t.SHR,t.PCFOCFTTM,t.PSTTM,t.ADJOPEN,t.PRCCHG]# 设置需要的字段
	def factor_definition(self):
		s = time.time()
		needData = self.needData  # 计算所需数据
		factor=regalpha15(decaylinear7(corr20(corr10(min5(diff6(sum6(log(regbeta30(needData[t.SHR], needData[t.PCFOCFTTM]))))), mean30(needData[t.PSTTM])), decaylinear10(needData[t.ADJOPEN]))), decaylinear6(delay10(needData[t.PRCCHG])))
		print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
		return factor
	def run_factor(self):
		self.run()
fct = Factor()
fct.run_factor()