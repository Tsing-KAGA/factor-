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
		self.needFields = [t.PS,t.SHR,t.NETCASHLYR]# ������Ҫ���ֶ�
	def factor_definition(self):
		s = time.time()
		needData = self.needData  # ������������
		factor=max6(regbeta20(max5(needData[t.PS]), decaylinear7(corr30(max6(needData[t.SHR]), max9(needData[t.NETCASHLYR])))))
		print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
		return factor
	def run_factor(self):
		self.run()
fct = Factor()
fct.run_factor()