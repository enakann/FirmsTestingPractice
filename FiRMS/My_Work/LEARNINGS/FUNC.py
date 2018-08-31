from Logging_my import Log
import logging
import sys
def func2(a,b):
    logger=logging.getLogger('__main__')
    streamhandler = logging.StreamHandler(sys.stdout)
    logger.addHandler(streamhandler)

    #logger=logging.getLogger('__main__')
    c=None
    try:
        print ("pre processing")
        c=a/b
    except Exception as e:
        logger.error("failed")
    return c