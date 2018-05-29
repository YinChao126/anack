# -*- coding: utf-8 -*-
'''
类名：M1809_finance_analysis（财务数据分析）
作者：徐抒田
日期：2018-5-28
描述：
1、初步调试机器学习方法

版本号：V0.1
'''


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

result_yinli = pd.read_csv('D:/999github/anack/M1809/result_yinli.csv')
result_yingyun = pd.read_csv('D:/999github/anack/M1809/result_yingyun.csv')
result_chengzhang = pd.read_csv('D:/999github/anack/M1809/result_chengzhang.csv')
result_changzhai = pd.read_csv('D:/999github/anack/M1809/result_changzhai.csv')
result_xianjin = pd.read_csv('D:/999github/anack/M1809/result_xianjin.csv')


df_final = pd.read_csv('D:/999github/anack/M1809/target.csv')
df_final = df_final[(df_final.firstincrase > 0.1) & (df_final.secondincrase > 0.1)]
df_final = pd.DataFrame({'code' : df_final['code'],
                   'label' : 1,
                   })


data = result_yinli
data = pd.merge(data, result_yingyun, on=['code','name'])
data = pd.merge(data, result_chengzhang, on=['code','name'])
data = pd.merge(data, result_changzhai, on=['code','name'])
data = pd.merge(data, result_xianjin, on=['code','name'])
data = pd.merge(data, df_final, on='code',how = 'left')

# =============================================================================
# null_counts = data.isnull().sum()
# print(null_counts)
# =============================================================================

data = data.fillna(0)
data = data.dropna(axis=0)



orig_columns = data.columns
drop_columns = []
for col in orig_columns:
    col_series = data[col].dropna().unique()
    if len(col_series) == 1:
        drop_columns.append(col)
data = data.drop(drop_columns, axis=1)
print(drop_columns)



target = data['label']
features = data.drop(['code','name','label'],axis=1)

features[features.currentratio20161 == '--'] = 0
features[features.quickratio20161=='--']=0
features[features.cashratio20161=='--']=0
features[features.icratio20161=='--']=0
features[features.sheqratio20161=='--']=0
features[features.adratio20161=='--']=0
features[features.currentratio20162=='--']=0
features[features.quickratio20162=='--']=0
features[features.cashratio20162=='--']=0
features[features.icratio20162=='--']=0
features[features.sheqratio20162=='--']=0
features[features.adratio20162=='--']=0
features[features.currentratio20163=='--']=0
features[features.quickratio20163=='--']=0
features[features.cashratio20163=='--']=0
features[features.icratio20163=='--']=0
features[features.sheqratio20163=='--']=0
features[features.adratio20163=='--']=0
features[features.currentratio20164=='--']=0
features[features.quickratio20164=='--']=0
features[features.cashratio20164=='--']=0
features[features.icratio20164=='--']=0
features[features.currentratio20171=='--']=0
features[features.quickratio20171=='--']=0
features[features.cashratio20171=='--']=0
features[features.icratio20171=='--']=0
features[features.sheqratio20171=='--']=0
features[features.adratio20171=='--']=0
features[features.currentratio20172=='--']=0
features[features.quickratio20172=='--']=0
features[features.cashratio20172=='--']=0
features[features.icratio20172=='--']=0
features[features.currentratio20173=='--']=0
features[features.quickratio20173=='--']=0
features[features.cashratio20173=='--']=0
features[features.icratio20173=='--']=0
features[features.currentratio20174=='--']=0
features[features.quickratio20174=='--']=0
features[features.cashratio20174=='--']=0
features[features.icratio20174=='--']=0
features[features.currentratio20181=='--']=0
features[features.quickratio20181=='--']=0
features[features.cashratio20181=='--']=0
features[features.icratio20181=='--']=0
features = features.astype('float64')


##基于树的方法不用做标准化、归一化处理
from sklearn import preprocessing
min_max_scaler = preprocessing.MinMaxScaler()
features_new = min_max_scaler.fit_transform(features)
features = pd.DataFrame(features_new, columns=features.columns)


from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_blobs
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split 
from sklearn.metrics import classification_report   
from sklearn import metrics


X_train,X_test,y_train,y_test = train_test_split(
features,target,test_size=0.25,random_state=42)

'''
Random_forset 
'''
clf = RandomForestClassifier(n_estimators=50,max_depth = 5,min_samples_split = 30,min_samples_leaf = 20,random_state=2018,class_weight="balanced")
clf = clf.fit(X_train, y_train)
y_pre = clf.predict(X_test)

y_pre_pro = clf.predict_proba(X_test)[:, 1]
print(y_pre_pro)
print(classification_report(y_test,y_pre))
print(metrics.roc_auc_score(y_test,y_pre))  #预测Y值得分

def aucfun(act,pred):
    fpr,tpr,thresholds = metrics.roc_curve(act,pred)
    plt.plot(fpr, tpr, color='darkorange',lw=2)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
# =============================================================================
#     print(fpr)
#     print(tpr)
#     print(thresholds)
# =============================================================================
    return metrics.auc(fpr,tpr)


aucfun(y_test,y_pre_pro)


importances = clf.feature_importances_
std = np.std([tree.feature_importances_ for tree in clf.estimators_],axis=0)
indices = np.argsort(importances)[::-1]
print("Feature ranking:")
for f in range(features.shape[1]):
    print("%d. feature %d (%f): %s" % (f + 1, indices[f], importances[indices[f]] , features.columns[indices[f]] ))




