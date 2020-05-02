import pandas as pd 
import numpy as np 
from sklearn.decomposition import FastICA, PCA
from pathlib import Path

ncomp = 10
inpath = '../results/aggregate_data/'
outpath = '../results/ica_'+str(ncomp)+'/'

Path(outpath).mkdir(parents=True, exist_ok=True)

t1 = list( range( 1, ncomp+1 ) )
cols_ = ['IC'+str(n) for n in t1]

# mortality_rate
mortality_rate = pd.read_csv( inpath+'mortality_rate_lognorm_wide.csv', index_col='Date' )
mortality_rate = mortality_rate.fillna(0)
X = np.array( mortality_rate )

print( 'Compute ICA' )
ica = FastICA(n_components=ncomp)
S_ = ica.fit_transform( X )
A_ = ica.mixing_

# # We can `prove` that the ICA model applies by reverting the unmixing.
# assert np.allclose(increase_rate, np.dot(S_, A_.T) + ica.mean_)

print( 'For comparison, compute PCA' )
pca = PCA(n_components=ncomp)
H = pca.fit_transform( X )  # Reconstruct signals based on orthogonal components

S_pd = pd.DataFrame( S_, index=mortality_rate.index, columns=cols_ )
S_pd.to_csv( outpath+'mortality_rate_ica'+str(ncomp)+'_signal.csv' )
A_pd = pd.DataFrame( A_, index=mortality_rate.columns, columns=cols_ )
A_pd.to_csv( outpath+'mortality_rate_ica'+str(ncomp)+'_mixing.csv', index_label='Country' )
H_pd = pd.DataFrame( H, index=mortality_rate.index, columns=cols_ )
H_pd.to_csv( outpath+'mortality_rate_pca'+str(ncomp)+'_signal.csv' )


# increase_rate
increase_rate = pd.read_csv( inpath+'increase_rate_lognorm_wide.csv', index_col='Date' )
increase_rate = increase_rate.fillna(0)
X = np.array( increase_rate )

print( 'Compute ICA' )
ica = FastICA(n_components=ncomp, max_iter=2000)
S_ = ica.fit_transform( X )
A_ = ica.mixing_

# # We can `prove` that the ICA model applies by reverting the unmixing.
# assert np.allclose(increase_rate, np.dot(S_, A_.T) + ica.mean_)

print( 'For comparison, compute PCA' )
pca = PCA(n_components=ncomp)
H = pca.fit_transform( X )  # Reconstruct signals based on orthogonal components

S_pd = pd.DataFrame( S_, index=increase_rate.index, columns=cols_ )
S_pd.to_csv( outpath+'increase_rate_ica'+str(ncomp)+'_signal.csv' )
A_pd = pd.DataFrame( A_, index=increase_rate.columns, columns=cols_ )
A_pd.to_csv( outpath+'increase_rate_ica'+str(ncomp)+'_mixing.csv', index_label='Country' )
H_pd = pd.DataFrame( H, index=increase_rate.index, columns=cols_ )
H_pd.to_csv( outpath+'increase_rate_pca'+str(ncomp)+'_signal.csv' )

