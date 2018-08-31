import re
import netaddr
import socket
import logging
import sys
from Logging_my import Log
#import Logging_my
#logger=Logging_my.Log().init_logger_singleton()
logger=Log().init_logger_singleton()
def get_ip_details(host):

    ips = set()
    hostname = None
    ip_details = {}

    if re.match('^\d+\.\d+\.\d+\.\d+', host):
        try:
            hostname = socket.gethostbyaddr(host)[0]
        except Exception as e:
            logger.warn('IP couldnt be resolved {}'.format(e))
            pass
    else:
        logger.warn('wrong')
        hostname = host
    #return hostname

    # If we are able to resolve IP to Host then attempt to find out if there are multiple IP's
    if hostname:
        try:
            out = socket.getaddrinfo(hostname, 80)
            for ip in out:
                if re.match("((\d+\.){3}\d+)$", ip[-1][0]):
                    ips.add(ip[-1][0])
        except Exception as e:
            logger.error('IP couldnt be resolved {}'.format(e), exc_info=True)
            # If we fail to resolve multiple IP scenario go ahead with just the IP
            ips.add(host)
            pass
    else:
        # If earlier we were not able to resolve IP to host then just add Input IP
        ips.add(host)
    print(ips)
    return ips

    error = ""
    for each_ip in ips:
        try:
            ip_int = int(netaddr.IPAddress(each_ip))
            ip_details[each_ip] = ip_int
        except Exception as e:
            error = error + 'Invalid IP passed: ' + each_ip
            logger.error('Invalid IP passed {}'.format(e), exc_info=True)

    if len(error) > 0:
        return (0, error)

    print (ip_details)

    return (1, ip_details)
import unittest
import mock
class Testip(unittest.TestCase):

    @mock.patch('get_ip_details.logger')
    def test_ip3_log(self, mocklog):
        # assert get_ip_details('1.1.1').pop() == '127.0.0.1'
        get_ip_details('1.1.1')
        mocklog.warn.assert_called_with('wrong')

    def test_ip4_log(self):
        logger = logging.getLogger('__main__')
        with mock.patch.object(logger, 'warn') as mocklog:
            get_ip_details('1.1.1')
            mocklog.assert_called_once_with('wrong')



if __name__ == '__main__':
    unittest.main()