import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from glmnet import ElasticNet
from scipy.stats import spearmanr, pearsonr, ttest_rel, ttest_1samp
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, confusion_matrix, accuracy_score, median_absolute_error
import sys

np.random.seed(0)

IN_app=sys.argv[1]
IN_FT='TrainingData/FTGenForGenomicCov_MergeStrands.py-cov5.csv-dropna.py-1.0.csv-Format.py.csv'
IN_meta='TrainingData/MetaPolished.csv'
Age_col='Age (years)'
MinCov=int(sys.argv[2])
N_splits=5

Sample=IN_app.split('/')[-1]
T=pd.read_csv(IN_app,sep='\t',header=None)
T.columns=['Chr','Pos','Cov','Met']
T['Ind']=T['Chr']+'_'+T['Pos'].astype('str')
T=T.set_index('Ind')
T[Sample]=T['Met']/T['Cov']
T_sel=T[T['Cov'] >= MinCov]

FT_app=T_sel[[Sample]]
FT=pd.read_csv(IN_FT,index_col=[0])
Common=FT.index.intersection(FT_app.index)
FT_common=FT.loc[Common]
FT_app_common=FT_app.loc[Common]
Meta=pd.read_csv(IN_meta,index_col=[0])

FT_commonT=FT_common.T
X=FT_commonT.values
y=Meta[Age_col].values

modelcv=ElasticNet(n_splits=10,alpha=0.5)
pred=np.zeros(len(y))
fold=np.zeros(len(y))
model_coef=[]
model_inter=[]
kf = KFold(n_splits=N_splits, shuffle=True)
k=0
for train_index, test_index in kf.split(X):
    k+=1
    modelcv.fit(X[train_index], y[train_index])
    pred_train=modelcv.predict(X[train_index])
    pred_test=modelcv.predict(X[test_index])
    pred[test_index]=pred_test
    fold[test_index]=k
    model_coef.append(modelcv.coef_)
    model_inter.append(modelcv.intercept_)

CV_table=FT_commonT.copy()
Pred_col='Predicted '+Age_col
CV_table[Pred_col]=pred
CV_table['CV fold']=fold.astype(int)
CV_table_out=CV_table[[Pred_col,'CV fold']]
CV_table_out.index.name='Sample name'
OUT_name=IN_app+'-'+sys.argv[0].split('/')[-1]+'-MinCov'+str(MinCov)+'-CV_table.csv'
print(OUT_name)
CV_table_out.to_csv(OUT_name)

CV_clocks=pd.DataFrame(model_coef,index=range(1,N_splits+1),columns=FT_commonT.columns)
CV_clocks['Interception']=model_inter
CV_clocks_T=CV_clocks.T
CV_clocks_T_out=CV_clocks_T.loc[['Interception']+list(CV_clocks_T.index[:-1])]
OUT_name=IN_app+'-'+sys.argv[0].split('/')[-1]+'-MinCov'+str(MinCov)+'-CV_clocks.csv'
print(OUT_name)
CV_clocks_T_out.to_csv(OUT_name)

Meta[Pred_col]=CV_table_out[Pred_col]
r,p = pearsonr(Meta[Age_col],Meta[Pred_col])
MedAE = median_absolute_error(Meta[Age_col],Meta[Pred_col])

# Prediction on test
Pred_list=[]
for Clock in CV_clocks_T_out.columns:
    Intercept=CV_clocks_T_out[Clock][0]
    Weights=CV_clocks_T_out[Clock][1:]
    FT_app_sel=FT_app.loc[Weights.index]
    Pred=(FT_app_sel[Sample]*Weights).sum()+Intercept
    Pred_list.append(Pred)
MeanPred=np.mean(Pred_list)

# Write the output
out=pd.DataFrame([[len(Common),r,MedAE,MeanPred]+Pred_list], 
              columns=['Intersected_sites','r_CV','MedAE_CV','MeanPred']+['Pred '+str(i) for i in range(1,len(Pred_list)+1)])
out.index=[Sample]
out.index.name = 'Sample'
out=out.round(3)
OUT_name=IN_app+'-'+sys.argv[0].split('/')[-1]+'-Pred.csv'
print(OUT_name)
out.to_csv(OUT_name)
