"""
# -*- coding: utf-8 -*-

Created on Sun Apr 22 21:53:02 2018

@author: chencong
"""
'''
Apriori原理可以帮我们减少可能感兴趣的项集。 Apriori原理是说如果某个项集是频繁的，
那么它的所有子集也是频繁的。这意味着如果{0,1}是频繁的，那么{0}、 {1}也一定是频繁的。
这个原理直观上并没有什么帮助，但是如果反过来看就有用了，也就是说如果一个项集是非频
繁集，那么它的所有超集也是非频繁的
项集的支持度（ support）被定义为数据集中包含该项集的记录所占的比例
可信度或置信度（ confidence）是针对一条诸如{尿布} ➞ {葡萄酒}的关联规则来定义的。这
条规则的可信度被定义为“支持度({尿布, 葡萄酒})/支持度({尿布})
关联分析的目标包括两项：发现频繁项集和发现关联规则
Apriori算法是发现频繁项集的一种方法。 Apriori算法的两个输入参数分别是最小支持度和数
据集。该算法首先会生成所有单个物品的项集列表。接着扫描交易记录来查看哪些项集满足最小
支持度要求，那些不满足最小支持度的集合会被去掉。然后，对剩下来的集合进行组合以生成包
含两个元素的项集。接下来，再重新扫描交易记录，去掉不满足最小支持度的项集。该过程重复
进行直到所有项集都被去掉
'''

print(__doc__)
from numpy import *

#导入数据
def loadDataSet():
    return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]


#将各项item归结为一个集合（固定集合）
def createC1(dataSet):
    C1=[]
    for transaction in dataSet:
        for item in transaction:
            if [item] not in C1:
                C1.append([item])
    C1.sort()
    return list(map(frozenset,C1))


#计算支持度  返回所有支持度大于给定值的频繁项
#D为数据集  Ck 候选项集列表（单元素）   给定的最小支持度
#实质上为先计算最小子项的支持度
def scanD(D,Ck,minsupport):
    ssCnt = {}
    #遍历数据集 遍历候选集 统计候选集元素的频率
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not can in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] +=1
    numItems = float(len(D))
    retList = []
    supportData = {}
    #计算频率
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minsupport:
            retList.insert(0,key)
            supportData[key] = support
    return retList,supportData
                
    


#父集合生成，以{0}、 {1}、 {2}作为输入，会生成{0,1}、 {0,2}以及{1,2}
#根据原始元素，生成数目为k个的集合
#比较集合{0,1}、 {0,2}、 {1,2}的第1个元素并只对第1个元
#素相同的集合求并操作，又会得到什么结果？ {0, 1, 2}，而且只有一次操作！这样就不需要遍历
#列表来寻找非重复值    
def aprioriGen(Lk,k):#(L0,2)
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1,lenLk):
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1==L2:
                retList.append(Lk[i] | Lk[j])
    return retList


#筛选支持度大于给定值的组合，并计算支持度
def apriori(dataSet,minsupport=0.5):
    C1 = createC1(dataSet)
    D = list(map(set,dataSet))
    L1,supportData = scanD(D,C1,minsupport)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2],k)
        Lk,supK = scanD(D,Ck,minsupport)
        if len(Lk) == 0:
            break
        supportData.update(supK)
        L.append(Lk)
        k  += 1
    return L,supportData

#生成关联规则        
#输入 频繁项集列表  频繁项集及对应支持度的字典  可信度的最小值    
#假设规则0,1,2 ➞ 3并不满足最小可信度要求，那么就知道任何左部为{0,1,2}子集的规则也不会满足最小可
#信度要求
def generateRules(L,supportData,minConf=0.7):
    bigRuleList = []
    for i in range(1,len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i>1):
                rulesFromConseq(freqSet,H1,supportData,bigRuleList,minConf)
            else:
                calcConf(freqSet,H1,supportData,bigRuleList,minConf)
    #生成一个包含可信度的规则列表            
    return bigRuleList

#frozenset({2, 3}),[frozenset({2}), frozenset({3})],supportdata,              
def calcConf(freqSet,H,supportData,brl,minConf=0.7) :
    prunedH = []
    for conseq in H:
        #支持度（2，3）/支持度（2）  循环
        conf = supportData[freqSet]/supportData[freqSet-conseq]
        #满足最小可信度
        if conf >= minConf:
            print(freqSet-conseq,'-->',conseq,'conf:',conf)
            brl.append((freqSet-conseq,conseq,conf))
            prunedH.append(conseq) 
    return prunedH




#递归计算频繁项集的规则
def rulesFromConseq(freqSet,H,supportData,brl,minConf=0.7):
    m = len(H[0])
    if (len(freqSet) > (m+1)):
        Hmpl = aprioriGen(H,m+1)
        #Hmpl = calcConf(freqSet,Hmpl,supportData,brl,minConf)
        print('Hmpl=',Hmpl)

        print('len(Hmpl)=',len(Hmpl),'len(freqSet)=',len(freqSet))
        if (len(Hmpl) > 1):
            return rulesFromConseq(freqSet,Hmpl,supportData,brl,minConf)




    






    
        
    






























    
    