'''
Created on 2013-1-15

@author: VTX
'''

import web

urls = ('/', 'index')

class index:
    def GET(self):
        return 'Hello, World!'




if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
