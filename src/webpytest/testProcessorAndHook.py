'''
Created on 2013-1-21

@author: VTX
'''

import web

urls = ('/', 'index')
app = web.application(urls, globals())

class index:
    def GET(self):
        print 'GET'
        return 'aaaaaaaaaaaaa'

def my_processor(handler):
    print 'before...'
    result = handler()
    print 'after...'
    return result

def my_loadhook():
    print 'my load hook'

def my_unloadhook():
    print 'my unload hook'

if __name__ == '__main__':
    #before...
    #GET
    #after...
    #before... ?? why this 'before...'
#    app.add_processor(my_processor)

    app.add_processor(web.loadhook(my_loadhook))
    app.add_processor(web.loadhook(my_unloadhook))
    app.run()
