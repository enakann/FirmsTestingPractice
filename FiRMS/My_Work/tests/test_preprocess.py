
import  unittest2
import sys
import socket
import argparse
import HtmlTestRunner
from excel_to_json_converter import excel_to_json_convert
from fpb_pre_process import pre_process, prepare_data,get_ip_details,get_subnet_details,port_format,mock_func_test
from fw_json_validator import validate_json,sanitize_port
from common.json_utilities import read_json_file
import mock
from mock import call,patch,MagicMock
from utils.SetUpSingleton import TestSuiteSetUp
import fpb_pre_process
class BaseTest:
      @classmethod
      def getConfig(cls):
        	return TestSuiteSetUp('tsrno456','test_180816-000213.xlsx').config()
      @staticmethod
      def messager(msg='assert OK'):
        	print msg
        	return True
      @classmethod
      def update(cls, attr,value):
         setattr(cls, attr, value)


      def assertingPrint(self,*args,**kwargs):
        try:
    	   func,params = args[0], args[1:]
	except TypeError, IndexError:
           raise
        mock_print = MagicMock()
        with patch('__builtin__.print', mock_print):
            func(*params)
        calls=[call(x) for x in kwargs['print_calls']]
        print(calls)
        print(mock_print.call_args_list)
        mock_print.assert_has_calls( calls )
      

      def assertingLog(self,*args,**kwargs):
        try:
	   patch_mod,func,params=args[0],args[1],args[2:]
        except TypeError, IndexError:
           raise
	calls=[call(x) for x in kwargs['log_calls']]
	
        @mock.patch(patch_mod)
        def _logAssertWithMock(mocklog):
            mock_foo=mocklog.return_value
            func(*params)
            mock_foo.info.assert_has_calls(calls)

	_logAssertWithMock()
      





       



class ExcelToJsonAndJsonValidator(BaseTest,unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        (cls.srno,cls.username,cls.pid,cls.input_file,cls.logfile)=cls.getConfig()



    def test1_XlsToJson(self):
        json_file_name=excel_to_json_convert(self.input_file,self.logfile)
	self.update('json_file',json_file_name)
	self.assertEqual(self.json_file,'test_180816-000213.json', msg="Created json_file is  {} but the Expected file is {}".format(self.json_file,'180809-000430.json'))
        self.messager("Excel to Json passed")



    def test2_ValidateJson(self):
	json_row_count = validate_json(self.json_file,self.logfile)
	self.assertEqual(json_row_count,15, msg="Excel To Json data row count doesnt match")
        self.messager("Json Validatin passed")



    def test3_ReadJsonFile(self):
        json_data_out=read_json_file(self.json_file)
        self.update('json_data',json_data_out)
        self.messager("Reading json passed")
 
    def test4_PrintXlsToJson(self):
         self.assertingPrint(excel_to_json_convert,"180809-000430.xlsx",self.logfile,print_calls=['in excel_to_json_convert'])


    def test5_LogXlsToJson(self):
        ls=['logging excel_to_json_convert',r"Column Names in input excel [u'SOURCE_SUBNET_NAME', u'SOURCE_SUBNET', u'DESTINATION_PORT/RANGE', u'DESTINATION_SUBNET_NAME', u'DESTINATION_SUBNET', u'PROTOCOL']",'Generated JSON file is 180809-000430.json']
        self.assertingLog("excel_to_json_converter.Logger",excel_to_json_convert,"180809-000430.xlsx",self.logfile,log_calls=ls)

class TestPreProcess(BaseTest,unittest2.TestCase):


    @classmethod
    def setUpClass(cls):
        (cls.srno,cls.username,cls.pid,cls.input_file,cls.logfile)=cls.getConfig()
        cls.json_file=excel_to_json_convert(cls.input_file,cls.logfile)
        cls.json_data=read_json_file(cls.json_file)



    def test_sanitize_port(self):
        self.assertEqual('443',sanitize_port("443.0"),msg="Failed to sanitize")
        self.assertEqual('3870-3890;4888',sanitize_port("3870-3890;4888"))
        self.assertEqual('3870-3890;4888',sanitize_port(";;3870-3890;4888;"),msg="3rd port test failed")
        self.assertEqual(';3870-3890;4888;',sanitize_port(";3870-3890;;4888;"),msg="4th port test failed")
        self.assertEqual('3870-3890;4888\n',sanitize_port("3870-3890;4888"),msg="5th port test failed")
        self.messager("Port sanitization  passed")




    def test_port_format(self):
        self.assertEqual('443',port_format("443"),msg="port formatting failed")
        self.assertEqual('1500-1999;3872-3885;6000-6999',port_format("3872-3885;1500-1999;6000-6999"),msg="port formatting failed")
        self.messager("Port Formatting passed")



    def test_get_subnet_details(self):
        self.assertEqual(173985720,get_subnet_details("10.94.207.184"),msg="get_subnet failed")
        self.assertEqual(170014336,get_subnet_details("10.34.54.128"),msg="get_subnet failed")
        self.messager("get_subnet_detailed passed")




    def test_get_ip_details(self):
        self.assertEqual(('10.94.207.184', 173985720),get_ip_details("10.94.207.184"),msg="Failure in getting ip")
        self.assertEqual(('10.47.2.11', 170852875),get_ip_details("CHOTM705SEDIS01.usdc2.oraclecloud.com"),msg="Failure in getting ip")
        self.assertEqual(('144.23.144.237', 2417463533),get_ip_details("aufsn4x0jkf05.oracleoutsourcing.com"),msg="Failure in getting ip")
        
        self.assertRaises(socket.gaierror,lambda:get_ip_details("1.1.1.d"))
        
        with self.assertRaises(socket.gaierror) as context:
               get_ip_details("1.1.1.d")
        exception=context.exception
        expected_msg="Name or service not known"
        actual_msg=exception.args[-1]
        self.assertEqual(expected_msg,actual_msg)


    
    def test_prepare_date(self):
        (data_to_load,no_of_batches)=prepare_data ( self.json_data, self.username, self.srno,self.pid)
        self.assertEqual(1,no_of_batches,msg="no of batch is wrong")
        self.assertEqual(15,len(data_to_load),msg="mismatch in no of input and output data")
        self.assertEqual(('tsrno456', 'netauto', '10.59.169.37', '12.38.120.138', '22', 'TCP', '1', 171682085, 203847818),data_to_load[0][:-4])
        self.assertEqual(('tsrno456', 'netauto', '10.72.150.0/26', '10.72.158.162', '443', 'TCP', '15', 172529152, 172531362),data_to_load[-1][:-4])
        #insert into incoming_request (sr_number,username,src_ip,dst_ip,port,protocol,id,src_ip_int,dst_ip_int,process_no,unix_process_no,inc_req_row_id,request_date)
        #print(data_to_load,no_of_batches)
   


    def test_load_data(self):
         with mock.patch('fpb_pre_process.load_data') as MockHelper:
            insert_query = "insert into incoming_request (sr_number,username,src_ip,dst_ip,port,protocol,id,src_ip_int,dst_ip_int,process_no,unix_process_no,inc_req_row_id,request_date) values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)"
            #input_file,sr_number,username,unix_proc_no,logfile)
            #(cls.srno,cls.username,cls.pid,cls.input_file,cls.logfile)
            no_of_batches= pre_process ( self.input_file,self.srno,self.username,self.pid,self.logfile )
         print(MockHelper.call_args)
         self.assertTrue(MockHelper.called)
    """def test_mock_func(self):
         with mock.patch('fpb_pre_process.mock_func') as MockHelper:
           mock_func_test(1,2)
         MockHelper.assert_called_once_with(1,2)"""
        



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Firms Test Suite Runner')
    parser.add_argument("-r",'--runner',
                        help='Type of Runner Require(Text or Html)',
                        default='Text')
    results = parser.parse_args()
    runner=results.runner

    JsonTest = unittest2.TestLoader().loadTestsFromTestCase(ExcelToJsonAndJsonValidator)
    PreProcessTest = unittest2.TestLoader().loadTestsFromTestCase(TestPreProcess)
    suite = unittest2.TestSuite([JsonTest,PreProcessTest])

	
    if runner=='Text':
    	unittest2.TextTestRunner(verbosity=2).run(suite)
    else:
        HtmlTestRunner.HTMLTestRunner(output="Htmloutdir").run(suite)

(FiRMS-venv1) bash-4.2$ 