'''
Created on 2013-1-20

@author: Administrator
'''


import web
import hashlib
from web.session import Session, DiskStore
from datetime import datetime
import random
import os
import cgi


web.config.debug = False
maxFileSize = 20
cgi.maxlen = maxFileSize * 1024 * 1024
web.config.session_parameters['timeout'] = 300

render = web.template.render('templates/')
urls = (
        '/', 'index',
        '/userlist', 'userlist',
        '/login', 'login',
        '/signup', 'signup',
        '/logout', 'logout',
        '/upload', 'upload'
        )

app = web.application(urls, globals())
db = web.database(dbn='mysql', user='root', pw='root', db='test')
ses = Session(app, DiskStore('sessions'), initializer={'userName':'', 'userId':'', 'token':''})

uploadDir = 'upload'


def checkToken():
    un = web.cookies().get('userName')
    tk = web.cookies().get('token')
    if(un and tk and ses):
        if(un == ses.userName and tk == ses.token):
            return True
    raise web.seeother('/login')

def setCookieSession(un, uid, pw):
    ses.userName = un
    ses.userId = uid
    ses.token = hashlib.md5(pw + str(random.randint(0, 99999999))).hexdigest()
    web.setcookie('userName', un, 300)
    web.setcookie('token', ses.token, 300)

class index:
    def GET(self):
        if(checkToken() == True):
            raise web.seeother('/userlist')

class login:
    def GET(self):
        return render.login()

    def POST(self):
        f = web.input()
        if(f.name and f.password):
            d = dict(f)
            d['pw'] = hashlib.md5(f.password).hexdigest()
            r = list(db.query("select * from user where name=$name and password=$pw", vars=d))
        if(len(r) > 0):
            setCookieSession(f.name, r[0].id, f.password)
            web.seeother('/userlist')
        else:
            raise web.seeother('/login')


class userlist:
    def GET(self):
        if(checkToken() == True):
            users = db.select('user')
            files = db.select('upload', where='userId=' + str(ses.userId))
            return render.userlist(users, files)

class logout:
    def GET(self):
        ses.kill()
        web.setcookie('token', '')
        return render.index()

class signup:
    def GET(self):
        return render.signup()

    def POST(self):
        i = web.input()
        if(i.name and i.password and i.password == i.confirm):
            pswdHash = hashlib.md5(i.password).hexdigest()
            r = db.insert('user', name=i.name, password=pswdHash, description=i.description, creationTime=datetime.now())
            setCookieSession(i.name, r, i.password)
            raise web.seeother('/userlist')

class upload:
    def GET(self):
        if(checkToken() == True):
            return render.upload()

    def POST(self):
        if(checkToken() == True):
            try:
                data = web.input(file={})
            except ValueError:
                return 'file larger than ' + maxFileSize + 'MB'
            fName = data.file.filename
            fPath = os.path.join(os.path.abspath(uploadDir), fName)
            f = open(fPath, 'wb')
            f.write(data.file.file.read())
            db.insert('upload', name=fName, userId=ses.userId, creationTime=datetime.now())
            raise web.seeother('userlist')


if __name__ == '__main__':
#    app.add_processor(web.loadhook(checkToken))
    app.run()
