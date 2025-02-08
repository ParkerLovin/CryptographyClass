#!/usr/bin/python3
import sys

def check_for_copies(ciphertext, substring_size):
	matches = {}
	for i in range(0, len(ciphertext) - substring_size + 1):
		substring = ciphertext[i:i+substring_size]
		positions = []
		start = i
		while True:
			start = ciphertext.find(substring, start)
			if start == -1:
				break
			positions.append(start)
			start += substring_size
		if len(positions) > 1:
			matches[substring] = positions
	print(matches)

def decrypt(ciphertext):
	check_for_copies(ciphertext, 2)

if len(sys.argv) < 2:
        print("Invalid arguments. Usage: python3 frequency_analyzer_vigenere.py \"CIPHERTEXT\"")
else:
        ciphertext = sys.argv[1]
        decrypt(ciphertext.lower().strip())
