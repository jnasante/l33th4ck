import numpy
import binascii

ID = '112901008'
no_rounds = 24

RC = [
	'0000000000000000000000000000000000000000000000000000000000000001',
	'0000000000000000000000000000000000000000000000001000000010000010',
	'1000000000000000000000000000000000000000000000001000000010001010',
	'1000000000000000000000000000000010000000000000001000000000000000',
	'0000000000000000000000000000000000000000000000001000000010001011',
	'0000000000000000000000000000000010000000000000000000000000000001',
	'1000000000000000000000000000000010000000000000001000000010000001',
	'1000000000000000000000000000000000000000000000001000000000001001',
	'0000000000000000000000000000000000000000000000000000000010001010',
	'0000000000000000000000000000000000000000000000000000000010001000',
	'0000000000000000000000000000000010000000000000001000000000001001',
	'0000000000000000000000000000000010000000000000000000000000001010',
	'0000000000000000000000000000000010000000000000001000000010001011',
	'1000000000000000000000000000000000000000000000000000000010001011',
	'1000000000000000000000000000000000000000000000001000000010001001',
	'1000000000000000000000000000000000000000000000001000000000000011',
	'1000000000000000000000000000000000000000000000001000000000000010',
	'1000000000000000000000000000000000000000000000000000000010000000',
	'0000000000000000000000000000000000000000000000001000000000001010',
	'1000000000000000000000000000000010000000000000000000000000001010',
	'1000000000000000000000000000000010000000000000001000000010000001',
	'1000000000000000000000000000000000000000000000001000000010000000',
	'0000000000000000000000000000000010000000000000000000000000000001',
	'1000000000000000000000000000000010000000000000001000000000001000'
]

def convert_RC():
	global RC
	for i in range(len(RC)):
		RC[i] = binascii.unhexlify(RC[i]).decode('utf-8')
		print(RC[i])

def bitwise_and(str1, str2):
	return '{0:064b}'.format(int(str1, 2) & int(str2, 2))

def bitwise_xor(str1, str2):
	return '{0:064b}'.format(int(str1, 2) ^ int(str2, 2))

def bitwise_not(str1):
	bits = ''
	for c in range(len(str1)):
		bits += '0' if str1[c] == '1' else '1'
	return bits

def create_matrix():
	m = numpy.empty(shape=(5,5), dtype='object')

	string = ''.zfill(64)
	m.fill(string)

	return m

def generate_inital_matrix():
	b = bin(int(binascii.hexlify(ID.encode()), 16))[2:]
	while (len(b) != 128):
		b += '0'
	matrix = create_matrix()
	matrix[0][0] = b[:64]
	matrix[0][1] = b[64:]
	return matrix

def pi(mat):
	new_mat = mat

	for i in range(5):
		for j in range(5):
			 new_mat[j][(2*i + 3*j)%5] = mat[i][j]

	return new_mat

def chi(mat):
	new_mat = mat
	for i in range(5):
		for j in range(5):
			new_mat[i][j] = bitwise_xor(mat[i][j], bitwise_and(bitwise_not(mat[i][(j+1)%5]), mat[i][(j+2)%5]))
	return new_mat

def iota(mat, round):
	new_mat = mat

	new_mat[0][0] = bitwise_xor(mat[0][0], RC[round])

	return new_mat

def sha3():
	mat = generate_inital_matrix()
	for r in range(no_rounds):
		mat = pi(mat)
		mat = chi(mat)
		mat = iota(mat, r)

		log_stmt = 'Round {0} matrix: \n{1}\n'.format(r+1, mat)
		print(log_stmt)

		with open('sha3_log.txt', 'a') as log:
			log.write(log_stmt + '\n')
			log.close()

sha3()
