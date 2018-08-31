import StringIO
import sys

def foo(inStr):
    print "hi"+inStr
    print "hello"
    print "u dr"

def test_foo():
    capturedOutput = StringIO.StringIO()          # Create StringIO object
    sys.stdout = capturedOutput                   #  and redirect stdout.
    foo('test')                                   # Call unchanged function.
    sys.stdout = sys.__stdout__                 # Reset redirect.
    out=capturedOutput.getvalue()
    ls=out.split("\n")
    print(ls)
    print 'Captured', capturedOutput.getvalue()   # Now works as before.

test_foo()