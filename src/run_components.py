import pandas as pd 
import numpy as np 
from sklearn.decomposition import FastICA, PCA

# mortality_rate
mortality_rate = pd.read_csv( '../results/mortality_rate_lognorm_wide.csv', index_col='Date' )
X = np.array( mortality_rate )

print( 'Compute ICA' )
ica = FastICA(n_components=3)
S_ = ica.fit_transform( X )
A_ = ica.mixing_

# # We can `prove` that the ICA model applies by reverting the unmixing.
# assert np.allclose(increase_rate, np.dot(S_, A_.T) + ica.mean_)

print( 'For comparison, compute PCA' )
pca = PCA(n_components=3)
H = pca.fit_transform( X )  # Reconstruct signals based on orthogonal components

cols_ = ['IC1', 'IC2', 'IC3']
S_pd = pd.DataFrame( S_, index=mortality_rate.index, columns=cols_ )
S_pd.to_csv( '../results/mortality_rate_ica_signal.csv' )
A_pd = pd.DataFrame( A_, index=mortality_rate.columns, columns=cols_ )
A_pd.to_csv( '../results/mortality_rate_ica_mixing.csv', index_label='Country' )
H_pd = pd.DataFrame( H, index=mortality_rate.index, columns=cols_ )
H_pd.to_csv( '../results/mortality_rate_pca_signal.csv' )


# increase_rate
increase_rate = pd.read_csv( '../results/increase_rate_lognorm_wide.csv', index_col='Date' )
X = np.array( increase_rate )

print( 'Compute ICA' )
ica = FastICA(n_components=3, max_iter=2000)
S_ = ica.fit_transform( X )
A_ = ica.mixing_

# # We can `prove` that the ICA model applies by reverting the unmixing.
# assert np.allclose(increase_rate, np.dot(S_, A_.T) + ica.mean_)

print( 'For comparison, compute PCA' )
pca = PCA(n_components=3)
H = pca.fit_transform( X )  # Reconstruct signals based on orthogonal components

cols_ = ['IC1', 'IC2', 'IC3']
S_pd = pd.DataFrame( S_, index=increase_rate.index, columns=cols_ )
S_pd.to_csv( '../results/increase_rate_ica_signal.csv' )
A_pd = pd.DataFrame( A_, index=increase_rate.columns, columns=cols_ )
A_pd.to_csv( '../results/increase_rate_ica_mixing.csv', index_label='Country' )
H_pd = pd.DataFrame( H, index=increase_rate.index, columns=cols_ )
H_pd.to_csv( '../results/increase_rate_pca_signal.csv' )

