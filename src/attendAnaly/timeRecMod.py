'''
Created on 2012-12-29
'''


class DayRecord(object):
    def __init__(self, rId, uId, userName, time=''):
        self.id = rId
        self.userId = uId
        self.userName = unicode(userName)
        self.time = time


class UserRecord(object):
    def __init__(self, uId='', userName=''):
        self.userId = uId
        self.userName = userName
        self.recDict = dict()  # key: date, value: list of record time
        self.late = 0
        self.early = 0
        self.totalTime = 0  # in minutes




