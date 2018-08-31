from __future__ import print_function

import socket,netaddr,re,time,datetime,os

from collections import OrderedDict
from netaddr import IPNetwork

# Import custom utlities
from excel_to_json_converter import excel_to_json_convert
from fw_json_validator import validate_json,sanitize_port,get_ip_details
from common.json_utilities import read_json_file
from common.db_utilities import load_data

from settings import CONFIG_PATH,LOG_CFG_PATH,ROOT_DIR

from common.log import Logger


# This python file would be responsible for pre-processing of data

# Function - pre_process
# Input Parameters - Excel Sheet, SR Number and Username,Unix PID
# Description - This function will be responsible to do all the pre-processing
# Return Value - Number of batches

def pre_process (input_file,sr_number,username,unix_proc_no,logfile):

    global logger
    log_json_path = LOG_CFG_PATH + '/logging.json'
    logger = Logger(name='firms_fpb', config_path=log_json_path, log_file=logfile)

    start_excel_time = time.time()
    logger.info ('Pre Process Start Time: {}'. format (start_excel_time))

    # Convert the excel sheet to json
    logger.info ('Convert excel to JSON')
    json_file = excel_to_json_convert (input_file,logfile)
    end_excel_time = time.time() - start_excel_time

    # Validate the json
    logger.info ('Validating JSON')
    is_valid_json = validate_json(json_file,logfile)
    #exit(1)

    # If excel sheet is not valid
    if not is_valid_json:
        logger.error ('Invalid excel sheet provided')
        print ("Invalid excel sheet provided")
        exit(1)

    start_read_json_time = time.time()

    # Read the JSON data
    json_data = read_json_file (json_file)
    end_read_json_time = time.time() - start_excel_time
    print("Total Time Taken for reading json: ", time.strftime("%H:%M:%S", time.gmtime(end_read_json_time)))
    exit(1)

    start_prep_time = time.time()

    # Open the json file and create the data structure for storing into db
    (data_to_load,no_of_batches) = prepare_data ( json_data, username, sr_number, unix_proc_no )

    end_prep_time = time.time() - start_prep_time
    print("Total Time Taken for preparing data: ", time.strftime("%H:%M:%S", time.gmtime(end_prep_time)))

    # Create the insert query and put it here

    insert_query = "insert into incoming_request (sr_number,username,src_ip,dst_ip,port,protocol,id,src_ip_int,dst_ip_int,process_no,unix_process_no,inc_req_row_id,request_date) values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13)"

    start_load_time = time.time()
 
    logger.info ('Loading input data into incoming_request table')
    logger.info ('Load start time: {}'. format (start_load_time))
   
    try:
        #print ("pre processing")
        is_loaded = load_data(data_to_load,insert_query)
    except Exception as e:
        logger.error ('Failed to insert data for pre-processing',e)
        print (e)
  
    end_load_time = time.time()
    total_load_time = end_load_time - start_load_time

    logger.info ('Load end time: {}'. format (end_load_time))

    #print("Total Time Taken for loading the data: ", time.strftime("%H:%M:%S", time.gmtime(total_load_time)))
    

    return no_of_batches


# Function - get_subnet_details
# Input parameters - Subnet
# Description - This function will get the subnet details
def get_subnet_details (subnet):
    ip_int = int(netaddr.IPAddress(subnet))
    return ip_int

def port_format (ports):
    port_l = ports.split(';')
    nums=[]
    for rec in port_l:
        if '-' in rec:
            rng = rec.split('-')
            for i in range(int(rng[0]),int(rng[1])+1):
                nums.append(i)
        else:
            nums.append(int(rec))

    nums.sort()
    nums = list(set(nums))
    ranges = sum((list(t) for t in zip(nums, nums[1:]) if t[0]+1 != t[1]), [])
    iranges = iter(nums[0:1] + ranges + nums[-1:])
    list_r = [str(n) + '-' + str(next(iranges)) for n in iranges]

    each_port=[]
    for r in list_r:
        rng = r.split('-')
        if rng[0] == rng[1]:
            r = rng[0]
        each_port.append(r)

    port_list = ';'.join(each_port)
    return port_list

# Function Name - prepare_data
# Input parameters - json data structure, username and sr_number, unix PID
# Description - This function will prepare the data so that it can be inserted into database table
# Return Value - This will return data structure list of tuples which can be directly inserted into the database
def prepare_data (data,username,sr_number,unix_proc_no):

    unique_data = OrderedDict()
    final_data = []
    count = 1
    index = 1
    unique_rec_num = 0
    regex_ip = re.compile('^\d+\.\d+\.\d+\.\d+$')

    request_date = datetime.datetime.now()
    
    duplicate_counter = 0
    duplicate = None

    # Loop through the records
    for record in data:
        source_ip = ""
        dst_ip = ""
        source_ip_int = None
        dest_ip_int = None
        src_ip_details = {}
        dst_ip_details = {}
        is_valid_input = None

        for key in record:
            value = str(record[key])
            value = re.sub(r'\s+|\n+|\r+', '', value)
            if key == 'source':
                if '/32' in value:
                    value = re.sub(r'\/32','',value)

                # If subnet is provided then insert that directly
                if '/' in value:
                    (head,tail) = value.split('/')
                    source_ip_int = get_subnet_details (head)
                    source_ip = value
                    src_ip_details[source_ip] = source_ip_int
                # If IP or hostname is provided then insert equivalent integer also
                else:
                    (is_valid_input,src_ip_details) = get_ip_details (value)
                    if is_valid_input:
                        source_ip = value

            if key == 'dest-port':
                 port = str(value)
                 port = sanitize_port(port)
                 port_list = port_format (port)

            if key == 'destination':
                if '/32' in value:
                    value = re.sub(r'\/32','',value)

                # If subnet is provided then get the portion before / and then get the int value
                if '/' in value:
                    (head,tail) = value.split('/')
                    dest_ip_int = get_subnet_details (head)
                    dest_ip = value
                    dst_ip_details[dest_ip] = dest_ip_int
                # If IP or hostname is provided then insert equivalent integer also
                else:
                    (is_valid_input,dst_ip_details) = get_ip_details (value)
                    if is_valid_input:
                        dest_ip = value

            if key == 'protocol':
                protocol = value

            if key == 'input_row_id':
                rec_no = value

        unique_key = str(source_ip) + str(dest_ip) + str(port) + str(protocol)

        if unique_key not in unique_data.keys():
            unique_data[unique_key] = 1
            for each_src_ip in src_ip_details:
                for each_dst_ip in dst_ip_details:
                    unique_rec_num += 1
                    final_data.append ( (sr_number,username,each_src_ip,each_dst_ip,port_list,protocol,unique_rec_num,src_ip_details[each_src_ip],dst_ip_details[each_dst_ip],index,unix_proc_no,rec_no,request_date) )

        else:
            logger.info ('Duplicate record found at line number: {}'. format (rec_no))
            print ("Duplicate record found at line number : ",rec_no)
            duplicate = 1

        count += 1

        # Form batches of 20 records
        if count == 20:
            count = 1
            index += 1

    if duplicate == 1:
        logger.error ('Exiting, since duplicate records found')
        print ("Exiting, since duplicate records found")
        exit(1)

    #print ("Total number of records in input file:", rec_no-1) 
    return (final_data,index)

