def readInput():
	# input file layout:
	# k
	# value0
	# value1
	# hash0
	# hash1
	# min range
	# max range

	global file_name
	with open(file_name, "r") as config:
		line = config.readline().strip()

		if (line):
			k_max = int(line)
			line = config.readline().strip()
		
		if (line):
			k_max = int(line)
			line = config.readline().strip()
		
		if (line):
			k_max = int(line)
			line = config.readline().strip()
		
		if (line):
			k_hashes.add() = int(line)
			line = config.readline().strip()
		
		if (line):
			k_max = int(line)
			line = config.readline().strip()
		
		if (line):
			k_max = int(line)
			line = config.readline().strip()
		
		if (line):
			k_max = int(line)
			line = config.readline().strip()

		config.close()
	
