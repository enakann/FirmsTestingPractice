import sys
sys.path.append("..")
from excel_to_json_converter import excel_to_json_convert
#print(dir(excel_to_json_converter))


class persistent_locals(object):
    def __init__(self, func):
        self._locals = {}
        self.func = func

    def __call__(self, *args, **kwargs):
        def tracer(frame, event, arg):
            if event=='return':
                self._locals = frame.f_locals.copy()

        # tracer is activated on next call, return or exception
        sys.setprofile(tracer)
        try:
            # trace the function call
            res = self.func(*args, **kwargs)
        finally:
            # disable tracer and replace with old one
            sys.setprofile(None)
        return res

    def clear_locals(self):
        self._locals = {}

    @property
    def locals(self):
        return self._locals




#@persistent_locals
def func():
    local1 = 1
    local2 = 2
    dic={'a':1,'b':2}
    ls=[]
    for i in range(100):
        ls.append(i)
    return ls


def decorateit(f):
    func=persistent_locals(f)
    return func
#func=decorateit(func)
#ls=func()
#print func.locals
#print("the result is {}".format(ls))

excel_to_json_convert=decorateit(excel_to_json_convert)
result=excel_to_json_convert(r"D:\my_Python\py_projects\FirmsTestingPractice\FiRMS\My_Work\tests\180809-000430.xlsx")
print(result)
d=excel_to_json_convert.locals

print("firewall list is {}".format(d['firewall_list']))
for k,v in excel_to_json_convert.locals.items():
    print(k)


#func()
#persistent_locals(func)
#persistent_locals(func)()


