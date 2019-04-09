#思路： (NETCASHTTM/NETASSET-Mean(NETCASHTTM/NETASSET,600))/Std(NETCASHTTM/NETASSET,600)
#!/usr/bin/env Python
# -*- coding:utf-8 -*-
# author: mqh
import time
import numpy as np
import pandas as pd
import math
from FactorModule.FactorBase import FactorBase
from DataReaderModule.Constants import ALIAS_FIELDS as t
class Factor(FactorBase):
	def __init__(self):
		super(Factor, self).__init__()
		self.neutral = True
		self.factorName = __name__.split('.')[-1]
		self.needFields = [t.NETCASHTTM,t.NETASSET]# ������Ҫ���ֶ�
	def factor_definition(self):
		s = time.time()
		needData = self.needData  # ������������
		element=needData[t.NETCASHTTM]
		asset=needData[t.NETASSET]
		assetmean=self.calculator.Mean(asset,20)
		rate = element/assetmean
		meanrate=self.calculator.Mean(rate,600)
		stdrate=self.calculator.Std(rate,600)
		zscore=(rate-meanrate)/stdrate
		factor=zscore
		print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
		return factor
	def run_factor(self):
		self.run()
fct = Factor()
fct.run_factor()