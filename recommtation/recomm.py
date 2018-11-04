# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 17:36:00 2018

@author: chenc
"""
import math 
from operator import itemgetter, attrgetter

#原始数据: 嵌套字典
#{'person':{'moive':mark},...}





#寻找相近的用户：1)欧几里得距离评价；2）皮尔逊相关度评价
#1）欧几里得
#导入数学函数

#定义距离函数sim_distance  输入值：原始数据   人物1   人物2
#定义初始存放结果值
#遍历1中电影   记录与2中相同的与字典（列表）中 

#列表长度为0  无共同评价电影  返回0

#列表长度不为0  遍历字典（列表） 使用公式

#返回计算值   return后直接接公式  相似度的值  0——1之间

def sim_distance(critic,p1,p2):
    item=[]
    sumsq = 0
    for movie in critic[p1]:
        if movie in p2:
            item.append(movie)
    if len(item)==0:return 0
    for x in item:
        sumsq+=(critic[p1][x]-critic[p2][x])**2
    #sumsq = sum(critic[p1][x]-critic[p2][x])**2 for x in item)
    #pow 函数   math.pow(critic[p1][x]-critic[p2][x],2) 
    return 1/(sumsq**0.5+1)
    #math.sqrt*()   
        
def sim_distance1(critic,p1,p2):
    
    sumsq = 0
    item = set(critic[p1].keys()) & set(critic[p1].keys())
    
    if len(item)==0:return 0
    for x in item:
        sumsq+=(critic[p1][x]-critic[p2][x])**2
    return 1/(sumsq**0.5+1)    


'''
2）皮尔逊相关度
定义函数 sim_pearson  输入值 原始数据  人物1  人物2
得到双方相同的评价列表
列表长度为0 返回0
列表长度不为0  计算Pearson系数
简单求和
平方和
乘积和
Pearson系数
若分母为0 返回0（n=1时） 不相关
计算r
'''

def sim_pearson(critic,p1,p2):
    item=[]
    for movie in critic[p1]:
        if movie in p2:
            item.append(movie)
    n=len(item)
    if n==0:return 0
    sumx = sum([critic[p1][x] for x in item])
    sumy = sum([critic[p2][y] for y in item])
    
    sumxsq = sum([critic[p1][x]**2 for x in item])
    sumysq = sum([critic[p2][y]**2 for y in item])
    
    psum = sum([critic[p1][x]*critic[p2][x]] for x in item)
    
    num = psum-sumx*sumy/n
    den = math.sqrt((sumxsq-sumx**2/n)*(sumysq-sumy**2/n))
    if den == 0:return 0
    return num/den
    





#其他算法  如  Jaccord系数   曼哈顿距离算法


#为评论者打分  输入值   原始数据 前n位 相似度函数   for in 
#为系数排序   sorted   key=itemgetter（2） reverse = True
#先sort 再reverse  默认第一个值排序

#返回与person最相似的n为person
def Topmatch(critic,n=5,person,sim=sim_pearson):
    
    score=[(sim(critic,per,person),per) for per in critic if per != person]
    score.sort()
    score.reverse()
    return score[0:n]







"""
推荐物品
对于自己未看过的影片进行推荐
按照与自己相似度的人物的权重对自己未看过的影片进行加权评分
定义函数 获得影片的排序列表 输入 原始数据  某人 相似度函数
定义空的存放变量
相似度*评价 movie
相似度之和  movie  出现即添加  dict

遍历所有的人物
    忽略自己 if continue
    计算相似度
    
    忽略相似度为0 或小于0的   人物
    遍历所有的电影
    影片不在自己的列表中  或者  自己的评分为0 的（未看）
    
    #相似度*评价值
    
    #相似度之和
    
相除并排序#排序
#return 
"""
def getrecomm(critic,person,sim=sim_distance):
    simProdMark={}
    sumSim={}
    for per in critic:
        if per == person:
            continue
        simd=sim(critic,per,person)
        if simd==0 or simd<0:
            continue
        for mov in critic[per]:
            if mov in critic[person] or critic[person][mov] != 0:
                continue
            perMark=simd*critic[per][mov]
            simProdMark.setdefault[mov,0]+=perMark
            if critic[per][mov] != 0: #同样可以用default  sumSim.setdefault(item,0)
                sumSim[mov]+=simd        #sumSim[item]+=simd 不存在时 加0 存在时加simd
    simProdMark[mov]/=sumSim
    ranking = simProdMark.items()
    rank = sorted(ranking,key=itemgetter(1))
    return rank
      

###重要 ： 不存在的值设为0    0的合理使用
###重要 ：  内循环持续记录外循环的值    
        
# 商品与人物交换
def transform(critic):
    trans = {}
    for person in critic:
        for item in critic[person]:
            trans.setdefault(item,{})
            trans[item][person]=critic[person][item]
    return trans
        
#通过不同人物的评分进行 sim 方法比较  得到与某item类似的item
#存在为负的情况 表明不喜欢的倾向
    









#使用推荐函数
#定义函数  输入值  原始数据   某人



#基于物品的推荐
#为每件物品计算好最为相近的其它物品
#向某人推荐时，查看他评过分的物品，从中选出排位靠前者
#构造加权列表：包含它的相近者（第一步计算好的）




def CalcItemScore(critic,n=10):#子函数的变量转移
    SimItem={}
    c=0
    Items=transform(critic)
    for item in Items:
        c+=1
        if c%20 == 0:
            print('%d / %d' % (c,len(Items)))  #每20个记录一次，做标记
        SimItem[item]=Topmatch(Items,n=n,item,sim=sim_pearson)#子函数的变量转移
    return SimItem






#获得推荐的item
    
def getRecommItem():
    SumSim={}
    SumMark={}
    #遍历user的评分从高到底列表
    for (item,score) in critic[user].items():
        for (simulity,per) in CalcItemScore(critic,n=10)[item]:
            SumSim.setdefault(item,0)
            SumSim[item]+=score*simulity
            SumMark.setdefault(item,0)
            SumMark[item]+=simulity
    ranking=[(item,SumMark[item]/SumSim[item]) for item in SumSim.keys()]
          #[(item,SumMark[item]/sumsim),for item,sumsim in SumSim.items()]
    ranking.sort()
    ranking.reverse()
    return ranking















