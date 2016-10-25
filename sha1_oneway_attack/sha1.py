import hashlib
import random
import string

prefix = 'ASAN1008'

def check_collision(hashed):
	k = 0
	for c in hashed:
		if (c != '0'):
			break;
		k += 1

	return k >= 4

def get_random_string():
	length = random.randint(1, 10)
	return ''.join(random.choice(string.printable[:-6]) for i in range(length))

def get_random_with_prefix():
	return prefix + get_random_string()

def add_prefix(value):
	return prefix + value

def hash(value):
	hash_slinging_slasher = hashlib.sha1()
	hash_slinging_slasher.update(value)
	return hash_slinging_slasher.hexdigest()

def found_collision(h, v):
	global hashed
	global value

	hashed = h
	value = v

	log1 = 'Found collision!\n'
	log2 = 'String: {0}\n'.format(value)
	log3 = 'Hash: {0}\n'.format(hashed)

	fanfare = log1 + log2 + log3

	print(fanfare)

	with open('sha1_log.txt', 'a') as log:
		log.write(fanfare)
		log.close()


# Generate value to be hashed
def generate_and_hash():
	iteration = 0
	while (True):
		if (iteration % 10000 == 0):
			print('Iteration: {0}'.format(iteration))
		value = get_random_with_prefix()
		hashed = hash(value)
		if (check_collision(hashed)):
			found_collision(hashed, value)
			break
		iteration += 1


generate_and_hash()
