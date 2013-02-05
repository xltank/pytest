'''
Created on 2013-2-5

@author: VTX
'''
import logging

debug = False

def deco(str):
    def realFunc(func):
        assert 1 == 2
        logging.info('decorated!')
        func.__name__ += str
        func.deco = True
        return func

    return realFunc

@deco('bb')
def test1(para):
    print test1.__name__
    return para


if __name__ == '__main__':
    test1(123)
    print test1.deco
