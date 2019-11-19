#!/usr/bin/env python3

'''
Module to find reciprocal hits in a blast search.
'''

from blast_utilities.blast_wrapper import run_blast

import sys
file_one = sys.argv[1]
file_two = sys.argv[2]
input_sequence_type = sys.argv[3]

def list_file(file):
    with open(file) as f:
        read = f.readlines()
    f.close()
    new = []
    last_line = ['san','ge','da','gou','bi']
    for line in read:
        line = line.strip()
        line = line.split('\t')
        if line[0] != last_line[0]:
            new.append(line[:2])
            last_line = line
    return new

def get_reciprocal_hits(file1,file2,seq_type):
    result = []
    fileOne = list_file(run_blast(file1,file2,seq_type))
    fileTwo = list_file(run_blast(file2,file1,seq_type))
    # for l2 in fileTwo: #output file 2
    #     for l1 in fileOne:
    #         if l1[0] == l2[1] and l1[1] == l2[0]:
    #             newline =  '\t'.join(l2)
    #             newline_flip = '\t'.join(l2[::-1])
    #             if newline not in result and newline_flip not in result:
    #                 result.append(newline)
    for l1 in fileOne: #output file 1
        for l2 in fileTwo:
            if l1[0] == l2[1] and l1[1] == l2[0]:
                newline =  '\t'.join(l1)
                newline_flip = '\t'.join(l1[::-1])
                if newline not in result and newline_flip not in result:
                    result.append(newline)
    return result

