# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 18:22:10 2018

@author: chenc
"""

import time
import random
import math

people=[('p1','BOS'),
        ('p2','DAL'),
        ('p3','CAK'),
        ('p4','MIA'),
        ('p5','ORD'),
        ('p6','OMA')]

destination = 'LGA'

#读取数据表，转换为如下形式
#{（origin，dest）：[(depart,arrive，int（price））,...],...}
#需要增加元素  setdefault


#计算某个时间在一天中的分钟数getminites
#输入t  time.strptime 函数



#[1,3,4,5,3,3,1,5,4,6,1,3]  代表题解
#将题解解释为实际情况printschedule 输入 r
#name origin out启航时间表 ret 返航时间表
#输出 name origin out0 out1 out2
#                 ret0 ret1 ret2




#成本函数
#schedulecost  输入方案solu
#初始值totalprice latestarrival earliestdepart
#遍历每个人 得到每个人的航班信息
#计算来和回的总价格
#记录最早到达和最早离开时间
#计算等待成本
#   遍历每个人
#   计算所有人等待的时间
#若最早离开时间大于最晚达到  租车费用多一天
#计算总时间


########优化算法，寻找最优解###########################
#1.随机搜索
#随机一群解  计算最小的
#randomoptimize  输入 domain costf
#domain为每一个航班的次数范围(tuple 次数上下限，每个航班的次数可能不一样，单个列出)（12个航班）[(0,9),(0,10)...]
#初始值  best  best_solu
#随机产生1000个随机解
#计算成本
#比较得到最优解


#2.爬山法（易陷入局部最优解）
#hillclimb   输入 domain costf
#创建一个随机解
#主循环（while 不确定次数的循环）
#创建相邻解的列表
#每个方向偏离一个单位  相邻列表包含len（domain）*2个列表（不一定）
#先加偏离（在domain范围内）
#再减偏离（在domain范围内）
#计算当前随机解的总费用
#最优解为随机解
#遍历相邻解列表
#是否由于当前解 若是 进行替换
#如果最优解仍等于当前解  已找到  退出循环
#得到最优解



#3.模拟退火算法
#annealingoptimize
#输入 domain costf  T=10000初始温度  cool-0.95冷却系数  step=1 方向变化量
#随机初始值
#主循环
#随机选择解的一个索引值
#随机选择一个改变索引值的方向（-step，step）
#创建新列表 改变其中一个值
#判断新解改变后是否超出domain
#计算新成本与旧成本
#模拟退火  判断是否是更优解  或者退火概率成立
#降低温度 
#返回最优解




#4.遗传算法
#geneticoptimize
#输入domain costf popsize=50种群大小 step=1 值的变化量 mutprob=0.2变异的概率  elite=0.2胜出者的概率 maxiter=100迭代次数
#交叉操作crossover vec1 vec2
#随机选择交叉点
#范围交叉后的解
#变异操作 mutate vec
#随机选择变异点  
#random.choice 变异
#判断是否超出domain
#返回变异的解
#
#构造初始种群[]
#随机产生popsize个初始种群
#每一代胜出者的数量
#主循环 迭代次数
#计算每个解的（cost，vec）
#按cost 排序
#对应的解排序
#选取胜出的解
##对胜出的解进行变异和交叉达到种群数量
#while 循环每变一次 数量加以一个:
#mutprob的概率变异 1-mutprob的概率交叉
#随机选择一个解进行变异并添加其后
#随机选择两个进行交叉并添加其后
#打印每一代的最佳者的cost
#返回最优解

    



























