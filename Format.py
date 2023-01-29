#First row of an example input: 
#Chr    Pos Ref Chain   Total   Met UnMet   MetRate Ref_context Type
#chr7    31498   g   -   8   0   8   0   CGG CpG

import sys
IN_name=sys.argv[1]
f=open(IN_name)
OUT_name=IN_name+'-'+sys.argv[0]+'.tsv'
f_out=open(OUT_name,'w')
print(OUT_name)
for l in f:
    sl=l.strip().split('\t')
    Chr=sl[0]
    Pos=sl[1]
    Cov=sl[4]
    Met=sl[5]
    Type=sl[9]
    if Type == 'CpG':
        f_out.write(Chr+'\t'+Pos+'\t'+Cov+'\t'+Met+'\n')
