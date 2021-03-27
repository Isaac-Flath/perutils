# export
from pathlib import Path
import pandas as pd
from fastai.tabular.all import *


# export
def get_corr(df):
    return pd.DataFrame(np.round(scipy.stats.spearmanr(df).correlation, 4),index=df.columns,columns=df.columns)

# export
def corr_drop_cols(cor, thresh):
    ''' input:  cor is a correlation df such as df.corr().abs().  Thresh is the cutoff for what is too corrolated
        output: list of columns to drop
    '''
    max_corr = dict()
    drop_list = L()
    for col in cor.columns:
        max_corr[col] = 0
        for row in cor.index:
            if row == col: continue
            if row in drop_list: continue
            if cor.loc[row,col] > max_corr[col]: max_corr[col] = cor.loc[row,col]
        if max_corr[col] > thresh: drop_list.append(col)
    return drop_list

# export
def rf_feat_importance(m, df):
    '''Code from github.com/fastai/fastbook chapter 9'''
    return pd.DataFrame({'cols':df.columns, 'imp':m.feature_importances_}).sort_values('imp', ascending=False)

# export
def plot_fi(fi): 
    '''Code from github.com/fastai/fastbook chapter 9'''
    return fi.plot('cols', 'imp', 'barh', figsize=(12,7), legend=False)

# export
@patch
def export(self:TabularPandas, fname='export.pkl', pickle_protocol=2):
    '''Export the contents of `self` without the items
    Written by Zach Mueller'''
    old_to = self
    self = self.new_empty()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        pickle.dump(self, open(Path(fname), 'wb'), protocol=pickle_protocol)
        self = old_to

# export
def load_pandas(fname):
    '''Load in a `TabularPandas` object from `fname`
    Written by Zach Mueller'''

    distrib_barrier()
    res = pickle.load(open(fname, 'rb'))
    return res

