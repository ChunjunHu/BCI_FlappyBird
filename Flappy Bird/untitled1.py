# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 19:50:38 2018

@author: jiyan
"""

import numpy as np
from sklearn.decomposition import PCA
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
#import pandas as pd
#import seaborn as sns
#import matplotlib.pyplot as plt
fea_vect0=np.loadtxt('08_08_21_47clo.txt')
fea_vect1=np.loadtxt('08_08_21_47op.txt')
fea_color=np.append(['g']*len(fea_vect0),['r']*len(fea_vect1))



fea_conc=np.append(fea_vect0,fea_vect1,axis=0).T
fea_PCA=PCA(n_components=3)
fea_PCA.fit(fea_conc)
pca_comp=fea_PCA.components

lable_color_map={-1:'k',0:'b',1:'g',2:'r',3:'mediumpurple',4:'y',5:'c'}
fig=pyplot.figure()
ax=Axes3D(fig)
sca=ax.scatter(pca_comp[0],pca_comp[1],pca_comp[2],s=150,c=fea_color)