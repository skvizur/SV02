def create_database(cursor):
	try:
		cursor.execute("CREATE DATABASE () DEFAULT CHARACHTER SET 'utf8'".format(DB_NAME))
	except psycopg2.connector.Error as err:
		print("Unable to create database: {}".format(err))
		exit(1)

	try:
		conn.database = DB_NAME
	except psycopg2.

def create_tables():
	create table movies (
	title varchar(250),
	year integer,
	movieid integer,
	primary key (movieid));

	create table username (
	gender varchar(250),
	age varchar(250),
	occupation integer,
	userid integer,
	primary key (userid)
	);

	create table rating (
	movie_id integer references movies(movieid),
	rating integer,
	user_id integer references username(userid),
	primary key (movie_id, user_id)
	);

	create table genre_id (
	movies_id integer references movies(movieid),
	genreid integer,
	primary key (movies_id,genreid)
	);




def many_movies(movie, cursor):
	m = """
	select title, year
	from movies 
	where title like %s """
	cursor.execute(m, (('%' + movie + '%',)))
	movies = cursor.fetchall()
	print(movies)
	movie, year = input("What movie did you mean? ")
	return movie
