import pandas as pd

df = pd.read_csv('sparsemoviematrix.csv', sep=',', encoding='utf-8', index_col=None, header=None)

# print(df.iloc[0:])

df_title = pd.read_csv('E:\PycharmProjects\prize-data\movie_titles.csv', encoding = "ISO-8859-1", header = None, names = ['Movie_Id', 'Year', 'Name'])


df_title.set_index('Movie_Id', inplace = True)

# print(df.sample(10))
# print(df_title.sample(3))



s = df.ix[:,0]


df.set_index(s, inplace=True)
df = df.drop(df.columns[0], axis=1)
df.columns = df.iloc[0]


df = df[1:]

# print(df)



def mean_approach(movie_title , cust_id):


    mean = df.stack().mean()
    i = int(df_title.index[df_title['Name'] == movie_title][0])
    # print(i)
    mean_movie = df[i].mean()


    mean_cust =  df.loc[cust_id].mean()


    res = mean + (mean_movie - mean) + (mean_cust - mean)

    if res>5.0:
        return 5.0
    elif res<1.0:
        return 1.0
    else:
        return res


print('\n\nPrediction with mean_approach: {:.4f}'.format(mean_approach('X2: X-Men United', 2649067)))