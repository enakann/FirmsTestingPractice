import inspect

def deco(f):
    def inner(*args,**kwargs):
        f(*args,**kwargs)
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        print 'function name "%s"' % inspect.getframeinfo(frame)[2]
        print(f.__code__.co_varnames)
        print(inspect.getargspec(f))
        print(f.func_code.co_varnames[:f.func_code.co_argcount])
        for i in args:
            print "    %s = %s" % (i, values[i])
        return [(i, values[i]) for i in args]
    return inner

@deco
def func():
    a=10
    b=20
    print("inside func")
func()


def deco2(f):
    def inner(*args,**kwargs):
        print(locals())
        print(dir(f))
        result=f(*args,**kwargs)
        print(locals())
        return result
    return inner
@deco2
def func2():
    a=1
    b=2
    c=3
func2()

def func3():
    z=1
    ls=[1,2,3]
    d={'a':1}
    ls1=[]
    for i,j in enumerate(range(10)):
        ls1.append((i,j))
    print(locals())