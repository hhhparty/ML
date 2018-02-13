#-*- coding:utf-8 -*-
'''
Zero base learning quantitative investment
chapter 1 
2018.02.13.
本例学习多种matplotlib模块库中的style绘图风格函数。共有22种不同风格的mpl图
可选的风格由plt.style.available枚举中，枚举后可通过plt.style.use(xss)使用。
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

def dr_xtyp(_dat):
    i = 0
    for xss in plt.style.available:
        plt.figure()
        plt.style.use(xss) # This is a important usage!
        _dat.plot()
        fss = "C:\\Users\\leo\\Desktop\\ml\\" + xss + ".png"
        i += 1;
        print(i,xss,",",fss)
        plt.show()

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
dr_xtyp(df)
