from __future__ import print_function

import sys
import re
import os
import cx_Oracle
import time
import netaddr
from pprint import pprint

#from log import Logger
##logger = Logger(name='firms-fpb', config_path='/FiRMS/builder/config/log/logging.json')


# Function Name - connect_db
# Input Parameters - None
# Description - This function will connect to the database using cx_Oracle
# Return Value - Connection String
def connect_db ():
    try:
        #logger.info ('Connecting to database')
        con = cx_Oracle.connect ('/@FiRMSReadWriteTNS1')
        #con = cx_Oracle.connect ('/@FiRMSReadWriteNoEncTNS1')
        return con
    except cx_Oracle.DatabaseError as e:
        #print (e)
        print ("Database connection error : ")
        print ("Exiting from the script now ...")
        #logger.error ('Database connection error: {}'. format (e))
        exit(1)


# This is a dedicated file with collection of DB related functions

# Function name - load_data
# Parameters - DB Connection String, Data to be loaded (list of tuples), Query, addl_para
# Description - Insert the data into the table
# Return Value - Number of records inserted
def load_data ( data, insert_query ):

    conn = connect_db()

    cursor = conn.cursor()

    try:
        #logger.info ('Preparing DB stmt {}'. format(insert_query))
        cursor.prepare(insert_query)
        #logger.info ('Executing DB stmt {}'. format(insert_query))
        cursor.executemany(insert_query,data)
    except Exception as e:
        print ("Failed to load the data for processing by FiRMS engine",e)
        #logger.error ('Failed to load the data for processing {}'. format(insert_query))
        #logger.error ('Database error {}'. format(e))
        #print (e)
        exit(1)

    conn.commit()

    #conn.close()

    return 1

# Function name - extract_data
# Parameters - DB Connection, Query
# Description - This function will do a simple select from the table based the query that is passed
# Return Value - Data structure containing all the records extracted from the table
def extract_data ( select_query,bind_data ):

    conn = connect_db()
    # Get the cursor
    cursor = conn.cursor()

    try:
        #logger.info ('Executing DB stmt {}'. format(select_query))
        cursor.execute(select_query,bind_data)
        ret_data = cursor.fetchall()
    except Exception as e:
        print ("Failed to extract the data for post processing")
        #print (e)
        #logger.error ('Failed to extract the data {}'. format(select_query))
        #logger.error ('Database error {}'. format(e))
        #exit(1)
        raise

    #conn.close()

    return ret_data


# Function name - call_plsql_proc
# Parameters - Name of the PL/SQL proc
# Description - This function will call the PL/SQL proc
# Return Value - 1 if success and 0 otherwise
def call_plsql_proc (name,process_no,unix_pid):

    # Connect to the database
    conn = connect_db()
   
    param = (process_no,unix_pid)

    cursor = conn.cursor()
    id = cursor.var(cx_Oracle.NUMBER)

    try:
        cursor.callproc ( name, param )
        return 1
    except Exception as e:
        #logger.error ('Failed to process FiRMDS engine {}'. format(name))
        #logger.error ('Database error {}'. format(e))
        #print ("inside db_util error")
        #print (e)
        #print ("FiRMS Engine failed to process, exiting now")
        raise

    try:
        conn.close()
    except:
        pass


# Functiona name - delete_all_tbl_data
# Parameters - name of table
# Description - This function will delete all the records for the table passed
# Return Value - None
def delete_all_tbl_data ( delete_query, bind_data ):

    # Connect to the database
    conn = connect_db()

    # Get the cursor
    cursor = conn.cursor()

    try:
        cursor.execute(delete_query,bind_data)
    except Exception as e:
        print ("Exception occured while deleting records from table")

    conn.commit()

    #conn.close()
    
    return

# Function name - load_networks_data
# Parameters - DB Connection String, Data to be loaded (list of tuples), Query, addl_para
# Description - Insert the data into the table
# Return Value - Number of records inserted
def load_networks_data ( data, insert_query ):

    conn = connect_db()

    cursor = conn.cursor()

    # Delete the existing data
    delete_query = "delete from networks"
    try:
        conn.execute(delete_query)
    except Exception as e:
        print ("Exception occured while deleting records from networks", e)
        conn.rollback()
        exit(1)

    try:
        #logger.info ('Preparing DB stmt {}'. format(insert_query))
        cursor.prepare(insert_query)
        #logger.info ('Executing DB stmt {}'. format(insert_query))
        cursor.executemany(insert_query,data)
    except Exception as e:
        print ("Failed to load the networks file")
        conn.rollback()
        #logger.error ('Failed to load the data for processing {}'. format(insert_query))
        #logger.error ('Database error {}'. format(e))
        print (e)
        exit(1)

    conn.commit()

    #conn.close()

    return 1

# Function name - load_emds_data
# Parameters - DB Connection String, Data to be loaded (list of tuples), Query, addl_para
# Description - Insert the data into the table
# Return Value - Number of records inserted
def load_emds_data ( data, insert_query ):

    conn = connect_db()

    cursor = conn.cursor()

    # Delete the existing data
    delete_query = "delete from emds_firewall_details"
    try:
        conn.execute(delete_query)
    except Exception as e:
        print ("Exception occured while deleting records from emds_firewall_details table", e)
        conn.rollback()
        exit(1)

    try:
        #logger.info ('Preparing DB stmt {}'. format(insert_query))
        cursor.prepare(insert_query)
        #logger.info ('Executing DB stmt {}'. format(insert_query))
        cursor.executemany(insert_query,data)
    except Exception as e:
        print ("Failed to load the emds_firewall_details table")
        conn.rollback()
        #logger.error ('Failed to load the data for processing {}'. format(insert_query))
        #logger.error ('Database error {}'. format(e))
        print (e)
        exit(1)

    conn.commit()

    #conn.close()

    return 1


if __name__ == '__main__':

    # Establish the connection to the database
    conn = connect_db()

    print (conn)
    exit(1)


