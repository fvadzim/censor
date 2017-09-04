# -*- coding:utf-8 -*-
f = open("data/publications.csv",'r')
i=0
for line in f:
	
        if '\0' in line:
             print(line)
        i+=1
        print(i)
