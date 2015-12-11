import psycopg2
import getpass
import pprint
import random as r
import pandas as pd
import string
import itertools


def create_tables(cursor):

	m = """
	create table movies (
	title varchar(250),
	year integer,
	movieid integer,
	primary key (movieid))"""
	cursor.execute(m)



	u = """
	create table username (
	gender varchar(250),
	age varchar(250),
	occupation integer,
	userid integer,
	primary key (userid)
	)"""
	cursor.execute(u)
	
	r = """
	create table rating (
	movie_id integer references movies(movieid),
	rating integer,
	user_id integer references username(userid),
	primary key (movie_id, user_id)
	)"""
	cursor.execute(r)

	g = """
	create table genre_id (
	movies_id integer references movies(movieid),
	genreid integer,
	primary key (movies_id,genreid)
	)"""
	cursor.execute(g)
	

def movies_table(filename):
	f = open(filename,'r')

	#GRUNNUR AD MOVIE TÖFLU MED ID, TITLI OG ÁRI.
	movie_table = {}
	index = 0

	for line in f:
		parts1 = line.split('::')
		if len(line) > 1:
			title = parts1[1].rsplit('(',1)
			updated_title=title[1].strip(')')
			movie_table[index] = {'movieid': parts1[0], 'title':title[0],'year':updated_title}
			index +=1

	f.close()

	return movie_table

def ratings_table(filename):
	f = open(filename,'r')

	rating_table = {}
	index = 0

	for line in f:
		parts = line.split('::')
		if len(line) > 1:
			rating_table[index] = {'user_id': parts[0],'movie_id':parts[1],'rating':parts[2]}
			index +=1

	f.close()

	return rating_table

def username_table(filename):
	f = open(filename,'r')

	user_table = {}
	index = 0

	for line in f:
		parts = line.split('::')
		if len(line) > 1:
			user_table[index] = {'userid': parts[0]}
			index +=1

	f.close()

	return user_table


def genres_table(filename):

	cols_movies = ['MovieID','Title', 'Genres']
	movies_table_panda = pd.read_csv(filename, sep='::', header = None, names = cols_movies, engine='python')

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
		i += 1


	adict = dict(zip(new_list,number_list))

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

	return movieid_genresid

#FALLIÐ KEMUR Í VEG FYRIR AÐ NOTANDI LENDI Í VANDA ÞEGAR HANN SLÆR INN MYND SEM ER EKKI TIL EÐA ER VITLAUST STAFSETT
def many_movies(movie, cursor):
	m = """
	select title, year
	from movies 
	where title like %s """
	cursor.execute(m, (('%' + movie + '%',)))
	movies = cursor.fetchall()
	print(movies)
	movie = input("What movie did you mean? ")
	return movie

#ATH HVORT MYND HAFI VERID SKRIFUD RETT EDA SE TIL I GAGNAGRUNNI
def check_movie(movie, cursor, many):
	check = """
	select title
	from movies
	where title = '%s'""" % movie
	cursor.execute(check)
	check_len = cursor.fetchall()

	if len(check_len) is not 1:
		movie_fun = many
		return movie_fun
	else:
		return movie


