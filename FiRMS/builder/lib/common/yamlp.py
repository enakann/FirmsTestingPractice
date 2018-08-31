import os

import yaml

class FCGYamlConf(object):

    def __init__(self, filename):
        self.file=filename

    def load(self):
        if (not os.path.isfile(self.file)):
            raise Exception("{} configuration file does not exist".format(self.file))
        
        with open(self.file, 'r') as f:
            self.conf = yaml.safe_load(f.read())
        
        return self.conf

    def conf(self):
        return self.conf

if __name__ == '__main__':
    pass
