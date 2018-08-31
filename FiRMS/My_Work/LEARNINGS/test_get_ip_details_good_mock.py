import unittest
from get_ip_details import get_ip_details
import mock
import logging


def func(ip):
    return ["10.10.10.0",10]

def func2(ip,port=80):
    return [(2, 0, 0, '', ('127.0.0.1', 80))]
class Mock_Ip(unittest.TestCase):
    """ @mock.patch('socket.gethostbyaddr',side_effect=func)
    def test_ip1(self,mockgethost):
        assert get_ip_details('1.1.1.0')=='10.10.10.0'
        assert get_ip_details('1.1.1.1') == '10.10.10.0'"""
    @mock.patch('socket.getaddrinfo', side_effect=func2)
    @mock.patch('socket.gethostbyaddr', side_effect=func)
    def test_ip2(self, mockgethost,mockgetaddr):
        assert get_ip_details('1.1.1').pop() == '127.0.0.1'

    @mock.patch('get_ip_details.logger')
    @mock.patch('socket.getaddrinfo', side_effect=func2)
    @mock.patch('socket.gethostbyaddr', side_effect=func)
    def test_ip3_log(self, mockgethost, mockgetaddr,mocklog):
        #assert get_ip_details('1.1.1').pop() == '127.0.0.1'
        get_ip_details('1.1.1')
        mocklog.warn.assert_called_with('wrong')
    def test_ip4_log(self):
        logger=logging.getLogger('get_ip_')
        with mock.patch.object(logger,'warn') as mocklog:
            get_ip_details('1.1.1')
            mocklog.assert_called_once_with('wrong')


