from mock import patch, call,DEFAULT,MagicMock

"""@patch('builtins.print')
def test_print(mocked_print):
    print('fdsdsdodo')
    print()
    assert mocked_print.mock_calls == [call('foo'), call()]"""

"""from StringIO import StringIO
def foo():
    print 'Something'

@patch('sys.stdout', new_callable=StringIO)
def test(mock_stdout):
    foo()
    assert mock_stdout.getvalue() == 'Something\n'
test()
#################################################

class Class(object):
    def method(self):
        pass

with patch('__main__.Class') as MockClass:
    instance = MockClass.return_value
    instance.method.return_value = 'foo'
    print(instance.method.return_value)
    assert Class() is instance
    assert Class().method() == 'foo'"""

######################################
""" ['__str__', 'assert_any_call', 'assert_called', 'assert_called_once', 'assert_called_once_with', 'assert_called_with', 'assert_has_calls', 'assert_not_called', 'attach_mock', 'call_args', 'call_args_list', 'call_count', 'called', 'configure_mock', 'method_calls', 'mock_add_spec', 'mock_calls', 'reset_mock', 'return_value', 'side_effect']"""
class SomeClass:
    def method(self,a):
        return a


@patch.object(SomeClass, 'method')
def test(mock_method):
    SomeClass.method(3)
    print(mock_method)
    print(dir(mock_method))
    mock_method.assert_called_with(3)
test()

##########################################

thing = object()
other = object()
@patch.multiple('__main__', thing=DEFAULT, other=DEFAULT)
def test_function(thing, other):
    assert isinstance(thing, MagicMock)
    assert isinstance(other, MagicMock)
test_function()

@patch('sys.exit')
@patch('sys.exit')
@patch.multiple('__main__', thing=DEFAULT, other=DEFAULT)
def test_function(mock_exit,another_exit, other, thing):
    assert 'other' in repr(other)
    assert 'thing' in repr(thing)
    assert 'exit' in repr(mock_exit)
    assert 'exit' in repr(another_exit)

test_function()