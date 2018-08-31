from error import FirmsNetConfConnException,FirmsNetConfRPCException

def func():
     raise FirmsNetConfRPCException('IO error')
     try:
        print 1/0
     except Exception,e:
        raise FirmsNetConfConnException('IO error',e)

if __name__ == '__main__':

    try:
        func()
    except FirmsNetConfRPCException,e:
        print e.name
    

