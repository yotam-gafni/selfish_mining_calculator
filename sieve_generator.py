import numpy as np

from copy import copy
from bisearch import BisectRetVal, generic_bisect

SIEVE_LENGTH = 200
SIEVE_DEPTH = 6
p = np.longdouble(0.25)
accuracy = np.longdouble(0.95)

def generate_first_sieve():
	sieve_dict = {}
	for i in range(1, SIEVE_LENGTH + 1):
		sieve_dict[i] = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
		for depth in range(1, SIEVE_DEPTH + 1):
			if depth == 1:
				if i in (1,2,):
					sieve_dict[i][1].append(np.longdouble(1.0))
				else:
					sieve_dict[i][1] = copy(sieve_dict[i-1][2])
					sieve_dict[i][1].append(- sieve_dict[i][1][-1])
					for j in range(2, len(sieve_dict[i][1])):
						sieve_dict[i][1][-j] -= sieve_dict[i][1][-j-1]
					sieve_dict[i][1][0] += 1
			else:
				if depth > i:
					continue
				elif depth + 1 >= i :
					sieve_dict[i][depth] = copy(sieve_dict[i-1][depth - 1])
					sieve_dict[i][depth].insert(0, np.longdouble(0.0))
				elif depth == 6:
					sieve_dict[i][depth] = copy(sieve_dict[i-1][depth])
					sieve_dict[i][depth].append(- sieve_dict[i][depth][-1])
					for j in range(2, len(sieve_dict[i][depth])):
						sieve_dict[i][depth][-j] -= sieve_dict[i][depth][-j-1]
					for j in range(1, len(sieve_dict[i][depth])):
						sieve_dict[i][depth][j] += sieve_dict[i-1][depth - 1][j-1]
				else:
					sieve_dict[i][depth] = copy(sieve_dict[i-1][depth+1])
					sieve_dict[i][depth].append(- sieve_dict[i][depth][-1])
					for j in range(2, len(sieve_dict[i][depth])):
						sieve_dict[i][depth][-j] -= sieve_dict[i][depth][-j-1]
					for j in range(1, len(sieve_dict[i][depth])):
						sieve_dict[i][depth][j] += sieve_dict[i-1][depth - 1][j-1]


	return sieve_dict

def generate_subsequent_sieve(initial_dict):
	sieve_dict = {}
	sieve_dict[0] = initial_dict
	for i in range(1, SIEVE_LENGTH + 1):
		sieve_dict[i] = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
		for depth in range(1, SIEVE_DEPTH + 1):
			if depth == 1:
				sieve_dict[i][1] = copy(sieve_dict[i-1][2])
				sieve_dict[i][1].append(- sieve_dict[i][1][-1])
				for j in range(2, len(sieve_dict[i][1])):
					sieve_dict[i][1][-j] -= sieve_dict[i][1][-j-1]
				sieve_dict[i][1][0] += 1
			else:
				if depth == 6:
					sieve_dict[i][depth] = copy(sieve_dict[i-1][depth])
					sieve_dict[i][depth].append(- sieve_dict[i][depth][-1])
					for j in range(2, len(sieve_dict[i][depth])):
						sieve_dict[i][depth][-j] -= sieve_dict[i][depth][-j-1]
					for j in range(1, len(sieve_dict[i][depth])):
						sieve_dict[i][depth][j] += sieve_dict[i-1][depth - 1][j-1]
				else:
					sieve_dict[i][depth] = copy(sieve_dict[i-1][depth+1])
					sieve_dict[i][depth].append(- sieve_dict[i][depth][-1])
					for j in range(2, len(sieve_dict[i][depth])):
						sieve_dict[i][depth][-j] -= sieve_dict[i][depth][-j-1]
					for j in range(1, len(sieve_dict[i][depth])):
						sieve_dict[i][depth][j] += sieve_dict[i-1][depth - 1][j-1]
	return sieve_dict

def is_accurate_enough(array, array_index):
	total_sum = 0
	current_p_value = p 
	for term in array[array_index]:
		total_sum += term * current_p_value
		current_p_value *= p
	if total_sum > accuracy:
		return BisectRetVal.LOWER # Go lower in the array
	else:
		print(total_sum)
		return BisectRetVal.HIGHER # Go Higher in the array

sieve_dict = generate_first_sieve()
rel_array = [sieve_dict[i][SIEVE_DEPTH] for i in range(1,SIEVE_LENGTH + 1)]
running_index = 0
while is_accurate_enough(rel_array, -1) == BisectRetVal.HIGHER:
	new_sieve_dict = generate_subsequent_sieve(sieve_dict[SIEVE_LENGTH])
	del sieve_dict
	sieve_dict = new_sieve_dict
	rel_array = [new_sieve_dict[i][SIEVE_DEPTH] for i in range(1,SIEVE_LENGTH + 1)]
	running_index += 200
	print(running_index)

#print(sieve_dict)
print(running_index + generic_bisect(rel_array, is_accurate_enough))
print(accuracy)



