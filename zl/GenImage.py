import gc
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

class GenImage:
	def __init__(self,filePath):
		self.FILE_PATH = filePath
		self.FONT = {
			'size' : 15
		}

	def generateImage(self, sourceName, fileName, image_kind):
		matplotlib.rcParams['font.family'] = 'SimHei'	
		matplotlib.rc('font', **self.FONT)               
		mydata = pd.read_csv(self.FILE_PATH + sourceName)		
		mydata.sort_index()

		if image_kind == 'pie':
			mydata.plot(kind='pie', subplots=True, figsize=(10,10), autopct='%1.1f%%', fontsize=20)
		elif image_kind == 'bar':
			mydata.plot(kind='bar', subplots=True, fontsize=10, figsize=(4,6))
		else:
			raise TypeError('参数错误')

		plt.savefig(self.FILE_PATH + 'images/' + fileName,dpi=100)
		plt.close()
	
