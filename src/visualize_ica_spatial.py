import numpy as np 
import pandas as pd 
import geopandas
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.axes_grid1 import make_axes_locatable
sns.set()

# inputs
ncomp = 10
inpath = '../results/ica_'+str(ncomp)+'/'
# modality = 'mortality'
modality = 'increase'
ref_path = '../data/covid-19/data/reference.csv'
outpath = inpath

# setup
t1 = list( range( 1, ncomp+1 ) )
cols_ = ['IC'+str(n) for n in t1]
plt.close('all')

ref = pd.read_csv( ref_path )
ref.drop_duplicates(subset='Country_Region', keep="first", inplace=True)
ref.rename(columns={'Country_Region': 'Country'}, inplace=True)
ref.set_index('Country', inplace=True) 

# components
ic_sig = pd.read_csv( inpath+modality+'_rate_ica'+str(ncomp)+'_mixing.csv', index_col='Country' )
ic_sig.reset_index(level=0, inplace=True)
ic_sig = pd.melt(ic_sig, id_vars='Country', value_vars=cols_) 

# join to get iso 
ic_sig = ic_sig.join( ref[['iso3']], on='Country')
ic_sig.rename( columns={'iso3': 'iso_a3'}, inplace=True )

# # step plot
# f, ax = plt.subplots(figsize=(48, 24))
# sns.lineplot(x='Country', y='value', hue='variable', data=ic_sig, ax=ax, drawstyle='steps-pre')
# plt.xticks(rotation=90)
# plt.title('mortality_rate IC signals')
# f.savefig( outpath+'mortality_rate_ica'+str(ncomp)+'_signal.png', bbox_inches='tight' )

# create choropleth maps
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
world = world[(world.pop_est>0) & (world.name!="Antarctica")]

for ic in range(0, ncomp):
    # set figure size
    fig, ax = plt.subplots(figsize=(18, 12))
    # subset the component dataframe based on IC#
    t1 = ic_sig.loc[ ic_sig.variable=='IC'+str(ic+1) ]
    # join with world dataframe country column
    t1 = world.join( t1.set_index('iso_a3'), on='iso_a3' )
    # colorbar limits
    vlim = max( abs( t1.value ) ) 
    # resize colorbar
    divider = make_axes_locatable( ax )
    cax = divider.append_axes("right", size="5%", pad=0.1)
    # plot
    t1.plot(column='value', ax=ax,
        cmap='Spectral', vmin=-vlim, vmax=vlim, cax=cax,
        legend=True, legend_kwds={'label': "Component weight", 'orientation': "vertical"})
    ax.set_title( modality+' rate IC '+str(ic+1) )
    # save
    fig.savefig( outpath+modality+'_ic'+str(ic+1)+'_map.png', dpi=300, bbox_inches='tight' )

# # PCA result
# H = pd.read_csv( inpath+'mortality_rate_pca_signal.csv' )





