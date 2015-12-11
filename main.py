import psycopg2
import getpass
import pprint
import random as r
import FOLL as F
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

f = open('movies.dat','r')

#GRUNNUR AD MOVIE TÖFLU MED ID, TITLI OG ÁRI.
movie_table = {}
index = 0

for line in f:
	parts1 = line.split('::')
	if len(line) > 1:
		title = parts1[1].rsplit('(',1)
		updated_title=title[1].strip(')')
		movie_table[index] = {'movieid': parts1[0], 'title':title[0],'year':updated_title}
		print(movie_table[index])
		index +=1


f.close()

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

host = 'localhost'
dbname = 'movies'

username = 'hildurrungudjonsdottir' #input('User name for {}.{}: '.format(host,dbname)) 
pw = '1313' #getpass.getpass()

conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(host, dbname, username, pw)

print("Connecting to database {}.{} as {}".format(host, dbname, username))

conn = psycopg2.connect(conn_string)

cursor = conn.cursor()


print("Connected!\n")

for s in movie_table:
	cursor.execute("insert into movies (movieid, title, year) values('{}','{}','{}')\n".format(movie_table[s]['movieid'],movie_table[s]['title'].strip().replace("'","''"),movie_table[s]['year'].strip()))

for a in user_table:
	cursor.execute("insert into username (userid, gender, age, occupation) values('{}','{}','{}','{}')\n".format(user_table[a]['userid'],user_table[a]['gender'],user_table[a]['age'],user_table[a]['occupation'].strip()))

for b in rating_table:
	cursor.execute("insert into rating (user_id, movie_id, rating) values('{}','{}','{}')\n".format(rating_table[b]['user_id'],rating_table[b]['movie_id'],rating_table[b]['rating'].strip()))

for k in movieid_genresid:
	cursor.execute("insert into genre_id (movies_id, genreid) values('{}','{}')\n".format(movieid_genresid[k]['movies_id'],movieid_genresid[k]['genreid']))

print("Enter the names of 3 movies you like: ")

movie1 = input("First movie: ")
movie1 = F.many_movies(movie1, cursor)

movie2 = input("Second movie: ")
movie2 = F.many_movies(movie2, cursor)

movie3 = input("Last movie: ")
movie3 = F.many_movies(movie3, cursor)

print('\n')

#Finn id-ið á myndunum sem eru slegnar inn
s = """
create view movieid_view as
select movieid
from movies
where title in ( '%s', '%s', '%s')""" % (movie1, movie2, movie3)

cursor.execute(s)

#print("What movies do you mean")

#Finn id-in á öllum genres sem eru sameiginleg á öllum myndunum
t = """
select g.genreid
from genre_id g, movieid_view mv
where mv.movieid = g.movies_id
group by genreid
having count(genreid)>1"""

cursor.execute(t)
genreids = cursor.fetchall()

g_len = len(genreids)
#Ef það eru fleiri en 3 genres sameiginleg þá eru 3 sameiginleg genres valin random
if g_len > 3:
	print('IF')
	r_genres = r.sample(genreid, 3)
	q="""
	CREATE VIEW typur AS 
	SELECT g.movies_id
	FROM genre_id g
	WHERE g.genreid IN ('%s','%s','%s')
	GROUP BY g.movies_id
	HAVING count(g.movies_id) > 2
	ORDER BY g.movies_id""" (r_genres[0][0],r_genres[1][0],r_genres[2][0])
	cursor.execute(q)

	sql3 = """
	select distinct m.title
	from flokkun f, rating r, genre_id g, movies_min_rating mmr, typur t, movies m
	where r.user_id = f.user_id and g.movies_id = r.movie_id
	and mmr.movie_id = r.movie_id and t.movies_id = r.movie_id
	and m.movieid = r.movie_id
	and r.rating > 3
	and m.title NOT IN ('%s', '%s', '%s')
	LIMIT 10""" % (movie1, movie2, movie3)
	cursor.execute(sql3)
	movie = cursor.fetchall()

	for i in range(len(movie)):
		print(movie[i][0])

elif g_len is 0:
	t = """
	select distinct genreid
	from genre_id g, movies m
	where m.movieid = g.movies_id
	and m.title in ( '%s', '%s', '%s')""" % (movie1, movie2, movie3)

	cursor.execute(t)
	genreids = cursor.fetchall()
	#pprint.pprint(genreids)
	i = 1
	print('We recommend these three movies:')
	while i < 4:
		u = """
		select title
		from movies"""
		cursor.execute(u)
		titles = cursor.fetchall()
		r_titles = r.sample(titles, 1)
		#print(r_titles)

		v = """
		select genreid
		from genre_id g, movies m
		where m.movieid = g.movies_id
		and m.title = '%s'""" % (r_titles[0][0].replace("'","''"))
		cursor.execute(v)
		genreid = cursor.fetchall()
		same = list(set(genreids).intersection(genreid))
		
		if len(same) > 0:
			print(r_titles[0][0])
			i+=1
else:
	x = """
	CREATE VIEW flokkun AS 
	SELECT r.user_id
	FROM rating r, movieid_view mv
	WHERE r.movie_id IN (mv.movieid) AND r.rating > 3
	GROUP BY r.user_id
	HAVING count(r.user_id) > 2
	ORDER BY r.user_id"""
	cursor.execute(x)

	y = """
	CREATE VIEW movies_min_rating AS 
	SELECT rating.movie_id
	FROM rating
	GROUP BY rating.movie_id
	HAVING count(rating.movie_id) > 100"""
	cursor.execute(y)

	if g_len is 1:
		w = """
		CREATE VIEW typur AS 
		SELECT g.movies_id
		FROM genre_id g
		WHERE g.genreid IN (%s)
		GROUP BY g.movies_id
		HAVING count(g.movies_id) > 0
		ORDER BY g.movies_id""" % (genreids[0][0])
		cursor.execute(w)

		sql1 = """
		select distinct m.title
		from flokkun f, rating r, genre_id g, movies_min_rating mmr, typur t, movies m
		where r.user_id = f.user_id and g.movies_id = r.movie_id
		and mmr.movie_id = r.movie_id and t.movies_id = r.movie_id
		and m.movieid = r.movie_id
		and r.rating > 3
		and m.title NOT IN ('%s', '%s', '%s')
		LIMIT 10""" % (movie1, movie2, movie3)
		cursor.execute(sql1)
		movie = cursor.fetchall()

		print('We recommend these three movies:')
		for i in range(len(movie)):
			print(movie[i][0])

	elif g_len is 2:
		z="""
		CREATE VIEW typur AS 
		SELECT g.movies_id
		FROM genre_id g
		WHERE g.genreid IN ('%s','%s')
		GROUP BY g.movies_id
		HAVING count(g.movies_id) > 1
		ORDER BY g.movies_id""" %(genreids[0][0],genreids[1][0])
		cursor.execute(z)

		sql2 = """
		select distinct m.title
		from flokkun f, rating r, genre_id g, movies_min_rating mmr, typur t, movies m
		where r.user_id = f.user_id and g.movies_id = r.movie_id
		and mmr.movie_id = r.movie_id and t.movies_id = r.movie_id
		and m.movieid = r.movie_id
		and r.rating > 3
		and m.title NOT IN ('%s', '%s', '%s')
		LIMIT 10""" % (movie1, movie2, movie3)
		cursor.execute(sql2)
		movie = cursor.fetchall()
		print('We recommend these movies:')
		for i in range(len(movie)):
			print(movie[i][0])


	elif g_len is 3:
		q="""
		CREATE VIEW typur AS 
		SELECT g.movies_id
		FROM genre_id g
		WHERE g.genreid IN ('%s','%s','%s')
		GROUP BY g.movies_id
		HAVING count(g.movies_id) > 2
		ORDER BY g.movies_id""" %(genreids[0][0],genreids[1][0],genreids[2][0])
		cursor.execute(q)

		sql3 = """
		select distinct m.title
		from flokkun f, rating r, genre_id g, movies_min_rating mmr, typur t, movies m
		where r.user_id = f.user_id and g.movies_id = r.movie_id
		and mmr.movie_id = r.movie_id and t.movies_id = r.movie_id
		and m.movieid = r.movie_id
		and r.rating > 3
		and m.title NOT IN ('%s', '%s', '%s')
		LIMIT 10""" % (movie1, movie2, movie3)
		cursor.execute(sql3)
		movie = cursor.fetchall()
		print('We recommend these movies:')
		for i in range(len(movie)):
			print(movie[i][0])














