import pandas as pd
import string

#cols_movies = ['MovieID','Title', 'Genres']
#cols_rating = ['UserID', 'MovieID', 'Rating','TimeStamp']
#cols_user = ['UserID', 'Gender', 'Age', 'Occupation','Zip Code']

#movies_table = pd.read_table(r'movies.dat', sep='::', header = None, names = cols_movies)
#rating_table = pd.read_table(r'ratings.dat', sep='::', header = None, names = cols_rating)
#user_table = pd.read_table(r'users.dat', sep='::', header = None, names = cols_user)

superheroes = {}

index = 0

with open('movies.dat') as infile:
	for line in infile:
		parts = line.split('::')
		if len(line) > 1:
			superheroes[index] = {'MovieID': parts[0],'Title':parts[1],'Genres':parts[2]}
			index +=1


outfile = open('movies_demo.sql','w')

for s in superheroes:
	outfile.write("insert into movies (MovieID,Title,Genres) values('{}','{}','{}')\n".format(s.replace("'","'"),superheroes[s]['MovieID'],superheroes[s]['Title'])

outfile.close()

		