import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# To create interactive plots
from plotly.offline import init_notebook_mode, plot, iplot
import plotly as py
import plotly.graph_objs as go

import NetflixDataLoad


df1 = pd.read_csv('E:\PycharmProjects\prize-data\movie_titles.csv', encoding = "ISO-8859-1", header = None, names = ['Movie_Id', 'Year', 'Name'])


print('Shape Movie-Titles:\t{}'.format(df1.shape))
df1.sample(10)


#
# data = df1['Year'].value_counts().sort_index()
# # Create trace
# trace = go.Scatter(x = data.index,
#                    y = data.values,                    )
# # Create layout
# layout = dict(title = '{} Movies Grouped By Year Of Release'.format(df1.shape[0]),
#               xaxis = dict(title = 'Release Year'),
#               yaxis = dict(title = 'Movies'))
# # Create plot
# fig1 = go.Figure(data=[trace], layout=layout)
# py.offline.plot(fig1)
#


# Get data
data = NetflixDataLoad.df['Rating'].value_counts().sort_index(ascending=False)

# Create trace
trace = go.Bar(x = data.index,
               text = ['{:.1f} %'.format(val) for val in (data.values / df.shape[0] * 100)],
               textposition = 'auto',
               textfont = dict(color = '#000000'),
               y = data.values,
               )
# Create layout
layout = dict(title = 'Distribution Of {} Netflix-Ratings'.format(df.shape[0]),
              xaxis = dict(title = 'Rating'),
              yaxis = dict(title = 'Count'))
# Create plot
fig = go.Figure(data=[trace], layout=layout)
py.offline.plot(fig)





