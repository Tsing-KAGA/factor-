#思路： (RegBeta(close,high,10)-Mean(RegBeta(close,high,18),600))/Std(RegBeta(close,high,18),600)
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
		self.needFields = [t.CLOSE,t.HIGH]
	def factor_definition(self):
		s = time.time()
		needData = self.needData
		high=needData[t.CLOSE]
		low=needData[t.HIGH]
		weightnow=self.calculator.RegBeta(high,low,10)
		weightlist=self.calculator.RegBeta(high,low,18)
		weightmean=self.calculator.Mean(weightlist,600)
		weightstd=self.calculator.Std(weightlist,600)
		zscore=(weightnow-weightmean)/weightstd
		factor = zscore
		print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
		return factor
	def run_factor(self):
		self.run()
fct = Factor()
fct.run_factor()