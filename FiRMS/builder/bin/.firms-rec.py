from __future__ import print_function

import sys,getopt,re,os,cx_Oracle,time,netaddr,socket,argparse,multiprocessing,pwd,grp,random

from pprint import pprint
from optparse import OptionParser
from multiprocessing import Pool
from shutil import copyfile
from datetime import datetime,date

import simplejson as json

import getpass

from settings import CONFIG_PATH,LOG_CFG_PATH,ROOT_DIR

# Custom files
from fpb_pre_process import pre_process
from common.db_utilities import extract_data,load_data,call_plsql_proc,delete_all_tbl_data
from fpb_post_process import post_process
from fpb_process import process

from common.log import Logger

log_json_path = LOG_CFG_PATH + '/logging.json'
sys_logger = Logger(name='sys-logger', config_path=log_json_path)

if __name__ == '__main__':

    # Note the start time so as to calculate the time time taken by the script to execute
    start_time = time.time()

    parser = argparse.ArgumentParser()
    
    parser.add_argument("-i", "--input_file", required=True)
    parser.add_argument("-t", "--ticket_number", required=True)

    args = parser.parse_args()

    # Get the excel sheet from the command line
    input_file = args.input_file
 
    # Get the SR Number from the command line
    sr_number  =  args.ticket_number
    sys_logger.info ('SR Number: {}'.format(sr_number))

    # Get the username
    username = getpass.getuser()

    #sys_logger.info ('Username: {}'.format(username))

    # Get current date
    today = str(date.today())
    (yy,mm,dd) = today.split('-')
    
    # Get timestamp
    curr_time = datetime.now().strftime("%H:%M:%S")
    curr_time = curr_time.replace(':','')

    user_dir = sr_number + '__' + str(curr_time)

    logfile = ROOT_DIR + '/log/' + str(username) + '__' + str(sr_number) + '__' + yy + mm + dd + '__' + str(curr_time) + '.log'

    os.umask (0007)

    logger = Logger(name='firms_fpb', config_path=log_json_path, log_file=logfile)

    logger.info ('Script Start Time: {}'. format (start_time) )
    logger.info ('Input File: {}'.format(input_file))
    logger.info ('Ticket Number: {}'.format(sr_number))
    logger.info ('Username: {}'.format(username))
           
    # Get the output directory name if passed
    output_dir = ROOT_DIR

    new_dir_json = output_dir + '/data/' + username + '/' + yy + '/' + mm + '/' + dd + '/' + user_dir + '/'
    new_dir_txt  = output_dir + '/out/' + username + '/' + yy + '/' + mm + '/' + dd + '/' + user_dir + '/' 

    try:
        logger.info ('Creating data directory at {}'.format (new_dir_json))
        if not os.path.exists(new_dir_json):
            os.makedirs (new_dir_json)

        logger.info ('Creating out directory at {}'.format (new_dir_txt))
        if not os.path.exists(new_dir_txt):
            os.makedirs (new_dir_txt)

    except:
        print ("Failed to create output directory, exiting..")
        logger.error ("Failed to create output directory, exiting {}" .format(e))
        exit(1)


    if os.access(new_dir_json,os.W_OK) is not True:
        logger.error ('Output Directory {} is not writable'. format(new_dir_json))
        print ("Output Directory is not writable", new_dir_json)
        exit(1)

    if os.access(new_dir_txt,os.W_OK) is not True:
        logger.error ('Output Directory {} is not writable'. format(new_dir_txt))
        print ("Output Directory is not writable", new_dir_txt)
        exit(1)


    (path,input_file_name) = os.path.split (input_file)

    # Copy the input file
    dst_file = new_dir_json + input_file_name

    try:
        copyfile (input_file,dst_file)
    except Exception as e:
        logger.error ('Failed to copy input file {}'.format(e))
        print ("Failed to copy input file for processing")
        exit(1)

    logger.info ('Input excel file copied at {}'.format(dst_file))

    print ("\n")
    print ("Input File:", input_file)
    print ("Ticket Number:", sr_number)
    print ("GUID:", username)
    print ("\n")

    unix_proc_no = os.getpid()
    ts = int(time.time())

    unix_proc_no = str(unix_proc_no) + str(ts)

    unix_proc_no = int (unix_proc_no)
    
    logger.info ( 'Process Number: {}'. format(unix_proc_no) )

    logger.info ( 'Pre Processing Start' )
    try:
        no_of_batches = pre_process (dst_file,sr_number,username,unix_proc_no,logfile)
    except Exception as e:
        print ("Failed to pre process the input file",e)
        logger.error ( 'Failed to pre process the input file {}'.format(e) )
        exit(1)

    exit(1)
    logger.info ('Number of batches {}'. format( no_of_batches) )
    plsql_start_time = time.time()
   
    logger.info ('FiRMS Engine execution start time: {}'. format (plsql_start_time))

    print ("\n")

    print ("Processing .....")

    logger.info ( 'Processing Start, call FiRMS Engine' )

    try:
        process (no_of_batches,unix_proc_no,logfile)
    except Exception as e:
        print ("Failed to process the input file, FiRMS engine failed")
        logger.error ( 'Failed to process the input file, FiRMS engine failed {}'.format(e) )
        exit(1)
       
    plsql_end_time = time.time()
    total_time_taken_pl_sql = plsql_end_time - plsql_start_time

    #logger.info ('FiRMS Engine execution end time: {}'. format (plsql_end_time))
    logger.info ('FiRMS Engine execution end time: {}'. format (plsql_end_time))
    logger.info ('Total Time Taken for data processing: {}'. format( time.strftime("%H:%M:%S", time.gmtime(total_time_taken_pl_sql)) ))

    #print("Total Time Taken for data processing: ", time.strftime("%H:%M:%S", time.gmtime(total_time_taken_pl_sql)))

    print ("Done")

    print ("\n")

    logger.info ( 'Post Processing Start' )

    try:
        # After the data is processed, do post processing
        is_post_processed = post_process (sr_number,username,unix_proc_no,input_file,new_dir_json,new_dir_txt,logfile)
    except Exception as e:
        print ("FiRMS Post Processing failed",e)
        logger.error ( 'FiRMS Post Processing failed {}'. format(e) )
        exit(1)
        
    os.umask (0022)

    # Cleanup the incoming_request table                                       
    delete_query = "delete from incoming_request where unix_process_no=:1" 
    bind_data = (unix_proc_no,)
    #delete_all_tbl_data(delete_query,bind_data) 

    print ("\n")

    elapsed_time = time.time() - start_time
    print("Total time taken: ", time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))

    logger.info ( 'Script End Time: {}'. format (elapsed_time) )
    logger.info ('Total time taken: {}' . format ( time.strftime("%H:%M:%S", time.gmtime(elapsed_time))) )

    print ("\n")
