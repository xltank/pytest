'''
Created on 2013-1-15

@author: VTX
'''

import web

urls = ('/\w+', 'index')

class index:
    def GET(self):
        i = web.input()
        return 'hello ' + i.name


if(__name__ == '__main__'):
    app = web.application(urls, globals())
    app.run()
