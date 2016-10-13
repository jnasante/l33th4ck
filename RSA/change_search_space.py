import sys

files = ["data1.txt", "data2.txt", "data3.txt", "data4.txt"]

for x in files:
	print(x)
	for line in open(x):
		parts = line.split(" ")

		increment = 4*(int(parts[3]) - int(parts[2]))
		start = int(parts[2]) + increment
		end = int(parts[3]) + increment

		print(parts[1]+'\n')

		f = file(x,'w')
		f.write(parts[0] + " ")
		f.write(parts[1] + " ")
		f.write(str(start) + " ")
		f.write(str(end) + " ")
		f.close()