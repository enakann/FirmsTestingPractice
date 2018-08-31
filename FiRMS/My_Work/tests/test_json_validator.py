import re
def sanitize_port(port):
    # Get rid of .0, spaces new line and \r
    port = re.sub(r'\.0+', "", port)
    port = re.sub(r'\s+|\n+|\r+', '', port)

    # Get rid of starting ending semi-colon
    port = re.sub('^;+|;+$', '', port)

    # Get rid of multiple consecutive semi-colons
    port = re.sub(';+', ';', port)

    # Get rid of multiple consecutive - in case of range
    port = re.sub('-+', '-', port)

    port = re.sub('(?i)ANY', '0-65535', port)
    port = re.sub('(?i)ALL', '0-65535', port)

    return port

port=sanitize_port(443.0)
print(port)