from common.log import Logger

logger = Logger(name='firms_fpb', config_path='/FiRMS/builder/config/log/logging.json', log_file="/FiRMS/builder/log/logfile")
#logger = Logger(name='firms_fpb', config_path='/FiRMS/builder/config/log/logging.json')
sys_logger = Logger(name='sys-logger', config_path='/FiRMS/builder/config/log/logging.json')

logger.info ('test')
sys_logger.info("test1")
