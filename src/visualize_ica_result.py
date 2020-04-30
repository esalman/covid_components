import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

ncomp = 10

t1 = list( range( 1, ncomp+1 ) )
cols_ = ['IC'+str(n) for n in t1]
plt.close('all')

# mortality_rate
# time course
tc = pd.read_csv( '../results/mortality_rate_ica'+str(ncomp)+'_signal.csv', index_col='Date' )
tc.reset_index(level=0, inplace=True)
tc = pd.melt(tc, id_vars='Date', value_vars=cols_) 

f, ax = plt.subplots(figsize=(24, 12))
sns.lineplot(x='Date', y='value', hue='variable', data=tc, ax=ax)
plt.xticks(rotation=90)
plt.title('mortality_rate Time courses')
f.savefig('../results/mortality_rate_ica'+str(ncomp)+'_mixing.png')

# components
ic_sig = pd.read_csv( '../results/mortality_rate_ica'+str(ncomp)+'_mixing.csv', index_col='Country' )
ic_sig.reset_index(level=0, inplace=True)
ic_sig = pd.melt(ic_sig, id_vars='Country', value_vars=cols_) 

f, ax = plt.subplots(figsize=(48, 24))
sns.lineplot(x='Country', y='value', hue='variable', data=ic_sig, ax=ax, drawstyle='steps-pre')
plt.xticks(rotation=90)
plt.title('mortality_rate IC signals')
f.savefig('../results/mortality_rate_ica'+str(ncomp)+'_signal.png')

# increase_rate
# time course
tc = pd.read_csv( '../results/increase_rate_ica'+str(ncomp)+'_signal.csv', index_col='Date' )
tc.reset_index(level=0, inplace=True)
tc = pd.melt(tc, id_vars='Date', value_vars=cols_) 

f, ax = plt.subplots(figsize=(24, 12))
sns.lineplot(x='Date', y='value', hue='variable', data=tc, ax=ax)
plt.xticks(rotation=90)
plt.title('increase_rate Time courses')
f.savefig('../results/increase_rate_ica'+str(ncomp)+'_mixing.png')

# components
ic_sig = pd.read_csv( '../results/increase_rate_ica'+str(ncomp)+'_mixing.csv', index_col='Country' )
ic_sig.reset_index(level=0, inplace=True)
ic_sig = pd.melt(ic_sig, id_vars='Country', value_vars=cols_) 

f, ax = plt.subplots(figsize=(48, 24))
sns.lineplot(x='Country', y='value', hue='variable', data=ic_sig, ax=ax, drawstyle='steps-pre')
plt.xticks(rotation=90)
plt.title('increase_rate IC signals')
f.savefig('../results/increase_rate_ica'+str(ncomp)+'_signal.png')

# H = pd.read_csv( '../results/mortality_rate_pca_signal.csv' )



