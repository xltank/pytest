'''
Created on 2013-1-23

@author: VTX
'''

import web, time

urls = ('/', 'count_holder',
        '/(.*)', 'count_down')

app = web.application(urls, globals())


class count_down:
    def GET(self, count):
        web.header('Content-Type', 'text/html')
        web.header('Transfer-Encoding', 'chunked')
        yield '<h2>Prepare for lunch!</h2>'
        j = '<li>Liftoff in %s...</li>'
        yield '<ul>'
        count = int(count)
        for i in range(count, 0, -1):
            out = j % i
            time.sleep(1)
            yield out
        yield '</ul>'
        time.sleep(1)
        yield '<h1>Lift off</h1>'

class count_holder:
    def GET(self):
        web.header('Content-type', 'text/html')
        web.header('Transfer-encoding', 'chunked')
        boxes = 4
        delay = 3
        countdown = 10
        for i in range(boxes):
            output = '<iframe src="/%d" width="200" height="500"></iframe>' % (countdown - i)
            yield output
            time.sleep(delay)




if __name__ == '__main__':
    app.run()
