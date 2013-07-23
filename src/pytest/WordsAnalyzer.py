# coding: utf8
'''
Created on Dec 21, 2012

@author: xl
'''
import Tkinter
import tkFileDialog
import re
from collections import OrderedDict

def btnClickHandler():
    f = tkFileDialog.askopenfile('r', filetypes=[('txt', '*.txt'),('py','*.py')])
    wordList = []
    reg = re.compile(r'\b\w+-*\w*\b')
    for line in f:
        t = reg.findall(line)
        if(t):
            wordList.extend(t)
        
    print wordList
    
    wordDict = OrderedDict()
    for w in wordList:
        if w in wordDict:
            wordDict[w] += 1
        else:
            wordDict[w] = 1

    for k in wordDict:
        print k.center(10), wordDict[k]

stage = Tkinter.Tk()
btn = Tkinter.Button(stage, text='Browser...', command=btnClickHandler)
btn.pack()
Tkinter.mainloop()