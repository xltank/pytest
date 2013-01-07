# coding: utf8
'''
Created on Jan 7, 2013

@author: xl
'''

from Tkinter import *

root = Tk()
# 创建两个Label
lb1 = Label(root,text = 'Hello')
lb2 = Label(root,text = 'Grid')

lb1.grid(row = 0, column = 0)
lb2.grid(row = 0, column = 1)

root.mainloop()