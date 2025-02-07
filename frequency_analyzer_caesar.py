#!/usr/bin/python3

# Author: Parker Lovin
# Course: CSC-4575-001
# Description: This program uses probabilities to decrypt ciphertext based on the Caesar cipher.

import sys

letter_to_number = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25}	# Dictionary used to convert letters to numbers

english_frequencies = [0.08, 0.015, 0.03, 0.04, 0.13, 0.02, 0.015, 0.06, 0.065, 0.005, 0.005, 0.035, 0.03, 0.07, 0.08, 0.02, 0.002, 0.065, 0.06, 0.09, 0.03, 0.01, 0.015, 0.005, 0.02, 0.002]	# Note that index 0 corresponds to 'a', 1 to 'b', and so on.

# This function returns an array with each value representing a correlation of frequencies for a given key. The key corresponds to the value of the index.
def correlation_of_frequencies(ciphertext, ciphertext_frequencies):
	correlations_arr = []
	for i in range(26):	# For each possible key value, 0-25
		correlation = 0
		for cipher_char in ciphertext:	# For each character in the ciphertext
			if cipher_char != " ":
				possible_plaintext_num = (letter_to_number[cipher_char] - i) % 26	# Calculate the possible plaintext character value for the hypothetical key, i
				possible_plaintext_char = list(letter_to_number.keys())[possible_plaintext_num]
				correlation += ciphertext_frequencies[cipher_char] * english_frequencies[possible_plaintext_num]	# Update the correlation value based on the formula f(c)f’(e – i)
		correlations_arr.append(correlation)
	return correlations_arr

# Returns the key with the highest correlation of frequencies.	
def get_probable_key(correlations_arr):
	probable_key = correlations_arr.index(max(correlations_arr))
	return probable_key

# Once the likely key has been determined, this function uses that key to find the plaintext.	
def decrypt_helper(ciphertext, key):
	plaintext = ""
	for character in ciphertext:
		if character != " ":
			char_val = letter_to_number[character]
			new_char_val = (char_val - key) % 26
			new_char = list(letter_to_number.keys())[new_char_val]
			plaintext += new_char
		else:	# Spaces are not affected by the key.
			plaintext += character
	return plaintext

# The "main" function for this program. Input: a string representing ciphertext. Output: prints the most likely key and plaintext.
def decrypt(ciphertext):
	# Calculate relative frequencies of letters in the ciphertext.
	ciphertext_length = len(ciphertext)
	ciphertext_frequencies = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}
	for char in ciphertext:
		if char != " ":
			ciphertext_frequencies[char] = ciphertext_frequencies[char] + 1 / ciphertext_length
	
	correlations_arr = correlation_of_frequencies(ciphertext, ciphertext_frequencies)	# Get an array of correlations of frequency.
	probable_key = get_probable_key(correlations_arr)	# Get the most likely key.
	print("Most likely key: " + str(probable_key))
	print("Most likely plaintext: " + decrypt_helper(ciphertext, probable_key))	# Perform the decryption using the key.
	

if len(sys.argv) < 2:
	print("Invalid arguments. Usage: python3 frequency_analyzer_caesar.py \"CIPHERTEXT\"")
else:
	ciphertext = sys.argv[1]
	decrypt(ciphertext.lower().strip())
