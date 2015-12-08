f = open('movies.dat', 'r')

lst = []

for line in f:
	lst += [line.split()]

print(lst)

f.close()
