import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# inputs
ncomp = 3
inpath = '../results/ica_'+str(ncomp)+'/'
# modality = 'mortality'
modality = 'increase'
outpath = inpath

# setup
t1 = list( range( 1, ncomp+1 ) )
cols_ = ['IC'+str(n) for n in t1]
plt.close('all')

# time course
tc_wide = pd.read_csv( inpath+modality+'_rate_ica'+str(ncomp)+'_signal.csv', index_col='Date' )
tc_wide.reset_index(level=0, inplace=True)
tc = pd.melt(tc_wide, id_vars='Date', value_vars=cols_) 

# plot time course
f, ax = plt.subplots(figsize=(24, 12))
sns.lineplot(x='Date', y='value', hue='variable', data=tc, ax=ax)
plt.xticks(rotation=90)
plt.title('mortality_rate Time courses')
f.savefig( outpath+modality+'_mixing_ica'+str(ncomp)+'.png', bbox_inches='tight' )

# FNC
f, ax = plt.subplots(figsize=(9, 9))
FNC = tc_wide.iloc[:,-3:].corr("pearson")
sns.heatmap(FNC, vmax=1.0, vmin=-1.0, cmap='Spectral',
            square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot = True)
f.savefig( outpath+modality+'_FNC_ica'+str(ncomp)+'.png', bbox_inches='tight' )

