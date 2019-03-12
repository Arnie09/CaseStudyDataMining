import math
import pandas as pd
import xlrd
from itertools import combinations
class treeNode:
    def __init__(self,name,count,parent,label):
        self.name=str(name)
        self.count=count
        self.parent=parent
        self.children={}
        self.nodeLink=None #to store the link to the next similar node in the fp tree
        self.label=str(label) #this is important for creating two different nodes of same name in the fptree display. If tree is not being displayed, this is useless
    #Adding Children to the current node
    def addChildren(self,child):
        self.children[child.name]=child
    #A display function just for debugging purpose
    def disp(self, ind=1):
        print ('  '*ind, self.name, ':', self.count)
        for child in self.children.values():
            child.disp(ind+1)


class FP_Tree:
    def __init__(self,**kwargs):
        self.minSup=kwargs.get('min')
        self.labelcount=0
        self.freqItems=[]
        self.dataSet={}

        if(kwargs.get('address') is not None):
            self.initialiseData(kwargs.get('address'),kwargs.get('TransID'),kwargs.get('ProductCode'))

        elif(kwargs.get('transactions') is not None):

            self.dataSet=kwargs.get('transactions')
            self.formatdata()


        self.mainTree,self.mainHeadertable=self.createTree(self.dataSet,self.minSup)# main FP tree and HeaderTable are formed


        self.mineTree(self.mainTree,self.mainHeadertable,[],math.inf) #Mining the main tree


    def formatdata(self):

        self.dataSet=list(self.dataSet.values())
        for i in self.dataSet:
            i.append(1)


    def initialiseData(self,path,TransID,ProductCode):#This function converts the dataset to the format in which our algorithm will work.
        dataset=pd.read_excel(path)
        invNo=dataset[TransID]
        productcode=dataset[ProductCode]

        for i in range(len(invNo)):
            self.dataSet[invNo[i]]=self.dataSet.get(invNo[i],[])+[str(productcode[i])]

        self.formatdata()


    def createTree(self,data,sup):#This function creates the FP tree for the data passed and returns the tree along with the corrosponding HeaderTable. This function was created keeping in mind that it will be used recursively
        headerTable={}

        for trans in data:
            for item in trans[:-1]:
                headerTable[item]=headerTable.get(item,0)+trans[-1]
        for k in set(headerTable):
            if headerTable[k]<sup:
                del(headerTable[k])
        for k in headerTable:
            headerTable[k]=[headerTable[k],None]

        retTree=treeNode('Null',0,None,'Null'+str(self.labelcount)) #The root node is created here with name null
        self.labelcount+=1 #Ignore label count as it is for tree visualisation only and useless here
        freqitems=list(headerTable.keys())

        for trans in data:
            local={}
            for item in trans[:-1]:
                if item in freqitems:
                    local[item]=headerTable[item][0]
            if(len(local)>0):
                ordereditems=[v[0] for v in sorted(local.items(),key=lambda p:p[1],reverse=True)] #sorted w.r.t support count in descending order
                self.updateTree(ordereditems,retTree,headerTable,trans[-1])




        return retTree,headerTable


    def updateTree(self,items,inTree,headerTable,count): #This function is used by create tree function to add each transaction as a subtree to the root node
        if items[0] in inTree.children:
            inTree.children[items[0]].count+=count
        else:
            newNode=treeNode(items[0],count,inTree,str(items[0])+str(self.labelcount))
            self.labelcount+=1
            inTree.addChildren(newNode)
            if headerTable[items[0]][1]==None:
                headerTable[items[0]][1]=newNode
            else:
                self.updateHeader(headerTable[items[0]][1],newNode)
        if len(items)>1:
            self.updateTree(items[1:],inTree.children[items[0]],headerTable,count)

    def updateHeader(self,nodeToTest,targetNode): #This function is used by updateTree function to keep the Header updated as pasr the tree
        while (nodeToTest.nodeLink != None):
            nodeToTest = nodeToTest.nodeLink
        nodeToTest.nodeLink = targetNode


    def ascendTree(self,node,path): #A small function used by findPrefixPath function to climb the tree while recording the path till it reaches root node

        if node.parent!=None:
            path.append(node.name)
            self.ascendTree(node.parent,path)

    def findPrefixPath(self,basePat,node): #This function returns the conditional pattern bases for a give node
        condPat=[]

        while node!=None:
            prefixpath=[]
            self.ascendTree(node,prefixpath)
            if len(prefixpath)>1:
                condPat.append(prefixpath[1:]+[node.count])
            node=node.nodeLink
        return condPat


    def mineTree(self,inTree,headerTable,preFix,count):#This function is for mining the main tree as well as the conditional trees

        #bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1][0])]
        bigL=headerTable

        for basePat in bigL:
            k=min(headerTable[basePat][0],count)
            newFreqItem=preFix.copy()
            newFreqItem.append(basePat)
            #if len(newFreqItem)>1:
            self.freqItems.append(newFreqItem+[k])
            condPattbases=self.findPrefixPath(basePat,headerTable[basePat][1])
            myCondTree,myHead=self.createTree(condPattbases,self.minSup)
            if myHead!=None:
                self.mineTree(myCondTree,myHead,newFreqItem,k)

    def display(self):
        ordereditems=[v for v in sorted(self.freqItems,key=len)]
        for i in ordereditems:
            print(i)

    def displayRules(self,conf=0.8):
        suppdata={}
        rules=[]
        k=list(self.mainHeadertable.keys())
        for i in range(len(self.freqItems)):
            t=self.freqItems[i][-1]
            self.freqItems[i]=[v for v in sorted(self.freqItems[i][:-1],key=k.index)]+[t]
        for i in self.freqItems:
            suppdata[tuple(i[:-1])]=i[-1]
        #print(suppdata)
        for key in suppdata:
            supL=suppdata[key]
            L=list(key)
            subsets=[]

            for i in range(1,len(key)):
                subsets=(list(combinations(key,i)))

                for subset in subsets:

                    S=list(subset)
                    LminusS=[i for i in L if i not in S]

                    supS=suppdata[subset]

                    confidence=supL/supS
                    if confidence>=conf:
                        rule=(str(S),str(LminusS),confidence*100)
                        print(rule[0],'=>',rule[1],":",str(round(rule[2]))+"%")










"""

obj=FP_Tree(address=r"E:\Projects\machine Learning\Book1.xlsx",TransID='InvoiceNo',ProductCode='StockCode',min=5)#address,TransID,ProductCode,minSup):
#obj.display()
obj.displayRules()"""
