# -*- coding: utf-8 -*-
'''
类名：M1809_finance_weight
作者：徐抒田
日期：2018-7-9
描述：
机器学习方法确定,权重()
遗留问题：
1、资产负债比,营业税增长率,营业现金增长率,现金增长净额,期末现金字段待解决
2、从库读文件待解决
版本号：V0.1
'''


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_blobs
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split 
from sklearn.metrics import classification_report   
from sklearn import metrics
import lightgbm as lgb


'''
修改成从数据库中读取文件
'''
result_yinli = pd.read_csv('D:/999github/anack/M1809/xst/result_yinli.csv')
result_yingyun = pd.read_csv('D:/999github/anack/M1809/xst/result_yingyun.csv')
result_chengzhang = pd.read_csv('D:/999github/anack/M1809/xst/result_chengzhang.csv')
result_changzhai = pd.read_csv('D:/999github/anack/M1809/xst/result_changzhai.csv')
result_xianjin = pd.read_csv('D:/999github/anack/M1809/xst/result_xianjin.csv')

df_final = pd.read_csv('D:/999github/anack/M1809/xst/target.csv')

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
code = data['code']
name = data['name']
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


'''
资产负债比,营业税增长率,营业现金增长率,现金增长净额,期末现金
'''
features = features[['targ20174','nav20174','gross_profit_rate20174','cashflowratio20174','net_profit_ratio20174','mbrg20174','currentratio20174','currentasset_turnover20174','inventory_days20174']]



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






def ml_for_weight(features,target):
    
    
    min_max_scaler = preprocessing.MinMaxScaler()
    features_new = min_max_scaler.fit_transform(features)
    features = pd.DataFrame(features_new, columns=features.columns)  
    X_train,X_test,y_train,y_test = train_test_split(features,target,test_size=0.25,random_state=42)

    '''
    调参
    '''
    clf = lgb.LGBMClassifier(
        boosting_type='gbdt', num_leaves=31, reg_alpha=0, reg_lambda=1,
        max_depth=-1, n_estimators=800, objective='binary',
        subsample=0.7, colsample_bytree=0.7, subsample_freq=2,
        learning_rate=0.05, min_child_weight=20, random_state=2018, n_jobs=-1,class_weight = 'balanced'
    )

    clf = clf.fit(X_train, y_train, eval_set=[(X_train, y_train),(X_test, y_test)], eval_names = ['train','test'],eval_metric='auc',early_stopping_rounds=100) 

    y_pre = clf.predict(X_test)

    y_pre_pro = clf.predict_proba(X_test)[:, 1]
# =============================================================================
# print(y_pre_pro)
# =============================================================================
    print(classification_report(y_test,y_pre))
    print(metrics.roc_auc_score(y_test,y_pre_pro))  #预测Y值得分
    aucfun(y_test,y_pre_pro)

    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1]
    print("Feature ranking:")
    for f in range(features.shape[1]):
        print("%d. feature %d (%f): %s" % (f + 1, indices[f], importances[indices[f]] , features.columns[indices[f]] ))

        
    return features.columns,importances


a,b = ml_for_weight(features,target)



# =============================================================================
# y_pre_pro_f = clf.predict_proba(features)[:, 1]
# 
# y_pre_pro_f = pd.DataFrame({'code' : code,
#                             'name' : name,
#                    'gailv' : y_pre_pro_f
#                    })
#     
# y_pre_pro_f.to_csv('D:/999github/anack/M1809/y_pre_pro_f.csv',index =False)
# =============================================================================
