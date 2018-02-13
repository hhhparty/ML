#-*- coding:utf-8 -*-
'''
Zero base learning quantitative investment
chapter 1 
2018.02.13.

22种不同风格的mpl图
'''

import numpy as np
import scipy as sp
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

%matplotlib inline

def sta001(k,nyear,xd):
    d2 = np.fv(k,nyear,-xd,-xd)
    d2 = round(d2)
    return d2

d40 = 1.4 * 40
print("d40,40 * 1.4 = ",d40)
d = sta001(0.05,40-1,1.4)
print("01 Conservative investment mode：", d, round(d/d40))

d2 = sta001(0.2,40-1,1.4)
print("02 Radical investment mode：", d2, round(d2/d40))

dk = round(d2/d)
print("dk, the difference of two above mode: ",dk)

dx05 = [sta001(0.05,x,1.4) for x in range(0,40)]
dx10 = [sta001(0.10,x,1.4) for x in range(0,40)] 
dx15 = [sta001(0.15,x,1.4) for x in range(0,40)]
dx20 = [sta001(0.2,x,1.4) for x in range(0,40)]

df = pd.DataFrame(columns = ['dx05','dx10','dx15','dx20'])
df['dx05'] = dx05
df['dx10'] = dx10
df['dx15'] = dx15
df['dx20'] = dx20
print(df.tail())
df.plot()
