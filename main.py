import psycopg2
import getpass
import pprint

host = 'localhost'
dbname = 'movies'

username = 'hildurrungudjonsdottir' # input('User name for {}.{}: '.format(host,dbname))
pw = getpass.getpass()

conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(host, dbname, username, pw)

print("Connecting to database {}.{} as {}".format(host, dbname, username))

conn = psycopg2.connect(conn_string)

cursor = conn.cursor()

print("Connected!\n")

nafn = 'Toy Story '

s = """
select g.genreid
from movies m, genre_id g
where m.movieid = g.movies_id
and m.title = '%s'""" % nafn


cursor.execute(s)

records = cursor.fetchall()
#pprint.pprint(records)

if len(records) > 0:
	for i in range(len(records)):
		row = records[i]
		print(row)




cursor.close()
conn.close()