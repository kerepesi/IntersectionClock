import os
import sys

f=open('file_list.csv')
for l in f:
    sl=l.strip().split()
    file_name=sl[0][:-3]
    c='python ../../LiftOver.py Data/'+file_name+'-Format.py.tsv 0 hg19 hg38'
    os.system(c)
