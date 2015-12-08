import pandas as pd

cols_movies = ['MovieID','Title', 'Genres']
cols_rating = ['UserID', 'MovieID', 'Rating','TimeStamp']
cols_user = ['UserID', 'Gender', 'Age', 'Occupation','Zip Code']

movies_table = pd.read_table(r'movies.dat', sep='::', header = None, names = cols_movies)
rating_table = pd.read_table(r'ratings.dat', sep='::', header = None, names = cols_rating)
user_table = pd.read_table(r'users.dat', sep='::',engine='python', header = None, names = cols_user)

print(user_table)


#HVERNIG LOKA EG SKRÁNNI??