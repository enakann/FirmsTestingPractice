import unittest
from fpb_process import *
import mock
import unittest
import cx_Oracle
import time
import argparse
import getpass


class TestProcess(unittest.TestCase):
    """"@classmethod
    def setUpClass(cls):
        parser=argparse.ArgumentParser()
        parser.add_argument("-i", "--input_file", required=True)
        parser.add_argument("-t", "--ticket_number", required=True)
        print ("Input File:", input_file)
        # 1
        print ("Ticket Number:", sr_number)
        cls.sr_number=sr_number# ------>arg1
        # 2
        username = getpass.getuser()
        print ("GUID:", username)
        cls.username=username  # --------->arg2
        # 3
        unix_proc_no = os.getpid()
        ts = int(time.time())
        unix_proc_no = str(unix_proc_no) + str(ts)
        unix_proc_no = int(unix_proc_no)
        unix_proc_no = os.getpid()
        cls.unix_proc_no=unix_proc_no  # -------->arg3
        # 4
        (path, input_file_name) = os.path.split(input_file)
        dst_file = new_dir_json + input_file_name
        cls.dst_file=dst_file       # ---->arg0
        # 5
        today = str(date.today())
        (yy, mm, dd) = today.split('-')
        curr_time = datetime.now().strftime("%H:%M:%S")
        curr_time = curr_time.replace(':', '')
        user_dir = sr_number + '__' + str(curr_time)
        logfile = ROOT_DIR + '/log/' + str(username) + '__' + str(sr_number) + '__' + yy + mm + dd + '__' + str(
            curr_time) + '.log'
        cls.logfile=logfile# ---->arg5"""
    def test_exec_process(self):
        with mock.patch('fpb_process.call_plsql_proc',side_effect=KeyboardInterrupt) as mockdb:
            exec_process('1-9000')
            self.assertRaises(KeyboardInterrupt)
    def test2_exec_process(self):
        with mock.patch('fpb_process.call_plsql_proc',side_effect=cx_Oracle.DatabaseError("4420","unable to connect")) as mockdb:
            self.assertEqual("ERROR",exec_process('1-9000'))

    def test2_exe3_process(self):
        with mock.patch('fpb_process.call_plsql_proc') as mockdb:
            self.assertEqual(1,exec_process('1-9000'))
            mockdb.assert_called_with("FiRMS_ENGINE.REQUEST_PROCESSOR",2,9000)

    """def test_process(self):
        no_of_batches = pre_process(dst_file, sr_number, username, unix_proc_no, logfile)

        process(no_of_batches,unix_pid,logfile)"""


if __name__ == '__main__':
    unittest.main()


