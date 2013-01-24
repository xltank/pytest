'''
Created on 2013-1-23

@author: VTX
'''

import web

urls = ('/', 'index',
        '/error', 'error')
app = web.application(urls, globals())

def notFound():
    return web.notfound("sorry....................")

def internalError():
    return web.internalerror("internal error............")

app.notfound = notFound
#app.internalerror = internalError

class index:
    def GET(self):
        raise web.notfound()

class error:
    def GET(self):
        raise web.internalerror('aaaaaaaaaaa')


if __name__ == '__main__':
    app.run()
