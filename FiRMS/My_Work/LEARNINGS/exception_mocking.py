"""
log = logging.getLogger(__name__)


class A(object):
    def __init__(self):
        log.debug('Init')
Assuming log is a global variable in a module mymod, you want to mock the actual instance that getLogger returned, which is what invokes debug. Then, you can check if log.debug was called with the correct argument.

with mock.patch('mymod.log') as log_mock:
    # test code
    log_mock.debug.assert_called_with('Init')

    assert_called_with(*args, **kwargs) # assert that calls are made in a particular way
assert_called_once_with(*args, **kwargs) # asserts that method is called once with specified arguments
assert_any_call(*args, **kwargs) # assert the mock has been called with the specified arguments.
assert_has_calls(calls, any_order=False) # assert the mock has been called with the specified calls.
assert_not_called(*args, **kwargs) # assert the mock was never called.
"""


from Logging_my import Log
from Logging_my import logging
import unittest
from mock import Mock,patch
import mock
from FUNC import func2


import logging
import sys


def iniddt_logger_singleton():
    global logger

    logger = logging.getLogger(name='mylogger')
    logger.setLevel(logging.WARN)
    formatter = logging.Formatter(
        '[%(asctime)s:%(module)s:%(lineno)s:%(levelname)s] %(message)s')
    streamhandler = logging.StreamHandler(sys.stdout)
    streamhandler.setLevel(logging.WARNING)
    streamhandler.setFormatter(formatter)
    logger.addHandler(streamhandler)
    filehandler = logging.FileHandler('mypython.log')
    filehandler.setLevel(logging.DEBUG)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
    return logger




def func(a,b):
    logger=Log().init_logger_singleton()
    #logger=logging.getLogger('__main__')
    c=None
    try:
        print ("pre processing")
        c=a/b
    except Exception as e:
        logger.error("failed")
    return c
class Testd(unittest.TestCase):

    """def test_func(self):
       with self.assertRaises(ZeroDivisionError) as context:
           func(1, 0)
       print(mocklog)
       exception=context.exception
       expected_msg="integer division or modulo by zero"
       actual_message=exception.args[0]
       self.assertEqual(expected_msg,actual_message)
    def test_func2(self):
        try:
            func(1,1)
        except ZeroDivisionError:
            pass
        except Exception as e:
            self.fail('Unexpected exception raised:', e)
        else:
            self.fail('ExpectedException not raised')"""


    """def test_func3(self):
        with patch('__main__.logging') as mocklog:
            #print(dir(func))
            func(1,0)
            #mocklog.error.assert_called_with('ZeroDivisionError')
            mocklog.error.assert_called_with('failed')"""
    """def test_func5(self):
        logger = logging.getLogger('Logging_my')
        with mock.patch.object(logger, 'error') as mock_debug:
            func(1,0)
            #mock_debug.assert_called_once_with('integer division or modulo by zero')
            mock_debug.assert_called_once_with('failed')"""
    def test_func6(self):
        logger = logging.getLogger('FUNC')
        #print(logger.__module__)
        #istead of Logging_my __main__ is working fine if logger is created in this module
        with mock.patch.object(logger, 'error') as mock_debug:
            func2(1,0)
            mock_debug.assert_called_once_with('failed')



    """@mock.patch(logging)
    def test_func4(self,mock_logger):
        mock_logger.warn.assert_called_with("integer division or modulo by zero")"""

    """def test_func5(self):
        logger = logging.getLogger('__main__.logger')
        with mock.patch.object(logger, 'error') as mock_debug:
            func(1,0)
           # mock_debug.assert_called_once_with('integer division or modulo by zero')
            mock_debug.error.assert_called_with('integer division or modulo by zero')"""


if __name__ == '__main__':
    unittest.main()
