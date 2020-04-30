import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# S_ = pd.read_csv( '../results/mortality_rate_ica_signal.csv' )
ic_sig = pd.read_csv( '../results/mortality_rate_ica_mixing.csv', index_col='Country' )
ic_sig.reset_index(level=0, inplace=True)
ic_sig = pd.melt(ic_sig, id_vars='Country', value_vars=['IC1', 'IC2', 'IC3']) 
# H = pd.read_csv( '../results/mortality_rate_pca_signal.csv' )

f, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='Country', y='value', hue='variable', data=ic_sig, ax=ax)
plt.title('IC signals')
f.savefig("../results/mortality_rate_ica_mixing.png")




