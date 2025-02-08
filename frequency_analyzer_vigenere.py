#!/usr/bin/python3
import sys

def check_for_copies(ciphertext, substring_size, matches_dict):
	for i in range(0, len(ciphertext) - substring_size + 1):
		substring = ciphertext[i:i+substring_size]
		if not substring in list(matches_dict.keys()):	# Prevents unnecessarily checking for the same substring in multiple iterations.
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

def decrypt(ciphertext):
	matches = {}
	for i in range(4, 1, -1):
		matches = check_for_copies(ciphertext, i, matches)
	print(matches)

if len(sys.argv) < 2:
        print("Invalid arguments. Usage: python3 frequency_analyzer_vigenere.py \"CIPHERTEXT\"")
else:
        ciphertext = sys.argv[1]
        decrypt(ciphertext.lower().strip())
