# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 21:52:26 2018

@author: chenc
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen,urlretrieve
from urllib.parse import urlparse
from urllib.parse import urljoin
import re
import pymysql
import nn
mynet=nn.Searchnet('nn')
#构建忽略词汇表
ignorewords=set(['a','the','to','in','on','is'])
#新建一个crawler类及相应的方法
class Crawler():
#对类进行初始化  传入保存数据的数据库
    def __init__(self,dbname):
        self.db=pymysql.connect("localhost","root","Chen1992#",dbname) #xiugai
        self.cursor=self.db.cursor()
#定制类 删除    
    def __del__(self):
        self.db.close()
#数据库执行函数
    def dbcommit(self):
        self.db.commit()
    
    
#辅助函数 获取条目id 若不存在 就加入数据库中
    def getentryid(self,table,field,value,createnew=True):
        #self.createindextables()
        self.cursor.execute("select rowid from %s where %s='%s'" % (table,field,value))
        res=self.cursor.fetchone()
        if res==None:
            self.cursor.execute("insert into %s (%s) value ('%s')" % (table,field,value))
            self.db.commit()
            return self.cursor.lastrowid
        else:
            return res[0]
    
#为每个网页建立索引
    def addtoindex(self,url,soup):
        if self.isindexed(url):return
        print('Indexing %s' % url)
        
        text=self.gettextonly(soup)
        words=self.separatewords(text)  #wordlist
        
        urlid=self.getentryid('urllib','url',url)
        
        for i in range(len(words)):
            word=words[i]
            if word in ignorewords:continue
            wordid=self.getentryid('wordlist','word',word)
            self.cursor.execute("insert into wordlist(wordid,word) values (%d,'%s')" % (wordid,word))
            self.cursor.execute('insert into wordlocation(urlid,wordid,location) values (%d,%d,%d)' % (urlid,wordid,i))
        
#从一个网页中提取文字（不带标签）
    def gettextonly(self,soup):
        v=soup.string
        if v==None:
            c=soup.contents
            resulttext=''
            for t in c:
                subtext=self.gettextonly(t)
                resulttext+=subtext+'\n'
            return resulttext
        else:
            return v.strip()
    
#对于非空空白字符进行分词处理
    
#如果url已经建立索引，返回False
    def isindexed(self,url):
        self.cursor.execute("select rowid from urllib where url='%s'" % url)
        u=self.cursor.fetchone()
        if u!=None:
            self.cursor.execute("select * from wordlocation where urlid=%d" % u[0])
            v=self.cursor.fetchone()
            if v!=None:return True
        return False
    
#添加一个关联两个网页的链接
    def addlinkref(self,urlFrom,urlTo,linkText):
        pass
    
#从一小组网页开始进行广度优先搜索，直至某一给定深度
#期间为网页建立索引
    def crawl(self,pages,depth=2):
        self.createindextables()
        for i in range(depth):
            newpages=set()
            for page in pages:
                try:
                    c=urlopen(page)
                except:
                    print('could not open %s' % page)
                    continue
                soup=BeautifulSoup(c.read(),'lxml')
                self.addtoindex(page,soup)
                
                links=soup.findAll('a') #找出页面下的链接标签 Set 集合
                for link in links: #筛选有链接网址的标签  可遍历 不可索引
                    if 'href' in link.attrs:#.attrs本身即为字典
                        url=urljoin(page,link['href']) #标签的属性  将基地址与一个相对地址形成一个绝对地址
                        if url.find("'")!=-1: continue
                        url=url.split('#')[0] #split处理后为列表
                        if url[0:4]=='http' and not self.isindexed(url):
                            newpages.add(url)
                            self.cursor.execute("insert into urllib(url) values ('%s')" % url)
                        linkText=self.gettextonly(link)
                        self.addlinkref(page,url,linkText)
                    self.db.commit()
                pages=newpages

#单词正则表达式提取
    def separatewords(self,text):
        splitter=re.compile('[^A-Za-z]')
        return [s.lower() for s in splitter.split(text) if len(s)>3]
    
#创建数据库表
    def createindextables(self):
        self.cursor=self.db.cursor()
        self.cursor.execute('create table urllib (rowid int(10) auto_increment,url varchar(200),primary key (rowid))')
        self.cursor.execute('create table wordlist (wordid int(10),rowid int(10) auto_increment,word varchar(50),primary key (rowid))')
        self.cursor.execute('create table wordlocation (urlid int(10),wordid int(10),location varchar(20))')
        self.cursor.execute('create table link (rowid int(10) auto_increment,fromid int(20),toid int(20),primary key (rowid))')
        self.cursor.execute('create table linkwords (wordid int(20),linkid int(20))')
        self.cursor.execute('create index wordidx on wordlist(word)')
        self.cursor.execute('create index urlidx on urllib(url)')
        self.cursor.execute('create index wordurlidx on wordlocation(wordid)')
        self.cursor.execute('create index urltoidx on link(toid)')
        self.cursor.execute('create index urlfromidx on link(fromid)')
        self.db.commit()
    
    

    def calculatepagerank(self,iterations=20):
        
        self.cursor.execute("drop table if exist pagerank")
        self.cursor.execute("create table pagerank(urlid int(10) primary key,score int(10))")

        self.cursor.execute("insert into pagerank select rowid,1.0 from urllib")
        self.db.commit()
        
        for i in range(iterations):
            print('iterations %d' % i)
            self.cursor.execute("select rowid from urllib")
            rows=self.cursor.fetchall()
            for urlid in rows:
                pr=0.15
                self.cursor.execute("select distinct fromid from link where toid=%d" % urlid) #execute内部不可有变量 变量都以%从外部传输
                linklist=self.cursor.fetchall()
                for linker in linklist:
                    self.cursor.execute("select score from pagerank where urlid=%d" %linker)
                    linkingpr=self.cursor.fetchone()[0]
                    self.cursor.execute("select count(*) from link where fromid=%d" %linker)
                    linkingcount=self.cursor.fetchone()[0]
                    pr+=0.85*(linkingpr/linkingcount)
                self.cursor.execute("update pagerank set score=%f where urlid=%d" %(pr.urlid))
            self.db.commit()















class Searcher(object):
    def __init__(self,dbname):
        self.db=pymysql.connect("localhost","root","Chen1992#",dbname)
        self.cursor=self.db.cursor()

    def __del__(self):
        self.db.close()
        
    def getmatchrows(self,q):
        
        fieldlist='w0.urlid'
        tablelist=''
        clauselist=''
        wordids=[]
        
        words=q.split(' ')
        tablenumble=0
        
        for word in words:
             self.cursor.execute("select rowid from wordlist where word='%s'" % word)
             wordrow=self.cursor.fetchone()  #tuple
             if wordrow!=None:
                 wordid=wordrow[0]          #(19,)
                 wordids.append(wordid)
                 if tablenumble>0:
                     tablelist+=','
                     clauselist+=' and '
                     clauselist+='w%d.urlid=w%d.urlid and ' % (tablenumble-1,tablenumble)
                 fieldlist+=',w%d.location' % tablenumble
                 tablelist+='wordlocation w%d' % tablenumble
                 clauselist+='w%d.wordid=%d' % (tablenumble,wordid)        #同一个表中进行多个相同类型查询的办法
                 tablenumble+=1
        
        fullquery="select %s from %s where %s" % (fieldlist,tablelist,clauselist)
        self.cursor.execute(fullquery)
        rows=self.cursor.fetchall()
#        rowss=[(row[0],row[1]) for row in rows]
        return rows,wordids




#基于内容的排名

    def getscoredlist(self,rows,wordids):
        totalscores=dict([(row[0],0) for row in rows])
        
        weights=[(1.0,self.frequencyscore(rows))]
        
        for (weight,scores) in weights:
            for urlid in totalscores:
                totalscores[urlid]+=weight*scores[urlid]
        return totalscores

    def geturlname(self,id):
        self.cursor.execute("select url from urllib where rowid=%d" % id)
        name=self.cursor.fetchone()[0] #tuple
        return name
        
    def query(self,q):
        rows,wordids=self.getmatchrows(q)
        scores=self.getscoredlist(rows,wordids)
        rankedscores=sorted([(score,urlid) for urlid,score in scores.items()],reverse=True)
        for (scores,urlid) in rankedscores[0:10]:
            print('%f\t%s' % (scores,self.geturlname(urlid)))
        return wordids,[r[1] for r in rankedscores[0:10]]





#归一化函数
    def normalizescores(self,scores,small_better=0):
        vsmall=0.00001   #避免除以0
        if small_better:
            minscore=min(scores.values())   #最小值除以所有其它值
            return dict([(u,float(minscore)/max(vsmall,l)) for (u,l) in scores.items()])
        else:
            maxscore=max(scores.values())  #其他值除以最大值
            if maxscore==0:maxscore=vsmall
            return dict([(u,float(l)/maxscore) for (u,l) in scores.items()])







#以单词频度作为接近程度的评价标准
    def frequencyscore(self,rows):
        counts={}
        for row in rows:
            counts.setdefault(row[0],0)
            counts[row[0]]+=1
        return self.normalizescores(counts)
        
    


#以文档位置作为接近程度的评价标准
    def locationscore(self,rows):
        pass
    
#以单词距离作为接近程度的评价标准
    def distancescore(self,rows):
        pass




#利用外部回指链接
    def inboundlinkscore(self,rows):
        uniqueurls=set([row[0] for row in rows])
        inboundcount={}
        for u in uniqueurls:
            self.cursor.execute("select count(*) from link where toid=%d" % u)
            count=self.cursor.fetchone()
            inboundcount[u]=count
        return self.normalizescores(inboundcount)




#pagerank算法
            
    def pagerankscore(self,rows):
        pageranks={}
        for row in rows:
            self.cursor.execute("select score from pagerank where urlid=%d" %row[0])
            score=self.cursor.fetchone()[0]
            pageranks[row[0]]=score
        maxrank=max(pageranks.values())
        nomalizedscores=dict([(u,float(l)/maxrank) for (u,l) in pageranks.items()])
        return nomalizedscores
    
    
    def nnscore(self,rows,wordids):
        urlids=[urlid for urlid in set([row[0] for row in rows])]
        nnres=mynet.getresult(wordids,urlids)
        scores=dict([(urlids[i],nnres[i]) for i in range(len(urlids))])
        return self.normalizescores(scores)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    























#cr.cursor.execute('create table wordlist2 (rowid int(10),word varchar(20),primary key (rowid))')
#for i in range(len(words)):
#    word=words[i]  
#    if word in ignorewords:continue
#    wordid=cr.getentryid('wordlist','word',word)
#    cr.cursor.execute('insert into wordlist(wordid,word) values (%d,%s)' % (wordid,word))
#    cr.cursor.execute('insert into wordlocation(urlid,wordid,location) values (%d,%d,%d)' % (urlid,wordid,i))
























































