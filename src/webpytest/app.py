'''
Created on 2013-1-15

@author: VTX
'''

import web

urls = ('/(\w+)', 'index')

render = web.template.render('templates/')

class index:
    def GET(self, name):
#        return render.index("<em>aaaaa</em>")
#        i = web.input(name=None)
        return render.index(name)



if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
