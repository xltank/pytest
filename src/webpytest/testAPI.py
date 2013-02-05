'''
Created on 2013-2-4

@author: VTX
'''

import web
import json
import datetime

urls = ('/login', 'login')

app = web.application(urls, globals())
con = web.database(dbn='mysql', user='root', pw='root', db='test')

dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None

class login:
    def GET(self):
        r = list(con.select('user'))
        j = json.dumps(r, default=dthandler)
        return j

    def POST(self):
        r = list(con.select('user'))
        return json.dumps(r, default=dthandler)


if __name__ == '__main__':
    app.run()
