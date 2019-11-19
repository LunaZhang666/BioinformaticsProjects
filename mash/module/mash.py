#!/usr/bin/env python
import random
from module.kmer_counter import *
import math
import os
import multiprocessing
import threading

k = 5
def Matrix(args): #if only -d is given 
	result = []
	files = os.listdir('./' + args.dir)
	prefix = './'+ args.dir + '/'
	files = [prefix + x for x in files if valid_name(x)]

	flag = 1
	if args.output is not None:
		flag = 0
		f_out = open(args.output, 'w')

	p = multiprocessing.Pool(args.threads)

	n = len(files)
	pos_d = {}
	dp = {}
	matrix = [['0.0' for _ in range(n)] for _ in range(n)]
	for row, file1 in enumerate(files):
		for col, file2 in enumerate(files):
			pos_d[(file1, file2)] = (row, col)
			if file1 == file2:
				dp[(file1, file2)] = [file1, file2, '0.0']
			elif (file1, file2) in dp or (file2, file1) in dp:
				result = dp[(file1, file2)]
				matrix[row][col] = result[2]
			else:
				results = p.map(multi_run_wrapper, [(file1, file2, args)])
				for result in results:
					file_row, file_col = pos_d[(result[0], result[1])]
					matrix[file_row][file_col] = result[2]
					dp[(result[0], result[1])] = result
					dp[(result[1], result[0])] = result
	row_header = []
	for file in files:
		row_header.append(file.replace(prefix, ''))

	if flag == 0:
		f_out.write('\t' + '\t'.join(row_header) + '\n')
	else:
		print('\t' + '\t'.join(row_header))

	for row, file1 in enumerate(files):
		if flag == 0:
			f_out.write(file1.replace(prefix, '') + '\t')
		else:
			print(file1.replace(prefix, '') + '\t'),
		for col, file2 in enumerate(files):	
			if flag == 0:
				f_out.write("{0}\t".format(matrix[row][col]))
			else:
				if col != n - 1:
					print(matrix[row][col] + '\t'),
				else:
					print(matrix[row][col] + '\t')
		if flag == 0:
			f_out.write('\n')
	p.close()


def single_pair(file_a, file_b, args):
	result = process(file_a, file_b, args)

	if args.output is None:
		print('{0}\t{1}\t{2}'.format(result[0], result[1], result[2]))
	else:
		with open(args.output, 'w') as f_out:
			f_out.write('{0}\t{1}\t{2}\n'.format(result[0], result[1], result[2]))

def multi_run_wrapper(args):
   return process(*args)

def process(file_a, file_b, args):
	list_kmer_A = kmer(file_a, k)
	list_kmer_B = kmer(file_b, k)
	# print(list_kmer_A)
	mash_dis = mash_distance(list_kmer_A, list_kmer_B, args)
	# print(file_a + file_b + mash_dis)
	result = [file_a, file_b, mash_dis]
	# result = file_a + '\t' + file_b +'\t' + mash_dis +'\n'
	return result

def valid_name(x):
	return '.fasta' in x or '.fna' in x or '.fas' in x
def all_against_a(args):
	result = []
	files = os.listdir('./' + args.dir)
	prefix = './'+ args.dir + '/'
	files = [prefix + x for x in files if valid_name(x)]

	flag = 1
	if args.output is not None:
		flag = 0
		f_out = open(args.output, 'w')

	p = multiprocessing.Pool(args.threads)

	for file in files:
		results = p.map(multi_run_wrapper, [(args.file_a, file, args)])
		for result in results:
			if flag == 0:
				f_out.write('{0}\t{1}\t{2}\n'.format(result[0], result[1].replace(prefix, ''), result[2]))
			else:
				print('{0}\t{1}\t{2}'.format(result[0], result[1].replace(prefix, ''), result[2]))
	p.close()


def mash_distance(list_A, list_B, args):

	random.Random(args.seed).shuffle(list_A)
	random.Random(args.seed).shuffle(list_B)
	set_A = list_A[:args.setsize]
	set_B = list_B[:args.setsize]
	d_A = list_to_d(set_A)
	d_B = list_to_d(set_B)
	Union, Inter = Union_Intersection(d_A, d_B)
	Union_count = 0.0
	Inter_count = 0.0
	for key, value in Union.items():
		Union_count += value
	for key, value in Inter.items():
		Inter_count += value
	# print(Union_count, Inter_count)
	J_dis = 1.0 - float(1.0 * Inter_count / Union_count)
	# print(J_dis)
	# print(round(-1/k * math.log(2.0 * J_dis /(1.0+J_dis)), 2))
	if int(J_dis) == 0:
		Mash_dis = 0.00
	else: 
		Mash_dis = round((-1.0/k) * math.log(2.0 * J_dis /(1.0 + J_dis)), 2)
	# print(Mash_dis)
	return str(Mash_dis)

def list_to_d(list_a):
	d_a = {}
	for value in list_a:
		if value not in d_a:
			d_a[value] = 1
		else:
			d_a[value] += 1
	return d_a

def Union_Intersection(d_A, d_B):
	Union = {}
	Inter = {}
	for key, value in d_A.items():
		if key in d_B:
			Union[key], Inter[key] = max(d_A[key],d_B[key]), min(d_A[key],d_B[key])
			d_A[key], d_B[key] = 0, 0
		else:
			Union[key] = d_A[key]
			d_A[key] = 0

	for key, value in d_B.items():
		if value != 0 :
			Union[key] = value
	return Union, Inter


def check_fasta(file):
	with open(file, 'r') as f:
		count = 0
		for index, line in enumerate(f):
			if index == 0 and line[0] != '>':
				return False
			else:
				return True