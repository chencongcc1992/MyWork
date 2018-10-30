# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 22:22:38 2018

@author: chenc
"""

from math import tanh
from bs4 import BeautifulSoup
from urllib.request import urlopen,urlretrieve
from urllib.parse import urlparse
from urllib.parse import urljoin
import re
import pymysql


class Searchnet(object):
    def __init__(self,dbname):
        self.db=pymysql.connect('localhost','root','Chen1992#',dbname)
        self.cursor=self.db.cursor()
        
    def __del__(self):
        self.db.close()
       
        #连接线表
    def maketables(self):
        self.cursor.execute("create table hiddennode (rowid int(10) auto_increment,create_key varchar(60),primary key (rowid))")
        self.cursor.execute("create table wordhidden (rowid int(10) auto_increment,fromid int(10),toid int(10),strength float(10),primary key (rowid))")
        self.cursor.execute("create table hiddenurl (rowid int(10) auto_increment,fromid int(10),toid int(10),strength float(10),primary key (rowid))")
        self.db.commit()


    def getstrength(self,fromid,toid,layer):
        if layer==0:table='wordhidden'
        if layer==1:table='hiddenurl'
        self.cursor.execute("select strength from %s where fromid=%d and toid=%d" % (table,fromid,toid))
        res=self.cursor.fetchone()
        if res==None:
            if layer==0:return -0.2
            if layer==1:return 0.0
        return res[0]
    
    def setstrength(self,fromid,toid,layer,strength):
        if layer==0:table='wordhidden'
        if layer==1:table='hiddenurl'
        self.cursor.execute("select rowid from %s where fromid=%d and toid=%d" % (table,fromid,toid))
        res=self.cursor.fetchone()
        if res==None:
            self.cursor.execute("insert into %s(fromid,toid,strength) values(%d,%d,%f)" % (table,fromid,toid,strength))
        else:
            self.cursor.execute("update %s set strength=%f where rowid=%d" % (table,strength,res[0]))
                    

    def generatehiddennode(self,wordids,urlids):
        if len(wordids)>3:return None
        createkey='_'.join(sorted([str(word) for word in wordids]))
        self.cursor.execute("select rowid from hiddennode where create_key='%s'" % createkey)
        res=self.cursor.fetchone()
        
        if res==None:
            self.cursor.execute("insert into hiddennode(create_key) values('%s')" % createkey)
            hiddenid=self.cursor.lastrowid
            #部分权重
            for wordid in wordids:
                self.setstrength(wordid,hiddenid,0,1.0/len(wordids))
            for urlid in urlids:
                self.setstrength(hiddenid,urlid,1,0.1)
        self.db.commit()




    def getallhiddenids(self,wordids,urlids):
        hi_id={}
        for wordid in wordids:
            self.cursor.execute("select toid from wordhidden where fromid=%d" % wordid)
            cur=self.cursor.fetchall()
            for row in cur:hi_id[row[0]]=1
        for urlid in urlids:
            self.cursor.execute("select fromid from hiddenurl where toid=%d" % urlid)
            cur=self.cursor.fetchall()
            for row in cur:hi_id[row[0]]=1    
        return hi_id.keys()
    
    #建立全权重(类的属性设置)
    def setupnetwork(self,wordids,urlids):
        #网络节点(类属性各函数通用)
        self.wordids=wordids
        self.hiddenids=list(self.getallhiddenids(wordids,urlids))
        self.urlids=urlids
        self.len_w=len(self.wordids)
        self.len_h=len(self.hiddenids)
        self.len_u=len(self.urlids)
        
        #各节点输出值
        self.ai=[1.0]*self.len_w
        self.ah=[1.0]*self.len_h
        self.ao=[1.0]*self.len_u
        
        #权重矩阵生成
        self.wi=[[self.getstrength(wordid,hiddenid,0) for hiddenid in self.hiddenids] for wordid in self.wordids]
        self.wo=[[self.getstrength(hiddenid,urlid,1) for urlid in self.urlids] for hiddenid in self.hiddenids]



    def feedforward(self):
        
        for i in range(self.len_w):
            self.ai[i]=1.0             #输入值始终不变，只改变权重，后面的输入输出随权重变化
            
        for j in range(self.len_h):
            sum_in = 0.0
            for i in range(self.len_w):
                sum_in+=self.ai[i]*self.wi[i][j]
            self.ah[j]=tanh(sum_in)
            
        for k in range(self.len_u):
            sum_in = 0.0
            for j in range(self.len_h):
                sum_in+=self.ah[j]*self.wo[j][k]
            self.ao[k]=tanh(sum_in) 
            
        return self.ao[:]
    
    
    def getresult(self,wordids,urlids):
        self.setupnetwork(wordids,urlids)
        return self.feedforward()
    
    
    def dtanh(self,y):
        return 1.0-y*y
    
    
    
    def backpropagate(self,targets,n=0.5):
        #误差
        output_deltas=[0.0]*self.len_u
        for k in range(self.len_u):
            error=targets[k]-self.ao[k]
            output_deltas[k]=self.dtanh(self.ao[k])*error
        
        #hidden层误差
        hidden_deltas=[0.0]*self.len_h
        for j in range(self.len_h):
            error=0.0
            #各url的误差乘以权重之和
            for k in range(self.len_u):
                error=error+output_deltas[k]*self.wo[j][k]
            hidden_deltas[j]=self.dtanh(self.ah[j])*error
                
            
        #根据误差更新权重
        for j in range(self.len_h):
            for k in range(self.len_u):
                change=output_deltas[k]*self.ah[j]
                self.wo[j][k]+=n*change
                
        for i in range(self.len_w):
            for j in range(self.len_h):
                change=hidden_deltas[j]*self.ai[i]
                self.wi[i][j]+=n*change
                

    #使用函数
    def trainquery(self,wordids,urlids,selectedurl):
        self.generatehiddennode(wordids,urlids)
        
        self.setupnetwork(wordids,urlids)
        self.feedforward()
        print(self.feedforward())
        targets=[0.0]*len(urlids)
        targets[urlids.index(selectedurl)]=1.0
        self.backpropagate(targets)
        self.updatedatabase()
        
        
    def updatedatabase(self):
        
        for i in range(self.len_w):
            for j in range(self.len_h):
                self.setstrength(self.wordids[i],self.hiddenids[j],0,self.wi[i][j])
        
        for j in range(self.len_h):
            for k in range(self.len_u):
                self.setstrength(self.hiddenids[j],self.urlids[k],1,self.wo[j][k])        
        self.db.commit()

























































































