import psycopg2
import getpass

host = 'localhost'

dbname = input('Database name: ')

username = input('Username for {}.{}: '.format(host,dbname))
pw = getpass.getpass()

conn_string = "host = '{}' dbname = '{}' user = '{}' password ='{}'".format(host, dbname, username, pw)

print("Connecting to database {}.{} as {}".format(host, dbname, username))

conn = psycopg2.connect(conn_string)

cursor = conn.cursor()

print('Connected!\n')

thesqlcommands = open('movies_demo.sql','r')
for line in thesqlcommands:
	cursor.execute(line.strip())

thesqlcommands.close()

conn.commit()

cursor.close()
conn.close()
