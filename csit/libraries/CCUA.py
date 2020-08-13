#!/usr/local/bin/python3

import time
import json
import os
import sys
import yaml
import re
from pprint import pprint
from netmiko import Netmiko
import datetime
from jinja2 import Template
import csv
import textfsm
from service import Service
import yaml
#from Class_Based_Spirent_Code_Generation import Spirent_L2_Traffic_Gen,Get_Spirent_Config,Create_Spirent_L2_Gen

file_path = os.path.dirname(os.path.realpath(__file__))
result = {}
def onnet_CCM_Y1564_CCA(A,B):

    print("!"*1)
    print("!"*2)
    print("************** Test {}{} type EP ************* ".format(A,B))
    print("!!"*3)
    dict1 = yaml.load(open(file_path + '/../Topology/inputfile_CCUA.yml'),Loader=yaml.Loader)
    dict1['site_list'][0]['port_type'] = '{}-type'.format(A)
    dict1['site_list'][1]['port_type'] = '{}-type'.format(B)
    dict1['site_list'][2]['port_type'] = '{}-type'.format(B)
    my_config = Service(**dict1)
    my_config.connect_OLO_nodes()
    my_config.create_commands_OLO()
    my_config.push_OLO_config()
    my_config.connect_nodes()
    my_config.parse_accedian()
    my_config = Service(**dict1)
    my_config.Command_Creation()
    my_config.push_config()
    time.sleep(10)
    test_result = {}
    test_result['ccm_status'] = my_config.Validate_ccm()
    #test_result['Loop_test'] = my_config.Y1564_test()
    #my_config.check_QOS_counters_config()
    #test_result['CFM_Stats_Acc'] = my_config.mep_statistic_accedian()
    #test_result['CFM_Stats_cisco'] = my_config.mep_statistic_cisco()     
    my_config.delete_config()
    my_config.disconnect_nodes()
    my_config.delete_OLO_config()
    my_config.disconnect_OLO_nodes()
    return test_result



# result['FF'] = onnet_CCM_Y1564_CCA('F','F')
# result['XX'] = onnet_CCM_Y1564_CCA('X','X')
# result['PP'] = onnet_CCM_Y1564_CCA('P','P')
# result['XP'] = onnet_CCM_Y1564_CCA('X','P')
result['PX'] = onnet_CCM_Y1564_CCA('P','X')
# result['FY'] = onnet_CCM_Y1564_CCA('F','Y')
# result['YF'] = onnet_CCM_Y1564_CCA('Y','F')
# result['YY'] = onnet_CCM_Y1564_CCA('Y','Y')

pprint(result)