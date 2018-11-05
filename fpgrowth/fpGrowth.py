# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 20:09:11 2018

@author: chencong
"""

print(__doc__)

class treeNode:
    def __init__(self,nameValue,numOccur,parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}
        
    def inc(self,numOccur):
        self.count += numOccur
        
    def disp(self,ind=1):
        print('   '*ind,self.name,' ',self.count)
        for child in self.children.values():
            child.disp(ind+1)
            
            
            
#load the data
def loadSimpDat():
    simpDat = [['r','z','h','j','p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat



     
    
def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        if not retDict.has_key(frozenset(trans)):
            retDict[frozenset(trans)] = 1
        else:
            retDict[frozenset(trans)] += 1
    return retDict


def updateHeader(nodeToTest,targetNode):
    while (nodeToTest.nodeLink is not None):
        nodeToTest = nodeToTest.nodeLink
        nodeToTest.nodeLink = targetNode
        
        

def updataTree(items,inTree,headerTable,count):
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[items[0]] = treeNode(items[0],count,inTree)
    if headerTable[items[0]][1] is None:
        headerTable[items[0]][1] = inTree.children[items[0]]
    else:
        updateHeader(headerTable[items[0]][1],inTree.children[items[0]])
    if len(items)>1:
        updataTree(items[1:],inTree.children[items[0]],headerTable.count)
    
    

def createTree(dataSet,minSup=1):
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable = headerTable.get(item,0)+dataSet[trans]
    for k in headerTable.keys():
        if headerTable[k]<minSup:
            del(headerTable[k])
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0:
        return None,None
    for k in headerTable:
        headerTable[k] = [headerTable[k],None]
        
        
    retTree = treeNode('Null Set',1,None)            
    for tranSet,count in dataSet.items():
        localId = {}
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(),\
                            key=lambda p:p[1],reverse=True)]
        updataTree(orderedItems,retTree,headerTable,count)
    return retTree,headerTable
            
            
            
    
    

















































