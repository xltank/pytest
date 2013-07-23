'''
Created on 2013-1-23

@author: VTX
'''

def myYield():
    print 'start'
    a = yield 1
    print a
    print 'break 1'
    yield 2
    print 'break 2'
    yield 3
    print 'break 3'

a = myYield()

# does not work
#print myYield().next() #print 'start'  \n 1
#print myYield().next() #print 'start'  \n 1
#print myYield().next() #print 'start'  \n 1

#print a.next()  #'start'  \n 1
#print a.next()  #'break 1'  \n 2
#print a.next()  #'break 2'  \n 3
#print a.next()  #'break 3' StopIteration

print a.next()
print
print a.send('aaa')
print
print a.send('aaa')
print
print a.send('aaa')
