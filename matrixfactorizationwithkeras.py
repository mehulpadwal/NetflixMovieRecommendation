import NetflixDataLoad
from tensorflow.keras.layers import Input, Embedding, Reshape, Dot, Concatenate, Dense, Dropout
from tensorflow.keras.models import Model
from sklearn.metrics import mean_squared_error
import numpy as np


user_id_mapping = {id:i for i, id in enumerate(NetflixDataLoad.df_filterd['User'].unique())}
movie_id_mapping = {id:i for i, id in enumerate(NetflixDataLoad.df_filterd['Movie'].unique())}


# Create correctly mapped train- & testset
train_user_data = NetflixDataLoad.df_train['User'].map(user_id_mapping)
train_movie_data = NetflixDataLoad.df_train['Movie'].map(movie_id_mapping)

test_user_data = NetflixDataLoad.df_test['User'].map(user_id_mapping)
test_movie_data = NetflixDataLoad.df_test['Movie'].map(movie_id_mapping)


# Get input variable-sizes
users = len(user_id_mapping)
movies = len(movie_id_mapping)
embedding_size = 10


##### Create model
# Set input layers
user_id_input = Input(shape=[1], name='user')
movie_id_input = Input(shape=[1], name='movie')

# Create embedding layers for users and movies
user_embedding = Embedding(output_dim=embedding_size,
                           input_dim=users,
                           input_length=1,
                           name='user_embedding')(user_id_input)
movie_embedding = Embedding(output_dim=embedding_size,
                            input_dim=movies,
                            input_length=1,
                            name='item_embedding')(movie_id_input)

# Reshape the embedding layers
user_vector = Reshape([embedding_size])(user_embedding)
movie_vector = Reshape([embedding_size])(movie_embedding)

# Compute dot-product of reshaped embedding layers as prediction
y = Dot(1, normalize=False)([user_vector, movie_vector])

# Setup model
model = Model(inputs=[user_id_input, movie_id_input], outputs=y)
model.compile(loss='mse', optimizer='adam')


# Fit model
model.fit([train_user_data, train_movie_data],
          NetflixDataLoad.df_train['Rating'],
          batch_size=256,
          epochs=1,
          validation_split=0.1,
          shuffle=True)

# Test model
y_pred = model.predict([test_user_data, test_movie_data])
y_true = NetflixDataLoad.df_test['Rating'].values

#  Compute RMSE
rmse = np.sqrt(mean_squared_error(y_pred=y_pred, y_true=y_true))
print('\n\nTesting Result With Keras Matrix-Factorization: {:.4f} RMSE'.format(rmse))