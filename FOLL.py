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