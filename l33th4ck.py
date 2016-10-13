import sha3
from os.path import commonprefix
import random, string
import sys

ID = '112901008'
hash_slinging_slasher = sha3.SHA3224()
file_name = 'h4ck_{0}.txt'.format(sys.argv[1])

hashes = []

values_attempted = set()
k_max = 0
k_hashes = []
k_map = {}
current_range = (1, 1)


def read_config():
	global current_range
	current_range = (1, 50)

def get_random_string():
	global max_range
	length = random.randint(current_range[0], current_range[1])
	return ''.join(random.choice(string.printable[:-6]) for i in range(length))

def get_random_with_prefix():
	return ID + get_random_string()

def insert_hash(hashed):
	global k_max
	global k_hashes
	global hashes

	index = 0
	while (index < len(hashes)):
		if (hashes[index] > hashed):
			break;
		index += 1
	hashes.insert(index, hashed)

	i = index-1
	for i in range(index-1, index):
		if (i+1 > len(hashes)-1 or i < 0):
			continue;
		k = getK(hashes[i:i+2])
		if (k > k_max):
			k_max = k
			k_hashes = hashes[i:i+2]
			print_results(k)

def print_results(k):
	values = k_map[k_hashes[0]], k_map[k_hashes[1]]
	hashes = k_hashes[0], k_hashes[1]

	print('FOUND NEW K: {0}'.format(k))
	print('Strings: {0}, {1}'.format(values[0], values[1]))
	print('Hashes: {0}, {1}\n'.format(hashes[0], hashes[1]))

	# Log to file
	with open(file_name, 'a') as log:
		log.write(str(k) + '\n')
		log.write(values[0] + '\t' + values[1] + '\n')
		log.write(str(hashes[0]) + '\t' + str(hashes[1]) + '\n\n')
		log.close()

# Generate value to be hashed
def generate_and_hash():
	# Ensure we haven't already generated this before
	value = get_random_with_prefix()
	while (value in values_attempted):
		value = get_random_with_prefix()

	values_attempted.add(value)
	hashed_value = hash(value)
	k_map[hashed_value] = value
	insert_hash(hashed_value)

def getK(byte_array):
	return len(commonprefix(byte_array)) * 4

def hash(string):
	hash_slinging_slasher = sha3.SHA3224()
	hash_slinging_slasher.update(string)
	return hash_slinging_slasher.hexdigest()

def start_hacking():
	read_config()
	while (True):
		generate_and_hash()

# Let's do this!!
start_hacking()

