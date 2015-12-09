import pandas as pd
import string

cols_movies = ['MovieID','Title', 'Genres']
#cols_rating = ['UserID', 'MovieID', 'Rating','TimeStamp']
#cols_user = ['UserID', 'Gender', 'Age', 'Occupation','Zip Code']

movies_table_panda = pd.read_csv('movies.dat', sep='::', header = None, names = cols_movies)
#rating_table = pd.read_table(r'ratings.dat', sep='::', header = None, names = cols_rating)
#user_table = pd.read_table(r'users.dat', sep='::', header = None, names = cols_user)

only_last = []
only_last = movies_table_panda['Genres']

new_list = []

for line in only_last:
	stak_i_linu = line.split('|')
	for i in stak_i_linu:
		new_list.append(i)

new_list = sorted(set(new_list))

genres_table = {}
index=1

for word in new_list:
	genres_table[index] = {'id': index, 'genres': word}
	print(genres_table[index])
	index += 1

movies_table = {}

index = 0

f = open('movies.dat','r')

for line in f:
	parts = line.split('::')
	if len(line) > 1:
		movies_table[index] = {'movieid': parts[0],'title':parts[1],'genres':parts[2]}
		index +=1


movie_table = {}

for line in f:
	parts1 = line.split('::')
	if len(line) > 1:
		title = parts1[1].split('(')
		updated_title=title[1].strip(')')
		movie_table[0] = {'id': parts1[0], 'title':title[0],'year':updated_title}


f.close()

#genre_table = {}
#result = {}
#k = 0
#a = 0

#with open('movies.dat') as infile:
#	for line in infile:
#		parts2 = line.split('::')
#		if len(line) > 1:
#			genre = parts2[2].split('|')
#			for i in genre:
#				genre_table[k] = {'Genre':i.strip()}
#				k += 1
#			for key,value in genre_table.items():
#				if value not in result.values():
#					result[key] = value
#					print(result[key])
			
					
index1 = 0

rating_table = {}

with open('ratings.dat') as infile:
	for line in infile:
		parts = line.split('::')
		if len(line) > 1:
			rating_table[index1] = {'user_id': parts[0],'movie_id':parts[1],'rating':parts[2],'timestamp':parts[3]}
			index1 +=1



index2 = 0

user_table = {}

with open('users.dat') as infile:
	for line in infile:
		parts = line.split('::')
		if len(line) > 1:
			user_table[index2] = {'userid': parts[0],'gender': parts[1],'age': parts[2],'occupation': parts[3],'zipcode': parts[4]}
			index2 +=1



outfile = open('movies_demo.sql','w')

for s in movies_table:
	outfile.write("insert into movies (movieid, title, genres) values('{}','{}','{}')\n".format(movies_table[s]['movieid'],movies_table[s]['title'].replace("'","''"),movies_table[s]['genres'].replace("'","''").strip()))

for a in user_table:
	outfile.write("insert into username (userid, gender, age, occupation, zipcode) values('{}','{}','{}','{}','{}')\n".format(user_table[a]['userid'],user_table[a]['gender'],user_table[a]['age'],user_table[a]['occupation'],user_table[a]['zipcode'].strip()))

for b in rating_table:
	outfile.write("insert into rating (user_id, movie_id, rating, timestamp) values('{}','{}','{}','{}')\n".format(rating_table[b]['user_id'],rating_table[b]['movie_id'],rating_table[b]['rating'],rating_table[b]['timestamp'].strip()))

outfile.close()

		