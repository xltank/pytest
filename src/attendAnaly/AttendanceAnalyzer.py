# coding:gbk
'''
Created on 2012-12-27

@author: VTX

1082    1    33    徐立              1    0    2012/4/9 9:9        
or
1082    1    0000000033    徐立              1    0    2012/04/09 09:09        

'''

import os
from xlwt import Workbook
from timeRecMod import *
from operator import attrgetter
import Tkinter
import tkFileDialog
import sys
from xlwt.Style import XFStyle
from datetime import datetime
from xlwt.Formatting import Font


fName = ''


def getRecords(logName):
    results = []
    f = open(logName, 'r')
    for r in f:
        if(r.count(monthStr) > 0):
            recTuple = fromString(r)
            results.append(DayRecord(recTuple[0], recTuple[1], recTuple[2], recTuple[3]))
    addLog('all records num: ' + str(len(results)))
    results.sort(key=attrgetter('userId'), reverse=False)
    return results


def fromString(s):
    s = s.strip()
    lis = s.split('\t')
    return lis[0], lis[2], unicode(lis[3]), lis[6]

# lis is DayRecord list
def orgnizeRecord(lis):
    results = []
    curUser = UserRecord()
    for a in lis:
        if(a.userId != curUser.userId):
            curUser = UserRecord(a.userId, a.userName)
            results.append(curUser)
        dayIndex = int(a.time[:10].split('/')[2])
        if(dayIndex not in curUser.recDict):
            curUser.recDict[dayIndex] = [a.time]
        else:
            curUser.recDict[dayIndex].append(a.time)

    results.sort(key=attrgetter('userId'), reverse=False)
    return results

# lis is UserRecord list
def genTotalSheet(lis):
    timeStyle = XFStyle()
    timeStyle.num_format_str = 'h:mm'
    
    lateStyle = XFStyle()
    lateStyle.num_format_str = 'h:mm'
    lateStyle.font = Font()
    ### when isLate = false, set colour_index = 0 will still get red font in Excel.
    lateStyle.font.colour_index = 2
    
    earlyStyle = XFStyle()
    earlyStyle.num_format_str = 'h:mm'
    earlyStyle.font = Font()
    earlyStyle.font.colour_index = 5

    global wb
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
                if(colName in a.recDict):
                    times = a.recDict[colName]
                    if(len(times) >= 2):
                        if(len(times) > 2):
                            addLog('!! ' + a.userName + ' ' + str(times))
                        onTime = times[0]
                        offTime = times[len(times) - 1]
                    elif(len(times) == 1):
                        onlyTime = strToTime(times[0])
                        if(onlyTime.hour < divider):
                            onTime = times[0]
                        else:
                            offTime = times[0]

                onTime = strToTime(onTime)
                offTime = strToTime(offTime)

                if(onTime and offTime):
                    a.totalTime += (offTime - onTime).seconds / 3600
                isLate, isEarly = checkTime(onTime, offTime, colName)
                if(isLate):  # late
                    a.late += 1
                    sheet1.write(rowNum, colNum, onTime, lateStyle)
                else:
                    sheet1.write(rowNum, colNum, onTime, timeStyle)
                    
                if(isEarly):  # early
                    a.early += 1
                    sheet1.write(rowNum + 1, colNum, offTime, earlyStyle)
                else:
                    sheet1.write(rowNum + 1, colNum, offTime, timeStyle)
                
                

        rowNum += 2

    genStaticsSheet(lis)
#    if(not os.path.exists('result.xls')):
    wb.save('result.xls')


def checkTime(onTime, offTime, date):
    time1 = strToTime(monthStr + str(date) + ' ' + '10:00:00')
    time2 = strToTime(monthStr + str(date) + ' ' + '18:00:00')
    islate = False
    isearly = False
    if((not onTime) or (onTime and (onTime - time1).total_seconds() >= 0)):
        islate = True
    if((not offTime) or ((offTime and (offTime - time2).total_seconds() < 0) or (onTime and offTime and (offTime - onTime).total_seconds() >= WORKSECOND))):
        isearly = True

    print onTime, offTime
    return islate, isearly

# lis is UserRecord list
def genStaticsSheet(lis):
    global wb
    sheet2 = wb.add_sheet(statisticsSheetName, True)

# s: 2012/4/9 18:47:00, return: datetime(y,m,d,h,minute,s)
def strToTime(s):
    if(not s):
        return ''
    r = s.split()
    y, m, d = r[0].split('/')
    t = r.pop().split(':')
    if(len(t) == 2):
        h, minute = t
        s = '00'
    elif(len(t) == 3):
        h, minute, s = t
    return datetime(int(y), int(m), int(d), int(h), int(minute), int(s))


def startUp():
    if(workday.get() < 0 or workday.get() > 31):
        print 'invalid workday number'
        return
    if(not fName):
        print 'please select a file'
        return

    os.chdir(os.path.split(unicode(fName))[0])
    records = orgnizeRecord(getRecords(fName))
    addLog('User Num: ' + str(len(records)))
    genTotalSheet(records)


def getFile():
    try:
        f = tkFileDialog.askopenfile()
    except Exception, e:
        print e
    global fName
    fName = f.name
    fnameText = f.name


def addLog(msg):
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
dayNum = 30 # day num for this month, come from user input.
divider = 12 # mediator for onTime and offTime, hour.
totalSheetName = u'概览表'
statisticsSheetName = u'统计表'
WORKTIME = 9 # standard worktime, hour.
WORKSECOND = WORKTIME * 3600 # standart worktime in second

titles = (userIdTitle, nameTitle) + tuple(range(1, dayNum + 1))

wb = Workbook(encoding='gbk')

stage = Tkinter.Tk()
stage.title('xuli')
stage.geometry('300x300')

btnBrowse = Tkinter.Button(stage, text=u'选择文件', command=getFile)
#btnBrowse.grid(row = 0, column = 0)
btnBrowse.pack()

fnameText = Tkinter.StringVar()
lbFileName = Tkinter.Label(stage, text=fnameText)
#lbFileName.grid(row = 0, column = 1)
lbFileName.pack()

lbWorkday = Tkinter.Label(stage, text=u'本月工作天数')
#lbWorkday.grid(row = 1, column = 0)
lbWorkday.pack()

workday = Tkinter.IntVar()
workdayInput = Tkinter.Entry(stage, textvariable=workday)
workday.trace('w', workdayChanged)
#lbWorkday.grid(row = 1, column = 1)
workdayInput.pack()

labelText = Tkinter.StringVar()
label = Tkinter.Label(stage, textvariable=labelText, width='300', justify='left', anchor='w')
label.pack()

btnStart = Tkinter.Button(stage, text=u'开始', command=startUp)
btnStart.pack()


Tkinter.mainloop()