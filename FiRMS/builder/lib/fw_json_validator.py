from __future__ import print_function

import sys
from collections import OrderedDict
import simplejson as json
import json
import re
import socket
import time
import netaddr

from common.log import Logger

from settings import LOG_CFG_PATH

def is_valid_format(col,value):

    # Strip out whitespaces
    new_value = re.sub(r'\s+|\r+|\n+', '', value)
    if len(new_value) == 0:
        retVal = "Error: Column " + col + " is empty"
        return retVal

    # Check for subnet
    if '/' in new_value:
        try:
            temp = netaddr.IPNetwork(new_value)
            return "Check Passed"
        except Exception as e:
            logger.error ('Invalid subnet passed {} ' .format( new_value ),exc_info=True )
            return "Error: Invalid input passed " + value
    
    else:
        # Check for IP for hostname
        (is_valid_input, ret_value) = get_ip_details (value)
        if is_valid_input:
            return "Check Passed"
        else:
            logger.error ('Invalid address passed {} ' .format( value ),exc_info=True )
            return "Error: Invalid input passed,failed resolution " + value


# Function - get_ip_details
# Input parameters - IP or hostname
# Description - This function will get the ip details
# Return Value - This will return the start_l and end_l
def get_ip_details (host):

    ips = set()
    hostname = None
    ip_details = {}
   
    if re.match ('^\d+\.\d+\.\d+\.\d+',host):
        try:
            hostname = socket.gethostbyaddr(host)[0]
        except Exception as e:
            logger.error ('IP couldnt be resolved {}' .format (e),exc_info=True )
            pass
    else:
        hostname = host

    # If we are able to resolve IP to Host then attempt to find out if there are multiple IP's
    if hostname:
        try:
            out=socket.getaddrinfo(hostname,80)
            for ip in out:
                if re.match("((\d+\.){3}\d+)$",ip[-1][0]):
                    ips.add(ip[-1][0])
        except Exception as e:
            logger.error ('IP couldnt be resolved {}' .format (e),exc_info=True )
            # If we fail to resolve multiple IP scenario go ahead with just the IP
            ips.add(host)
            pass
    else:
        # If earlier we were not able to resolve IP to host then just add Input IP
        ips.add (host)

    error = ""
    for each_ip in ips:
        try:
            ip_int = int(netaddr.IPAddress(each_ip))
            ip_details[each_ip] = ip_int
        except Exception as e:
            error = error + 'Invalid IP passed: ' + each_ip
            logger.error ('Invalid IP passed {}' .format (e),exc_info=True )
            
    if len(error) > 0:
        return (0,error)

    print (ip_details)
    
    return (1,ip_details)


def sanitize_port (port):

     # Get rid of .0, spaces new line and \r 
     port = re.sub(r'\.0+',"",port)
     port = re.sub(r'\s+|\n+|\r+', '', port)

     # Get rid of starting ending semi-colon
     port = re.sub('^;+|;+$','',port)

     # Get rid of multiple consecutive semi-colons
     port = re.sub(';+',';',port)

     # Get rid of multiple consecutive - in case of range
     port = re.sub('-+','-',port)

     port = re.sub('(?i)ANY','0-65535',port)
     port = re.sub('(?i)ALL','0-65535',port)

     return port
 


def is_valid_port_format(port):
     
     ret = "Check passed"
     port_orig = port

     port = sanitize_port(port)

     if len(port) == 0:
         return "Error: Port is empty"
           
     pattern = re.compile(r'^(\d+|\d+-\d+)((;(\d+|\d+-\d+))+)?$')
     if pattern.match(port):
         splitted_ports = port.split(";")
         for p in splitted_ports:
             if '-' in p:
                 port_range = p.split("-")
                 if int(port_range[0]) > int(port_range[1]):
                     ret = "Error: Invalid port number passed " + port_orig
                 elif not 0 <= int(port_range[0]) <= 65535:
                     ret = "Error: Invalid port number passed " + port_orig
                 elif not 0 <= int(port_range[1]) <= 65535:
                     ret = "Error: Invalid port number passed " + port_orig
             else:
                 if not 0 <= int(p) <= 65535:
                     ret = "Error: Invalid port number passed " + port_orig
     else:
         ret = "Error: Invalid port passed " + port_orig

     return ret


def is_valid_protocol(protocol):

    # The passed string should be either TCP or UDP
    p = re.sub(r'\s+|\n+|\r+', '', protocol)
  
    if len(p) == 0:
        return "Error: Protocol is empty "
    
    if re.search(r'\bTCP\b',p):
        return "Check passed"
    elif re.search(r'\bUDP\b',p):
        return "Check passed"
    else:
        return "Error: Invalid Protocol it should be either TCP or UDP " + protocol


def validate_json (input_file,logfile):

    log_json_file = LOG_CFG_PATH + '/logging.json' 
    global logger
    logger = Logger(name='firms_fpb', config_path=log_json_file, log_file=logfile)

    with open(input_file) as json_data:
        jsonData = json.load(json_data)

    # print the keys and values
    count = 0
    all_errors = OrderedDict()
    final_errors = ""
 
    for rec in jsonData:
        for key,value in rec.iteritems():
            line_number = str(rec['input_row_id'])

            #  Check 1 - Value should not be empty
            if key not in 'protocol' and not value:
                retVal = " Error : Record number :" + line_number + " Column " + key + " is empty \n"
                final_errors += retVal
                continue

            # Check 2 - Only ASCII characters allowed
            try:
                temp_val = str(value)
                temp_val.encode('ascii')
            except:
                retVal = "Error : Record number : " + line_number + " Column " + str(key) + " has non ASCII character \n"
                final_errors += retVal
                continue
 
            # Check 3 - Valid values
            if key == 'source':
                retVal = is_valid_format(key, str(value))
            elif key == 'dest-port':
                retVal = is_valid_port_format(str(value))
            elif key == 'destination':
                retVal = is_valid_format(key, str(value))
            elif key == 'protocol':
                retVal = is_valid_protocol(str(value))
            elif key == 'input_row_id':
                retVal = "Check passed"

            if 'Error' in retVal:
                final_errors += "Record number: " + line_number + " " + str(retVal) + "\n"           
          
        count += 1
 

    logger.info ('Total records {}' .format( count ) )
    print ('Total records : ', count )

    # IF there are validation errors
    if final_errors:
        pattern = re.compile('(.*?).json')
        match = pattern.match (input_file)
        filename = match.group(1)
        new_filename = filename.replace ( "data", "out" )

        curr_time = time.time()
        output_filename = new_filename + '__val__errors__' + str(curr_time) + '.' + 'txt'
       
        # Write to file
        try:
            with open(output_filename, 'w') as f:
                f.write(final_errors)
            print ("Input file parsing errors generated at : ", output_filename)
            logger.info ('Excel validation errors generated at : {}' . format(output_filename))
            print ("\nExiting FiRMS Gen, failed to validate input file \n")
            exit(1)
        except Exception as e:
            print ("Failed to create validation errors file",e)
            logger.error ('Failed to create validation errors file {}' . format(e))
            exit(1)


    return (count) 

if __name__ == "__main__":
    # Get the input excel sheet
    input_file= sys.argv[1];

    print ("Input file received is ", input_file)

    validate_json(input_file)
