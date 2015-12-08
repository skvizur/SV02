f = open('movies.dat', 'r')

lst = []

for line in f:
	lst += [line.split()]

print(lst)

print(mer finnst ogedslega gaman i thessu)

f.close()
