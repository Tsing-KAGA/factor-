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
		self.needFields = list(set([t.PCTCHG,t.PRCCHG,t.OPEN,t.CLOSE,t.AMOUNT,t.LOW,t.HIGH]))# 设置需要的字段
	def factor_definition(self):
		s = time.time()
		needData = self.needData  # 计算所需数据
		factor=minus(rank(delay8(max9(min7(diff5(needData[t.PCTCHG]))))), delay8(add(decaylinear10(rank(regalpha5(needData[t.PRCCHG], needData[t.OPEN]))), corr60(mean60(corr60(max8(min7(log(needData[t.CLOSE]))), needData[t.AMOUNT])), corr10(decaylinear10(needData[t.LOW]), min6(needData[t.HIGH]))))))
		print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
		return factor
	def run_factor(self):
		self.run()
fct = Factor()
fct.run_factor()