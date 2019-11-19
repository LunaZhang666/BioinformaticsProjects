import sys
import re
with open(sys.argv[1],"r") as f:
    infile = f.readlines()
f.close()
t = '' # fna/faa
name = re.match(r'^.*[\.]',sys.argv[1]) # 只保留最后一个点之前的
if infile[0].startswith("@"): # fastq
    for c in infile[1]:
        if c in 'ATCGNatcgn\n':
            t = 'fna'
        else:
            t = 'faa' 
            break
    # name = re.match(r'^[A-z0-9]*[\.]',sys.argv[1]) # 保留第一个点之前的
    outfile = open('Luna_'+name.group(0)+t,"a+")
    for line in range(0,len(infile),4):
        outfile.write('>'+infile[line][1:])
        outfile.write(infile[line+1])

elif infile[0].startswith("#"): # mega updated Nov.4 and tested with files on gitlab
    if infile[3].startswith("#") and infile[4].startswith("#"): # interleaved
        context = {}
        for line in range(3,len(infile)):
            if infile[line] != "\n":
                l = infile[line].split(" ")
                l = [x for x in l if x != '']
                if l[0][1:] not in context.keys():
                    context[l[0][1:]] = l[1]
                elif l[0][1:] in context.keys():
                    context[l[0][1:]] += l[1]
        for key in context.keys():
            for c in context[key]:
                if c in 'ATCGNatcgn\n':
                    t = 'fna'
                else:
                    t = 'faa'
                    break
        outfile = open(name.group(0)+t,"a+")
        for key, value in context.items():
            outfile.write('>'+key+'\n')
            outfile.write(value) # keep sequence as-is
    else: # noninterleaved/sequential
        for c in infile[4]: 
            if c in 'ATCGNatcgn\n':
                t = 'fna'
            else:
                t = 'faa'
                break
        outfile = open(name.group(0)+t,"a+")
        for line in range(3,len(infile)): 
            if infile[line] == "\n":
                continue
            if infile[line].startswith("#"):
                outfile.write('>'+infile[line][1:])
            else:
                outfile.write(infile[line]) # keep sequence as-is

elif infile[0].startswith("I"): # embl worked with protein and nucleotide
    accid = []
    descrip = []
    seqs = []
    seqCharacter = re.compile(r'[A-z]')
    for l in infile:
        if l.startswith("ID"):
            accid += [l[5:].split(";")[0]]
            print (accid)
            de = ''
            seq = ''
        if l.startswith("DE"):
            de += l[5:-1]
        if l.startswith("  "):
            for x in l:
                if re.match(seqCharacter,x):
                    seq += x
        if l.startswith("//"):
            descrip += [de]
            seqs += [seq]
    for c in seq:
        if c in 'ATCGNatcgn':
            t = 'fna'
        else:
            t = 'faa' 
            break
    # name = re.match(r'^[A-z0-9]*[\.]',sys.argv[1])
    outfile = open('Luna_embl_'+name.group(0)+t,"a+")
    for i in range(len(accid)):
        outfile.write('>'+accid[i]+'|'+descrip[i][:-1]+'\n')
        outfile.write(seqs[i]+'\n') # sequence as one-liner; can break into any length if needed

elif infile[0].startswith("L"): # genebank worked with both protein and nucleotide
    accid = []
    definition = []
    seqs = []
    seqidentifier = re.compile(r'^[\s]+[0-9]+[\s]')
    seqCharacter = re.compile(r'[A-z]')
    for l in infile:
        if l.startswith("LOCUS"):
            de = ''
            seq = ''
        elif l.startswith("DEFINITION"):
            de += l[12:]
        elif l.startswith("VERSION"):
            accid += [l[12:-1]] 
        elif re.match(seqidentifier,l[:11]):
            for x in l:
                if re.match(seqCharacter,x):
                    seq += x
        elif l.startswith("//"):
            seqs += [seq]
            definition += [de]
    for c in seq:
        if c in 'ATCGNatcgn':
            t = 'fna'
        else:
            t = 'faa' 
            break
    # name = re.match(r'^[A-z0-9]*[\.]',sys.argv[1])
    outfile = open('Luna_gb_'+name.group(0)+t,"a+")
    for i in range(len(accid)):
        outfile.write('>'+accid[i]+'|'+definition[i])
        outfile.write(seqs[i]+'\n') # sequence as one-liner; can break into any length if needed

# mega改成不靠title区分