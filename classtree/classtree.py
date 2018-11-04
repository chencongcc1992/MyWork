# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 23:42:51 2018

@author: chenc
"""

my_data=[['slashdot','USA','yes',18,'None'],
        ['google','France','yes',23,'Premium'],
        ['digg','USA','yes',24,'Basic'],
        ['kiwitobes','France','yes',23,'Basic'],
        ['google','UK','no',21,'Premium'],
        ['(direct)','New Zealand','no',12,'None'],
        ['(direct)','UK','no',21,'Basic'],
        ['google','USA','no',24,'Premium'],
        ['slashdot','France','yes',19,'None'],
        ['digg','USA','no',18,'None'],
        ['google','UK','no',18,'None'],
        ['kiwitobes','UK','no',19,'None'],
        ['digg','New Zealand','yes',12,'Basic'],
        ['slashdot','UK','no',21,'None'],
        ['google','UK','yes',18,'Basic'],
        ['kiwitobes','France','yes',19,'Basic']]





"""
#创造决策树，节点类
创造一个节点的类，decisionnode具有如下特征：
col 判断条件（用列索引表示）
value 判断值 使结果为true的值
tb fb 判断值为true和false时的子节点 （递归）
results 经过该判断条件的结果 dict 其它节点：None 叶节点：非空







#数据集拆分函数（按条件拆分数据集）
在某一列上（某一列特征、属性）对数据集合进行拆分 divideset
输入：数据集rows 列索引column 判断值 value
判断数据特征是数值型数据  还是字符型数据  匿名函数 初始值用None
数值型用>=拆分   字符型用等于拆分
返回set1（>= 或 等于） set2（！>= 或 不等于） for in  if 判断条件
调试







#选择合适的拆分方案
1.统计拆分结果uniquecounts  统计数据集中不同结果的样本的个数
输入：数据集rows  输出  字典 不同结果的个数
















"""

