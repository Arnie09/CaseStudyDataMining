import pandas as pd
from itertools import combinations
class apriori:

    def __init__(self,**kwargs):

        if(kwargs.get('rules_len') is not None):
            self.rulesLength = kwargs.get('rules_len')
        else:
            self.rulesLength = 999
        self.min=kwargs.get('min')
        self.rulesMin = kwargs.get('rulesMin')
        if(kwargs.get('address') is not None):
            self.dataset=pd.read_excel(kwargs.get('address'))
            self.columnheader=list(self.dataset.columns.values)
            self.invNo=self.dataset[kwargs.get('invNo')] #list of the invoice no.
            self.productcode=self.dataset[kwargs.get('productCode')] #list of all the product codes

        if(kwargs.get('transactions') is not None):
            self.transaction = kwargs.get('transactions')
            self.uniqproductcode = kwargs.get('productlist')
        else:
            self.transaction={}  #to store all the transactions w.r.t invNo
            self.uniqproductcode=[] #storing the codes of each product only once

        self.allLs={}
        self.finalL={}
        self.finalRules={}

        if(self.transaction):# boolean on an empty dictionary returns false
            self.createL1()
            self.createLs()
        else:
            self.initialise()
            self.createL1()
            self.createLs()

    def initialise(self):#to store the data required in transaction and uniqproductcode
        for item in self.productcode:
            if item not in self.uniqproductcode:
                self.uniqproductcode.append(item)

        #All products with same invoice no. are listed together
        for i in range(0,len(self.invNo)):
            if self.invNo[i] not in self.transaction:
                self.transaction[self.invNo[i]]=[self.productcode[i]]
            else:
                self.transaction[self.invNo[i]]=self.transaction[self.invNo[i]]+[self.productcode[i]]

    def createL1(self):

        l1={}
        temp=[]
        for item in self.uniqproductcode:
            count=0
            for eachlist in self.transaction:
                if item in self.transaction[eachlist]:
                    count+=1
            if count>=self.min:
                temp.append(item)
                l1[tuple(temp)]=count
                temp=[]

        self.allLs[1]=l1

    def createLs(self):
        List=self.allLs[1]
        a=1

        while(len(List)!= 0 and a<=self.rulesLength):
            a+=1
            List=self.createList(List,a)
            self.allLs[a]=List
            self.finalL=self.allLs[a]
            self.displayRules(a)

    def createList(self,List,a):
        lx={}
        combo=[] #We dont want anagrams of a similar combo so we store each uniq combination here and compare the new one with each of its item
        lprevKeys=list(List.keys())
        L=len(lprevKeys)
        for i in range(0,L):
            for j in range(i+1,L):

                pair=self.comb(list(lprevKeys[i]),list(lprevKeys[j]))

                if len(pair)==a:
                    uniqcheck=True

                    for eachcombo in combo:
                        if all(i in eachcombo for i in pair):
                            uniqcheck=False
                    if uniqcheck:
                        count=0
                        for eachlist in self.transaction:
                            if all(elem in self.transaction[eachlist] for elem in pair):
                                count+=1
                        if(count>=self.min):
                            lx[tuple(pair)]=count
                            combo.append(pair)
        return lx

    def displayRules(self,a):
        #print("All the important associations are:  \n")
        rules=[]
        for keys in self.finalL:
            supL=self.finalL[keys] #support of FinalList
            L=list(keys) #items of finallist stored as a list

            subsets=[]


            for i in range(1,len(keys)):
                subsets.append(list(combinations(keys,i))) #all non-empty subsets created and stored as tuples in subsets list

            #we will use S to store each subset. L stores the main set
            minconfi=self.rulesMin
            for eachlist in subsets:
                for subset in eachlist:
                    S=list(subset)
                    LminusS=[i for i in L if i not in S]
                    supS=self.allLs[len(subset)][subset]
                    confidence = supL/supS

                    if confidence>=minconfi:
                        rule=(str(S)+"=>"+str(LminusS)+": "+str(confidence*100)+"%")
                        rules.append(rule)
        self.finalRules[a]=rules

    def comb(self,A,B): #It combines two lists without keeping duplicates while maintaining the order
        c=A+[]
        for i in B:
            if i not in A:
                c.append(i)
        return c
