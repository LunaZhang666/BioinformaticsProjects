#!/usr/bin/env python3

'''
Define different blast wrapper functions here.
'''

# Add your code here

import subprocess
import os
import sys

if 'tmp' not in os.listdir():
    os.mkdir('tmp')


def get_file_PathName(argument):
    path, filename = os.path.split(argument)
    return [path,filename]

file_one = sys.argv[1]
file_two = sys.argv[2]
input_sequence_type = sys.argv[3]

def run_blast(query,subj,seq_type):
    inputPath = get_file_PathName(query)[0]+'/'
    queryName = get_file_PathName(query)[1]
    subjName = get_file_PathName(subj)[1]
    db = './tmp/db_'+subjName
    result = './tmp/'+queryName+'vs'+subjName+'.out'
    if seq_type == 'n':
        subprocess.run(['makeblastdb','-in',inputPath+subjName,'-dbtype','nucl','-out',db])
        subprocess.run(['blastn','-db',db,'-query',inputPath+queryName,'-out',result,'-max_target_seqs','1','-outfmt','6'])
    elif seq_type == 'p':
        subprocess.run(['makeblastdb','-in',inputPath+subjName,'-dbtype','prot','-out',db])
        subprocess.run(['blastp','-db',db,'-query',inputPath+queryName,'-out',result,'-max_target_seqs','1','-outfmt','6'])
    return result


# command line examples
# makeblastdb -in <./input_files/testSpeciesA.fasta> -dbtype <nucl> -out <dbA>
# makeblastdb -in ./input_files/testSpeciesB.fasta -dbtype nucl -out dbB
# blastn -db dbB -query ./input_files/testSpeciesA.fasta -out testoutput_AinB.txt -max_target_seqs 1 -outfmt 6
# blastn -db dbA -query ./input_files/testSpeciesB.fasta -out testoutput_BinA.txt -max_target_seqs 1 -outfmt 6