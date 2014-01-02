# use: python targetString test.log
# open target txt file, grab lines which contains targetString and save them in a txt file.

import sys

args = sys.argv
print len(args)
#for arg in args:
#    print arg
    
f = open(args[2])
result = ""
for line in f:
    if line.find(args[1]) != -1 :
        result += line
        
target = open("target_"+args[1]+".txt", "w")
target.writelines(result)
target.flush()
target.close()