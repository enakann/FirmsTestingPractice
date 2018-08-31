# uncompyle6 version 3.1.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.5 (default, Apr 11 2018, 17:41:36) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28.0.1)]
# Embedded file name: fpb_post_process.py
# Compiled at: 2018-06-11 12:26:27
from __future__ import print_function
from common.db_utilities import extract_data
from collections import OrderedDict
import simplejson as json, time, copy, os, re
from datetime import datetime
from shutil import copyfile
from itertools import groupby
from operator import itemgetter
from club_policies import club
from common.json_utilities import write_json_file, read_json_file
from settings import LOG_CFG_PATH
from common.log import Logger
log_json_file = LOG_CFG_PATH + '/logging.json'
sys_logger = Logger(name='sys-logger', config_path=log_json_file)

def generate_sep_fw_pol(json_file, output_dir):
    policies = read_json_file(json_file)
    if 'no_policies' in policies.keys():
        return 1
    compare_cmd = policies['compare_cmd']
    policies.pop('compare_cmd', None)
    is_policies = 0
    for each_fw in policies.keys():
        output_file_name = output_dir + each_fw + '.txt'
        output_file = open(output_file_name, 'w')
        output_keys = policies[each_fw].keys()
        if len(output_keys) == 0:
            continue
        is_policies = 1
        output_file.write('\n')
        if 'new_src_cmd' in policies[each_fw].keys():
            for each_src_cmd in policies[each_fw]['new_src_cmd'].keys():
                output_file.write(policies[each_fw]['new_src_cmd'][each_src_cmd])

            policies[each_fw].pop('new_src_cmd')
        if 'new_dst_cmd' in policies[each_fw].keys():
            for each_dst_cmd in policies[each_fw]['new_dst_cmd'].keys():
                output_file.write(policies[each_fw]['new_dst_cmd'][each_dst_cmd])

            policies[each_fw].pop('new_dst_cmd')
        if 'new_app_cmd' in policies[each_fw].keys():
            for each_app_cmd in policies[each_fw]['new_app_cmd'].keys():
                output_file.write(policies[each_fw]['new_app_cmd'][each_app_cmd])

            policies[each_fw].pop('new_app_cmd')
        for each_cmd in sorted(policies[each_fw].keys()):
            for each_key in policies[each_fw][each_cmd].keys():
                if each_key == 'src_cmd':
                    src_cmds = policies[each_fw][each_cmd][each_key]
                elif each_key == 'dst_cmd':
                    dst_cmds = policies[each_fw][each_cmd][each_key]
                elif each_key == 'app_cmd':
                    app_cmds = policies[each_fw][each_cmd][each_key]
                elif each_key == 'permit_cmd':
                    permit_cmds = policies[each_fw][each_cmd][each_key]
                elif each_key == 'row_num':
                    row_num = policies[each_fw][each_cmd][each_key]

            row_num_final = None
            for row in row_num:
                if len(row_num) > 1:
                    if row_num_final != None:
                        row_num_final = str(row_num_final) + ',' + str(row)
                    else:
                        row_num_final = row
                else:
                    row_num_final = row

            row_num_message = 'Policies recommended for record number(s): %s' % row_num_final
            output_file.write('\n')
            output_file.write(row_num_message)
            output_file.write('\n')
            for src in src_cmds:
                output_file.write(src)
                output_file.write('\n')

            for dst in dst_cmds:
                output_file.write(dst)
                output_file.write('\n')

            for app in app_cmds:
                output_file.write(app)
                output_file.write('\n')

            for permit in permit_cmds:
                output_file.write(permit)
                output_file.write('\n')

        if is_policies == 1:
            output_file.write('\n')
            output_file.write(compare_cmd)
        output_file.close()

    return


def convert_json_to_txt_policies(json_file, output_file_name):
    policies = read_json_file(json_file)
    output_file = open(output_file_name, 'w')
    if 'no_policies' in policies.keys():
        output_file.write(policies['no_policies'])
        print('Policies recommended in:', output_file_name)
        return 1
    compare_cmd = policies['compare_cmd']
    policies.pop('compare_cmd', None)
    is_policies = 0
    for each_fw in policies.keys():
        output_keys = policies[each_fw].keys()
        if len(output_keys) == 0:
            continue
        is_policies = 1
        print_fw = u'***%s \n =============================================== \n' % each_fw
        output_file.write('\n')
        output_file.write(print_fw)
        output_file.write('\n')
        if 'new_src_cmd' in policies[each_fw].keys():
            for each_src_cmd in policies[each_fw]['new_src_cmd'].keys():
                output_file.write(policies[each_fw]['new_src_cmd'][each_src_cmd])

            policies[each_fw].pop('new_src_cmd')
        if 'new_dst_cmd' in policies[each_fw].keys():
            for each_dst_cmd in policies[each_fw]['new_dst_cmd'].keys():
                output_file.write(policies[each_fw]['new_dst_cmd'][each_dst_cmd])

            policies[each_fw].pop('new_dst_cmd')
        if 'new_app_cmd' in policies[each_fw].keys():
            for each_app_cmd in policies[each_fw]['new_app_cmd'].keys():
                output_file.write(policies[each_fw]['new_app_cmd'][each_app_cmd])

            policies[each_fw].pop('new_app_cmd')
        for each_cmd in sorted(policies[each_fw].keys()):
            for each_key in policies[each_fw][each_cmd].keys():
                if each_key == 'src_cmd':
                    src_cmds = policies[each_fw][each_cmd][each_key]
                elif each_key == 'dst_cmd':
                    dst_cmds = policies[each_fw][each_cmd][each_key]
                elif each_key == 'app_cmd':
                    app_cmds = policies[each_fw][each_cmd][each_key]
                elif each_key == 'permit_cmd':
                    permit_cmds = policies[each_fw][each_cmd][each_key]
                elif each_key == 'row_num':
                    row_num = policies[each_fw][each_cmd][each_key]

            row_num_final = None
            for row in row_num:
                if len(row_num) > 1:
                    if row_num_final != None:
                        row_num_final = str(row_num_final) + ',' + str(row)
                    else:
                        row_num_final = row
                else:
                    row_num_final = row

            row_num_message = 'Policies recommended for record number(s) %s' % row_num_final
            output_file.write('\n')
            output_file.write(row_num_message)
            output_file.write('\n')
            for src in src_cmds:
                output_file.write(src)
                output_file.write('\n')

            for dst in dst_cmds:
                output_file.write(dst)
                output_file.write('\n')

            for app in app_cmds:
                output_file.write(app)
                output_file.write('\n')

            for permit in permit_cmds:
                output_file.write(permit)
                output_file.write('\n')

    if is_policies == 1:
        output_file.write('\n')
        output_file.write(compare_cmd)
    print('Policies recommended in:', output_file_name)
    return 1


def convert_json_to_txt_issues(json_file, output_file_name):
    route_issues = read_json_file(json_file)
    print('Red Flags generated in:', output_file_name)
    output_file = open(output_file_name, 'w')
    if len(route_issues) == 0:
        output_file.write('No red flags')
        return 1
    output_file.write('\n')
    output_file.write('FiRMS Red Flag (FRF) Code details at: http://goto/FiRMS-RF-Codes')
    output_file.write('\n\n')
    output_file.write('-' * 190)
    output_file.write('\n')
    output_file.write(('{}\t{}\t{}\t{}\t\t{}\t\t{}\t{}\t\t{}\t{}\t{}\n').format('Rec#', 'Src_Addr', 'Dst_Addr', 'Src_Fw', 'SF_Ing_Zone', 'SF_Egr_Zone', 'Dst_Fw', 'DF_Ing_Zone', 'DF_Egr_Zone', 'Red_Flag_Code'))
    output_file.write('-' * 190)
    output_file.write('\n')
    route_issues = sorted(route_issues, key=lambda k: k['Input-Row-ID'])
    each_row = 0
    while each_row < len(route_issues):
        source_ip = route_issues[each_row]['Source-IP']
        dst_ip = route_issues[each_row]['Destination-IP']
        src_firewall = route_issues[each_row]['Source-Firewall']
        dst_firewall = route_issues[each_row]['Destination-Firewall']
        port = route_issues[each_row]['Port']
        exc_message = route_issues[each_row]['Routing-Issue-Reason']
        src_zone = route_issues[each_row]['Source-Zone']
        src_zone_2 = route_issues[each_row]['Source-Zone-2']
        dst_zone = route_issues[each_row]['Dest-Zone']
        dst_zone_2 = route_issues[each_row]['Dest-Zone-2']
        row_id = route_issues[each_row]['Input-Row-ID']
        if 'FRF-1003' in exc_message:
            src_firewall = ''
        if 'FRF-1004' in exc_message:
            dst_firewall = ''
        output_file.write(('{}\t{}\t{}\t{}\t{}\t\t{}\t\t{}\t\t{}\t{}\t\t{}\n').format(row_id, source_ip, dst_ip, src_firewall, src_zone, dst_zone, dst_firewall, src_zone_2, dst_zone_2, exc_message))
        each_row += 1

    return 1


def convert_json_to_existing_txt_policies(json_file, output_file_name):
    existing_policies = read_json_file(json_file)
    print('Existing policies generated in:', output_file_name)
    output_file = open(output_file_name, 'w')
    each_row = 0
    if len(existing_policies) == 0:
        output_file.write('No existing policies')
        return 1
    existing_policies = sorted(existing_policies, key=lambda k: k['Input-Row-ID'])
    output_file.write('-' * 190)
    output_file.write('\n')
    output_file.write(('{}\t{}\t\t{}\t{}\t\t{}\t\t\t\t\t\t\t{}\n').format('Record Number', 'Source Address', 'Destination Address', 'Port', 'Policy Name', 'Firewall'))
    output_file.write('-' * 190)
    output_file.write('\n')
    existing_pol = []
    while each_row < len(existing_policies):
        source_ip = existing_policies[each_row]['Source-IP']
        dst_ip = existing_policies[each_row]['Destination-IP']
        port = existing_policies[each_row]['Port']
        policy_name = existing_policies[each_row]['Policy-Name']
        row_id = existing_policies[each_row]['Input-Row-ID']
        firewall = existing_policies[each_row]['Firewall']
        existing_pol.append(row_id)
        output_file.write(('{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t\t\t{}\n').format(row_id, source_ip, dst_ip, port, policy_name, firewall))
        each_row += 1

    total_existing_pol = set(existing_pol)
    total_existing_pol_cnt = len(total_existing_pol)
    logger.info(('Total existing policies: {}').format(total_existing_pol_cnt))
    return 1


def create_address(addr_book, addr_name, subnet):
    cmd = 'set security address-book %s address %s %s \n' % (addr_book, addr_name, subnet)
    return cmd


def create_application(app_name, app_dest, nw_protocol):
    cmd = 'set applications application %s protocol %s\nset applications application %s destination-port %s\n' % (app_name, nw_protocol, app_name, app_dest)
    return cmd


def create_policy(policy_data, sr_number, username, row_numbers):
    final_policy = OrderedDict()
    i = 0
    index = 0
    total_recom_policies = []
    for each_fw in policy_data:
        if each_fw not in final_policy.keys():
            final_policy[each_fw] = OrderedDict()
        for each_cmd in policy_data[each_fw].keys():
            if each_cmd == 'new_app_cmd':
                if len(policy_data[each_fw][each_cmd]) > 0:
                    final_policy[each_fw]['new_app_cmd'] = OrderedDict()
                    for each_app_cmd in policy_data[each_fw]['new_app_cmd'].keys():
                        app_dest = policy_data[each_fw]['new_app_cmd'][each_app_cmd]['app_dest']
                        net_protocol = policy_data[each_fw]['new_app_cmd'][each_app_cmd]['net_proto'].lower()
                        app_cmd = create_application(each_app_cmd, app_dest, net_protocol)
                        final_policy[each_fw]['new_app_cmd'][each_app_cmd] = app_cmd

            elif each_cmd == 'new_src_cmd':
                if len(policy_data[each_fw][each_cmd]) > 0:
                    final_policy[each_fw]['new_src_cmd'] = OrderedDict()
                    for each_src_cmd in policy_data[each_fw]['new_src_cmd'].keys():
                        subnet = policy_data[each_fw]['new_src_cmd'][each_src_cmd]['subnet']
                        src_addr_book = policy_data[each_fw]['new_src_cmd'][each_src_cmd]['src_addr_book']
                        src_cmd = create_address(src_addr_book, each_src_cmd, subnet)
                        final_policy[each_fw]['new_src_cmd'][each_src_cmd] = src_cmd

            elif each_cmd == 'new_dst_cmd':
                if len(policy_data[each_fw][each_cmd]) > 0:
                    final_policy[each_fw]['new_dst_cmd'] = OrderedDict()
                    for each_dst_cmd in policy_data[each_fw]['new_dst_cmd'].keys():
                        subnet = policy_data[each_fw]['new_dst_cmd'][each_dst_cmd]['subnet']
                        dst_addr_book = policy_data[each_fw]['new_dst_cmd'][each_dst_cmd]['dst_addr_book']
                        dst_cmd = create_address(dst_addr_book, each_dst_cmd, subnet)
                        final_policy[each_fw]['new_dst_cmd'][each_dst_cmd] = dst_cmd

            else:
                src_zone, dst_zone = each_cmd.split('_')
                for each_pol in policy_data[each_fw][each_cmd]:
                    src_cmd_final = []
                    dst_cmd_final = []
                    app_cmd_final = []
                    row_num_final = []
                    permit_cmd = []
                    index += 1
                    policy_name = str(sr_number) + '_' + username + '_' + str(index)
                    final_policy[each_fw][index] = OrderedDict()
                    src_list = each_pol['src']
                    dst_list = each_pol['dst']
                    app_list = each_pol['app']
                    for src in src_list:
                        src_cmd = 'set security policies from-zone %s to-zone %s policy %s match source-address %s' % (src_zone, dst_zone, policy_name, src)
                        src_cmd_final.append(src_cmd)

                    for dst in dst_list:
                        dst_cmd = 'set security policies from-zone %s to-zone %s policy %s match destination-address %s' % (src_zone, dst_zone, policy_name, dst)
                        dst_cmd_final.append(dst_cmd)

                    for app in app_list:
                        app_cmd = 'set security policies from-zone %s to-zone %s policy %s match application %s' % (src_zone, dst_zone, policy_name, app)
                        app_cmd_final.append(app_cmd)

                    for src in src_list:
                        for dst in dst_list:
                            for app in app_list:
                                key = src + '__' + dst + '__' + app
                                if key in row_numbers:
                                    row_id = row_numbers[key]
                                row_num_final.append(row_id)
                                total_recom_policies.append(row_id)

                    rows = set(row_num_final)
                    row_num_final = list(rows)
                    row_num_final.sort()
                    permit_cmd.append('set security policies from-zone %s to-zone %s policy %s then permit' % (src_zone, dst_zone, policy_name))
                    final_policy[each_fw][index] = {'src_cmd': src_cmd_final, 'dst_cmd': dst_cmd_final, 'app_cmd': app_cmd_final, 'permit_cmd': permit_cmd, 'row_num': row_num_final}

    if len(final_policy.keys()) > 0:
        compare_cmd = 'show | compare'
        final_policy['compare_cmd'] = compare_cmd
    else:
        final_policy['no_policies'] = 'No policies generated'
    final_recom = set(total_recom_policies)
    recom_count = len(final_recom)
    logger.info(('Policies recommended for records: {}').format(recom_count))
    return final_policy


def post_process(sr_number, username, unix_proc_no, input_file, new_dir_json, new_dir_txt, logfile):
    #global logger
    #logger = Logger(name='firms_fpb', config_path=log_json_file, log_file=logfile)
    #time_before_select = time.time()
    select_query = 'select route_issue,src_ip,dst_ip,port,protocol,src_firewall,src_zone,dst_zone,src_addr_book,src_addr_name,src_addr_nm_exists,dst_addr_book,dst_addr_name,dst_addr_nm_exists,app_name,policy_exists,net_proto,app_name_exists,app_dst,dst_firewall,inc_req_row_id,src_ip_int,dst_ip_int,exception_msg,dst_firewall,policy_name,src_zone_2,dst_zone_2,src_addr_book_2,src_addr_name_2,src_addr_nm_exists_2,dst_addr_book_2,dst_addr_name_2,dst_addr_nm_exists_2,app_name_2,app_name_exists_2,policy_exists_2,policy_name_2,src_subnet,dst_subnet from incoming_request where unix_process_no=:1'
    #logger.info(('Select Query {}').format(select_query))
    bind_data = (unix_proc_no,)
    temp_data = extract_data(select_query, bind_data)
    data = []
    for record in temp_data:
        existing_record = list(record)
        data.append(existing_record)
        if record[5] != record[19] and record[0] != 'Y':
            if True:
                new_record = list(record)
                new_record[0] = 'N'
                new_record[5] = record[24]
                new_record[6] = record[26]
                new_record[7] = record[27]
                new_record[8] = record[28]
                new_record[9] = record[29]
                new_record[10] = record[30]
                new_record[11] = record[31]
                new_record[12] = record[32]
                new_record[13] = record[33]
                new_record[14] = record[34]
                new_record[17] = record[35]
                new_record[15] = record[36]
                new_record[25] = record[37]
                data.append(new_record)

    time_after_select = time.time()
    total_time_taken_select = time_after_select - time_before_select
    all_policies = {}
    src_dst_port_dict = {}
    row_numbers = {}
    route_issues = []
    route_issue_count = 0
    existing_policies = []
    existing_pol_count = 0
    issue_record_count = 0
    counter = 0
    all_src_addr = OrderedDict()
    all_dst_addr = OrderedDict()
    all_apps = OrderedDict()
    for record in data:
        route_issue = record[0]
        src_ip = record[1]
        dst_ip = record[2]
        port = record[3]
        protocol = record[4]
        src_firewall = record[5]
        src_zone = record[6]
        dst_zone = record[7]
        src_addr_book = record[8]
        src_addr_name = record[9]
        src_addr_nm_exists = record[10]
        dst_addr_book = record[11]
        dst_addr_name = record[12]
        dst_addr_nm_exists = record[13]
        app_name = record[14]
        policy_exists = record[15]
        net_proto = record[16]
        app_name_exists = record[17]
        app_dest = record[18]
        dst_firewall = record[19]
        row_id = record[20]
        src_ip_int = str(record[21])
        dst_ip_int = str(record[22])
        route_exc_message = record[23]
        dst_firewall = record[24]
        existing_pol_name = record[25]
        src_zone_2 = record[26]
        dst_zone_2 = record[27]
        src_subnet_nw = record[38]
        dst_subnet_nw = record[39]
        total_rec_policies = 0
        if route_issue == 'Y':
            route_issues.append({'Source-IP': src_ip, 'Destination-IP': dst_ip, 'Port': port, 'Source-Firewall': src_firewall, 'Destination-Firewall': dst_firewall, 'Routing-Issue-Reason': route_exc_message, 'Source-Zone': src_zone, 'Dest-Zone': dst_zone, 'Source-Zone-2': src_zone_2, 'Dest-Zone-2': dst_zone_2, 'Input-Row-ID': row_id})
            route_issue_count += 1
        else:
            if src_firewall not in all_policies.keys():
                all_policies[src_firewall] = {'new_src_cmd': {}, 'new_dst_cmd': {}, 'new_app_cmd': {}}
                src_dst_port_dict[src_firewall] = {}
            total_rec_policies += 1
            if src_addr_nm_exists == 'N':
                if '/' not in src_ip:
                    src_subnet = src_ip + '/32'
                else:
                    if src_subnet_nw is None:
                        src_subnet = src_ip
                    else:
                        src_subnet = src_subnet_nw
                all_policies[src_firewall]['new_src_cmd'][src_addr_name] = {'subnet': src_subnet, 'src_addr_book': src_addr_book, 'src_addr_name': src_addr_name}
            if dst_addr_nm_exists == 'N':
                if '/' not in dst_ip:
                    dst_subnet = dst_ip + '/32'
                else:
                    if dst_subnet_nw is None:
                        dst_subnet = dst_ip
                    else:
                        dst_subnet = dst_subnet_nw
                all_policies[src_firewall]['new_src_cmd'][dst_addr_name] = {'subnet': dst_subnet, 'src_addr_book': dst_addr_book, 'src_addr_name': dst_addr_name}
            app_exists_list = str(app_name_exists).split(',')
            app_name_list = str(app_name).split(',')
            app_dest_list = str(app_dest).split(',')
            i = 0
            while i < len(app_name_list):
                key = src_addr_name + '__' + dst_addr_name + '__' + app_name_list[i]
                try:
                    row_numbers[key] = row_id
                except Exception as e:
                    logger.error(e)

                i += 1

            pol_name_list = str(existing_pol_name).split(',')
            port_list = str(port).split(';')
            i = 0
            if len(app_exists_list) > 0:
                if 'new_app_cmd' not in all_policies[src_firewall].keys():
                    all_policies[src_firewall]['new_app_cmd'] = OrderedDict()
                while i < len(app_exists_list):
                    is_exists = app_exists_list[i]
                    if is_exists == 'N':
                        new_app_name = app_name_list[i]
                        new_app_dest = app_dest_list[i]
                        all_policies[src_firewall]['new_app_cmd'][new_app_name] = {'app_dest': new_app_dest, 'net_proto': net_proto}
                    i += 1

            policy_exists_list = str(policy_exists).split(',')
            if src_zone == None or dst_zone == None:
                logger.error(('FiRMS engine couldnt process record number {}').format(row_id))
                print('FiRMS engine couldnt process record number ', format(row_id))
                issue_record_count += 1
                continue
            src_dst_key = src_zone + '_' + dst_zone
            i = 0
            while i < len(policy_exists_list):
                is_exist_policy = policy_exists_list[i]
                app = app_name_list[i]
                if is_exist_policy == 'N':
                    key = src_addr_name + '__' + dst_addr_name + '__' + app
                    if src_dst_key not in all_policies[src_firewall].keys():
                        all_policies[src_firewall][src_dst_key] = {key: key}
                    else:
                        all_policies[src_firewall][src_dst_key][key] = key
                else:
                    pol_name = pol_name_list[i]
                    existing_policies.append({'Source-IP': src_ip, 'Destination-IP': dst_ip, 'Port': app_dest_list[i], 'Policy-Name': pol_name, 'Input-Row-ID': row_id, 'Firewall': src_firewall})
                i += 1

    counter = 0
    new_policies = copy.deepcopy(all_policies)
    for each_fw in all_policies.keys():
        for each_zone in all_policies[each_fw].keys():
            if each_zone == 'new_src_cmd':
                continue
            if each_zone == 'new_dst_cmd':
                continue
            if each_zone == 'new_app_cmd':
                continue
            new_policies[each_fw].pop(each_zone, None)

    for each_fw in all_policies.keys():
        for each_zone in all_policies[each_fw].keys():
            data = []
            if each_zone == 'new_src_cmd':
                continue
            if each_zone == 'new_dst_cmd':
                continue
            if each_zone == 'new_app_cmd':
                continue
            for each_key in all_policies[each_fw][each_zone].keys():
                src, dst, port = each_key.split('__')
                temp_rec = {'src': [src], 'dst': [dst], 'app': [port]}
                data.append(temp_rec)

            grouped_data = club(data)
            new_policies[each_fw][each_zone] = grouped_data

    logger.info(('Possible Red Flags {}').format(route_issue_count))
    sys_logger.info(('Possible Red Flags: {}').format(route_issue_count))
    sys_logger.info(('Policies recommended for: {}').format(total_rec_policies))
    print('Possible Red Flags: ', route_issue_count)
    final_policies = create_policy(new_policies, sr_number, username, row_numbers)
    policies_file = sr_number + '_policies'
    json_file = policies_file + '.json'
    json_new_pol_path = new_dir_json + json_file
    txt_new_pol_path = new_dir_txt + policies_file + '.txt'
    write_json_file(final_policies, json_new_pol_path)
    logger.info(('JSON Policies file generated {}').format(json_new_pol_path))
    convert_json_to_txt_policies(json_new_pol_path, txt_new_pol_path)
    route_issues_file = sr_number + '_red_flags'
    json_route_issue = route_issues_file + '.json'
    json_red_flag_path = new_dir_json + json_route_issue
    txt_red_flag_path = new_dir_txt + route_issues_file + '.txt'
    write_json_file(route_issues, json_red_flag_path)
    logger.info(('JSON Red Flags file generated {}').format(json_red_flag_path))
    convert_json_to_txt_issues(json_red_flag_path, txt_red_flag_path)
    existing_pol_file = sr_number + '_existing_policies'
    json_existing_pol = existing_pol_file + '.json'
    json_ex_pol_path = new_dir_json + json_existing_pol
    txt_ex_pol_path = new_dir_txt + existing_pol_file + '.txt'
    write_json_file(existing_policies, json_ex_pol_path)
    logger.info(('JSON Existing Policies file generated {}').format(json_ex_pol_path))
    convert_json_to_existing_txt_policies(json_ex_pol_path, txt_ex_pol_path)
    return 1
# okay decompiling fpb_post_process_PROD_Bef_Mult.pyc
