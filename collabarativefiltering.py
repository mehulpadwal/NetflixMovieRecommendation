import surprise as sp
from surprise import Dataset
from surprise.model_selection import cross_validate
import NetflixDataLoad


#for 100000 rows for fast processing
data = Dataset.load_from_df(NetflixDataLoad.df_filterd[['Cust_Id', 'Movie_Id', 'Rating']][:100000])

n_folds = 5

for algo in [sp.SVD(), sp.SVDpp(),sp.KNNBasic(), sp.KNNWithMeans()]:
    print(cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=n_folds, verbose=True))


# Output Example
# Evaluating RMSE, MAE of algorithm SVD on 5 split(s).
#
#             Fold 1  Fold 2  Fold 3  Fold 4  Fold 5  Mean    Std
# RMSE        0.9311  0.9370  0.9320  0.9317  0.9391  0.9342  0.0032
# MAE         0.7350  0.7375  0.7341  0.7342  0.7375  0.7357  0.0015
# Fit time    6.53    7.11    7.23    7.15    3.99    6.40    1.23
# Test time   0.26    0.26    0.25    0.15    0.13    0.21    0.06








