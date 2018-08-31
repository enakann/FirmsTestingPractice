import unittest
from mock import patch
from logging_mock_demo1 import check_value

class MyUnitTest(unittest.TestCase):

    @patch('logging_mock_demo1.logging')
    def test_check_value_logs_warning(self, mock_logging):
        check_value({}, 'key')
        #self.assertTrue(mock_logging.warn.called)
        #mock_logging.assert_called_once_with('failed')
        mock_logging.warn.assert_called_with("failed")

if __name__ == '__main__':
    unittest.main()