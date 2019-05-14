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
		self.needFields = list(set([t.OPEN,t.LOW,t.LOW,t.HIGH,t.OPEN,t.CLOSE,t.AMOUNT,t.LOW]))# 设置需要的字段
	def factor_definition(self):
		s = time.time()
		needData = self.needData  # 计算所需数据
		factor=minus(regalpha30(corr20(mean30(max6(regalpha15(needData[t.OPEN], needData[t.LOW]))), add(mean60(sum8(needData[t.LOW])), log(delay9(needData[t.HIGH])))), regalpha30(decaylinear10(max8(tsmax5(needData[t.OPEN]))), mean10(decaylinear9(regalpha10(needData[t.CLOSE], needData[t.AMOUNT]))))), delay8(needData[t.LOW]))
		print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
		return factor
	def run_factor(self):
		self.run()
fct = Factor()
fct.run_factor()