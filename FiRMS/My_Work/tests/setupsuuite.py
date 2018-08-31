
from settings import CONFIG_PATH,LOG_CFG_PATH,ROOT_DIR
from common.log import Logger
from datetime import datetime,date
import getpass
import os


class Singleton(type):
    _instance = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
                cls._instance[cls]=super(Singleton,cls).__call__(*args, **kwargs)
        return cls._instance[cls]



class TestSuiteSetUp:
    __metaclass__ = Singleton
    def __init__(self,srno,input_file):
          self.srno=srno
          self.input_file=input_file
          self.username=getpass.getuser()
          self.logfile=None
          self.pid=os.getpid()
    def config(self):
	 log_json_path = LOG_CFG_PATH + '/logging.json'
   	 (yy,mm,dd) =  str(date.today()).split('-')
   	 curr_time = datetime.now().strftime("%H:%M:%S").replace(':','')
   	 user_dir = str(self.srno) + '__' + str(curr_time)
   	 self.logfile = ROOT_DIR + '/log/' + str(self.username) + '__' + str(self.srno) + '__' + yy + mm + dd + '__' + str(curr_time) + '.log'
   	 return (self.srno,self.username,self.pid,self.input_file,self.logfile)


#obj=TestSuiteSetUp(1000,"test.xlsx")
#logfile=obj.config()
#print(logfile)

(FiRMS-venv1) bash-4.2$ 