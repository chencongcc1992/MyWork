# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 20:56:07 2018

@author: chencong
"""
from random import seed,randrange,random
def loadDataSet(filename):
    dataSet = []
    with open(filename,'r') as fr:
        for line in fr.readlines():
            if not line:
                continue
            lineArr = []
            for feature in line.split(','):
                str_f = feature.strip()
                if str_f.isdigit():
                    lineArr.append(float(str_f))
                else:
                    lineArr.append(str_f)
            dataSet.append(lineArr)
    return dataSet


#样本无放回抽样
def cross_validation_split(dataSet,n_folds):
    dataSet_split = list()
    dataSet_copy = list(dataSet)
    fold_size = len(dataSet)/n_folds
    for i in range(n_folds):
        fold = list()
        while len(fold)<fold_size:
            index = 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        