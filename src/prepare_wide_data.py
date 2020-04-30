import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# inputs
ref_path = '../data/covid-19/data/reference.csv'
country_agg_path = '../data/covid-19/data/countries-aggregated.csv'

# load data
ref = pd.read_csv( ref_path )
country_agg = pd.read_csv( country_agg_path )

# get countries from country_agg which is a subset of Country_Region
countries = country_agg.Country.unique()

# add mortality rate and increase rate columns
country_agg['mortality_rate'] = np.nan
country_agg['increase_rate'] = np.nan

for cc in countries:
    cc_idx = country_agg.index[country_agg.Country.str.match(cc)].tolist() 
    for t1, cc_i in enumerate(cc_idx):
        if t1 == 0:
            continue
        
        # check 
        # print(t1, cc_i, cc_idx[t1-1])

        # determine mortality_rate
        t2 = country_agg.at[cc_i, 'Confirmed']
        t3 = country_agg.at[cc_i, 'Deaths']
        country_agg.at[cc_i, 'mortality_rate'] = 100 * t3 / t2
        
        # determine increase_rate
        t2 = country_agg.at[cc_i, 'Confirmed']
        t3 = country_agg.at[cc_idx[t1-1], 'Confirmed']
        if t3 != 0:
            country_agg.at[cc_i, 'increase_rate'] = 100 * (t2-t3) / t3

# view and save mortality_rate and increase_rate
print( country_agg )
country_agg.to_csv( '../results/country_agg.csv', index=False )

country_agg['Confirmed'] = np.log10( country_agg['Confirmed'], where=0<country_agg['Confirmed'], out=np.nan * np.ones_like( country_agg['Confirmed'] ) )
country_agg['Recovered'] = np.log( country_agg['Recovered'], where=0<country_agg['Recovered'], out=np.nan * np.ones_like( country_agg['Recovered'] ) )
country_agg['Deaths'] = np.log( country_agg['Deaths'], where=0<country_agg['Deaths'], out=np.nan * np.ones_like( country_agg['Deaths'] ) )
country_agg['mortality_rate'] = np.log( country_agg['mortality_rate'], where=0<country_agg['mortality_rate'], out=np.nan * np.ones_like( country_agg['mortality_rate'] ) )
country_agg['increase_rate'] = np.log( country_agg['increase_rate'], where=0<country_agg['increase_rate'], out=np.nan * np.ones_like( country_agg['increase_rate'] ) )

print( country_agg )
country_agg.to_csv( '../results/country_agg_lognorm.csv', index=False )

# long to wide
Confirmed = country_agg.pivot(index='Date', columns='Country', values='Confirmed')
Recovered = country_agg.pivot(index='Date', columns='Country', values='Recovered')
Deaths = country_agg.pivot(index='Date', columns='Country', values='Deaths')
mortality_rate = country_agg.pivot(index='Date', columns='Country', values='mortality_rate')
increase_rate = country_agg.pivot(index='Date', columns='Country', values='increase_rate')

# heatmaps
f, ax = plt.subplots(figsize=(90, 60))
cmap = sns.color_palette("husl", 100)
sns.heatmap(Confirmed, fmt="d", ax=ax, cmap=cmap)
print('plotting Confirmed Cases')
plt.title('Confirmed Cases (logarithmic)')
f.savefig("../results/confirmed_heatmap.png")

f, ax = plt.subplots(figsize=(90, 60))
cmap = sns.color_palette("husl", 100)
sns.heatmap(Recovered, fmt="d", ax=ax, cmap=cmap)
print('plotting Recovered Cases')
plt.title('Recovered Cases (logarithmic)')
f.savefig("../results/recovered_heatmap.png")

f, ax = plt.subplots(figsize=(90, 60))
cmap = sns.color_palette("husl", 100)
sns.heatmap(Deaths, fmt="d", ax=ax, cmap=cmap)
print('plotting Deaths')
plt.title('Deaths (logarithmic)')
f.savefig("../results/deaths_heatmap.png")

f, ax = plt.subplots(figsize=(90, 60))
cmap = sns.color_palette("husl", 100)
sns.heatmap(mortality_rate, fmt="d", ax=ax, cmap=cmap)
print('plotting Mortality Rate')
plt.title('Mortality Rate (logarithmic)')
f.savefig("../results/mortality_rate_heatmap.png")

f, ax = plt.subplots(figsize=(90, 60))
cmap = sns.color_palette("husl", 100)
sns.heatmap(increase_rate, fmt="d", ax=ax, cmap=cmap)
print('plotting Increase Rate')
plt.title('Increase Rate (logarithmic)')
f.savefig("../results/increase_rate_heatmap.png")


