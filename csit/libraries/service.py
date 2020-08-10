#!/usr/local/bin/python3

import time
import json
import os
import sys
import yaml
import re
from pprint import pprint
from netmiko import Netmiko,ConnectHandler
import datetime
from jinja2 import Template
import csv
import textfsm
from multiprocessing import Pool

create_delete_list = ['create','delete']
Loop_list = ['L1','L2']
mep_meg_dmm_slm_list = ['meg','mep','dmm','slm']
maxhosts = 5
dict2 = {}
file_path = os.path.dirname(os.path.realpath(__file__))
test_result = {}

class Service:

    def __init__(self,**kwargs):
        self.data = kwargs

    def connect_nodes(self):
        for node in self.data["site_list"]:
            node['connect_obj'] = Netmiko(**node['login'])
            print("**** connection established with node {}".format(node['Node_name']))
    def disconnect_nodes(self):
        for node in self.data["site_list"]:
            node['connect_obj'].disconnect()
            print("**** disconnected successfully from node {}".format(node['Node_name']))

    def Command_Creation(self):                        
        for create_delete in create_delete_list:
            for node in self.data["site_list"]:
                with open(file_path + '/templates/create_xc_config_{}_{} copy.j2'.format(node["side"],create_delete),'r') as f:
                    Temp = f.read()
                    failure_command = Template(Temp).render(**self.data,**node)
                    file_open = open(file_path + '/commands/XC_command_{}_{}.txt'.format(node["Node_name"],create_delete), 'w+')
                    file_open.write(failure_command)
                    file_open.write('\n')
                    file_open.close()


    def push_config(self):
        for node in self.data["site_list"]:  
            print("****  Logged in node : {}".format(node['Node_name']))
            with open(file_path + '/commands/XC_command_{}_create.txt'.format(node["Node_name"]),'r') as f:
                f2 = f.readlines()
                output = node['connect_obj'].send_config_set(f2)
                print(output)
                if node['login']['device_type'] == 'cisco_xr':
                    node['connect_obj'].commit()
                    node['connect_obj'].exit_config_mode()
                else:
                    pass
                print("****  Configration completed on {}".format(node['Node_name']))
        time.sleep(10)
        print("*** wait for 10 seconds")  

    def check_QOS_counters_config(self):
        for node in self.data["site_list"]:
            if 'EP' in node['side']:
                if node['login']['device_type'] == 'cisco_xr':
                    output = node['connect_obj'].send_command("show policy-map interface {}.{}".format(node["main_interface"],self.data['item']))
                    print(output)
                    output = node['connect_obj'].send_command("show qos interface {}.{} input".format(node["main_interface"],self.data['item']))
                    print(output)
                else:
                    pass
            else:
                pass             



    def delete_config(self):
        for node in self.data["site_list"]:
            with open(file_path + '/commands/XC_command_{}_delete.txt'.format(node["Node_name"]),'r') as f:
                f2 = f.readlines()
                output = node['connect_obj'].send_config_set(f2)
                print(output)
                if node['login']['device_type'] == 'cisco_xr':
                    node['connect_obj'].commit()
                    node['connect_obj'].exit_config_mode()
                else:
                    pass

    def parse_accedian(self):
        for node in self.data["site_list"]:
            if node['login']['device_type'] == 'cisco_xr':
                pass
            else:          
                
                print("****  Logged in node : {}".format(node['Node_name']))
                node['index'] = {}
                if node['Protected'] == 'YES':
                    node['out_port'] = 'LAG-{}'.format(node['Nni_port'] // 2 + 1)
                else:
                    node['out_port'] = 'PORT-{}'.format(node['Nni_port'])                                
                for mep_meg_dmm_slm in mep_meg_dmm_slm_list:
                    output = node['connect_obj'].send_command('cfm show {} configuration'.format(mep_meg_dmm_slm))
                    template = open(file_path + '/TEXTFSM/accedian_show_{}_index.textfsm'.format(mep_meg_dmm_slm))
                    re_table = textfsm.TextFSM(template)
                    fsm_results = re_table.ParseText(output)
                    if mep_meg_dmm_slm == 'meg':
                        node['index']['del_meg'] = 1
                        for rows in fsm_results:
                            if rows[1] == 'LEXXX-{}'.format(100000 + self.data['item']):
                                node['index']['del_meg'] = rows[0]
                    if len(fsm_results) == 0:
                        node['index'][mep_meg_dmm_slm] = 1
                    else:                   
                        node['index'][mep_meg_dmm_slm] = int(fsm_results[-1][0]) + 1
                print("****  persing completed on {}".format(node['Node_name']))
                print(node['index'])

        return node['index']


    def Validate_ccm(self):
        test_result = {}
        for node in self.data["site_list"]:
            mep_name = 100000 + self.data['item']
            if 'EP' in node['side']:
                if node['login']['device_type'] == 'accedian':
                    print(node['Node_name'],end=' : ')
                    output = node['connect_obj'].send_command("cfm show mep status LEXXX-{}|{}|{}".format(mep_name,self.data['MEG_level'],node['Remote_MEP']))
                    if len(re.findall("Inactive", output)) == 14:
                        print("ccm is UP")
                        test_result[node['Node_name']] = 'pass'
                    else:
                        print("CCm did not came Up")
                        test_result[node['Node_name']] = 'fail'      
                else:
                    print("**** {}".format(node['Node_name']),end=' : ')
                    output = node['connect_obj'].send_command("show ethernet cfm services domain COLT-{} service ALX_NCS_LE-{}".format(self.data['MEG_level'],mep_name))
                    if len(re.findall("all operational, no errors", output)) == 2:
                        print("ccm is UP")
                        test_result[node['Node_name']] = 'pass'
                    else:
                        print("CCm did not came Up")
                        test_result[node['Node_name']] = 'fail'
        return test_result
    def Y1564_test(self):
        list1 = []
        test_result = {}
        mep_name = 100000 + self.data['item']
        for node in self.data["site_list"]:
            if 'EP' in node['side']:
                list1.append(node['login']['device_type'])
            else:
                pass
        if list1 == ['accedian','accedian']:
            for node in self.data["site_list"]:
                if node['login']['device_type'] == 'accedian':
                    output = node['connect_obj'].send_command("cfm show mep database LEXXX-{}|{}|{}".format(mep_name,self.data['MEG_level'],node['Remote_MEP']))
                    node['remote_mac'] = re.findall("\w\w[:]\w\w[:]\w\w[:]\w\w[:]\w\w[:]\w\w", output)[0]
                    if node['Protected'] == 'YES':
                        output = node['connect_obj'].send_command("port show status PORT-{}".format(node['Nni_port']))
                        if re.findall("Down|Up", output)[0] == 'Down':
                            node['Nni_port'] = node['Nni_port'] + 1
                    node['packet_type'] = 'l2-accedian'
                    for create_delete in create_delete_list:
                        with open(file_path + '/templates/Accedian_{}_{}_Y1564.j2'.format(node["side"],create_delete),'r') as f:
                            Temp = f.read()
                            failure_command = Template(Temp).render(**self.data,**node)
                            file_open = open(file_path + '/commands/Accedian_{}_{}_Y1564.txt'.format(node["Node_name"],create_delete), 'w+')
                            file_open.write(failure_command)
                            file_open.write('\n')
                            file_open.close()
                            print("**** {} templating done on node {} ".format(create_delete,node['Node_name']))
                            with open(file_path + '/commands/Accedian_{}_{}_Y1564.txt'.format(node["Node_name"],create_delete),'r') as f:
                                f2 = f.readlines()
                                output = node['connect_obj'].send_config_set(f2)
                                print(output)
                            if create_delete == "create":
                                time.sleep(190)
                            output = node['connect_obj'].send_command("Y1564 show activation Y1564-LE-{}".format(mep_name))
                            print(output)
                            x = re.findall("PASSED|FAILED", output)
                            if x[0] == 'PASSED':
                                test_result[node['Node_name']][looptype] = 'pass'
                            elif x[0] == 'FAILED':
                                test_result[node['Node_name']][looptype] = 'fail'
                            else:
                                test_result[node['Node_name']][looptype] = 'something wrong'                            
        elif list1 == ['cisco_xr','cisco_xr']:
            print("Loop can not be performed")
        elif list1 == ['cisco_xr','accedian'] or list1 == ['accedian','cisco_xr']:
            for node in self.data["site_list"]:
                if node['login']['device_type'] == 'accedian' and 'EP' in node['side']:
                    if node['Protected'] == 'YES':
                        output = node['connect_obj'].send_command("port show status PORT-{}".format(node['Nni_port']))
                        if re.findall("Down|Up", output)[0] == 'Down':
                            node['Nni_port'] = node['Nni_port'] + 1
                        output = node['connect_obj'].send_command("port show configuration PORT-{}".format(node['Nni_port']))
                        node['remote_mac'] = re.findall("\w\w[:]\w\w[:]\w\w[:]\w\w[:]\w\w[:]\w\w", output)[0]                       
                    node['packet_type'] = 'l2-generic'
                    for create_delete in create_delete_list:
                        for looptype in Loop_list:
                            if looptype == 'L2':
                                node['remote_mac'] = '00:22:00:22:00:22'
                            else:
                                pass
                            with open(file_path + '/templates/Accedian_{}_{}_Y1564.j2'.format(node["side"],create_delete),'r') as f:
                                Temp = f.read()
                                failure_command = Template(Temp).render(**self.data,**node)
                                file_open = open(file_path + '/commands/Accedian_{}_{}_{}_Y1564.txt'.format(node["Node_name"],looptype,create_delete), 'w+')
                                file_open.write(failure_command)
                                file_open.write('\n')
                                print("*** Loop {} commands are templated for {}".format(create_delete,node['Node_name']))
                elif node['login']['device_type'] == 'cisco_xr' and 'EP' in node['side']:
                    node['loop_ID'] = 1
                    for create_delete in create_delete_list:
                        for looptype in Loop_list:
                            with open(file_path + '/templates/Cisco_{}_loop_{}_Y1564.j2'.format(looptype,create_delete),'r') as f:
                                Temp = f.read()
                                failure_command = Template(Temp).render(**self.data,**node)
                                file_open = open(file_path + '/commands/Cisco_{}_{}_{}_Y1564.txt'.format(node["Node_name"],looptype,create_delete), 'w+')
                                file_open.write(failure_command)
                                file_open.write('\n')
                                print("*** {} Loop {} commands are templated for {}".format(looptype,create_delete,node['Node_name']))
                else:
                    pass
            for looptype in Loop_list:
                for create_delete in create_delete_list:
                    for node in self.data["site_list"]:
                        if node['login']['device_type'] == 'cisco_xr' and 'EP' in node['side']:
                            with open(file_path + '/commands/Cisco_{}_{}_{}_Y1564.txt'.format(node["Node_name"],looptype,create_delete),'r') as f:
                                f2 = f.readlines()
                                output = node['connect_obj'].send_config_set(f2)
                                node['connect_obj'].commit()
                                node['connect_obj'].exit_config_mode()
                                print(output)
                                if looptype == 'L2' and create_delete == 'create':
                                    output = node['connect_obj'].send_command("show ethernet loopback active | in ID")
                                    node['loop_ID'] = re.split("\s", output)[-1]
                                    with open(file_path + '/templates/Cisco_L2_loop_delete_Y1564.j2','r') as f:
                                        Temp = f.read()
                                        failure_command = Template(Temp).render(**self.data,**node)
                                        file_open = open(file_path + '/commands/Cisco_{}_L2_delete_Y1564.txt'.format(node["Node_name"]), 'w+')
                                        file_open.write(failure_command)
                                        file_open.write('\n')
                                        file_open.close()
                        elif node['login']['device_type'] == 'accedian' and 'EP' in node['side']:
                            with open(file_path + '/commands/Accedian_{}_{}_{}_Y1564.txt'.format(node["Node_name"],looptype,create_delete),'r') as f:
                                f2 = f.readlines()
                                output = node['connect_obj'].send_config_set(f2)
                                print(output)
                                if create_delete == "create":
                                    time.sleep(10)
                                    output = node['connect_obj'].send_command("Y1564 show activation Y1564-LE-{}".format(mep_name))
                                    print(output)
                                    x = re.findall("FAILED|PROGRESS", output)
                                    if x[0] == 'FAILED':
                                        test_result[looptype] = 'fail'
                                    else:
                                        time_to_wait = (self.data["config_test"]*4) + (self.data["performance_test"]*60) + 20
                                        print("***  Hold your breathe for {} seconds".format(time_to_wait))
                                        time.sleep(time_to_wait)
                                        output = node['connect_obj'].send_command("Y1564 show activation Y1564-LE-{}".format(mep_name))
                                        print(output)                             
                                        x = re.findall("PASSED|FAILED|PROGRESS", output)
                                        if x[0] == 'PASSED':
                                            test_result[looptype] = 'pass'
                                        elif x[0] == 'FAILED':
                                            test_result[looptype] = 'fail'
                                        else:
                                            test_result[looptype] = 'something Wrong,still in progress'            
        else:
            pass
        return test_result





