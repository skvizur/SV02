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

index1 = 0

superheroes1 = {}

with open('ratings.dat') as infile:
	for line in infile:
		parts = line.split('::')
		if len(line) > 1:
			superheroes1[index1] = {'UserID': parts[0],'MovieID':parts[1],'Rating':parts[2],'TimeStamp':parts[3]}
			index1 +=1


index2 = 0

superheroes2 = {}

with open('users.dat') as infile:
	for line in infile:
		parts = line.split('::')
		if len(line) > 1:
			superheroes2[index2] = {'UserID': parts[0],'Gender': parts[1],'Age': parts[2],'Occupation': parts[3],'Zip Code': parts[4]}
			index2 +=1



outfile = open('movies_demo.sql','w')

for s in superheroes:
	outfile.write("insert into movies (MovieID, Title, Genres) values('{}','{}','{}')\n".format(superheroes[s]['MovieID'],superheroes[s]['Title'],superheroes[s]['Genres']))

for b in superheroes1:
	outfile.write("insert into ratings (UserID, MovieID, Rating, TimeStamp) values('{}','{}','{}','{}')\n".format(superheroes1[b]['UserID'],superheroes1[b]['MovieID'],superheroes1[b]['Rating'],superheroes1[b]['TimeStamp']))

for a in superheroes2:
	outfile.write("insert into user (UserID, Gender, Age, Occupation, Zip Code) values('{}','{}','{}','{}')\n".format(superheroes2[a]['UserID'],superheroes2[a]['Gender'],superheroes2[a]['Age'],superheroes2[a]['Occupation'],superheroes2[a]['Zip Code']))

outfile.close()

		