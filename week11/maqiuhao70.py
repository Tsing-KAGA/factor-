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
		self.needFields = list(set([t.ADJOPEN,t.AMOUNT,t.PCTCHG,t.LOW,t.ADJOPEN,t.AMOUNT,t.ADJOPEN,t.ADJOPEN]))# 设置需要的字段
	def factor_definition(self):
		s = time.time()
		needData = self.needData  # 计算所需数据
		factor=sum8(std5(divide(tsmin5(diff10(delay10(divide(diff10(sum10(needData[t.ADJOPEN])), regbeta15(diff10(var5(corr15(decaylinear7(max7(delay5(needData[t.AMOUNT]))), tsmin5(needData[t.PCTCHG])))), mean15(regalpha5(diff30(diff80(needData[t.LOW])), sum8(diff4(needData[t.ADJOPEN]))))))))), regbeta15(needData[t.AMOUNT], mean15(multiply(needData[t.ADJOPEN], needData[t.ADJOPEN]))))))
		print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
		return factor
	def run_factor(self):
		self.run()
fct = Factor()
fct.run_factor()