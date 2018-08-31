import os.path

ROOT_DIR = '/home/netauto/FiRMS/builder'
CONFIG_PATH = os.path.join(ROOT_DIR, 'config')
LOG_CFG_PATH = os.path.join(CONFIG_PATH, 'log')

DATABASE = {
    'TNS' : {
        'READ_WRITE' : 'FiRMSReadWriteTNS1',
        'READ_ONLY' : 'FiRMSReadOnlyTNS1'
    }
}

