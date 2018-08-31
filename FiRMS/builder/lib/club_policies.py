from itertools import groupby
from operator import itemgetter
from collections import Counter

grouper = itemgetter("app", "src")
grouper1 = itemgetter("app", "dst")
grouper2 = itemgetter("src", "dst")

data = [{'src': ['lpclmx0017'], 'app': ['tcp-8000', 'tcp-3875', 'junos-ssh'], 'dst': ['host-129.158.75.115/32']}, {'src': ['lpclmx0017'], 'app': ['tcp-8000', 'tcp-3875', 'junos-ssh'], 'dst': ['us6-ashburn-colo-opc-nat1-129.158.75.116/32']}]
data=[{'src': ['lpclmx0017'], 'dst': ['us6-ashburn-colo-opc-nat1-129.158.75.116/32'], 'app': ['tcp-8000']}, {'src': ['lpclmx0017'], 'dst': ['host-129.158.75.115/32'], 'app': ['junos-ssh']}, {'src': ['lpclmx0017'], 'dst': ['host-129.158.75.115/32'], 'app': ['tcp-3875']}, {'src': ['lpclmx0017'], 'dst': ['host-129.158.75.115/32'], 'app': ['tcp-8000']}, {'src': ['lpclmx0017'], 'dst': ['us6-ashburn-colo-opc-nat1-129.158.75.116/32'], 'app': ['tcp-3875']}, {'src': ['lpclmx0017'], 'dst': ['us6-ashburn-colo-opc-nat1-129.158.75.116/32'], 'app': ['junos-ssh']}]
def club(input_data,max_depth=None):
    result = []
    result1=[]
    result2=[]
    returnval = []
    mydict={}
    tempdict={}
    for key, grp in groupby(sorted(input_data, key = grouper2), grouper2):
        temp_dict = dict(zip(["src", "dst"], key))
        list1=[]
        for item in grp:
            list1.append(item['app'])
        temp_dict["app"] = list1 
        result2.append(temp_dict)

    new_input_data=[]
    for r2 in result2:
        tempdict={}
        if len(r2['app']) > 1:
            tempdict['app']=r2['app']
            tempdict['src']=[r2['src']]
            tempdict['dst']=[r2['dst']]
            returnval.append(tempdict)
            #print r2
        else:
            my_dict={}
            my_dict['app'] = r2['app'][0]
            my_dict['src'] = r2['src']
            my_dict['dst'] = r2['dst']
            new_input_data.append(my_dict)

    #print new_input_data
    for key, grp in groupby(sorted(new_input_data, key = grouper), grouper):
        temp_dict = dict(zip(["app", "src"], key))
        list1=[]
        for item in grp:
            list1.append(item['dst'])
        list1.sort()
        temp_dict["dst"] = list1
        result.append(temp_dict)
    counter_list = [tuple(res['app']) for res in result];
    cnt_dict_src = dict(Counter(counter_list))

    for key, grp in groupby(sorted(new_input_data, key = grouper1), grouper1):
        temp_dict = dict(zip(["app", "dst"], key))
        list1=[]
        for item in grp:
            list1.append(item['src'])
        list1.sort()
        temp_dict["src"] = list1
        result1.append(temp_dict)
    counter_list = [tuple(res['app']) for res in result1];
    cnt_dict_dst = dict(Counter(counter_list))

    #print result
    #print result1
    #print cnt_dict_src
    #print cnt_dict_dst 

    for k,v in cnt_dict_src.iteritems():
        if v > cnt_dict_dst[k]:
            for r in result1:
                tempdict={}
                if r['app'] == list(k):
                    tempdict['app']=[r['app']]
                    tempdict['src']=r['src']
                    tempdict['dst']=[r['dst']]
                    returnval.append(tempdict)
        else:
            for r in result:
                tempdict={}
                #print 'else at the very end'
                #print r['app']
                #print k
                if r['app'] == list(k):
                    tempdict['app']=[r['app']]
                    tempdict['src']=[r['src']]
                    tempdict['dst']=r['dst']
                    returnval.append(tempdict)

    #print returnval
    op = format_output(returnval)
    if max_depth is None:
        #print 'inside max depth none'
        op = club(op,max_depth=1)
    #else:
        #print 'elsesssssss'
        #print op
    return op
d=[]
def format_output(output):
    global d
    #print output
    l_src=[]
    l_dst=[]
    l_app=[]
    final_list=[]
    for o in output:
        #print o
        temhash={}
    	src = o['src']
    	l_src = type_chk(src)
        l_src.sort()
        temhash['src']=l_src
        d = []
    	dst = o['dst']
    	l_dst = type_chk(dst)
        l_dst.sort()
        temhash['dst']=l_dst
        d = []
    	app = o['app']
    	l_app = type_chk(app)
        l_app.sort()
        temhash['app']=l_app
        d = []
        final_list.append(temhash)
        #print l_src
        #print l_dst
        #print l_app
    return final_list

def type_chk(l):
    global d
    for ele in l:
        if isinstance(ele, list):
            #print 'inside'
            type_chk(ele)
        else:
            d.append(ele)
    return d
if __name__ == '__main__':
    gd = club(data)
    print gd
