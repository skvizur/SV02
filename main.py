import psycopg2
import getpass
import pprint
import random as r
import FOLL as F
import pandas as pd
import string
import itertools

#GRUNNUR AD MOVIES TÖFLU
movie_table = F.movies_table('movies.dat')

#GRUNNUR AD RATING TÖFLLU					
rating_table = F.ratings_table('ratings.dat')

#GRUNNUR AÐ NOTENDATÖFLU
user_table = F.username_table('users.dat')

#GRUNNUR AÐ GENRES TÖFLU
movieid_genresid = F.genres_table('movies.dat')


#TENGJUMST GAGNAGRUNNI

host = 'localhost'
dbname = 'movies'

username = 'hildurrungudjonsdottir' #input('User name for {}.{}: '.format(host,dbname)) 
pw = '1313' #getpass.getpass()

conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(host, dbname, username, pw)

print("Connecting to database {}.{} as {}".format(host, dbname, username))

conn = psycopg2.connect(conn_string)

cursor = conn.cursor()

print("Connected!\n")

#F.create_tables(cursor)

test = """ 
select movieid
from movies"""
cursor.execute(test)
total = cursor.fetchall()
is_empty = len(total)
print('ÆKSDJFAKÆ')
print('BALBABALB',is_empty)

#LESUM INN Í TOFLURNAR EF ÞAÐ HEFUR EKKI NÚ ÞEGAR VERIÐ GERT
if is_empty is 0:

	for s in movie_table:
		cursor.execute("insert into movies (movieid, title, year) values('{}','{}','{}')\n".format(movie_table[s]['movieid'],movie_table[s]['title'].strip().replace("'","''"),movie_table[s]['year'].strip()))

	for a in user_table:
		cursor.execute("insert into username (userid) values('{}')\n".format(user_table[a]['userid']))

	for b in rating_table:
		cursor.execute("insert into rating (user_id, movie_id, rating) values('{}','{}','{}')\n".format(rating_table[b]['user_id'],rating_table[b]['movie_id'],rating_table[b]['rating'].strip()))

	for k in movieid_genresid:
		cursor.execute("insert into genre_id (movies_id, genreid) values('{}','{}')\n".format(movieid_genresid[k]['movies_id'],movieid_genresid[k]['genreid']))


#EIGUM NÚ SAMSKIPTI VIÐ NOTANDA

print("Enter the names of 3 movies you like: ")

movie1 = input("First movie: ")
movie1 = F.check_movie(movie1, cursor)

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

#Finn id-in á öllum genres sem eru sameiginleg á öllum myndunum
t = """
select g.genreid
from genre_id g, movieid_view mv
where mv.movieid = g.movies_id
group by genreid
having count(genreid)>1"""

cursor.execute(t)
genreids = cursor.fetchall()
g_len = len(genreids) #tuple sem inniheldur 

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




