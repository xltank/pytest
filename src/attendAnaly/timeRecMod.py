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
        self.totalTime = 0  # in seconds

        self.ill = 0
        self.leave = 0
        self.absent = 0
        self.annual = 0
        self.trip = 0
        self.out = 0
        self.exchange = 0
        self.game = 0
        self.dead = 0
        self.marriage = 0

