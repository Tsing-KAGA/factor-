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
		self.needFields = list(set([t.OPEN,t.AMOUNT,t.LOW,t.CLOSE,t.HIGH,t.AMOUNT,t.CLOSE,t.LOW,t.CLOSE,t.LOW,t.CLOSE,t.LOW,t.AMOUNT,t.CLOSE,t.HIGH,t.VOLUME,t.CLOSE,t.HIGH,t.CLOSE,t.HIGH]))# 设置需要的字段
	def factor_definition(self):
		s = time.time()
		needData = self.needData  # 计算所需数据
		factor=regalpha10(regbeta5(regalpha10(min7(sum10(regbeta10(max8(corr15(needData[t.OPEN], needData[t.AMOUNT])), rank(cmpmax(needData[t.LOW], needData[t.CLOSE]))))), log(diff6(sum6(log(regbeta30(corr30(regalpha60(tsmax5(needData[t.HIGH]), mean5(needData[t.AMOUNT])), diff10(regbeta10(needData[t.CLOSE], needData[t.LOW]))), needData[t.CLOSE])))))), sum7(sum5(divide(add(log2(regbeta5(needData[t.LOW], needData[t.CLOSE])), tsmin5(max5(needData[t.LOW]))), corr20(add(corr10(needData[t.AMOUNT], needData[t.CLOSE]), decaylinear5(needData[t.HIGH])), regalpha30(regbeta5(needData[t.VOLUME], needData[t.CLOSE]), max9(needData[t.HIGH]))))))), delay8(decaylinear6(max7(diff8(mean20(std5(add(needData[t.CLOSE], needData[t.HIGH]))))))))
		print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
		return factor
	def run_factor(self):
		self.run()
fct = Factor()
fct.run_factor()