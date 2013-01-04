# coding:gbk
'''
Created on 2012-12-27

@author: VTX

1082    1    33    徐立              1    0    2012/4/9 18:47        

'''

import os
from xlwt import Workbook, Worksheet
from timeRecMod import UserRecord, DayRecord
from xlwt.Workbook import Workbook
from operator import attrgetter
import Tkinter
import tkFileDialog
from Tkinter import StringVar


def getRecords(logName):
    if(not os.path.exists(logName)):
        setLog(logName+' not exists!')
        return
    
    results = []
    f = open(logName, 'r')
    for r in f:
        if(unicode(r).count(monthStr)  > 0):
            recTuple = fromString(unicode(r))
            results.append(DayRecord(recTuple[0],recTuple[1],recTuple[2],recTuple[3]))
    setLog('all records num: '+str(len(results)))
    results.sort(key=attrgetter('userId'), reverse=False)
    return results
    
    
def fromString(s):
    s = s.strip().replace('  ', '')
    lis = unicode(s).split('\t')
    return lis[0], lis[2], lis[3], lis[6]


def orgnizeRecord(lis):
    results = []
    curUser = UserRecord()
    for a in lis:
        if(a.userId != curUser.userId):
            curUser = UserRecord(a.userId, a.userName)
            results.append(curUser)
        dayIndex = a.time.split(' ')[0].split('/')[2]
        if(dayIndex not in curUser.recDict):
            curUser.recDict[dayIndex] = [a.time]
        else:
            curUser.recDict[dayIndex].append(a.time)
    
    results.sort(key=attrgetter('userId'), reverse=False)
    return results
                

def genTotalSheet(lis):
    wb = Workbook(encoding='gbk')
    sheet1 = wb.add_sheet(totalSheetName, True)
    rowNum = 0
    for i, s in enumerate(titles): # write header
        sheet1.write(0, i, str(s))
    rowNum +=1
    
    for a in lis:
        for colNum, colName in enumerate(titles):
            if(colNum == 0):
                sheet1.write_merge(rowNum, rowNum+1, colNum, colNum, a.userId)
            elif(colNum == 1):
                sheet1.write_merge(rowNum, rowNum+1, colNum, colNum, a.userName)
            else:
                onTime = ''
                offTime = ''
                if(str(colName) in a.recDict):
                    times = a.recDict[str(colName)]
                    if(len(times) >= 2):
                        if(len(times) > 2):
                            setLog('!! ' + a.userName+' '+str(times))
                        onTime = times[0]
                        offTime = times[len(times)-1]
                    elif(len(times) == 1):
                        if(times[0].split(' ')[1] < divider):
                            onTime = times[0]
                        else:
                            offTime = times[0]
                            
                if(onTime):
                    onTime = onTime.split(' ')[1]
                if(offTime):
                    offTime = offTime.split(' ')[1]
                sheet1.write(rowNum, colNum, onTime)
                sheet1.write(rowNum+1, colNum, offTime)
        
        rowNum += 2
    
#    if(not os.path.exists('result.xls')):
    wb.save('result.xls')


def startUp():
    f = tkFileDialog.askopenfile()
    srcFile = f.name
    os.chdir(os.path.split(unicode(srcFile))[0])
    
    records = orgnizeRecord(getRecords(srcFile))
    setLog('User Num: '+str(len(records)))
    genTotalSheet(records)
    

def setLog(msg):
    print msg
    labelText.set(labelText.get() + msg+'\n')


monthStr = '2012/11/'
userIdTitle = u'编号'
nameTitle = u'姓名'
dayNum = 30
divider = '12:00'
totalSheetName = u'概览表'

titles = (userIdTitle, nameTitle) + tuple(range(1, dayNum+1))

stage = Tkinter.Tk()
stage.title('xuli')
stage.geometry('300x300')
btn = Tkinter.Button(stage, text='选择文件', command=startUp)
btn.pack()
labelText = StringVar()
label = Tkinter.Label(stage, textvariable=labelText, width='300', justify='left', anchor='w')
label.pack()
Tkinter.mainloop()

    
