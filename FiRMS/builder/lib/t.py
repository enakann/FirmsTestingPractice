#ll=[1,2,4,[12,11,[44,22,33],[7,9]]]
#d=[]
#def type_chk(l):
#    global d
#    for ele in l:
#        if isinstance(ele, list):
#            print 'inside'
#            type_chk(ele)
#        else:
#            d.append(ele)
#    return d
#d = type_chk(ll)
#print d
#

import signal

for i in [x for x in dir(signal) if x.startswith("SIG")]:
  try:
    signum = getattr(signal,i)
    signal.signal(signum,sighandler)
  except Exception as m: #OSError for Python3, RuntimeError for 2
    print ("Skipping {}".format(i))
