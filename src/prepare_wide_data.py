import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import math

# inputs
ref_path = '../data/covid-19/data/reference.csv'
country_agg_path = '../data/covid-19/data/countries-aggregated.csv'
outpath = '../results/aggregate_data/'

# setup
sns.set()
figsize = (120, 60)
fontsize=60
cmap = sns.color_palette("YlGnBu", 100)
plt.close('all')
Path(outpath).mkdir(parents=True, exist_ok=True)

# load data
ref = pd.read_csv( ref_path )
country_agg = pd.read_csv( country_agg_path )

# join
ref.drop_duplicates(subset='Country_Region', keep="first", inplace=True)
ref.rename(columns={'Country_Region': 'Country'}, inplace=True)
ref.set_index('Country', inplace=True) 
country_agg = country_agg.join( ref[['Population']], on='Country')

# # drop Congo
# congo = country_agg.loc[ country_agg.iso3=='COG' ].index
# country_agg.drop( congo, inplace=True )

# get countries from country_agg which is a subset of Country_Region
countries = country_agg.Country.unique()

# add rate columns
country_agg['mortality_rate'] = country_agg['Deaths'] / country_agg['Confirmed']
country_agg['increase_rate'] = 0.0
country_agg['Confirmed_rate'] = country_agg['Confirmed'] / country_agg['Population']
country_agg['Recovered_rate'] = country_agg['Recovered'] / country_agg['Population']
country_agg['Deaths_rate'] = country_agg['Deaths'] / country_agg['Population']

# determine increase_rate
for cc in countries:
    cc_idx = country_agg.index[ country_agg.Country == cc ].tolist() 
    for t1, cc_i in enumerate(cc_idx):
        if t1 == 0:
            continue

        t2 = country_agg.loc[cc_i, 'Confirmed']
        t3 = country_agg.loc[cc_idx[t1-1], 'Confirmed']
        if t3 > 0:
            country_agg.at[cc_i, 'increase_rate'] = 100 * (t2-t3) / t3
        
country_agg['Confirmed_rate'] = np.log( country_agg['Confirmed_rate'], where=0.0<country_agg['Confirmed_rate'], out=np.nan * np.ones_like( country_agg['Confirmed_rate'] ) )
country_agg['Recovered_rate'] = np.log( country_agg['Recovered_rate'], where=0.0<country_agg['Recovered_rate'], out=np.nan * np.ones_like( country_agg['Recovered_rate'] ) )
country_agg['Deaths_rate'] = np.log( country_agg['Deaths_rate'], where=0.0<country_agg['Deaths_rate'], out=np.nan * np.ones_like( country_agg['Deaths_rate'] ) )
country_agg['mortality_rate'] = np.log( country_agg['mortality_rate'], where=0.0<country_agg['mortality_rate'], out=np.nan * np.ones_like( country_agg['mortality_rate'] ) )
country_agg['increase_rate'] = np.log( country_agg['increase_rate'], where=0.0<country_agg['increase_rate'], out=np.nan * np.ones_like( country_agg['increase_rate'] ) )

print( country_agg )
country_agg.to_csv( outpath+'country_agg_lognorm.csv', index=False )

# long to wide
Confirmed = country_agg.pivot(index='Date', columns='Country', values='Confirmed_rate')
Confirmed.to_csv( outpath+'Confirmed_lognorm_wide.csv', index=True )

Recovered = country_agg.pivot(index='Date', columns='Country', values='Recovered_rate')
Recovered.to_csv( outpath+'Recovered_lognorm_wide.csv', index=True )

Deaths = country_agg.pivot(index='Date', columns='Country', values='Deaths_rate')
Deaths.to_csv( outpath+'Deaths_lognorm_wide.csv', index=True )

mortality_rate = country_agg.pivot(index='Date', columns='Country', values='mortality_rate')
mortality_rate.to_csv( outpath+'mortality_rate_lognorm_wide.csv', index=True )

increase_rate = country_agg.pivot(index='Date', columns='Country', values='increase_rate')
increase_rate.to_csv( outpath+'increase_rate_lognorm_wide.csv', index=True )

# heatmaps
print('plotting Confirmed Cases')
f, ax = plt.subplots(figsize=figsize)
ax = sns.heatmap(Confirmed, fmt="d", ax=ax, cmap=cmap)
ax.set_xlabel( ax.get_xlabel(), fontsize=fontsize)
ax.set_ylabel( ax.get_ylabel(), fontsize=fontsize)
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=fontsize)
plt.title('Confirmed Cases (normalized by population, logarithmic)', fontdict={'fontsize':fontsize})
f.savefig( outpath+'confirmed_heatmap.png', bbox_inches='tight' )

print('plotting Recovered Cases')
f, ax = plt.subplots(figsize=figsize)
ax = sns.heatmap(Recovered, fmt="d", ax=ax, cmap=cmap)
ax.set_xlabel( ax.get_xlabel(), fontsize=fontsize)
ax.set_ylabel( ax.get_ylabel(), fontsize=fontsize)
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=fontsize)
plt.title('Recovered Cases (normalized by population, logarithmic)', fontdict={'fontsize':fontsize})
f.savefig( outpath+'recovered_heatmap.png', bbox_inches='tight' )

print('plotting Deaths')
f, ax = plt.subplots(figsize=figsize)
ax = sns.heatmap(Deaths, fmt="d", ax=ax, cmap=cmap)
ax.set_xlabel( ax.get_xlabel(), fontsize=fontsize)
ax.set_ylabel( ax.get_ylabel(), fontsize=fontsize)
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=fontsize)
plt.title('Deaths (normalized by population, logarithmic)', fontdict={'fontsize':fontsize})
f.savefig( outpath+'deaths_heatmap.png', bbox_inches='tight' )

print('plotting Mortality Rate')
f, ax = plt.subplots(figsize=figsize)
ax = sns.heatmap(mortality_rate, fmt="d", ax=ax, cmap=cmap)
ax.set_xlabel( ax.get_xlabel(), fontsize=fontsize)
ax.set_ylabel( ax.get_ylabel(), fontsize=fontsize)
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=fontsize)
plt.title('Mortality Rate (logarithmic)', fontdict={'fontsize':fontsize})
f.savefig( outpath+'mortality_rate_heatmap.png', bbox_inches='tight' )

print('plotting Increase Rate')
f, ax = plt.subplots(figsize=figsize)
ax = sns.heatmap(increase_rate, fmt="d", ax=ax, cmap=cmap)
ax.set_xlabel( ax.get_xlabel(), fontsize=fontsize)
ax.set_ylabel( ax.get_ylabel(), fontsize=fontsize)
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=fontsize)
plt.title('Increase Rate (logarithmic)', fontdict={'fontsize':fontsize})
f.savefig( outpath+'increase_rate_heatmap.png', bbox_inches='tight' )


