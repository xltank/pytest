'''
Created on 2013-1-20

@author: Administrator
'''


import web
import hashlib

render = web.template.render('templates/')
urls = (
        '/', 'index',
        '/userlist', 'userlist',
        '/login', 'login',
        '/signup', 'signup',
        '/logout', 'logout'
        )

app = web.application(urls, globals())

db = web.database(dbn='mysql', user='root', pw='root', db='test')


class index:
    def GET(self):
        return render.index()

class login:
    def GET(self):
        return render.login()

    def POST(self):
        f = web.input()
        if(f.name and f.password):
            f.password = hashlib.md5(f.password).hexdigest()
            r = db.query("select * from user where name=$name and password=$password", vars=dict(f))
        if(len(r) > 0):
            web.seeother('/userlist')
        else:
            raise web.seeother('/')


class userlist:
    def GET(self):
        items = db.select('user')
        return render.userlist(items)

class logout:
    def GET(self):
        return render.index()

class signup:
    def GET(self):
        return render.signup()

    def POST(self):
        i = web.input()
        if(i.name and i.password and i.password == i.confirm):
            pswdHash = hashlib.md5(i.password).hexdigest()
            db.insert('user', name=i.name, password=pswdHash, description=i.description)
        raise web.seeother('/signup')


if __name__ == '__main__':
    app.run()
