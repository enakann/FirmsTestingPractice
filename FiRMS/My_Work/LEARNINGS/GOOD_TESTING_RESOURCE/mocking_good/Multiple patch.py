import unittest
import os
import mock

def simple_urandom(length):
    return 'f' * length


def different_sep():
    return '-'


class TestRandom(unittest.TestCase):
    @mock.patch('os.urandom', side_effect=simple_urandom)
    @mock.patch('os.sep', side_effect=different_sep)
    def test_random(self, urandom_function, sep_function):
        assert os.urandom(5) == 'fffff'
        assert os.sep() == '-'

if __name__ == '__main__':
    unittest.main()