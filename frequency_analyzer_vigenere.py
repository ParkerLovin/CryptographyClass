#!/usr/bin/python3
import sys
import math

MAX_KEY_LENGTH = 30
ALPHABET = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

def check_for_copies(ciphertext, substring_size, matches_dict):
	for i in range(0, len(ciphertext) - substring_size + 1):
		substring = ciphertext[i:i+substring_size]
		if not substring in matches_dict.keys():	# Prevents unnecessarily checking for the same substring in multiple iterations.
			positions = []
			start = i
			while True:
				start = ciphertext.find(substring, start)
				if start == -1:
					break
				positions.append(start)
				start += substring_size
			if len(positions) > 1:
				#print(positions)
				matches_dict[substring] = positions
	#print(matches_dict)
	return matches_dict

def get_distance_between_repeats(matches):
	all_distances = []
	for substring in matches.keys():
		#distances_for_this_substring = []
		for i in range(1, len(matches[substring])):
			all_distances.append(matches[substring][i] - matches[substring][0])	# This may need to be reworked. If there are 3+ matches for a substring, this would account for the distance between 0 and 1 and between 0 and 2, but not between 1 and 2.
	return all_distances

def factor(num):
	n = num
	factors = []
	for i in range(2, n):
		while n % i == 0:
			factors.append(i)
			n = n // i
	if n == num:	# In this case, num is prime.
		factors = [num]
	return factors
			

def get_factors_of_distances(distances):
	all_factors = []
	for d in distances:
		all_factors += factor(d)
	return all_factors

def calc_index_of_coincidence(ciphertext):
	n = len(ciphertext)
	summation = 0
	for letter in ALPHABET:
		ni = ciphertext.count(letter)
		summation += ni * (ni - 1)
	return summation / (n * (n - 1))

def decrypt(ciphertext):
	matches = {}
	for i in range(MAX_KEY_LENGTH, 1, -1):
		matches = check_for_copies(ciphertext, i, matches)
	distances = get_distance_between_repeats(matches)
	#print(matches)
	#print()
	#distances.sort(reverse=True)
	#print(distances)
	factors = get_factors_of_distances(distances)
	print(factors)	

if len(sys.argv) < 2:
        print("Invalid arguments. Usage: python3 frequency_analyzer_vigenere.py \"CIPHERTEXT\"")
else:
        ciphertext = sys.argv[1]
        decrypt(ciphertext.lower().replace(" ",""))
