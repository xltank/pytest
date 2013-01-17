'''
Created on 2013-1-17

@author: VTX
'''

import web

urls = ('/', 'index')
render = web.template.render('templates/')

db = web.database(dbn='mysql', user='root', pw='root', db='test')

class index:
    def GET(self):
        items = db.select('test')
#        for i in items:
#            print i.id, i.name
        return render.dbtest(items)


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
