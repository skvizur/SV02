import pandas as pd
import string
import itertools

cols_movies = ['MovieID','Title', 'Genres']
#cols_rating = ['UserID', 'MovieID', 'Rating','TimeStamp']
#cols_user = ['UserID', 'Gender', 'Age', 'Occupation','Zip Code']

movies_table_panda = pd.read_csv('movies.dat', sep='::', header = None, names = cols_movies, engine='python')
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
number_list = list(range(0,19))


genres_id_table = {}
i=1

for word in new_list:
	genres_id_table[word] =i
	print(genres_id_table[word])
	i += 1


adict = dict(zip(new_list,number_list))
print(adict)

s = movies_table_panda['Genres'].str.split('|').apply(pd.Series,1).stack()
s.index = s.index.droplevel(-1)
s.name = 'Genres'

del movies_table_panda['Genres']
y = movies_table_panda.join(s)

movie_id_col = list(y.iloc[:,0])
movie_genre_col = list(y.iloc[:,2])

movieid_genresid = {}
for i in range(len(movie_id_col)):
	movieid_genresid[i] = {'movies_id': movie_id_col[i], 'genreid': genres_id_table[movie_genre_col[i]]}



#print(movieId_genre_table)
#print(movieId_genre_table)
#index = 0

#print(range(len(movie_id_col)))

#for item in movie_id_col:
#	movieId_genre_table[index] = {'MovieID':item,'Genres':movie_genre_col[index]}
#	print(movieId_genre_table[index])
#	index +=1


#area_dict = dict(zip(y['MovieID'], y['Genres']))


f = open('movies.dat','r')

#GRUNNUR AD MOVIE TÖFLU MED ID TITLI OG GENRES (ÞARF ANNAÐ HVORT ÞESSA EÐA HINA FYRIR NEÐAN)
#movies_table = {}
index = 0

#for line in f:
#	parts = line.split('::')
#	if len(line) > 1:
#		movies_table[index] = {'movieid': parts[0],'title':parts[1],'genres':parts[2]}
#		index +=1


#GRUNNUR AD MOVIE TÖFLU MED ID, TITLI OG ÁRI.
movie_table = {}

for line in f:
	parts1 = line.split('::')
	if len(line) > 1:
		title = parts1[1].rsplit('(',1)
		updated_title=title[1].strip(')')
		movie_table[index] = {'movieid': parts1[0], 'title':title[0],'year':updated_title}
		print(movie_table[index])
		index +=1


f.close()

#TILLAGA AD TOFLU MED OLLUM TYPUM GENRES

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
	



#GRUNNUR AD RATING TÖFLLU					
index = 0
rating_table = {}

with open('ratings.dat') as infile:
	for line in infile:
		parts = line.split('::')
		if len(line) > 1:
			rating_table[index] = {'user_id': parts[0],'movie_id':parts[1],'rating':parts[2]}
			index +=1


#GRUNNUR AÐ NOTENDATÖFLU
index = 0
user_table = {}

with open('users.dat') as infile:
	for line in infile:
		parts = line.split('::')
		if len(line) > 1:
			user_table[index] = {'userid': parts[0],'gender': parts[1],'age': parts[2],'occupation': parts[3]}
			index +=1



outfile = open('movies_demo.sql','w')

for s in movie_table:
	outfile.write("insert into movies (movieid, title, year) values('{}','{}','{}')\n".format(movie_table[s]['movieid'],movie_table[s]['title'].replace("'","''"),movie_table[s]['year'].strip()))

for a in user_table:
	outfile.write("insert into username (userid, gender, age, occupation) values('{}','{}','{}','{}')\n".format(user_table[a]['userid'],user_table[a]['gender'],user_table[a]['age'],user_table[a]['occupation'].strip()))

for b in rating_table:
	outfile.write("insert into rating (user_id, movie_id, rating) values('{}','{}','{}')\n".format(rating_table[b]['user_id'],rating_table[b]['movie_id'],rating_table[b]['rating'].strip()))

for k in movieid_genresid:
	outfile.write("insert into genre_id (movies_id, genreid) values('{}','{}')\n".format(movieid_genresid[k]['movies_id'],movieid_genresid[k]['genreid']))

outfile.close()


#ATH MUNA AÐ SETJA INDEXA

		