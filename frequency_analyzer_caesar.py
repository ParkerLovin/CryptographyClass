#!/usr/bin/python3

import sys


letter_to_number = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25}

english_frequencies = [0.08, 0.015, 0.03, 0.04, 0.13, 0.02, 0.015, 0.06, 0.065, 0.005, 0.005, 0.035, 0.03, 0.07, 0.08, 0.02, 0.002, 0.065, 0.06, 0.09, 0.03, 0.01, 0.015, 0.005, 0.02, 0.002]
#english_frequencies = {'a': 0.08, 'b': 0.015, 'c': 0.03, 'd': 0.04, 'e': 0.13, 'f': 0.02, 'g': 0.015, 'h': 0.06, 'i': 0.065, 'j': 0.005, 'k': 0.005, 'l': 0.035, 'm': 0.03, 'n': 0.07, 'o': 0.08, 'p': 0.02, 'q': 0.002, 'r': 0.065, 's': 0.06, 't': 0.09, 'u': 0.03, 'v': 0.01, 'w': 0.015, 'x': 0.005, 'y': 0.02, 'z': 0.002}

def correlation_of_frequencies(ciphertext, ciphertext_frequencies):
	correlations_arr = []
	for i in range(26):
		correlation = 0
		for j in range(len(ciphertext)):
			if ciphertext[j] != " ":
				possible_plaintext_num = (letter_to_number[ciphertext[j]] - i) % 26
				possible_plaintext_char = list(letter_to_number.keys())[possible_plaintext_num]
				correlation += ciphertext_frequencies[ciphertext[j]] * english_frequencies[possible_plaintext_num]
		correlations_arr.append(correlation)
	return correlations_arr
	
def get_probable_key(correlations_arr):
	probable_key = correlations_arr.index(max(correlations_arr))
	return probable_key
	
def decrypt_helper(ciphertext, key):
	plaintext = ""
	for character in ciphertext:
		if character != " ":
			char_val = letter_to_number[character]
			new_char_val = (char_val - key) % 26
			new_char = list(letter_to_number.keys())[new_char_val]
			plaintext += new_char
		else:
			plaintext += character
	return plaintext

def decrypt(ciphertext):
	ciphertext_length = len(ciphertext)
	ciphertext_frequencies = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}
	#ciphertext_frequencies = []
	#for i in range(26):
	#	ciphertext_frequencies.append(0)
	#print("Temp: " + str(len(ciphertext_frequencies)))
	for char in ciphertext:
		if char != " ":
			ciphertext_frequencies[char] = ciphertext_frequencies[char] + 1 / ciphertext_length
	#print(ciphertext_frequencies)
	correlations_arr = correlation_of_frequencies(ciphertext, ciphertext_frequencies)
	probable_key = get_probable_key(correlations_arr)
	print("Most likely key: " + str(probable_key))
	print("Most likely plaintext: " + decrypt_helper(ciphertext, probable_key))
	

if len(sys.argv) < 2:
	print("Invalid arguments. Usage: python3 frequency_analyzer_caesar.py CIPHERTEXT")
else:
	ciphertext = sys.argv[1]
	decrypt(ciphertext.lower().strip())
