import sys

files = ["data1.txt", "data2.txt", "data3.txt", "data4.txt"]

for x in files:
#for x in sys.argv[1:]:
	print x
	for line in open(x):
		output = line.split(" ")
		print str(output[0]) + '\n' + str(output[1]) + '\n' + str(output[2]) + '\n' + str(output[3]) + '\n'