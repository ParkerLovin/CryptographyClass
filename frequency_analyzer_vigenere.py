#!/usr/bin/python3

"""
Author: Parker Lovin
Date: 2/11/2025
Course: CSC-4575-001
Purpose: This program decrypts a Vigenere cipher by dividing ciphertext into alphabets and performing frequency analysis on each alphabet.
"""

import sys

MAX_KEY_LENGTH = 30	# Assumes the key is 30 characters or shorter to save time; can be modified if necessary.
LETTER_TO_NUMBER = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20,
	'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25}  # Dictionary used to convert letters to numbers
ENGLISH_FREQUENCIES = [0.08, 0.015, 0.03, 0.04, 0.13, 0.02, 0.015, 0.06, 0.065, 0.005, 0.005, 0.035, 
		0.03, 0.07, 0.08, 0.02, 0.002, 0.065, 0.06, 0.09, 0.03, 0.01, 0.015, 0.005, 0.02, 0.002]	# A-Z letter frequencies in English.

# Function to check for duplicate substrings of a given length, which helps in finding key length.
# Duplicates are returned in the form of a dictionary.
def check_for_copies(ciphertext, substring_size, matches_dict):
	for i in range(0, len(ciphertext) - substring_size + 1):
		substring = ciphertext[i:i+substring_size]
		if not substring in matches_dict.keys():	# Prevents unnecessarily checking for the same substring in multiple iterations.
			positions = []
			start = i	# This variable tracks the current position so that no instance of a substring is double counted.
			while True:
				start = ciphertext.find(substring, start)
				if start == -1:	# Handle the event in which no more duplicates of this substring can be found.
					break
				positions.append(start)
				start += substring_size
			if len(positions) > 1:
				matches_dict[substring] = positions	# The key is the substring, and the value is a list of positions for that substring.
	return matches_dict

# Takes in a dictionary of matches (repeat substring info) and outputs the distances between matches.
def get_distance_between_repeats(matches):
	all_distances = []
	# For each substring in the dictionary, calculate the distances between the substring's instances.
	for substring in matches.keys():
		for i in range(len(matches[substring])):
			for j in range(i + 1, len(matches[substring])):	# Starting this loop at "i" prevents double counting.
				all_distances.append(matches[substring][j] - matches[substring][i])
	return all_distances

# Simple function to factor an integer.
def factor(num):
	n = num
	factors = []
	for i in range(2, n + 1):
		while n % i == 0:
			factors.append(i)
			n = n // i
	return factors			

# For every distance (between identical substrings), factor that distance using the factor() helper function.
def get_factors_of_distances(distances):
	all_factors = []
	for d in distances:
		all_factors += factor(d)
	return all_factors

# Uses the formula sum(ni * (ni-1)) / (n * n-1) to calculate index of coincidence for a ciphertext/alphabet.
def calc_index_of_coincidence(ciphertext):
	n = len(ciphertext)
	summation = 0
	for letter in LETTER_TO_NUMBER.keys():	# Account for all 26 possible letters.
		ni = ciphertext.count(letter)
		summation += ni * (ni - 1)
	return str(summation / (n * (n - 1)))

# For a given alphabet, find the likely key. This is similar to solving a shift cipher.	
def find_key_for_alphabet(alphabet):
	alphabet_length = len(alphabet)
	alphabet_frequencies = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0,
		'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}	# Keep track of letter frequencies in this particular alphabet.
	
	# Calculate frequencies of characters in this particular alphabet/ciphertext.
	for char in alphabet:
		alphabet_frequencies[char] = alphabet_frequencies[char] + 1 / alphabet_length
	
	correlations_arr = []
	for i in range(26):  # For each possible key value, 0-25
		correlation = 0
		for cipher_char in alphabet:  # For each character in the alphabet
			if cipher_char != " ":
				possible_plaintext_num = (LETTER_TO_NUMBER[cipher_char] - i) % 26  # Calculate the plaintext character value for the hypothetical key, i
				possible_plaintext_char = list(LETTER_TO_NUMBER.keys())[possible_plaintext_num]
				correlation += alphabet_frequencies[cipher_char] * ENGLISH_FREQUENCIES[possible_plaintext_num]  # Update the correlation value based on the formula f(c)f’(e – i)
		correlations_arr.append(correlation)
	probable_key = correlations_arr.index(max(correlations_arr))  # Get the most likely key.
	return list(LETTER_TO_NUMBER.keys())[probable_key]	# Return the key in the form of a letter.

# Takes a ciphertext and splits it into multiple alphabets. The number of alphabets is determined by test_len, a hypothetical key length.
# Also calls the calc_index_of_coincidence function to get the IC for each alphabet.
# Returns a possible key for the entire ciphertext.
def handle_alphabets(ciphertext, test_len):
	alphabets = []
	for i in range(test_len):
		a = []
		j = 0
		while i + test_len * j < len(ciphertext):	# Prevents attempts to access out-of-bounds index.
			a.append(ciphertext[i + test_len * j])
			j += 1
		alphabets.append(a)
		print("Index of coincidence for alphabet " + str(i) + ":     " + calc_index_of_coincidence("".join(a)))
	possible_key = ""
	for a in alphabets:	# Concatenate the alphabet keys into one unified key.
		possible_key += find_key_for_alphabet(a)
	return possible_key

# Decrypts a ciphertext based on a given key.
def decrypt_helper(ciphertext, key):
	plaintext = ""
	key_index = 0	# Keeps track of which character in the key is currently being used for decryption.
	for character in ciphertext:
		if character != " ":
			# Calculate the value of the plaintext character based on the current key
			char_val = LETTER_TO_NUMBER[character]
			shift = LETTER_TO_NUMBER[key[key_index]]
			new_char_val = (char_val - shift) % 26
			# Obtain the plaintext character and add it to the plaintext string
			new_char = list(LETTER_TO_NUMBER.keys())[new_char_val]
			plaintext += new_char
			# Increment the key index, then use the modulus operator to avoid exceeding the key length.
			key_index += 1
			key_index = key_index % len(key)
		else:	# Spaces are not affected by the key.
			plaintext += character
	return plaintext

# Loops through multiple decryption processes until the user is satisfied, finally outputting the possible key and plaintext.
# Input: the original ciphertext and the factors calculated for the distances between substrings.	
def decryption_loop(ciphertext, factors):
	looping = True
	possible_key = ""
	possible_plaintext = ""
	while looping:
		# Allow the user to view the distance factors and make a decision about the key length.
		print("\nThis program has calculated the distance between repeats in the ciphertext, then factored these distances. Here are the factors: ")
		print(factors)
		test_len = int(input("\nWhat integer would you like to use as your key length? It is suggested that you use one of your most common factors (or a product of your most common factors). "))
		print()
		
		# For the provided key length, calculate the possible key and plaintext.
		possible_key = handle_alphabets(ciphertext, test_len)
		print("\nPossible key: " + possible_key)
		possible_plaintext = decrypt_helper(ciphertext, possible_key)
		print("Possible plaintext: " + possible_plaintext)
		
		# If the user is unsatisfied with the plaintext, he/she has the option to try a different key length.
		looping = input("\nWould you like to try again with a different key length? Y/N ") == "Y"
	
	# Display the current plaintext, then give the user the opportunity to fine-tune the plaintext.
	print("\n\n\nYour current plaintext is: " + possible_plaintext)
	correcting = input("\nWould you like to correct any flaws in the plaintext? Y/N ") == "Y"
	while correcting:
		print("\n1) See the locations breakdown for characters in the current plaintext")
		print("2) Choose a character to modify")
		print("3) Finalize result\n")
		choice = input("Please enter 1, 2, or 3: ")
		if choice == "1":	# Display indices to prevent the user from having to count.
			for i in range(len(possible_plaintext)):
				print(str(i) + ": " + possible_plaintext[i])
		elif choice == "2":	# The user chooses a location to replace in the plaintext, then chooses the new character for that location.
			index = int(input("\nEnter the index of the character you would like to replace. "))
			current_char = possible_plaintext[index]
			print("\nThe character \'" + current_char + "\' is at this index.")
			replacement = input("What character would you like to insert in place of \'" + current_char + "\'? ").strip().lower()
			
			# Based on the user's replacement choice, calculate the new key value.
			replacement = LETTER_TO_NUMBER[replacement]
			key_index = index % len(possible_key)	# Determine which character in the key to replace.
			key_char_diff = replacement - LETTER_TO_NUMBER[current_char]	# Determine how much to increment this key character by.
			new_key_char_val = (LETTER_TO_NUMBER[possible_key[key_index]] + key_char_diff) % 26
			possible_key = list(possible_key)	# Convert key to list to allow changing characters.
			possible_key[key_index] = list(LETTER_TO_NUMBER.keys())[new_key_char_val]	# Replace the designated character in the key with the updated value.
			possible_key = "".join(possible_key)	# Return the key to string form.
			print("\nUpdated key: " + possible_key)
			possible_plaintext = decrypt_helper(ciphertext, possible_key)
			print("\nUpdated plaintext: " + possible_plaintext)
		elif choice == "3":
			correcting = False
	# Display final output info about the key and plaintext.
	print("\n" * 4)
	print("Final key: " + possible_key)
	print("\nFinal plaintext: " + possible_plaintext)
		
# The "main" function for this program.
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
