import pandas as pd

f = open('movies.dat', 'r')

cols = ['MovieID','Title', 'Genres']

movies_table = pd.read_table(r'movies.dat', sep='::', header = None, names = cols)

print(movies_table)



f.close()
