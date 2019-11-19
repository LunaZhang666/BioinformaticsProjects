#!/usr/bin/env python
import sys
import re
import os
import random
import argparse
import multiprocessing
import threading

from module.kmer_counter import kmer
from module.mash import *

def main():
	global args
	parser = argparse.ArgumentParser()
	parser.add_argument("-a", "--file_a", type = str, nargs='?', help = " An input genome")
	parser.add_argument("-b", "--file_b", type = str, nargs='?', help = " Another input genome")
	parser.add_argument("-d", "--dir", type = str, nargs='?', help = " Directory containing input genomes files")
	parser.add_argument("-s", "--setsize", type = int, default=1000, help = " Number of random kmers to evaluates, default to 1000")
	parser.add_argument("-S", "--seed", type = int, default=100, help = " Seed value for random set generation")
	parser.add_argument("-o", "--output", action="append", type = str, nargs='?', help = " Output file namegs")
	parser.add_argument("-t", "--threads", type = int, default=1, help = " Number of theads/processes to run the analysis, defaults to 1")
	parser.add_argument("-v", "--verbose", action="store_true", default=False, help = "Verbose mode")
	parser.add_argument("-f", "--force", action="store_true", default=False, help = "Overwrite files if they exist. Do not overwrite by default")
	args  = parser.parse_args()


def check_arg():



	if not args.force: # no -f, do not overwrite
		# if args.output == None:
		# 	raise Exception("Please wirte output file name")
		if args.output == [None]:
			if os.path.isfile('geneDist_output.txt'):
				raise Exception('Output file already exists.')
			else: # save file as default name
				args.output = 'geneDist_output.txt'
		else:
			if args.output is not None and os.path.isfile(''.join(args.output)):
				raise Exception('Output file already exists.')		
	else:
		if args.output == None:
			raise Exception("Please wirte output file name")
		if args.output == [None]:
			args.output = 'geneDist_output.txt'
	
	if args.output is not None and not type(args.output) == str:
		args.output = ''.join(args.output)
	
	if args.threads < 0:
		raise Exception("Invalid thread value")


	if args.file_a is not None: # -a true
		if not args.file_b and not args.dir:
			raise Exception("Missing one input sequence")
		elif args.file_b and args.dir:
			raise Exception("Invalid multiple input")
		elif args.file_b:
			single_pair(args.file_a, args.file_b, args)
		elif args.dir:
			if os.path.isdir('./'+ args.dir) is False:
				raise Exception("No such directory")
			else:
				all_against_a(args)
	else: # no a
		if args.file_b is None and args.dir is None:
			raise Exception("Missing two inputs")
		if args.file_b and args.dir is None:
			raise Exception("Missing one input sequence")
		if args.file_b is None and args.dir is not None:
			if os.path.isdir('./'+ args.dir) is False:
				raise Exception("No such directory")
			else:
				Matrix(args)


if __name__ == "__main__":
	main()
	check_arg()

#./genomeDist.py -a A.fasta -b B.fasta -o geneDist_output.txt -s 100
#./genomeDist.py -a A.fasta -d file -o a_verse_dir.txt -t 10
# ./genomeDist.py -a A.fasta -d file -o a_verse_dir.txt -t 10
# ./genomeDist.py -a A.fasta -d file -o a_verse_dir.txt -t 10 -f
#./genomeDist.py -d file -o geneDist_output.txt -t 100 -s 100 -f

