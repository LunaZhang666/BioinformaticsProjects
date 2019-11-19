import sys
def onelineseq(file):
    fasta = open(file).readlines()[1:]
    seq = []
    for i in fasta:
        seq.append(i.replace('\n',''))
    seq = ''.join(seq)
    return seq
seq2=onelineseq(sys.argv[1])
seq1=onelineseq(sys.argv[2])
m = [[0 for x in range(len(seq2)+1)] for y in range(len(seq1)+1)]
d = [[0 for x in range(len(seq2)+1)] for y in range(len(seq1)+1)]

for i in range(1,len(m[0])): #first line
    m[0][i]=-i
for j in range(1,len(m)): #first column
    m[j][0]=-j

def cell_score(ri,ci):
    dofscore = [0,[]]
    u = m[ri-1][ci]-1
    l = m[ri][ci-1]-1
    if seq1[ri-1] == seq2[ci-1]:
        ul = m[ri-1][ci-1]+1
    if seq1[ri-1] != seq2[ci-1]:
        ul = m[ri-1][ci-1]-1
    if max(u,l,ul) == ul:
        dofscore[0] = ul
        dofscore[1] += ri-1, ci-1
    elif max(u,l,ul) == u:
        dofscore[0] = u
        dofscore[1] += ri-1, ci
    elif max(u,l,ul) == l:
        dofscore[0] = l
        dofscore[1] += ri, ci-1
    return dofscore
for r in range(1,len(m)):
    for c in range(1,len(m[0])):
        m[r][c] = cell_score(r,c)[0]
        d[r][c] = cell_score(r,c)[1]
#trace back
h=len(m)-1
s=len(m[0])-1
align = ''
seq1a = ''
seq2a = ''
while h>0 or s>0:
    if d[h][s] == [h-1,s-1] and seq2[s-1] == seq1[h-1]: #match
        align += "|"
        seq2a += seq2[s-1]
        seq1a += seq1[h-1]
        h-=1
        s-=1
    elif d[h][s] == [h-1,s-1] and seq2[s-1] != seq1[h-1]: #mis
        align += " "
        seq2a += seq2[s-1]
        seq1a += seq1[h-1]
        h-=1
        s-=1
    elif d[h][s] == [h-1,s]: #up
        align += " "
        seq2a += "-"
        seq1a += seq1[h-1]
        h-=1
    elif d[h][s] == [h,s-1]: #left
        align += " "
        seq2a += seq2[s-1]
        seq1a += "-"
        s-=1
    elif d[h][s] == 0: # either h or s reaches 0 first
        if s == 0:
            align += " "
            seq1a += seq1[h-1]
            seq2a += "-"
            h-=1
        elif h == 0:
            align += " "
            seq2a += seq2[s-1]
            seq1a += "-"
            s-=1

print (seq2a[::-1])
print (align[::-1])
print (seq1a[::-1])
score = align.count("|") - align.count(" ")
print ("Alignment score:", score)