# coding:gbk
'''
Created on 2012-12-27

@author: VTX

1082    1    33    徐立              1    0    2012/4/9 18:47        

'''

import os
from xlwt import Workbook, Worksheet
from timeRecMod import *
from operator import attrgetter
import Tkinter
import tkFileDialog
import string
import sys


fName = ''


def getRecords(logName):
    if(not os.path.exists(logName)):
        setLog(logName + ' not exists!')
        return

    results = []
    f = open(logName, 'r')
    for r in f:
        if(r.count(monthStr) > 0):
            recTuple = fromString(r)
            results.append(DayRecord(recTuple[0], recTuple[1], recTuple[2], recTuple[3]))
    setLog('all records num: ' + str(len(results)))
    results.sort(key=attrgetter('userId'), reverse=False)
    return results


def fromString(s):
    s = s.strip()
    lis = s.split('\t')
    return lis[0], lis[2], unicode(lis[3]), lis[6]


def orgnizeRecord(lis):
    results = []
    curUser = UserRecord()
    for a in lis:
        if(a.userId != curUser.userId):
            curUser = UserRecord(a.userId, a.userName)
            results.append(curUser)
        dayIndex = string.atoi(a.time[:10].split('/')[2])
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
    for i, s in enumerate(titles):  # write header
        sheet1.write(0, i, str(s))
    rowNum += 1

    for a in lis:
        for colNum, colName in enumerate(titles):
            if(colNum == 0):
                sheet1.write_merge(rowNum, rowNum + 1, colNum, colNum, a.userId)
            elif(colNum == 1):
                sheet1.write_merge(rowNum, rowNum + 1, colNum, colNum, a.userName)
            else:
                onTime = ''
                offTime = ''
                if(colNum in a.recDict):
                    times = a.recDict[colNum]
                    if(len(times) >= 2):
                        if(len(times) > 2):
                            setLog('!! ' + a.userName + ' ' + str(times))
                        onTime = times[0]
                        offTime = times[len(times) - 1]
                    elif(len(times) == 1):
                        if(times[0].split(' ')[1] < divider):
                            onTime = times[0]
                        else:
                            offTime = times[0]

                if(onTime):
                    onTime = onTime.split(' ').pop()[:5]
                if(offTime):
                    offTime = offTime.split(' ').pop()[:5]
                sheet1.write(rowNum, colNum, onTime)
                sheet1.write(rowNum + 1, colNum, offTime)

        rowNum += 2

#    if(not os.path.exists('result.xls')):
    wb.save('result.xls')


def startUp():
    if(workday.get() < 0 or workday.get() > 31):
        print 'invalid workday number'
        return
    if(not fName):
        print 'please select a file'
        return
    
    os.chdir(os.path.split(unicode(fName))[0])
    records = orgnizeRecord(getRecords(fName))
    setLog('User Num: ' + str(len(records)))
    genTotalSheet(records)


def getFile():
    try:
        f = tkFileDialog.askopenfile()
    except Exception, e:
        print e
    global fName
    fName = f.name
    

def setLog(msg):
    print msg
    labelText.set(labelText.get() + msg + '\n')


def workdayChanged(*args):
#    print args
    print workday




reload(sys)
sys.setdefaultencoding('gbk')

monthStr = '2012/11/'
userIdTitle = u'编号'
nameTitle = u'姓名'
dayNum = 30
divider = '12:00'
totalSheetName = u'概览表'

titles = (userIdTitle, nameTitle) + tuple(range(1, dayNum + 1))

stage = Tkinter.Tk()
stage.title('xuli')
stage.geometry('300x300')

btnBrowse = Tkinter.Button(stage, text='选择文件', command=getFile)
btnBrowse.pack()

btnStart = Tkinter.Button(stage, text='开始', command=startUp)
btnStart.pack()

lbWorkday = Tkinter.Entry(stage, text='本月工作天数: ')
lbWorkday['state'] = 'readonly'
lbWorkday.pack()

workday = Tkinter.IntVar()
workdayInput = Tkinter.Entry(stage, textvariable=workday)
workday.trace('w', workdayChanged)
workdayInput.pack()

labelText = Tkinter.StringVar()
label = Tkinter.Label(stage, textvariable=labelText, width='300', justify='left', anchor='w')
label.pack()
Tkinter.mainloop()
