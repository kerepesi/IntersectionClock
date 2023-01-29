import os
import sys

f=open('file_list.csv')
for l in f:
    sl=l.strip().split()
    file_name=sl[0][:-3]
    c='python Format.py Data/'+file_name
    print(c)
    os.system(c)
