import sys
sys.path.append('.')
import os
import signal,subprocess
from multiprocessing import Pool,cpu_count
from common.db_utilities import call_plsql_proc

from common.log import Logger

from settings import LOG_CFG_PATH

#def handler(signum, frame):
#    print('Ctrl+Z pressed,terminating now')
#    print (os.getpid(),os.getppid())
#    parent_id = os.getpid()
#    ps_command = subprocess.Popen("ps -o pid --ppid %d --noheaders" % parent_id, shell=True, stdout=subprocess.PIPE)
#    ps_output = ps_command.stdout.read()
#    retcode = ps_command.wait()
#    for pid_str in ps_output.strip().split("\n")[:-1]:
#        print (pid_str)
#        os.kill(int(pid_str), signal.SIGTERM)
#    
#    os.kill (int(parent_id),signal.SIGKILL) 
#    exit(1)

def init_worker():
    #signal.signal(signal.SIGTSTP, handler)
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)


# Function name - process
# Parameters - Number of batches
# Description - This function would call the PL/SQL required for processing
# Return Value - 1 or 0 depending on whether all the processes finished or not
def exec_process (process_no):

    (p,unix_pid) = process_no.split('-')
    
    p = int(p)
    unix_pid = int(unix_pid)

    p += 1

    try:
        call_plsql_proc("FiRMS_ENGINE.REQUEST_PROCESSOR",p,unix_pid)
    except KeyboardInterrupt:
        raise
    except Exception as e:
        logger.error ('Error occurred while processing {}'. format (e) )
        return ("ERROR") 

    return 1


# Function name - process
# Parameters - Number of batches
# Description - This function would do the parallel processing
# Return Value - 1 or 0 depending on whether all the processes finished or not
def process (num_of_batches,unix_pid,logfile) :

    global logger
    log_json_file = LOG_CFG_PATH + '/logging.json'
    logger = Logger(name='firms_fpb', config_path=log_json_file, log_file=logfile)
  
    batch_range = range(num_of_batches)

    unix_pid = str(unix_pid)

    batch_range = map(lambda x:'{}-{}'.format(x,unix_pid),batch_range)

    p = Pool(8,init_worker)
    
    try:
        results = []
        r = p.map_async(exec_process,batch_range,callback=results.append)
        r.wait()

        if 'ERROR' in results[0]:
            print ("Error occurred while processing FiRMS engine, exiting now")
            p.terminate()
            p.join()
            exit(1)
            
        p.close()
        p.join()
    except KeyboardInterrupt:
        print ("Process killed by user")
        logger.error ('Process was interrupted by the user, process exited')
        p.terminate()
        p.join()
        exit(1)
    except Exception as e:
        logger.error ('Error occurred while processing {}'. format (e) )
        p.terminate()
        #raise
        

    return 1
