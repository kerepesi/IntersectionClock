import sys
from liftover import get_lifter
# Run: python LiftOver.py GSM1240860_hSperm-524-90.cpgs.txt-head-10000.csv 1 hg19 hg38
# This program shifts the coordinates by 'Shift' then
# lifts the positions and omits unsuccesfully lifted as well as duplicated coordinates (keep the first). 

IN_name=sys.argv[1]
Shift=int(sys.argv[2])
Lift_from=sys.argv[3]
Lift_to=sys.argv[4]
Occured={}

converter = get_lifter(Lift_from, Lift_to)

f_in=open(IN_name)
OUT_name=IN_name+'-'+sys.argv[0].split('/')[-1]+'_'+str(Shift)+'_'+Lift_from+'_'+Lift_to+'.txt'
print(OUT_name)
f_out=open(OUT_name,'w')
for l in f_in:
    sl=l.strip().split('\t')
    Chr=sl[0]
    Pos=int(sl[1])
    Cov=sl[2]
    Met=sl[3]
    Pos=Pos+Shift
    try:
        Conv = converter[Chr][Pos]
        ConvChr = str(Conv[0][0])
        ConvPos = str(Conv[0][1])
        Ind = ConvChr+'_'+ConvPos
        if Ind not in Occured: 
            f_out.write(ConvChr+'\t'+ConvPos+'\t'+Cov+'\t'+Met+'\n')
            Occured[Ind]=1
    except:
        skip=1
