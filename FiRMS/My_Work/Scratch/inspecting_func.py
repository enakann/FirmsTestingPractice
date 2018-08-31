import inspect

def func(a, b, c):
    frame = inspect.currentframe()
    args, _, _, values = inspect.getargvalues(frame)
    print 'function name "%s"' % inspect.getframeinfo(frame)[2]
    for i in args:
        print "    %s = %s" % (i, values[i])
    return [(i, values[i]) for i in args]

def deco(f):
    def inner(*args,**kwargs):
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        print 'function name "%s"' % inspect.getframeinfo(frame)[2]
        for i in args:
            print "    %s = %s" % (i, values[i])
        return [(i, values[i]) for i in args]
    return inner

def func(a,b,c):
    print locals().keys()
####################################
from module import myfunc

myfunc = double_decorator(myfunc)

x = myfunc(2) # returns 4
##################################
def a(num):
    return num * 1

def double(f):
    def wrapped(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapped

print(double(a)(2))


####################################

ls=func(1,2,3)
print(ls)