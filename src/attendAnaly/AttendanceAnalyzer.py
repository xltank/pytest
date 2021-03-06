# coding:gbk
'''
Created on 2012-12-27

@author: VTX

1082    1    33    徐立              1    0    2012/4/9 9:9        
or
1082    1    0000000033    徐立              1    0    2012/04/09 09:09        

1，每日打卡记录：只有一条，以12:00为界决定是上班还是下班；超过两条，取第一和最后一条。
2，
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
import xlrd
from xlrd.xldate import xldate_as_tuple


def getFile():
    try:
        f = tkFileDialog.askopenfile(filetypes=[('txt', '*.txt')])
    except Exception, e:
        print e

    if(f):
        global sourceFileName, fnameText
        sourceFileName = f.name
        fnameText.set(sourceFileName)


def grapRecords():
    if(not sourceFileName):
        addLog('Please select a file!')
        return

    if(workdayIntVar.get() < 0 or workdayIntVar.get() > 31):
        print 'invalid workday number'
        return

    getTargetMonth()

    os.chdir(os.path.split(unicode(sourceFileName))[0])
    records = orgnizeRecord(getRecords(sourceFileName))
    addLog(str(len(records)) + ' members')
    genTotalSheet(records)


def getRecords(logName):
    results = []
    f = open(logName, 'r')
    for r in f:
        if(r.count(monthStr) > 0):
            recTuple = fromString(r)
            results.append(DayRecord(recTuple[0], recTuple[1], recTuple[2], recTuple[3]))
    addLog(str(len(results)) + ' records in ' + monthStr)
    results.sort(key=attrgetter('userId'), reverse=False)
    return results


def fromString(s):
    s = s.strip()
    lis = s.split('\t')
    return lis[0], lis[2], unicode(lis[3].strip()), lis[6]


def orgnizeRecord(lis):
    """ lis is DayRecord list """
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


def genTotalSheet(lis):
    """ lis is UserRecord list """
    global wb
    wb = Workbook(encoding='gbk')

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
    earlyStyle.font.colour_index = 7

    sheet1 = wb.add_sheet(TOTAL_SHEET_NAME)
    rowNum = 0
    for i, s in enumerate(totalSheetTitles):  # write header
        sheet1.write(0, i, str(s))
    rowNum += 1

    for a in lis:
        for colNum, colName in enumerate(totalSheetTitles):
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
                            print '! ' + a.userName + ' ' + monthStr + str(colName) + ' 两条以上打卡记录.'
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

#                if(onTime and offTime):
#                    a.totalTime += (offTime - onTime).seconds / 3600
                isLate, isEarly = checkTime(onTime, offTime, colName)
                if(isLate):  # late
#                    a.late += 1
                    sheet1.write(rowNum, colNum, onTime, lateStyle)
                else:
                    sheet1.write(rowNum, colNum, onTime, timeStyle)

                if(isEarly):  # early
#                    a.early += 1
                    sheet1.write(rowNum + 1, colNum, offTime, earlyStyle)
                else:
                    sheet1.write(rowNum + 1, colNum, offTime, timeStyle)

        rowNum += 2

    getTargetFileName()

    try:
        wb.save(targetFileName)
        addLog('"' + targetFileName + '" is in the same directory of the .txt file.')
    except IOError:  #IOError: [Errno 13] Permission denied: '***.xls'
        addLog('please close ' + targetFileName + ' and retry')


def checkTime(onTime, offTime, date):
    time10Clock = strToTime(monthStr + str(date) + ' ' + '10:00:00')
    time18Clock = strToTime(monthStr + str(date) + ' ' + '18:00:00')
    time19Clock = strToTime(monthStr + str(date) + ' ' + '19:00:00')
    islate = False
    isearly = False
    if((not onTime) or (onTime and (onTime - time10Clock).total_seconds() >= 0)):
        islate = True

    flag18Clock = offTime and ((offTime - time18Clock).total_seconds() < 0)  # early
    flag19Clock = offTime and ((offTime - time19Clock).total_seconds() >= 0)  # must not early
    flag9Hours = onTime and offTime and ((offTime - onTime).total_seconds() < WORKSECONDS)  #early
    if((not offTime) or flag18Clock or (not flag19Clock and flag9Hours)):
        isearly = True

    return islate, isearly


def strToTime(s):
    """"s: 2012/4/9 18:47:00, return: datetime(y,m,d,h,minute,s) """
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


def addLog(msg):
    print msg
    msgText.set(msgText.get() + msg + '\n')


def guessTargetMonth():
    global theYear, theMonth, monthStr
    now = datetime.now()
    theYear = now.year
    theMonth = now.month - 1 or 12
    if(theMonth == 12):
        theYear -= 1

    yearIntVar.set(theYear)
    monthIntVar.set(theMonth)
    monthStr = str(theYear) + '/' + str(theMonth) + '/'
    global targetFileName
    targetFileName = str(theYear) + str(theMonth).center(2) + '.xls'


def getTargetMonth():
    global theYear, theMonth, monthStr
    theYear = yearIntVar.get()
    theMonth = monthIntVar.get()
    monthStr = str(theYear) + '/' + str(theMonth) + '/'
    global targetFileName
    targetFileName = str(yearIntVar.get()) + str(monthIntVar.get()).center(2) + '.xls'


def getTargetFileName():
    """ if 201211.xls exists, use 201211_n.xls """
    getTargetMonth()
    global targetFileName
    originName = targetFileName
    if(os.path.exists(targetFileName)):
        for i in range(1, 100):
            name1, name2 = os.path.splitext(originName)
            targetFileName = name1 + '_' + str(i) + name2
            if(not os.path.exists(targetFileName)):
                break


##############################
def readxls():
    try:
        f = tkFileDialog.askopenfile(filetypes=[('Excel File', '*.xls *.xlsx')])
    except Exception, e:
        addLog(str(e))
    if(f):
        global targetFileName
        tmp = os.path.splitext(f.name)
        targetFileName = tmp[0] + u'_统计表' + tmp[1]
        bk = xlrd.open_workbook(filename=f.name, encoding_override='gbk')  # xlrd.Book to read data.
        if(not bk):
            addLog('Please select the xls file with correction sheet.')
            return
        parseSheets(bk)


def parseSheets(bk):
    sheet1 = bk.sheet_by_index(0)
    titlesRow = sheet1.row_values(0)
    rowNum = sheet1.nrows
    colNum = sheet1.ncols
    userRecords = []
    for r in range(1, rowNum, 2):
        row1_data = sheet1.row_values(r)
        row2_data = sheet1.row_values(r + 1)
        print row1_data[1]
        userRec = UserRecord()
        userRec.userId = row1_data[0]
        userRec.userName = row1_data[1]
        for c in range(2, colNum):
            setAttendaceStatus(row1_data[c], row2_data[c], titlesRow[c], userRec)

        userRecords.append(userRec)

#    global wb
#    wb = copy.copy(bk)  # set to xlwt.WorkBook to write and save.
    print len(userRecords)

    global wb
    wb = Workbook(encoding='gbk')
    genAttendanceSheet(userRecords)
    genStateSheet(userRecords)

    try:
        wb.save(targetFileName)
        addLog('"' + targetFileName + '" is in the same directory of the .xls file.')
    except IOError:  #IOError: [Errno 13] Permission denied: '***.xls'
        addLog('please close ' + targetFileName + ' and retry')


def setAttendaceStatus(c1, c2, date, userRec):
    date = str(int(date))  # date is float
    time10Clock = strToTime(monthStr + date + ' ' + '10:00:00')
    time12Clock = strToTime(monthStr + date + ' ' + '12:00:00')
    time13Clock = strToTime(monthStr + date + ' ' + '13:00:00')
    time18Clock = strToTime(monthStr + date + ' ' + '18:00:00')
    # if out in morning and back in afternoon, if offTime < 18:30, it's a early
    time1830Clock = strToTime(monthStr + date + ' ' + '18:30:00')
    time19Clock = strToTime(monthStr + date + ' ' + '19:00:00')
    if(isinstance(c1, float)):  # use column date to be compatible with '09:11:11'
        t1 = xldate_as_tuple(c1, 0)
        c1 = strToTime(monthStr + date + ' ' + str(t1[3]) + ':' + str(t1[4]) + ':' + str(t1[5]))
    if(isinstance(c2, float)):
        t2 = xldate_as_tuple(c2, 0)
        c2 = strToTime(monthStr + date + ' ' + str(t2[3]) + ':' + str(t2[4]) + ':' + str(t2[5]))

#    if(isinstance(c1, datetime)):
#        time1Str = c1.strftime('%Y/%m/%d %H:%M:%S')
#    if(isinstance(c2, datetime)):
#        time2Str = c2.strftime('%Y/%m/%d %H:%M:%S')

    if(isinstance(c1, datetime)):
        if(isinstance(c2, datetime)):
            userRec.totalTime += (c2 - c1).total_seconds() - 3600  # - 1 hour lunch time

            if((c1 - time10Clock).total_seconds() >= 0):
                userRec.late += 1

            flag18Clock = c2 and ((c2 - time18Clock).total_seconds() < 0)  # early
            flag19Clock = c2 and ((c2 - time19Clock).total_seconds() >= 0)  # must not early
            flag9Hours = c1 and c2 and ((c2 - c1).total_seconds() < WORKSECONDS)  #early
            if((not c2) or flag18Clock or (not flag19Clock and flag9Hours)):
                userRec.early += 1

#            userRec.recDict[date] = [time1Str, time2Str]
        elif(isinstance(c2, unicode)):
            if(stateDictCn2En.has_key(c2)):
                prop = stateDictCn2En[c2]
                setattr(userRec, prop, getattr(userRec, prop) + 1)
            if(c2 == STATE_GAME):
                userRec.totalTime += WORKSECONDS_STD
            else:
                userRec.totalTime += (time12Clock - c2).total_seconds()
    elif(isinstance(c1, unicode)):
        if(stateDictCn2En.has_key(c1)):
            prop = stateDictCn2En[c1]
            setattr(userRec, prop, getattr(userRec, prop) + 1)
        if(c2 and stateDictCn2En.has_key(c2)):
            prop = stateDictCn2En[c2]
            setattr(userRec, prop, getattr(userRec, prop) + 1)
        elif(isinstance(c2, datetime)):
            if(prop == STATE_OUT):
                if((c2 - time1830Clock).total_seconds() < 0):
                    userRec.early += 1

            userRec.totalTime += (c2 - time13Clock).total_seconds()




def genAttendanceSheet(lis):
    """ lis is UserRecord list """
    sheet2 = wb.add_sheet(ATTENDANCE_SHEET_NAME, True)
    percentStyle = XFStyle()
    percentStyle.num_format_str = '0%'
    integerStyle = XFStyle()
    integerStyle.num_format_str = '0'
    titles = ('姓名', '总工作日（天）', '总工时（小时）', '个人总出勤（小时）', '个人日均（小时）', '个人出勤率')
    row = 0
    for i, item in enumerate(titles):
        sheet2.write(row, i, item)
    row += 1
    workdays = workdayIntVar.get()
    workhours = workdays * 8
    lis.sort(key=attrgetter('totalTime'), reverse=True)
    for u in lis:
        hours = round(u.totalTime / 3600.0)
        sheet2.write(row, 0, u.userName)
        sheet2.write(row, 1, workdays)
        sheet2.write(row, 2, workhours, integerStyle)
        sheet2.write(row, 3, hours, integerStyle)
        sheet2.write(row, 4, hours / workdays, integerStyle)
        sheet2.write(row, 5, round(hours / workhours, 2), percentStyle)
        row += 1


def genStateSheet(lis):
    sheet3 = wb.add_sheet(STATISTICS_SHEET_NAME, True)

    titles = ('姓名', '迟到次数', '姓名', '早退次数', '姓名', '请假次数', '姓名', '请假时长',)
    for i, item in enumerate(titles):
        sheet3.write(0, i, item)
    # late
    row = 1
    col = 0
    lis.sort(key=attrgetter('late'), reverse=True)
    for u in lis:
        if(u.late > 0):
            sheet3.write(row, col, u.userName)
            sheet3.write(row, col + 1, u.late)
            row += 1
    # early
    row = 1
    col += 2
    lis.sort(key=attrgetter('early'), reverse=True)
    for u in lis:
        if(u.early > 0):
            sheet3.write(row, col, u.userName)
            sheet3.write(row, col + 1, u.early)
            row += 1

    # ill and leave
    row = 1
    col += 2
    lis.sort(cmp=lambda a, b: cmp(a.ill + a.leave, b.ill + b.leave), reverse=True)
    for u in lis:
        if(u.ill + u.leave > 0):
            sheet3.write(row, col, u.userName)
            sheet3.write(row, col + 1, u.ill + u.leave)
            row += 1



#################
reload(sys)
sys.setdefaultencoding('gbk')  # ignore error reminder in PyDev

theYear = 2012
theMonth = 12
monthStr = '2012/11/'
userIdTitle = u'编号'
nameTitle = u'姓名'
dayNum = 30  # day num for this month, come from user input.
divider = 12  # mediator for onTime and offTime, hour.

sourceFileName = None
targetFileName = None
TOTAL_SHEET_NAME = u'概览表'
ATTENDANCE_SHEET_NAME = u'出勤表'
STATISTICS_SHEET_NAME = u'统计表'
WORKHOURS = 9  # standard worktime, hour.
WORKSECONDS = WORKHOURS * 3600  # 9 hours worktime in second
WORKSECONDS_STD = 8 * 3600  # standard worktime in second

wb = None
totalSheetTitles = (userIdTitle, nameTitle) + tuple(range(1, dayNum + 1))

#STATE_LATE = u"迟到"
#STATE_EARLY = u"早退"
STATE_ILL = u"病假"
STATE_LEAVE = u"事假"
STATE_ABSENT = u"旷工"
STATE_ANNUAL = u"年假"
STATE_TRIP = u"出差"
STATE_OUT = u"外出"
STATE_EXCHANGE = u"调休"
STATE_GAME = u"活动"
STATE_DEAD = u"丧假"
STATE_MARRIAGE = u"婚假"

statisticsSheetTitles = ("userName", "late", "early", "ill", "leave", "absent", "annual", "trip")
stateDictEn2Cn = {  "ill" : STATE_ILL,
                    "leave" : STATE_LEAVE,
                    "absent" : STATE_ABSENT,
                    "annual" : STATE_ANNUAL,
                    "trip" : STATE_TRIP,
                    "out" : STATE_OUT,
                    "exchange" : STATE_EXCHANGE,
                    "game" : STATE_GAME,
                    "dead" : STATE_DEAD,
                    "marriage" : STATE_MARRIAGE
                  }
stateDictCn2En = dict(tuple([(stateDictEn2Cn[k], k) for k in stateDictEn2Cn]))

stage = Tkinter.Tk()
stage.title('Attendance Records Organizer')
stage.geometry('500x500')


#### grap records from .txt
yearLabel = Tkinter.Label(stage, text=u'年：')
yearLabel.grid(row=0, column=0, columnspan=2, sticky='w')

yearIntVar = Tkinter.IntVar()
yearEntry = Tkinter.Entry(stage, textvariable=yearIntVar, width=5)
yearEntry.grid(row=0, column=2, columnspan=2, sticky='w')

monthLabel = Tkinter.Label(stage, text=u'月：')
monthLabel.grid(row=1, column=0, columnspan=2, sticky='w')

monthIntVar = Tkinter.IntVar()
monthEntry = Tkinter.Entry(stage, textvariable=monthIntVar, width=3)
monthEntry.grid(row=1, column=2, columnspan=2, sticky='w')

workdayLabel = Tkinter.Label(stage, text=u'本月工作天数:')
workdayLabel.grid(row=2, column=0, columnspan=2, sticky='w')

workdayIntVar = Tkinter.IntVar()
workdayIntVar.set(22)
workdayInput = Tkinter.Entry(stage, textvariable=workdayIntVar, width=3)
workdayInput.grid(row=2, column=2, columnspan=2, sticky='w')


hdLine = Tkinter.Label(stage, text=str('-' * 40))
hdLine.grid(row=3, column=0, columnspan=5)


browserButton = Tkinter.Button(stage, text=u'选择文件', command=getFile)
browserButton.grid(row=4, column=0, sticky='w')

fnameText = Tkinter.StringVar()
fnameLabel = Tkinter.Label(stage, textvariable=fnameText)
fnameLabel.grid(row=5, column=0, sticky='w')

btnStart = Tkinter.Button(stage, text=u'提取记录', command=grapRecords)
btnStart.grid(row=4, column=1, sticky='w')


vdLine = Tkinter.Label(stage, text=str('|\n' * 6))
vdLine.grid(row=4, rowspan=3, column=2)


#### analyze modified Excel file
browserButton2 = Tkinter.Button(stage, text=u'选择文件', command=readxls)
browserButton2.grid(row=4, column=3, sticky='w')

fnameText2 = Tkinter.StringVar()
fnameLabel2 = Tkinter.Label(stage, textvariable=fnameText2)
fnameLabel2.grid(row=5, column=4, sticky='w')

#btnAnalyse = Tkinter.Button(stage, text=u'开始统计', command=analyzeCorrectionSheet)
#btnAnalyse.grid(row=1, column=4, sticky='w')


msgText = Tkinter.StringVar()
msgLabel = Tkinter.Label(stage, textvariable=msgText)
msgLabel.grid(row=6, column=0, columnspan=5, sticky='w')


guessTargetMonth()

stage.mainloop()

