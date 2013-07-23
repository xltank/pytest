# coding: utf8

'''
Created on 2012-12-25

@author: VTX
'''
import MySQLdb

def showTables():
    if(cursor):
        sql = 'show tables'
        cursor.execute(sql)
        allTables = cursor.fetchall()
        print type(allTables)
        print 'all tables: ', allTables


#def createTestTable():
#    cursor.execute('create table test (id varchar(20), name varchar(50), description text)')


def createDummyRecords():
    cursor.execute('delete from user')
    for i in range(20):
        cursor.execute('insert into user(name, description) values(%s, %s)' % (i * 10, i * 100))


def getRecords():
    cursor.execute('select * from user')
    allRecords = cursor.fetchall()
    print allRecords


host = 'localhost'
port = 3306
un = 'root'
pwd = 'root'
db = 'test'

con = MySQLdb.connect(host = host, port = port, user = un, passwd = pwd, db = db)
cursor = con.cursor()

showTables()
createDummyRecords()




getRecords()

con.close()

if __name__ == '__main__':
    pass
