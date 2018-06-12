import numpy as np

from copy import copy,deepcopy
from bisearch import BisectRetVal, generic_bisect

SIEVE_LENGTH = 200
SIEVE_DEPTH = 6
CHECK_DEPTH = 6
p = np.longdouble(0.25)
accuracy = np.longdouble(0.5)

def generate_first_sieve():
	sieve_dict = {}
	for i in range(0, SIEVE_LENGTH + 1):
		sieve_dict[i] = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
		for depth in range(SIEVE_DEPTH + 1):
			if depth == 0:
				if i == 0:
					sieve_dict[i][depth].append(np.longdouble(1.0))
				elif i == 1:
					sieve_dict[i][depth] = copy(sieve_dict[i-1][depth])
					sieve_dict[i][depth].append(- sieve_dict[i][depth][-1])
				else: 
					sieve_dict[i][depth] = copy(sieve_dict[i-1][depth])
					sieve_dict[i][depth].append(- sieve_dict[i][depth][-1])
					for j in range(2, len(sieve_dict[i][depth])):
						sieve_dict[i][depth][-j] -= sieve_dict[i][depth][-j-1]
					temp_coeff = copy(sieve_dict[i-1][depth + 1])
					temp_coeff.append(- temp_coeff[-1])
					for j in range(2, len(temp_coeff)):
						temp_coeff[-j] -= temp_coeff[-j-1]
					min_ind = min(len(temp_coeff), len(sieve_dict[i][depth]))
					max_ind = max(len(temp_coeff), len(sieve_dict[i][depth]))
					for j in range(min_ind):
						sieve_dict[i][depth][j] += temp_coeff[j]
					for j in range(min_ind, max_ind):
						sieve_dict[i][depth].append(temp_coeff[j])
			else:
				if depth > i:
					continue
				elif depth == SIEVE_DEPTH:
					sieve_dict[i][depth] = copy(sieve_dict[i-1][depth])
					sieve_dict[i][depth].insert(0, np.longdouble(0.0))
					temp_coeff = copy(sieve_dict[i-1][depth - 1])
					temp_coeff.insert(0, np.longdouble(0.0))
					min_ind = min(len(temp_coeff), len(sieve_dict[i][depth]))
					max_ind = max(len(temp_coeff), len(sieve_dict[i][depth]))
					for j in range(min_ind):
						sieve_dict[i][depth][j] += temp_coeff[j]
					for j in range(min_ind, max_ind):
						sieve_dict[i][depth].append(temp_coeff[j])
				elif depth + 1 >= i :
					sieve_dict[i][depth] = copy(sieve_dict[i-1][depth - 1])
					sieve_dict[i][depth].insert(0, np.longdouble(0.0))
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
		sieve_dict[i] = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
		for depth in range(SIEVE_DEPTH + 1):
			if depth == 0:
				sieve_dict[i][depth] = copy(sieve_dict[i-1][depth])
				sieve_dict[i][depth].append(- sieve_dict[i][depth][-1])
				for j in range(2, len(sieve_dict[i][depth])):
					sieve_dict[i][depth][-j] -= sieve_dict[i][depth][-j-1]
				temp_coeff = copy(sieve_dict[i-1][depth + 1])
				temp_coeff.append(- temp_coeff[-1])
				for j in range(2, len(temp_coeff)):
					temp_coeff[-j] -= temp_coeff[-j-1]
				min_ind = min(len(temp_coeff), len(sieve_dict[i][depth]))
				max_ind = max(len(temp_coeff), len(sieve_dict[i][depth]))
				for j in range(min_ind):
					sieve_dict[i][depth][j] += temp_coeff[j]
				for j in range(min_ind, max_ind):
					sieve_dict[i][depth].append(temp_coeff[j])
			else:
				if depth == SIEVE_DEPTH:
					sieve_dict[i][depth] = copy(sieve_dict[i-1][depth])
					sieve_dict[i][depth].insert(0, np.longdouble(0.0))
					temp_coeff = copy(sieve_dict[i-1][depth - 1])
					temp_coeff.insert(0, np.longdouble(0.0))
					min_ind = min(len(temp_coeff), len(sieve_dict[i][depth]))
					max_ind = max(len(temp_coeff), len(sieve_dict[i][depth]))
					for j in range(min_ind):
						sieve_dict[i][depth][j] += temp_coeff[j]
					for j in range(min_ind, max_ind):
						sieve_dict[i][depth].append(temp_coeff[j])
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
	current_p_value = 1
	for term in array[array_index]:
		total_sum += term * current_p_value
		current_p_value *= p
	if total_sum > accuracy:
		#print(total_sum)
		return BisectRetVal.LOWER # Go lower in the array
	else:
		#print(total_sum)
		return BisectRetVal.HIGHER # Go Higher in the array

def sanity_test(column):
	total_sum = 0
	current_p_value = 1
	for depth in column:
		current_p_value = 1
		temp_sum = 0
		for term in column[depth]:
			temp_sum += term * current_p_value
			current_p_value *= p
		total_sum += temp_sum

	if total_sum >= 1.01 or total_sum <= 0.99:
		print("SANITY TEST ISSUE")

def sanity_check(column):
	new_column = deepcopy(column)
	new_column = dict(list(filter(lambda x: x[1]!= [], new_column.items())))
	total_sum_array = new_column[len(new_column) -1]
	for i in range(len(new_column)-2,-1,-1):
		for j in range(len(new_column[i])):
			total_sum_array[j] += new_column[i][j]


	if total_sum_array[0] >= 1.01 or total_sum_array[0] <= 0.99:
		print("SANITY CHECK ISSUE")
	for i in range(1,len(total_sum_array)):
		if total_sum_array[i] >= 0.01 or total_sum_array[i] <= -0.01:
			print("SANITY CHECK ISSUE")


def sum_util(column, coeff_ind):
	total_sum = 0
	for i in range(7):
		total_sum += column[i][coeff_ind]
	print(total_sum)


def where_is_it_wrong(column, pre_column, coeff_ind):
	expected_values = [0,0,0,0,0,0,0]
	expected_values[0] = pre_column[0][coeff_ind] - pre_column[0][coeff_ind -1]
	expected_values[0] += pre_column[1][coeff_ind] - pre_column[1][coeff_ind -1]
	expected_values[1] = pre_column[0][coeff_ind -1] + pre_column[2][coeff_ind] - pre_column[2][coeff_ind -1]
	expected_values[2] = pre_column[1][coeff_ind -1] + pre_column[3][coeff_ind] - pre_column[3][coeff_ind -1]
	expected_values[3] = pre_column[2][coeff_ind -1] + pre_column[4][coeff_ind] - pre_column[4][coeff_ind -1]
	expected_values[4] = pre_column[3][coeff_ind -1] + pre_column[5][coeff_ind] - pre_column[5][coeff_ind -1]
	expected_values[5] = pre_column[4][coeff_ind -1] + pre_column[6][coeff_ind] - pre_column[6][coeff_ind -1]
	expected_values[6] = pre_column[5][coeff_ind -1] + pre_column[6][coeff_ind -1]

	print(expected_values)
	for i in range(7):
		print(column[i][coeff_ind])




sieve_dict = generate_first_sieve()
#for i in range(SIEVE_LENGTH):
	#print(i)
	#sanity_check(sieve_dict[i])
rel_array = [sieve_dict[i][CHECK_DEPTH] for i in range(1,SIEVE_LENGTH + 1)]

running_index = 0
while is_accurate_enough(rel_array, -1) == BisectRetVal.HIGHER:
	new_sieve_dict = generate_subsequent_sieve(sieve_dict[SIEVE_LENGTH])
	del sieve_dict
	sieve_dict = new_sieve_dict
	#for i in range(SIEVE_LENGTH):
	#	sanity_check(sieve_dict[i])
	rel_array = [new_sieve_dict[i][CHECK_DEPTH] for i in range(1,SIEVE_LENGTH + 1)]
	running_index += 200
	print(running_index)

print(running_index + generic_bisect(rel_array, is_accurate_enough))
print(accuracy)



