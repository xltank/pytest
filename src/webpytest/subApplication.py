'''
Created on 2013-1-21

@author: VTX
'''

import web

urls = ('', 'resub',
        '/', 'dosub')

app = web.application(urls, globals())

class resub:
    def GET(self):
        raise web.seeother('/')

class dosub:
    def GET(self):
        return 'done'

