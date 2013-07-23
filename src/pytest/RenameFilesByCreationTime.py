# coding: utf8
"""
Created on 2012-12-21

@author: VTX
"""
import os
import operator
from genericpath import getctime

rootDir = r"E:\pyTest"

os.chdir(rootDir)
dirs = os.listdir(rootDir)
for i in dirs:
    os.chdir(os.path.join(rootDir, i))
    subs = os.listdir(os.getcwd())
#    print subs
    fileList = []
    for f in subs:
        creaTime = getctime(f)
        obj = {"name":f, "creaTime":creaTime}
        fileList.append(obj)
    fileList.sort(key=operator.itemgetter('creaTime'))
    print fileList
    ind = 0
    for fn in fileList:
        os.rename(fn['name'], str(ind) + os.path.splitext(fn['name'])[1])
        ind += 1




