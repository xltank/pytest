'''
Created on 2013-1-21

@author: VTX
'''

import web

urls = ('/(.*)', 'index')

app = web.application(urls, globals())

class index:
    def GET(self, pathPara):
        return pathPara


if __name__ == '__main__':
    app.run()

