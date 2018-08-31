import os.path
ROOT_DIR = r'D:\my_Python\py_projects\FirmsTestingPractice\FiRMS\My_Work'
CONFIG_PATH = os.path.join(ROOT_DIR, 'config')
LOG_CFG_PATH = os.path.join(CONFIG_PATH, 'log')

DATABASE = {
    'TNS' : {
        'READ_WRITE' : 'FiRMSReadWriteTNS1',
        'READ_ONLY' : 'FiRMSReadOnlyTNS1'
    }
}

