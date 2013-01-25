'''
Created on 2013-1-24
@author: VTX
'''

import web
from web.session import Session, DiskStore

web.config.debug = False

urls = ('/count', 'count',
        '/reset', 'reset')

app = web.application(urls, globals())

session = Session(app, DiskStore('sessions'), initializer={'count':0})

class count:
    def GET(self):
        session.count += 1
        return str(session.count)

class reset:
    def GET(self):
        session.kill()
        return ""

if __name__ == '__main__':
    app.run()
