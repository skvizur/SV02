import psycopg2
import getpass
import pprint

host = 'localhost'
dbname = 'movies'

username = 'hildurrungudjonsdottir' #input('User name for {}.{}: '.format(host,dbname)) 
pw = '1313' #getpass.getpass()

conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(host, dbname, username, pw)

print("Connecting to database {}.{} as {}".format(host, dbname, username))

conn = psycopg2.connect(conn_string)

cursor = conn.cursor()

print("Connected!\n")

nafn = 'Toy Story '

s = """
create view genres as
select g.genreid
from movies m, genre_id g
where m.movieid = g.movies_id
and m.title = '%s'""" % nafn

cursor.execute(s)
#print(genre)

records = cursor.fetchall()
#print(len(records))
#pprint.pprint(records)

#Finnum allar myndir eð sama genre og myndirnar sem slegnar eru inn
if len(records) is 1:
	genre1 = records[0]
	a = """
	select distinct m.movieid
	from movies m, genre_id g
	where m.movieid = g.movies_id
	and g.genreid = %s""" % (genre1[0])
	cursor.execute(a)

	movieid_genres = cursor.fetchall()

	#if len(movieid_genres) > 0:
	#	for i in range(len(movieid_genres)):
	#		print('1')


elif len(records) is 2:
	genre1 = records[0]
	genre2 = records[1]

	a = """
	select distinct m.movieid
	from movies m, genre_id g
	where m.movieid = g.movies_id
	and (g.genreid = %s or g.genreid = %s)""" % (genre1[0], genre2[0])
	cursor.execute(a)

	movieid_genres = cursor.fetchall()

	#if len(movieid_genres) > 0:
		#for i in range(len(movieid_genres)):
		#	print('2')


elif len(records) is 3:
	genre1 = records[0]
	genre2 = records[1]
	genre3 = records[2]

	a = """
	select distinct m.movieid
	from movies m, genre_id g
	where m.movieid = g.movies_id
	and (g.genreid = %s or g.genreid = %s or g.genreid = %s)"""
	
	v = (genre1[0], genre2[0], genre3[0])

	cursor.execute(a, v)

	movieid_genres = cursor.fetchall()



for i in movieid_genres:
	u = """
	select r.user_id
	from rating r
	where %s in (1,2,3)
	and r.rating > 3
	group by r.user_id
	having count(r.user_id) > 2
	order by r.user_id""" % i[0]
	cursor.execute(u)
	user = i.cursor.fetchall(u)


#print(u)



#if len(movieid_genres) > 0:
#	for i in range(len(movieid_genres)):
	#	print('3')


#Finnum notendur sem hafa rate-að allar þessar myndir




cursor.close()
conn.close()