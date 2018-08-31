import unittest
from mock import patch
import os
#from os import urandom

def func(num):
    return 'f'*num

def abc_urandom(length):
    return 'abc' + os.urandom(length)


class Testing(unittest.TestCase):
    @patch('os.urandom',side_effect=func)
    def test_func1(self,urandom_function):
        assert os.urandom(5)=='fffff'

    @patch('os.urandom', side_effect=func)
    def test_abc_urandom(self, abc_urandom_function):
        assert abc_urandom(5) == 'abcfffff'

    def test_func2(self):
        with patch('os.urandom', return_value='pumpkins') as abc_urandom_function:
            assert abc_urandom(5) == 'abcpumpkins'

    @patch('os.urandom')
    def test_abc_urandom2(self, urandom_function):
        urandom_function.return_value = 'pumpkins'
        assert os.urandom(5) == 'pumpkins'
        urandom_function.return_value = 'lemons'
        assert os.urandom(5) == 'lemons'
        urandom_function.side_effect = (
            lambda l: 'f' * l
        )
        assert os.urandom(5) == 'fffff'

    @mock.patch('os.urandom', return_value='pumpkins')
    def test_abc_urandom(self, urandom_function):
        # The mock function hasn't been called yet
        assert not urandom_function.called

        # Here we call the mock function twice and assert that it has been
        # called and the number of times called is 2
        assert os.urandom(5) == 'pumpkins'
        assert os.urandom(5) == 'pumpkins'
        assert urandom_function.called
        assert urandom_function.call_count == 2

        # Finally, we can reset all function call statistics as though the
        # mock function had never been used
        urandom_function.reset_mock()
        assert not urandom_function.called
        assert urandom_function.call_count == 0

    @mock.patch('os.urandom', return_value='pumpkins')
    def test_abc_urandom(self, urandom_function):
        assert os.urandom(1) == 'pumpkins'
        assert os.urandom(3) == 'pumpkins'
        assert os.urandom(10) == 'pumpkins'

        # Function was last called with argument 10
        args, kwargs = urandom_function.call_args
        assert args == (10,)
        assert kwargs == {}

        # All function calls were called with the following arguments
        args, kwargs = urandom_function.call_args_list[0]
        assert args == (1,)
        assert kwargs == {}
        args, kwargs = urandom_function.call_args_list[1]
        assert args == (3,)
        assert kwargs == {}
        args, kwargs = urandom_function.call_args_list[2]
        assert args == (10,)
        assert kwargs == {}



if __name__ == '__main__':
    unittest.main()