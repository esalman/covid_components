# Method

## Data Preparation

I obtained the data from https://github.com/datasets/covid-19.
The data contained one row for each (date, country) combination.
Each row contained 3 statistics: the number of confirmed cases, deaths and recovered cases.
Initially, the numbers are zero, and then then gradually increase.
I derived two more statistics from the data. 
The first one is `mortality_rate`, which is the ratio of deaths and confirmed cases for a given country on a given date.
The second one is `increase_rate`, which is the percent increase in confirmed cases for a given country on a given date compared to the previous date.
I log-normalized the numbers and then pivoted the data from long format to wide format (date x country tables).
Then I created heatmaps for all of the above 5 statistics which are saved in the results folder (`*_heatmap.png` files).

## Independent Component Analysis

I ran ICA on the `mortality_rate` and `increase_rate` statistics (date x country tables) separately.
I used the `FastICA` function from `scikit-learn` to perform the ICA.
Number of ICs were set to 3 and 10.
The resulting signal, mixing matrices and corresponding plots are saved in results folder.






