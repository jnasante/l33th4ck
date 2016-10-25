import sha3
from os.path import commonprefix
import random, string
import sys
import base64
import bisect

ID = '112901008'
hash_slinging_slasher = sha3.SHA3224()
file_name = '{0}_h4ck.txt'.format(sys.argv[1])

hashes = []

values_attempted = set()
k_max = 0
k_hashes = []
k_map = {}
current_range = (1, 20)

def get_random_string():
	global max_range
	length = random.randint(current_range[0], current_range[1])
	return ''.join(random.choice(string.printable[:-6]) for i in range(length))

def get_random_with_prefix():
	return ID + get_random_string()

def convert_to_value(hashed):
	return ID+hashed.decode('utf-8')

def convert_to_binary_partial(sHex):
    sReturn = ''

    for i in range(25):
    	if (sHex[i] == '0'):
    		sReturn += '0000'
    	elif (sHex[i] == '1'):
    		sReturn += '0001'
     	elif (sHex[i] == '2'):
    		sReturn += '0010'
    	elif (sHex[i] == '3'):
    		sReturn += '0011'
    	elif (sHex[i] == '4'):
    		sReturn += '0100'
    	elif (sHex[i] == '5'):
    		sReturn += '0101'
    	elif (sHex[i] == '6'):
    		sReturn += '0110'
    	elif (sHex[i] == '7'):
    		sReturn += '0111'
    	elif (sHex[i] == '8'):
    		sReturn += '1000'
    	elif (sHex[i] == '9'):
    		sReturn += '1001'
    	elif (sHex[i] == 'a'):
    		sReturn += '1010'
    	elif (sHex[i] == 'b'):
    		sReturn += '1011'
    	elif (sHex[i] == 'c'):
    		sReturn += '1100'
    	elif (sHex[i] == 'd'):
    		sReturn += '1101'
    	elif (sHex[i] == 'e'):
    		sReturn += '1110'
    	elif (sHex[i] == 'f'):
    		sReturn += '1111'

    return sReturn


def pollard_rho():
	seed = get_random_with_prefix()
	iterations = 0
	tortoise = seed
	tortoise_hash = hash(seed)
	hare = seed
	hare_hash = hash(seed)

	while (True):
		if (iterations % 10000000 == 0):
			print('\nIteration: {0}\n'.format(iterations))

		tortoise = convert_to_value(tortoise_hash)
		tortoise_hash = hash(tortoise)
		for _ in range(2):
			hare = convert_to_value(hare_hash)
			hare_hash = hash(hare)

			# Ensure we don't have a false positive on the very first identical ones
			if (iterations == 0):
				continue

			hash_array = [tortoise_hash, hare_hash]
			k = getK([convert_to_binary_partial(tortoise_hash), convert_to_binary_partial(hare_hash)])
			if (k > k_max):
				k_map[tortoise_hash] = tortoise
				k_map[hare_hash] = hare
				found_new_k(k, hash_array)

		iterations += 1

def insert_hash(hashed):
	global k_max
	global k_hashes
	global hashes

	index = bisect.bisect(hashes, hashed)
	hashes.insert(index, hashed)

	i = index-1
	for i in range(index-1, index):
		if (i+1 > len(hashes)-1 or i < 0):
			continue;
		k = getK(hashes[i:i+2])
		k = getK([convert_to_binary_partial(hashes[i]), convert_to_binary_partial(hashes[i+1])])
		if (k > k_max):
			found_new_k(k, hashes[i:i+2])

def found_new_k(k, hash_array):
	global k_max
	global k_hashes

	k_max = k
	k_hashes = hash_array
	print_results(k)

def print_results(k):
	values = k_map[k_hashes[0]], k_map[k_hashes[1]]
	hashes = k_hashes[0], k_hashes[1]

	print_k = 'FOUND NEW K: {0}'.format(k)
	print_strings = 'Strings: {0}, {1}'.format(values[0], values[1])
	print_hashes = 'Hashes: {0}, {1}'.format(hashes[0], hashes[1])
	fanfare = '\n{0}\n{1}\n{2}\n'.format(print_k, print_strings, print_hashes)

	print(fanfare)

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
	return len(commonprefix(byte_array))

def hash(string):
	hash_slinging_slasher = sha3.SHA3224()
	hash_slinging_slasher.update(string)
	return hash_slinging_slasher.hexdigest()

def start_hacking():
	while (True):
		generate_and_hash()

# Let's do this!!
start_hacking()
# pollard_rho()
