import simplejson as json
from collections import OrderedDict

#from log import Logger
#logger = Logger(name='firms-fpb', config_path='/home/netauto/FiRMS/builder/config/log/logging.json')

# This file will have the functions only related to JSON

# Function Name - read_json_file
# Input parameters - JSON File
# Description - This function will take json file and convert to a data structure format
# Output - JSON Data structure
def read_json_file (file):

    try:
        with open(file) as json_data:
            jsonData = json.load(json_data,object_pairs_hook=OrderedDict)
    except Exception as e:
         #logger.error ('Failed to open JSON file for reading' . format (e))
         print ('Failed to open JSON file for reading' . format (e))

    return jsonData

# Function Name - write_json_file
# Input parameters - JSON File
# Description - This function will take json data struct and convert into JSON File
# Output - JSON File
def write_json_file (data_struct, output_filename):

    j = json.dumps(data_struct)
    #j = json.dumps(data_struct, ensure_ascii=False).encode('utf8')
    
    # Write to file
    try:
        with open(output_filename, 'w') as f:
            f.write(j)
            #f.write(j.encode("utf-8"))
    except Exception as e:
         #logger.error ('Failed to open JSON file for writing' . format (e))
         print ('Failed to open JSON file for writing' . format (e))

    return 1
