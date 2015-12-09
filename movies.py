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
			superheroes[index] = {'movieid': parts[0],'title':parts[1],'genres':parts[2]}
			index +=1

index1 = 0

superheroes1 = {}

with open('ratings.dat') as infile:
	for line in infile:
		parts = line.split('::')
		if len(line) > 1:
			superheroes1[index1] = {'user_id': parts[0],'movie_id':parts[1],'rating':parts[2],'timestamp':parts[3]}
			index1 +=1


index2 = 0

superheroes2 = {}

with open('users.dat') as infile:
	for line in infile:
		parts = line.split('::')
		if len(line) > 1:
			superheroes2[index2] = {'userid': parts[0],'gender': parts[1],'age': parts[2],'occupation': parts[3],'zipcode': parts[4]}
			index2 +=1



outfile = open('movies_demo.sql','w')

for s in superheroes:
	outfile.write("insert into movies (movieid, title, genres) values('{}','{}','{}')\n".format(superheroes[s]['movieid'],superheroes[s]['title'].replace("'","''"),superheroes[s]['genres'].replace("'","''").strip()))

for a in superheroes2:
	outfile.write("insert into username (userid, gender, age, occupation, zipcode) values('{}','{}','{}','{}','{}')\n".format(superheroes2[a]['userid'],superheroes2[a]['gender'],superheroes2[a]['age'],superheroes2[a]['occupation'],superheroes2[a]['zipcode'].strip()))

for b in superheroes1:
	outfile.write("insert into rating (user_id, movie_id, rating, timestamp) values('{}','{}','{}','{}')\n".format(superheroes1[b]['user_id'],superheroes1[b]['movie_id'],superheroes1[b]['rating'],superheroes1[b]['timestamp'].strip()))

outfile.close()

		