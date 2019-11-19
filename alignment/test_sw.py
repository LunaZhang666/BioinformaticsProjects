# seq1='GTAACTCCCCTTCTGGCCGG' # horizontal
# seq2='CTCTCATCATACACCACTTC' # vertical
import sys
def onelineseq(file):
    fasta = open(file).readlines()[1:]
    seq = []
    for i in fasta:
        seq.append(i.replace('\n',''))
    seq = ''.join(seq)
    return seq
seq1=onelineseq(sys.argv[1])
seq2=onelineseq(sys.argv[2])
m = [[0 for x in range(len(seq1)+1)] for y in range(len(seq2)+1)]
d = [[0 for x in range(len(seq1)+1)] for y in range(len(seq2)+1)]

for i in range(1,len(m[0])): #first line
    m[0][i]=0
for j in range(1,len(m)): #first column
    m[j][0]=0

def cell_score(ri,ci): # if tie occurs, pick the highest origin by consider ul > u > l
    dofscore = [0,[]]
    u = m[ri-1][ci]-1
    l = m[ri][ci-1]-1
    if seq1[ci-1] == seq2[ri-1]:
        ul = m[ri-1][ci-1]+1
    if seq1[ci-1] != seq2[ri-1]:
        ul = m[ri-1][ci-1]-1
    if max(u,l,ul) < 0: # write 0 if negative score are calculated
        dofscore[0] = 0
        dofscore[1] += 0, 0
    elif ul >= u and ul >= l: # ul being highest score or tie
        dofscore[0] = ul
        dofscore[1] += ri-1, ci-1
    elif u >= ul and u >= l: # u being highest score or tie
        dofscore[0] = u
        dofscore[1] += ri-1, ci
    elif l >= ul and l >= u: # l being highest score or tie
        dofscore[0] = l
        dofscore[1] += ri, ci-1
    # elif ul == u :
    #     if m[ri-1][ci-1] > m[ri-1][ci]: # ul origin has higher score -> ul
    #         dofscore[0] = ul
    #         dofscore[1] += ri-1, ci-1
    #     elif m[ri-1][ci-1] <= m[ri-1][ci]: # u origin has higher score -> u
    #         dofscore[0] = u
    #         dofscore[1] += ri-1, ci
    # elif ul == l :
    #     if m[ri-1][ci-1] > m[ri][ci-1]: # ul origin has higher score -> ul
    #         dofscore[0] = ul
    #         dofscore[1] += ri-1, ci-1
    #     elif m[ri-1][ci-1] <= m[ri][ci-1]: # l origin has higher score -> l
    #         dofscore[0] = l
    #         dofscore[1] += ri, ci-1
    # elif u == l :
    #     if m[ri-1][ci] > m[ri][ci-1] : # u origin has higher score -> u
    #         dofscore[0] = u
    #         dofscore[1] += ri-1, ci
    #     elif m[ri-1][ci] <= m[ri][ci-1] : # l origin has higer score -> l
    #         dofscore[0] = l
    #         dofscore[1] += ri, ci-1
    return dofscore



scores={}
highest = [-9,[-9,-9]] # 1)assign score to each cell 2)keep track of max score
for r in range(1,len(m)):
    for c in range(1,len(m[0])):
        m[r][c] = cell_score(r,c)[0]
        d[r][c] = cell_score(r,c)[1]
        if cell_score(r,c)[0] > highest[0]:
            highest[0] = cell_score(r,c)[0]
            scores[cell_score(r,c)[0]] = [[r,c]]
        elif cell_score(r,c)[0] >= highest[0]:
            scores[cell_score(r,c)[0]] += [[r,c]]

# print (scores)
# for i in (m):
#     print (i)
# print (" ")
# for i in (d):
#     print (i)
# print ("Back tracing starts at:",start)

# back tracing
align = ['']*len(scores[max(scores.keys())])
seq1a = ['']*len(scores[max(scores.keys())])
seq2a = ['']*len(scores[max(scores.keys())])
count = 0
for point in scores[max(scores.keys())]:
    h = point[0]
    s = point[1]
    while h>0 or s>0:
        if m[h][s] == 0:
            break
        if d[h][s] == [h-1,s-1] and seq1[s-1] == seq2[h-1]: #match
            align[count] += "|"
            seq1a[count] += seq1[s-1]
            seq2a[count] += seq2[h-1]
            h-=1
            s-=1
        elif d[h][s] == [h-1,s-1] and seq1[s-1] != seq2[h-1]: #mis
            align[count] += " "
            seq1a[count] += seq1[s-1]
            seq2a[count] += seq2[h-1]
            h-=1
            s-=1
        elif d[h][s] == [h-1,s]: #up
            align[count] += " "
            seq1a[count] += "-"
            seq2a[count] += seq2[h-1]
            h-=1
        elif d[h][s] == [h,s-1]: #left
            align[count] += " "
            seq1a[count] += seq1[s-1]
            seq2a[count] += "-"
            s-=1
    count+=1

# print (seq1a)
# print (align)
# print (seq2a)

def longest(aligns):
    long = ''
    if len(aligns)-1 == 0 :
        return aligns[0]
    for i in range(len(aligns)):
        if len(aligns[i]) > len(long):
            long = aligns[i]
    return long

print (longest(seq1a)[::-1])
print (longest(align)[::-1])
print (longest(seq2a)[::-1])
score = longest(align).count("|") - longest(align).count(" ")
print ("Alignment score:", score)

# same as cmm
# direction priority 