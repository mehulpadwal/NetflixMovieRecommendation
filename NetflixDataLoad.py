import pandas as pd
import numpy as np
import gc

from collections import deque





#Use one at a time to for faster procesing
df1 = pd.read_csv('E:\PycharmProjects\prize-data\combined_data_1.txt', header = None , names=['User', 'Rating', 'Date'], usecols=[0, 1, 2] )
# df1 = pd.read_csv('E:\PycharmProjects\prize-data\combined_data_2.txt', header = None , names=['User', 'Rating', 'Date'], usecols=[0, 1, 2] )
# df1  pd.read_csv('E:\PycharmProjects\prize-data\combined_data_3.txt', header = None , names=['User', 'Rating', 'Date'], usecols=[0, 1, 2] )
# df1 = pd.read_csv('E:\PycharmProjects\prize-data\combined_data_4.txt', header = None , names=['User', 'Rating', 'Date'], usecols=[0, 1, 2] )

df_raw  = df1


tmp_movies = df_raw[df_raw['Rating'].isna()]['User'].reset_index()
movie_indices = [[index, int(movie[:-1])] for index, movie in tmp_movies.values]

shifted_movie_indices = deque(movie_indices)
shifted_movie_indices.rotate(-1)

user_data = []


for [df_id_1, movie_id], [df_id_2, next_movie_id] in zip(movie_indices, shifted_movie_indices):

    # Check if it is the last movie in the file
    if df_id_1 < df_id_2:
        tmp_df = df_raw.loc[df_id_1 + 1:df_id_2 - 1].copy()
    else:
        tmp_df = df_raw.loc[df_id_1 + 1:].copy()

    # Create movie_id column
    tmp_df['Movie'] = movie_id

    # Append dataframe to list
    user_data.append(tmp_df)

# Combine all dataframes
df = pd.concat(user_data)
del user_data, df_raw, tmp_movies, shifted_movie_indices, movie_indices
print('Shape User-Ratings:\t{}'.format(df.shape))
print(df.sample(5))

# df.to_csv('movie_1.csv', encoding= 'utf-8', sep= ',')
# df.to_csv('movie_2.csv', encoding= 'utf-8', sep= ',')
# df.to_csv('movie_3.csv', encoding= 'utf-8', sep= ',')
# df.to_csv('movie_4.csv', encoding= 'utf-8', sep= ',')




min_movie_ratings = 10000
filter_movies = (df['Movie'].value_counts()>min_movie_ratings)
filter_movies = filter_movies[filter_movies].index.tolist()

# Filter sparse users
min_user_ratings = 200
filter_users = (df['User'].value_counts()>min_user_ratings)
filter_users = filter_users[filter_users].index.tolist()

# Actual filtering
df_filterd = df[(df['Movie'].isin(filter_movies)) & (df['User'].isin(filter_users))]
del filter_movies, filter_users, min_movie_ratings, min_user_ratings
gc.collect()

# print('Shape User-Ratings unfiltered:\t{}'.format(df.shape))
# print('Shape User-Ratings filtered:\t{}'.format(df_filterd.shape))

# Shuffle DataFrame
df_filterd = df_filterd.drop('Date', axis=1).sample(frac=1).reset_index(drop=True)

# SPlitting train-test data
n = 100000

# Split train- & testset
df_train = df_filterd[:-n]
df_test = df_filterd[-n:]




