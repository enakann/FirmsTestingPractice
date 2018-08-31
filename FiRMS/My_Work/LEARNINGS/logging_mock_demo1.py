import logging

def check_value(data_dict, value):
    try:
        return data_dict[value] > 10
    except KeyError:
        #logging.warn("Data does not contain '%s'", value)
        logging.warn("failed")
    return False