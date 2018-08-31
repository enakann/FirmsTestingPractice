import unittest
import sys
from json_utilities import read_json_file


import StringIO
sys.path.append("..")
from settings import CONFIG_PATH,LOG_CFG_PATH,ROOT_DIR
from excel_to_json_converter import excel_to_json_convert
from fpb_pre_process import prepare_data,get_ip_details,get_subnet_details,port_format
from fw_json_validator import validate_json,sanitize_port,get_ip_details
from time import time
from datetime import datetime,date
from mock import Mock,patch,MagicMock,call
def gettime():
    today = str(date.today())
    (yy, mm, dd) = today.split('-')

    # Get timestamp
    curr_time = datetime.now().strftime("%H:%M:%S")
    curr_time = curr_time.replace(':', '')
    return (yy,mm,dd,curr_time)

class ExcelToJsonTest(unittest.TestCase):
    @classmethod
    def SetUpClass(cls):
        json_file = None
        logfile = None
        json_data = None
    @classmethod
    def update(cls, attr,value):
        #ExcelToJsonTest.__dict__[attr]=value
        #self.__class__.__dict__[attr]=value
        setattr(cls, attr, value)

    """def test_xl_to_json(self):
        yy, mm, dd, curr_time=gettime()
        self.logfile = ROOT_DIR + r"\log" + "test_preprocess" + "__" + yy + mm + dd + "__" + str(curr_time) + '.log'
        #capturedOutput = StringIO.StringIO()  # Create StringIO object
        #sys.stdout = capturedOutput  # and redirect stdout.
        self.json_file=excel_to_json_convert("180809-000430.xlsx")
        #sys.stdout = sys.__stdout__  # Reset redirect.
        #out = capturedOutput.getvalue()
        #ls = out.split("\n")
        #print(ls)"""
    """def test_vaidatejson(self):
        #preprocess-->excel_to_json_coverter--->preprocess-->validate_json(fw_json_validator.py)-->[is_valid_protocol,is_valid_format--->[get_ip_details],is_valid_port-->[sanitize_port]]
        yy, mm, dd, curr_time = gettime()
        logfile=self.logfile = ROOT_DIR + r"\log" + "test_preprocess" + "__" + yy + mm + dd + "__" + str(curr_time) + '.log'
        is_valid_json = validate_json("180809-000430.json",logfile)
        print(is_valid_json)"""
    def test_1read_json_file(self):
        print("ran first")
        json_data_out=read_json_file("180809-000430.json")
        self.update('json_data',json_data_out)
        #print(self.json_data)
        #self.__class__.json_data = json_data_out
    #<------Prepare_data----------->
    #port

    def test_sanitize_port(self):
        port=sanitize_port("443.0")
        print(port)

    def test_port_format(self):
        port_list = port_format("443.0")
        print(port_list)

    #subnet
    def test_get_subnet_details(self):
        src_dst_ip_int=get_subnet_details("10.94.207.184")
        print(src_dst_ip_int)

    #ip_details
    """def test_get_ip_details(self):
        (is_valid_input, dst_ip_details) = get_ip_details("10.94.207.184")
        print(is_valid_input,dst_ip_details)"""


    def test_prepare_date(self):
        #prepare_date(fpb_preprocess.py)-->[get_subnet_details.get_ip_details]
        #print(self.json_data)
        (data_to_load,no_of_batches)=prepare_data ( self.json_data, "kannan", 111222, 1409 )
        print(data_to_load,no_of_batches)


    def test2(self):
        mock_print = MagicMock()
        with patch('__builtin__.print', mock_print):
            excel_to_json_convert("180809-000430.xlsx")
            #print(mock_print.call_args)
        #print(mock_print.call_args)
        print(mock_print.call_args_list)
        mock_print.assert_has_calls( [call([u'SOURCE_SUBNET_NAME', u'SOURCE_SUBNET', u'DESTINATION_PORT/RANGE', u'DESTINATION_SUBNET_NAME', u'DESTINATION_SUBNET', u'PROTOCOL']),
 call(u'source_subnet_name'),
 call('Generated output file is: ', '180809-000430.json')] )
if __name__=='__main__':
    unittest.main(verbosity=True)