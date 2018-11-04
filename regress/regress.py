# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 21:47:50 2018

@author: chencong
"""

from numpy import *
import matplotlib.pylab as plt

#导入数据
def loadDataSet(filename):
    fr = open(filename)
    #特征的个数
    numFeat = len(fr.readline().split('\t')) - 1
    #输入数据  输出值
    dataMat = []
    labelMat = []
#最后一列为label    
    for line in fr.readlines():
        #每一组数据
        lineArr = []
        #strip去掉首位空格  split 去掉中间table
        curLine = line.strip().split('\t')
        for i in range(numFeat):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        #最后一位为label
        labelMat.append(float(curLine[-1]))
    return dataMat, labelMat



#多元线性回归系数计算公式 （X.T x X）-1 X.T y
def standRegres(xArr, yArr):
    xMat = mat(xArr)
    yMat = mat(yArr).T
    xTx = xMat.T * xMat
    if linalg.det(xTx) == 0.0:
        print("This matrix is singular, cannot do inverse")
        return
    ws = xTx.I * (xMat.T * yMat)
    return ws     

#相关系数计算(回归结果与实际结果)  评价回归效果
def cocoef(ws,xArr,yArr):
    xMat = mat(xArr)
    yMat = mat(yArr)
    yHat=xMat*ws
    return np.corrcoef(yHat.T,yMat)

#局部加权线性回归 
#核函数对每个数据点赋予权重
#testpoint  一个样本数据
#每一个不同的点，均有针对性的回归方程
#针对该点唯一的回归方程，唯一的回归结果，类似与KNN
def lwlr(testPoint, xArr, yArr, k=1.0):
    #输入值 输入label
    xMat = mat(xArr)
    yMat = mat(yArr).T
    #样本的数量
    m = shape(xMat)[0]
    #权重对角矩阵（样本数量个）
    weights = mat(eye((m)))
    for j in range(m):
        #与testpoint越接近的数据，权重越大（高斯核，接近元素筛选）
        diffMat = testPoint - xMat[j, :]
        weights[j, j] = exp(diffMat * diffMat.T / (-2.0 * k**2))
    xTx = xMat.T * (weights * xMat)
    if linalg.det(xTx) == 0.0:
        print("This matrix is singular, cannot do inverse")
        return
    ws = xTx.I * (xMat.T * (weights * yMat))
    return testPoint * ws
 
    

#多个样本（样本表）逐个调用lwlr函数逐个回归      
def lwlrTest(testArr, xArr, yArr, k=1.0):
    m = shape(testArr)[0]
    #存放回归值
    yHat = zeros(m)    
    for i in range(m):   
        yHat[i] = lwlr(testArr[i], xArr, yArr, k) 
    return yHat
        
  

      
#排序作图       
def lwlrTestPlot(xArr, yArr, k=1.0):     
    yHat = zeros(shape(yArr))   
    xCopy = mat(xArr)  
    xCopy.sort(0)
    for i in range(shape(xArr)[0]):   
        yHat[i] = lwlr(xCopy[i], xArr, yArr, k)
    return yHat, xCopy
        
        
#计算回归误差      
def rssError(yArr, yHatArr):       
    return ((yArr - yHatArr)**2).sum()
        



##################岭回归################################## 
#用于特征比样本数还多的情况（非满秩矩阵，求逆不存在）
#XTX 加一个λI从而使得矩阵非奇异，进而能对XTX + λI求逆
def ridgeRegres(xMat,yMat,lam=0.2):
    xTx = xMat.T*xMat
    #xTx 加上lam 
    denom = xTx + eye(shape(xMat)[1])*lam
    if linalg.det(denom) == 0.0:
        print('this matrix is singular,cannot do inverse')
        return
    ws = denom.I*(xMat.T * yMat.T)
    return ws



#岭回归在一组数值上进行测试
def ridgeTest(xArr,yArr):
    #数据归一化
    xMat = mat(xArr)
    yMat = mat(yArr)
    yMean = mean(yMat,axis=1)
    yMat =yMat - yMean
    xMeans = mean(xMat,axis=0)
    xVar = var(xMat,axis=0)
    xMat = (xMat-xMeans)/xVar
    #进行30次循环，计算不同lam值下的回归系数
    numTestPts = 30
    wMat = zeros((numTestPts,shape(xMat)[1]))
    for i in range(numTestPts):
        ws = ridgeRegres(xMat,yMat,exp(i-10))
        wMat[i,:] = ws.T
    return wMat


#regularlize with column
def regularize(xMat):
    inMat = xMat.copy()
    inMeans = mean(inMat,0)
    inVar = var(inMat,0)
    inMat = (inMat-inMeans)/inVar
    return inMat



#############逐步向前线性回归#####################
def stageWise(xArr,yArr,eps=0.01,numIt=100):
    xMat = mat(xArr)
    yMat = mat(yArr).T
    yMean = mean(yMat,0)
    yMat = yMat- yMean
    xMat = regularize(xMat)
    m,n=shape(xMat)
    #记录每一次迭代的回归系数结果
    returnMat=zeros((numIt,n))
    ws = zeros((n,1))
    wsTest = ws.copy()
    wsMax = ws.copy()
    for i in range(numIt):
        print(ws.T)
        lowestError = inf
        for j in range(n):
            for sign in [-1,1]:
                wsTest = ws.copy()
                #使用0.005的epsilon值并经过100次迭代
                wsTest[j] += eps*sign
                yTest = xMat *wsTest
                rssE = rssError(yMat.A,yTest.A)
                if rssE < lowestError:
                    lowestError = rssE
                    wsMax = wsTest
        ws = wsMax.copy()
        returnMat[i,:]=ws.T
    return returnMat









































        
        