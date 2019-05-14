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
		self.needFields = [t.PCFOCFTTM,t.PCFOCF,t.CLOSE,t.PCFOCFTTM]# 设置需要的字段
	def factor_definition(self):
		s = time.time()
		needData = self.needData  # 计算所需数据
		factor=tsmax5(add(log(needData[t.PCFOCFTTM]), cmpmin(mean30(regalpha15(needData[t.PCFOCF], tsmax5(decaylinear7(needData[t.CLOSE])))), decaylinear8(diff5(needData[t.PCFOCFTTM])))))
		print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
		return factor
	def run_factor(self):
		self.run()
fct = Factor()
fct.run_factor()