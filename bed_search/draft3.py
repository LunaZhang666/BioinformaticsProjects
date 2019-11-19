import time
starttime = time.time()
import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-j", help = "join the two entries",action="store_true")
parser.add_argument("-i1", help = "Input file 1")
parser.add_argument("-i2", help = "Input file 2")
parser.add_argument("-m", help = "INT: minimal overlap", type = int)
parser.add_argument("-o", help = "Output file")
args = parser.parse_args()

if args.o in os.listdir("."):
    os.remove(args.o)
# if 'log.txt' in os.listdir("."):
#     os.remove('log.txt')

def chai_chr(file):
    with open(file) as f:
        read = f.readlines()
    f.close()
    chai = {}
    for line in read:
        line = line.strip()
        line = line.split('\t')
        if line[0] not in chai.keys():
            chai[line[0]] = [line]
        else:
            chai[line[0]] += [line]
    return chai
target = chai_chr(args.i1) 
ref = chai_chr(args.i2)

def noJoverlap(chromo): 
    count = 0
    index_t = 0
    index_r = 0
    out = open(args.o,"a+")
    #log = open('log.txt',"a+")
    nextloop = '0'
    overlaped = 0 
    write2file = 0
    while index_t <= len(target[chromo])-1:
        if write2file == 1:
            index_t += 1
            write2file = 0
            if overlaped > 0:
                index_r = int(nextloop)
                overlaped = 0
        elif index_r >= len(ref[chromo]):
            index_r = int(nextloop)
            index_t += 1
            write2file = 0
        if index_r > len(ref[chromo])-1 or index_t > len(target[chromo])-1:
            break
        #log.write("comparing target "+'\t'.join(target[chromo][index_t])+" with reference "+'\t'.join(ref[chromo][index_r])+"\n")        
        if int(target[chromo][index_t][2]) < int(ref[chromo][index_r][1]) : # target 在 ref 前
            index_t += 1
            write2file = 0
            if overlaped > 0:
                index_r = int(nextloop)
                overlaped = 0
        elif int(target[chromo][index_t][1]) > int(ref[chromo][index_r][2]) : # target在 ref 后
            index_r += 1
        else:
            overlaped +=1
            if overlaped == 1:
                nextloop = str(index_r)
            if int(target[chromo][index_t][2]) >= int(ref[chromo][index_r][1]) and \
            int(target[chromo][index_t][2]) <= int(ref[chromo][index_r][2]) and \
            int(target[chromo][index_t][1]) >= int(ref[chromo][index_r][1]) and \
            int(target[chromo][index_t][1]) <= int(ref[chromo][index_r][2]) : # target 在 ref 中间
                percent = 100
                if percent >= args.m: # output each target once
                    out.write('\t'.join(target[chromo][index_t])+"\n")
                    count += 1
                    write2file = 1
                else:
                    index_r += 1
            elif int(target[chromo][index_t][1]) < int(ref[chromo][index_r][1]) and \
            int(target[chromo][index_t][2]) > int(ref[chromo][index_r][2]) : # target 在 ref 外面
                percent = ( (int(ref[chromo][index_r][2]) - int(ref[chromo][index_r][1])) / (int(target[chromo][index_t][2])-int(target[chromo][index_t][1])) )* 100
                if percent >= args.m: # output each target once
                    out.write('\t'.join(target[chromo][index_t])+"\n")
                    count += 1
                    write2file = 1
                else:
                    index_r += 1
            elif int(target[chromo][index_t][2]) >= int(ref[chromo][index_r][1]) and \
            int(target[chromo][index_t][2]) <= int(ref[chromo][index_r][2]) : # target 尾在 ref 里面
                percent = ((int(target[chromo][index_t][2]) - int(ref[chromo][index_r][1])) / (int(target[chromo][index_t][2])-int(target[chromo][index_t][1]))) * 100
                if percent >= args.m: # output each target once
                    out.write('\t'.join(target[chromo][index_t])+"\n")
                    count += 1
                    write2file = 1
                else:
                    index_r += 1
            elif int(target[chromo][index_t][1]) >= int(ref[chromo][index_r][1]) and \
            int(target[chromo][index_t][1]) <= int(ref[chromo][index_r][2]) : # target 头在 ref 里面
                percent =((  int(ref[chromo][index_r][2])  - int(target[chromo][index_t][1]) ) / (int(target[chromo][index_t][2])-int(target[chromo][index_t][1]))) * 100
                if percent >= args.m: # output each target once
                    out.write('\t'.join(target[chromo][index_t])+"\n")
                    count += 1
                    write2file = 1
                else:
                    index_r += 1
    out.close()
    return count

def joinoverlap(chromo):
    count = 0
    index_t = 0
    index_r = 0
    out = open(args.o,"a+")
    #log = open('log.txt',"a+")
    nextloop = '0'
    overlaped = 0 
    while index_t <= len(target[chromo])-1:
        if index_r >= len(ref[chromo]):
            index_r = int(nextloop)
            index_t += 1
        # elif index_t == len(target[chromo])-1 and index_r != len(ref[chromo])-2 and index_r != len(ref[chromo])-1:
        #     index_r += 1
        if index_r > len(ref[chromo])-1 or index_t > len(target[chromo])-1:
            break
        #log.write("comparing target "+'\t'.join(target[chromo][index_t])+" with reference "+'\t'.join(ref[chromo][index_r])+"\n")        
        if int(target[chromo][index_t][2]) < int(ref[chromo][index_r][1]): # target 在 ref 前
            index_t += 1
            if overlaped > 0:
                index_r = int(nextloop)
                overlaped = 0
        elif int(target[chromo][index_t][1]) > int(ref[chromo][index_r][2]) : # target在 ref 后
            index_r += 1
        else:
            overlaped +=1
            if overlaped == 1:
                nextloop = str(index_r)
            if int(target[chromo][index_t][2]) >= int(ref[chromo][index_r][1]) and \
            int(target[chromo][index_t][2]) <= int(ref[chromo][index_r][2]) and \
            int(target[chromo][index_t][1]) >= int(ref[chromo][index_r][1]) and \
            int(target[chromo][index_t][1]) <= int(ref[chromo][index_r][2]) : # target 在 ref 中间
                percent = 100
                if percent >= args.m:
                    out.write('\t'.join(target[chromo][index_t])+'\t'+'\t'.join(ref[chromo][index_r])+"\n")
                    count += 1
                index_r += 1
            elif int(target[chromo][index_t][1]) < int(ref[chromo][index_r][1]) and \
            int(target[chromo][index_t][2]) > int(ref[chromo][index_r][2]) : # target 在 ref 外面
                percent = ( (int(ref[chromo][index_r][2]) - int(ref[chromo][index_r][1])) / (int(target[chromo][index_t][2])-int(target[chromo][index_t][1])) )* 100
                if percent >= args.m:
                    out.write('\t'.join(target[chromo][index_t])+'\t'+'\t'.join(ref[chromo][index_r])+"\n")
                    count += 1
                index_r += 1
            elif int(target[chromo][index_t][2]) >= int(ref[chromo][index_r][1]) and \
            int(target[chromo][index_t][2]) <= int(ref[chromo][index_r][2]) : # target 尾在 ref 里面
                percent = ((int(target[chromo][index_t][2]) - int(ref[chromo][index_r][1])) / (int(target[chromo][index_t][2])-int(target[chromo][index_t][1]))) * 100
                if percent >= args.m:
                    out.write('\t'.join(target[chromo][index_t])+'\t'+'\t'.join(ref[chromo][index_r])+"\n")
                    count += 1
                index_r += 1 # t -> r
            elif int(target[chromo][index_t][1]) >= int(ref[chromo][index_r][1]) and \
            int(target[chromo][index_t][1]) <= int(ref[chromo][index_r][2]) : # target 头在 ref 里面
                percent =((  int(ref[chromo][index_r][2])  - int(target[chromo][index_t][1]) ) / (int(target[chromo][index_t][2])-int(target[chromo][index_t][1]))) * 100
                if percent >= args.m:
                    out.write('\t'.join(target[chromo][index_t])+'\t'+'\t'.join(ref[chromo][index_r])+"\n")
                    count += 1
                index_r += 1
    out.close()
    return count

total = 0
if args.j:
    for key in target.keys():
        if key in ref.keys(): # 想办法改成读取时判断
            print(key)
            total += joinoverlap(key)
            print("Total:", total)
else:
    for key in target.keys():
        if key in ref.keys(): # 想办法改成读取时判断
            print(key)
            total += noJoverlap(key)
            print("Total:", total)

# print(joinoverlap('chr12'))

print ("Times used:", time.time()-starttime)