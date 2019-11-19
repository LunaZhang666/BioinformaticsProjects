#!/usr/bin/env python

def kmer(file, int_k):
	k_mer = []
	# print(file)
	# print(int_k)
	with open(file, mode='r') as input_file:
		sequence = ""
		for index,line in enumerate(input_file):
			if index == 0: continue
			line_temp = line[:-1]

			sequence += line_temp
		
		s = ""
		d = { 'A':'T', 'T':'A', 'C':'G', 'G':'C'}
		for i in range(len(sequence)-int_k+1):
			s = sequence[i:i+int_k].upper()
			reverse_s = ''.join([d[x] for x in s]) #加一个reverse的function 
			if s < reverse_s: 
				k_mer.append(s)
			else:
				k_mer.append(reverse_s)
		k_mer.sort()
	
	return k_mer
	
