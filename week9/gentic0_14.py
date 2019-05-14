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
		self.needFields = [t.ADJOPEN,t.MKTCAPFL,t.ADJCLOSE,t.PE,t.TURN,t.VOLUME,t.NETPCMTTM,t.TURN,t.AMOUNT]# 设置需要的字段
	def factor_definition(self):
		s = time.time()
		needData = self.needData  # 计算所需数据
		factor=sum5(divide(add(log2(regbeta5(needData[t.ADJOPEN], needData[t.MKTCAPFL])), tsmin5(max5(needData[t.ADJCLOSE]))), corr20(add(corr10(needData[t.PE], needData[t.TURN]), decaylinear5(needData[t.VOLUME])), regalpha30(regbeta5(needData[t.NETPCMTTM], needData[t.TURN]), max9(needData[t.AMOUNT])))))
		print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
		return factor
	def run_factor(self):
		self.run()
fct = Factor()
fct.run_factor()