import pandas as pd
import gc

# df1 = pd.read_csv('movie_1.csv' ,usecols=[1,2,4])
# df2 = pd.read_csv('movie_2.csv',usecols=[1,2,4])
# df3 = pd.read_csv('movie_3.csv',usecols=[1,2,4])
# df4 = pd.read_csv('movie_4.csv', usecols=[1,2,4])
#
#
# df = df1
# df = df.append(df2)
# df = df.append(df3)
# df = df.append(df4)
#
#
# df.to_csv('main_movies.csv', encoding='utf-8', sep= ',' , columns=['User', 'Rating', 'Movie'], index= False)


df  = pd.read_csv('movie_4.csv', usecols = [1,2,4])



min_movie_ratings = 10000
filter_movies = (df['Movie'].value_counts()>min_movie_ratings)
filter_movies = filter_movies[filter_movies].index.tolist()

# Filter sparse users
min_user_ratings = 200
filter_users = (df['User'].value_counts()>min_user_ratings)
filter_users = filter_users[filter_users].index.tolist()
#
# # Actual filtering
df_filterd = df[(df['Movie'].isin(filter_movies)) & (df['User'].isin(filter_users))]
del filter_movies, filter_users, min_movie_ratings, min_user_ratings
gc.collect()
# print('Shape User-Ratings unfiltered:\t{}'.format(df.shape))
# print('Shape User-Ratings filtered:\t{}'.format(df_filterd.shape))
#
# # Shuffle DataFrame
# df_filterd = df_filterd.drop('Date', axis=1).sample(frac=1).reset_index(drop=True)
#
# # Testingsize
n = 100000
#
# # Split train- & testset
df_train = df_filterd[:-n]
df_test = df_filterd[-n:]
#
#
df_p = df.pivot_table(index='User', columns='Movie', values='Rating')
#
df_p.to_csv('sparsemoviematrix.csv', sep=',', encoding='utf-8')
#
print('Shape User-Movie-Matrix:\t{}'.format(df_p.shape))
# print(df_p.sample(3))
