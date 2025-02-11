#!/usr/bin/python3
import sys
import math

MAX_KEY_LENGTH = 30
ALPHABET = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
LETTER_TO_NUMBER = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25}  # Dictionary used to convert letters to numbers

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
	
def find_key_for_alphabet(alphabet):
	english_frequencies = [0.08, 0.015, 0.03, 0.04, 0.13, 0.02, 0.015, 0.06, 0.065, 0.005, 0.005, 0.035, 0.03, 0.07, 0.08, 0.02, 0.002, 0.065, 0.06, 0.09, 0.03, 0.01, 0.015, 0.005, 0.02, 0.002]
	alphabet_length = len(alphabet)
	alphabet_frequencies = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}
	for char in alphabet:
		if char != " ":
			alphabet_frequencies[char] = alphabet_frequencies[char] + 1 / alphabet_length
	correlations_arr = []
	for i in range(26):  # For each possible key value, 0-25
		correlation = 0
		for cipher_char in alphabet:  # For each character in the alphabet
			if cipher_char != " ":
				possible_plaintext_num = (LETTER_TO_NUMBER[cipher_char] - i) % 26  # Calculate the possible plaintext character value for the hypothetical key, i
				possible_plaintext_char = list(LETTER_TO_NUMBER.keys())[possible_plaintext_num]
				correlation += alphabet_frequencies[cipher_char] * english_frequencies[possible_plaintext_num]  # Update the correlation value based on the formula f(c)f’(e – i)
		correlations_arr.append(correlation)
	probable_key = correlations_arr.index(max(correlations_arr))  # Get the most likely key.
	#print("Most likely key: " + str(probable_key))
	return ALPHABET[probable_key]

def handle_alphabets(ciphertext, test_len):
	alphabets = []
	for i in range(test_len):
		a = []
		j = 0
		while i + test_len * j < len(ciphertext):	# Prevents attempts to access out-of-bounds index.
			a.append(ciphertext[i + test_len * j])
			j += 1
		alphabets.append(a)
	#print(alphabets)
	possible_key = ""
	for a in alphabets:
		possible_key += find_key_for_alphabet(a)
	return possible_key

def decrypt_helper(ciphertext, key):
	plaintext = ""
	key_index = 0
	for character in ciphertext:
		if character != " ":
			char_val = LETTER_TO_NUMBER[character]
			shift = ALPHABET.index(key[key_index])
			new_char_val = (char_val - shift) % 26
			new_char = list(LETTER_TO_NUMBER.keys())[new_char_val]
			plaintext += new_char
			key_index += 1
			key_index = key_index % len(key)
		else:	# Spaces are not affected by the key.
			plaintext += character
	return plaintext
	
def decryption_loop(ciphertext, factors):
	looping = True
	while looping:
		print(factors)
		test_len = int(input("What integer would you like to use as your key? It is suggested that you use one of your most common factors (or a product of your most common factors). "))
		possible_key = handle_alphabets(ciphertext, test_len)
		print("Possible key: " + possible_key)
		possible_plaintext = decrypt_helper(ciphertext, possible_key)
		print(possible_plaintext)
		looping = input("Would you like to try again with a different key? Y/N ") == "Y"
	print("\nYour current plaintext is: " + possible_plaintext)
	correcting = input("\nWould you like to correct any flaws in the plaintext? Y/N ") == "Y"
	while correcting:
		print("1) See the locations breakdown for characters in the current plaintext")
		print("2) Choose a character to modify")
		print("3) Finalize result")
		choice = input("Please enter 1, 2, or 3: ")
		if choice == "1":
			for i in range(len(possible_plaintext)):
				print(str(i) + ": " + possible_plaintext[i])
		elif choice == "2":
			index = int(input("Enter the index of the character you would like to replace. "))
			current_char = possible_plaintext[index]
			print("The character \'" + current_char + "\' is at this index.")
			replacement = input("What character would you like to insert in place of \'" + current_char + "\'? ").strip().lower()
			replacement = LETTER_TO_NUMBER[replacement]
			key_index = index % len(possible_key)
			key_char_diff = replacement - LETTER_TO_NUMBER[current_char]
			new_key_char_val = (LETTER_TO_NUMBER[possible_key[key_index]] + key_char_diff) % 26
			possible_key = list(possible_key)	# Convert key to list to allow changing characters.
			possible_key[key_index] = ALPHABET[new_key_char_val]
			possible_key = "".join(possible_key)
			print(possible_key)
			possible_plaintext = decrypt_helper(ciphertext, possible_key)
			print(possible_plaintext)
		elif choice == "3":
			correcting = False
		
		

def decrypt(ciphertext):
	matches = {}
	for i in range(MAX_KEY_LENGTH, 1, -1):
		matches = check_for_copies(ciphertext, i, matches)
	distances = get_distance_between_repeats(matches)
	factors = get_factors_of_distances(distances)
	factors.sort()
	decryption_loop(ciphertext, factors)

if len(sys.argv) < 2:
        print("Invalid arguments. Usage: python3 frequency_analyzer_vigenere.py \"CIPHERTEXT\"")
else:
        ciphertext = sys.argv[1]
        decrypt(ciphertext.lower().replace(" ",""))
