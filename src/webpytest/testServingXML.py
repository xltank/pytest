'''
Created on 2013-1-21

@author: VTX
'''

import web


urls = ('/(.*)', 'index')
render = web.template.render('templates')
app = web.application(urls, globals())

class index:
    def GET(self, d):
        print d
        return render.testXML(d)


if __name__ == '__main__':
    app.run()
