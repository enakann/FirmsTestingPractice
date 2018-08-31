from __future__ import print_function

import xlrd
import sys
import re
import io

from collections import OrderedDict
import simplejson as json

from common.log import Logger

from settings import LOG_CFG_PATH

def excel_to_json_convert (input_file,logfile):

    log_json_file = LOG_CFG_PATH + '/logging.json'
    global logger
    logger = Logger(name='firms_fpb', config_path=log_json_file, log_file=logfile)

    # Open the workbook and select the first worksheet
    wb = xlrd.open_workbook(input_file)
    sh = wb.sheet_by_index(0)

    # List to hold dictionaries
    firewall_list = []

    column_names = sh.row_values(0)

    logger.info ('Column Names in input excel {}'. format (column_names) )

    col1 = column_names[0].lower()
    pattern = r'(^|[^\w]){}([^\w]|$)'.format(col1)
    src_matches = re.search(pattern, col1)

    if not src_matches:
        logger.info ('Input file is in invalid format, first column should denote Source')
    #    print ("Input file is in invalid format, first column should denote Source")
    #    exit (1)

    col2 = column_names[1].lower()
    pattern = r'(^|[^\w]){}([^\w]|$)'.format(col2)
    ip_matches = re.search(pattern, col1)
    pattern = re.compile(r'(ip|subnet)')
    if not pattern.search(col2):
        logger.info ('Input file is in invalid format, second column should denote Source IP or Source Subnet')
    #    print("Input file is in invalid format, second column should denote Source IP or Source Subnet")
    #    exit(1)

    col3 = column_names[2].lower()
    pattern = re.compile(r'(port)')
    if not pattern.search(col3):
        logger.info ('Input file is in invalid format, third column should denote port')
    #    print("Input file is in invalid format, third column should denote port")
    #    exit(1)

    col4 = column_names[3].lower()
    pattern = re.compile(r'(destination)')
    if not pattern.search(col4):
        logger.info ('Input file is in invalid format, fourth column should denote Destination')
    #    print ("Input file is in invalid format, fourth column should denote Destination")
    #    exit(1)

    col5 = column_names[4].lower()
    pattern = re.compile(r'(ip|subnet)')
    if not pattern.search(col5):
        logger.info ('Input file is in invalid format, fifth column should denote Destination IP or Destination Subnet')
    #    print ("Input file is in invalid format, fifth column should denote Destination IP or Destination Subnet")
    #    exit(1)

    isProtocol = False
   #print(len(column_names))
    if len(column_names) >= 6:
       #print('inside column_names')
        col6 = column_names[5].lower()
        if not re.match("protocol",col6):
            logger.info ('Sixth column should be Protocol')
            print ("Protocol column not provided, defaulting to TCP")
        else:
            isProtocol = True

    # Iterate through each row in worksheet and fetch values into dict
    for rownum in range(1, sh.nrows):

        firewall = OrderedDict()
        row_values = sh.row_values(rownum)

        firewall['source'] = row_values[1]

        dest_port = row_values[2]
        firewall['dest-port'] = dest_port
         
        firewall['destination'] = row_values[4]
        
        if isProtocol:
            if not row_values[5]:
                protocol = 'TCP'
            else:
               #print('insideeeee')
                protocol = row_values[5]
        else:
           #print('else block')
            protocol = 'TCP'
       #print('PROTOCOL')
       #print (protocol,row_values[5])
        firewall['protocol'] = protocol.upper()

        firewall['input_row_id'] = rownum
        firewall_list.append(firewall)

    # Serialize the list of dicts to JSON
    j = json.dumps(firewall_list)

    pattern = re.compile('(.*?).xls')
    match = pattern.match (input_file)
    filename = match.group(1)
    output_filename = filename + '.' + 'json'

    # Write to file
    with open(output_filename, 'w') as f:
        f.write(j)
        

    #print ("Generated output file is: ",output_filename)
    logger.info ('Generated JSON file is {}'. format (output_filename))

    return (output_filename)

if __name__ == '__main__':

    # Get the input excel sheet
    input_file = sys.argv[1];

    # Get the file from command line
    print("Input file received is \t")
    print(input_file)

    excel_to_json_convert (input_file)
