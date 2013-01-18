'''
Created on 2013-1-17

@author: VTX

DATABASE 'test' and TABLE 'test' with (id, name, gender, description) are needed.

'''

import web

urls = ('/', 'index', '/add', 'add')
render = web.template.render('templates/')

app = web.application(urls, globals())

db = web.database(dbn='mysql', user='root', pw='root', db='test')

class index:
    def GET(self):
        items = db.select('test')
        return render.dbtest(items)


class add:
    def POST(self):
        i = web.input();
        n = db.insert('test', name=i.name, gender=i.gender, description=i.description)
        raise web.seeother('/')

    def GET(self):
        i = web.input();
        n = db.insert('test', name=i.name, gender=i.gender, description=i.description)


if __name__ == '__main__':
    app.run()
