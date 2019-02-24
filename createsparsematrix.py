import pandas as pd
import numpy as np
import math



df1 = pd.read_csv('E:\PycharmProjects\prize-data\combined_data_1.txt', header = None , names=['Cust_Id', 'Rating'], usecols=[0, 1] )
# df2 = pd.read_csv('E:\PycharmProjects\prize-data\combined_data_2.txt', header = None , names=['Cust_Id', 'Rating'], usecols=[0, 1] )
# df3 = pd.read_csv('E:\PycharmProjects\prize-data\combined_data_3.txt', header = None , names=['Cust_Id', 'Rating'], usecols=[0, 1] )
# df4 = pd.read_csv('E:\PycharmProjects\prize-data\combined_data_4.txt', header = None , names=['Cust_Id', 'Rating'], usecols=[0, 1] )


df1['Rating'] = df1['Rating'].astype(float)
# df2['Rating'] = df2['Rating'].astype(float)
# df3['Rating'] = df3['Rating'].astype(float)
# df4['Rating'] = df4['Rating'].astype(float)

df =df1
# df = df.append(df2)
# df = df.append(df3)
# df = df.append(df4)

df.index = np.arange(0,len(df))


df_nan = pd.DataFrame(pd.isnull(df.Rating))
df_nan = df_nan[df_nan['Rating'] == True]
df_nan = df_nan.reset_index()

movie_np = []
movie_id = 1

for i,j in zip(df_nan['index'][1:],df_nan['index'][:-1]):
    # numpy approach
    temp = np.full((1,i-j-1), movie_id)
    movie_np = np.append(movie_np, temp)
    movie_id += 1

# Account for last record and corresponding length
# numpy approach
last_record = np.full((1,len(df) - df_nan.iloc[-1, 0] - 1),movie_id)
movie_np = np.append(movie_np, last_record)


df = df[pd.notnull(df['Rating'])]

df['Movie_Id'] = movie_np.astype(int)
df['Cust_Id'] = df['Cust_Id'].astype(int)

print(df)


f = ['count','mean']

df_movie_summary = df.groupby('Movie_Id')['Rating'].agg(f)
df_movie_summary.index = df_movie_summary.index.map(int)
movie_benchmark = round(df_movie_summary['count'].quantile(0.8),0)
drop_movie_list = df_movie_summary[df_movie_summary['count'] < movie_benchmark].index


df_cust_summary = df.groupby('Cust_Id')['Rating'].agg(f)
df_cust_summary.index = df_cust_summary.index.map(int)
cust_benchmark = round(df_cust_summary['count'].quantile(0.8),0)
drop_cust_list = df_cust_summary[df_cust_summary['count'] < cust_benchmark].index




df = df[~df['Movie_Id'].isin(drop_movie_list)]
df = df[~df['Cust_Id'].isin(drop_cust_list)]


df_p = pd.pivot_table(df,values='Rating',index='Cust_Id',columns='Movie_Id')

# df_p.to_csv('sparsemoviematrix.csv', sep=',', encoding='utf-8')


df_title = pd.read_csv('E:\PycharmProjects\prize-data\movie_titles.csv', encoding = "ISO-8859-1", header = None, names = ['Movie_Id', 'Year', 'Name'])


df_title.set_index('Movie_Id', inplace = True)


print(df_p.shape)

i = int(df_title.index[df_title['Name'] == 'X2: X-Men United'][0])

print(len(df_p[i]))
# print(df_p.index)
#
# df_p.index = df_p.iloc[0]
#
#
# print(df_p.index)





#
# def recommend(movie_title, min_count):
#     print("For movie ({})".format(movie_title))
#     print("- Top 10 movies recommended based on Pearsons'R correlation - ")
#     i = int(df_title.index[df_title['Name'] == movie_title][0])
#     target = df_p[i]
#     similar_to_target = df_p.corrwith(target)
#     corr_target = pd.DataFrame(similar_to_target, columns = ['PearsonR'])
#     corr_target.dropna(inplace = True)
#     corr_target = corr_target.sort_values('PearsonR', ascending = False)
#     corr_target.index = corr_target.index.map(int)
#     corr_target = corr_target.join(df_title).join(df_movie_summary)[['PearsonR', 'Name', 'count', 'mean']]
#     print(corr_target[corr_target['count']>min_count][:10].to_string(index=False))
#
#
# recommend("X2: X-Men United", 0)
#













