import sys
import inspect

class FirmsBusinessCoreException(Exception):
 
    """
      Base class for all exceptions raised by it's subclasses

    """
   
    def __init__(self, info, excp=None):

        super(FirmsBusinessCoreException,self).__init__(info)
        
        self.info      = info 
        self.exception = excp
        self.name      = self.__class__.__name__

class FirmsNotEnoughCPUException(FirmsBusinessCoreException):
    """ raised when CPU idle percent is less than threshold """
    pass

class FirmsEnvException(FirmsBusinessCoreException):
    """ IO/OS exception """
    pass

class FirmsNetConfConnException(FirmsBusinessCoreException):
    """ parent class for all connection related exceptions """
    pass

class FirmsNetConfRPCException(FirmsBusinessCoreException):
    """ parent class for all junos-pyez RPC Exceptions """
    pass

class FirmsAnyMethodConnException(FirmsBusinessCoreException):
    """ raised when it's unable to connect to device using any 
    of the method defined in the config file """
    pass
