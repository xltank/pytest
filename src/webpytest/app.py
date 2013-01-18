'''
Created on 2013-1-15

@author: VTX
'''

import web

urls = ('/(\w+)', 'index')
#render = web.template.render('templates/')
app = web.application(urls, globals())

class index:
    def GET(self, name):
        print name
        return name

def hello(handler):
    print handler()
    return 'Hello ', handler()


if __name__ == '__main__':
    app.add_processor(hello)
    app.run()
