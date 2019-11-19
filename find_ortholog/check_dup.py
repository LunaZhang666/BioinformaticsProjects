import sys
with open(sys.argv[1],'r') as f:
    repeative = f.readlines()
f.close()

outputline = 'caonixiema'
ct = 0
rep = 0
for line in repeative:
    if line != outputline:
        ct += 1
        outputline = line
    else :
        rep += 1
        print (line)
print (ct,"unique")
print (rep, "duplicated")