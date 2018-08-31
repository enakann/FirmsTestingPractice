import netaddr,time,socket,re,time
import os
#import pdb

all_ips = open ("/home/netauto/FiRMS/builder/lib/all_ips.txt")
os.environ['RES_OPTIONS'] = '"rotate timeout:1 attempts:2"'
for ip in all_ips:
    host = ip.rstrip()
    start_time = time.time()
    ips = set()
    ip_details = {}
    s = socket.socket()
    hostname = None
    if re.match ('^\d+\.\d+\.\d+\.\d+',host):
        try:
            hostname = socket.gethostbyaddr(host)[0]
        except Exception as e:
            print "Cant resolve: ", host
            pass
    else:
        hostname = host
    
    if ((time.time()-start_time) > 1):
        print (time.time()-start_time) 
    if hostname:
        try:
            out=socket.getaddrinfo(hostname,80)
            for ip in out:
                if re.match("((\d+\.){3}\d+)$",ip[-1][0]):
                    ips.add(ip[-1][0])
        except Exception as e:
            ips.add(host)
            pass

    else:
        ips.add (host)
os.environ['RES_OPTIONS'] = ''
