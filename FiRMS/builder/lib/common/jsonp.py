#
# Module reads json configuration file
# 
import os, sys
import json

class FCGJsonConf(object):
    def __init__(self, filename):
        self.file = filename

    def load(self):
        if (not os.path.isfile(self.file)):
            raise Exception("{} configuration file does not exist".format(self.file)) 

        with open(self.file) as json_data:
            self.__conf = json.load(json_data)

	return self.__conf
    
    def conf(self):
        return self.__conf

if __name__ == '__main__':
    pass
