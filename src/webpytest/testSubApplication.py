'''
Created on 2013-1-21

@author: VTX
'''

import web
import subApplication

urls = ('/sub', subApplication.app,
        '/', 'index')

app = web.application(urls, globals())

class index:
    def GET(self):
        return 'index'


if __name__ == '__main__':
    app.run()

