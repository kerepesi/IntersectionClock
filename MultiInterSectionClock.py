import os
import sys
import pandas as pd

MinCov=sys.argv[1]
f=open('file_list.csv')
for l in f:
    sl=l.strip().split()
    file_name=sl[0][:-3]
    c='python ../../InterSectionClock.py Data/'+file_name+'-Format.py.tsv-LiftOver.py_0_hg19_hg38.txt '+MinCov
    os.system(c)
