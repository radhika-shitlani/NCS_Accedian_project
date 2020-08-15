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
from Class_Based_Spirent_Code_Generation import Spirent_L2_Traffic_Gen,Get_Spirent_Config,Create_Spirent_L2_Gen

file_path = os.path.dirname(os.path.realpath(__file__))
result = {}

def spirent_call(A,B):
    if A == 'F' or A == 'X':
        StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Single_Tagged_VLAN_Mbps(0,1,**Spirent_InputParam)
    elif A == 'Y':
        StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_Mbps(0,1,**Spirent_InputParam)
    elif A == 'P':
        StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Without_VLAN_Mbps(0,1,**Spirent_InputParam)
    else:
        pass    
    if B == 'F' or B == 'X':
        StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Single_Tagged_VLAN_Mbps(1,0,**Spirent_InputParam)
    elif B == 'Y':
        StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_Mbps(1,0,**Spirent_InputParam)
    elif B == 'P':
        StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Without_VLAN_Mbps(1,0,**Spirent_InputParam)
    else:
        pass

def onnet_CCM_Y1564_CCA(A,B):

    print("!"*1)
    print("!"*2)
    print("************** Test {}{} type EP ************* ".format(A,B))
    print("!!"*3)
    dict1 = yaml.load(open(file_path + '/../Topology/inputfile.yml'),Loader=yaml.Loader)
    dict1['site_list'][0]['port_type'] = '{}-type'.format(A)
    dict1['site_list'][1]['port_type'] = '{}-type'.format(B)
    dict1['site_list'][2]['port_type'] = '{}-type'.format(B)
    #Spirent_InputParam_1TAG = {'Rate_Mbps': dict1['service_BW']//1000,'VLAN_ID': str(dict1['item'])}
    Spirent_InputParam_2TAG = {'Rate_Mbps': (dict1['service_BW']*dict1['STP_percentage'])//100000,'Outer_VLAN_ID': str(dict1['item'] + 100), 'Inner_VLAN_ID': str(dict1['item'])}
    Spirent_InputParam_2TAG_BC = {'Rate_Mbps': (dict1['service_BW']*dict1['STP_percentage'])//100000,'Outer_VLAN_ID': str(dict1['item'] + 100), 'Inner_VLAN_ID': str(dict1['item']),'MAC_Dest':'FF:FF:FF:FF:FF:FF'}
    Spirent_InputParam_2TAG_MC = {'Rate_Mbps': (dict1['service_BW']*dict1['STP_percentage'])//100000,'Outer_VLAN_ID': str(dict1['item'] + 100), 'Inner_VLAN_ID': str(dict1['item']),'MAC_Dest':'01:00:5E:0B:01:02'}
    my_config = Service(**dict1)
    my_config.connect_nodes()
    my_config.parse_accedian()
    my_config = Service(**dict1)
    my_config.Command_Creation()
    my_config.push_config()
    time.sleep(10)
    test_result = {}
    test_result['ccm_status'] = my_config.Validate_ccm()
    test_result['Loop_test'] = my_config.Y1564_test()
    Spirent_L2_Gen = Create_Spirent_L2_Gen()
    Spirent_L2_Gen.Port_Init()
    # StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Single_Tagged_VLAN_Mbps(0,1,**Spirent_InputParam_1TAG)
    # StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Single_Tagged_VLAN_Mbps(1,0,**Spirent_InputParam_1TAG)
    StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_Mbps(0,1,**Spirent_InputParam_2TAG)
    StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_Mbps(1,0,**Spirent_InputParam_2TAG)
    Spirent_L2_Gen.Generate_Traffic()
    Spirent_L2_Gen.Traffic_Collection()
    test_result['Spirent_UC_traffic'] = Spirent_L2_Gen.Validate_Traffic_Result2()
    Spirent_L2_Gen.delete_streams_clear_counters()

    StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_Mbps(0,1,**Spirent_InputParam_2TAG_BC)
    StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_Mbps(1,0,**Spirent_InputParam_2TAG_BC)
    Spirent_L2_Gen.Generate_Traffic()
    Spirent_L2_Gen.Traffic_Collection()
    test_result['Spirent_BC_traffic'] = Spirent_L2_Gen.Validate_Traffic_Result2()
    Spirent_L2_Gen.delete_streams_clear_counters()

    StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_Mbps(0,1,**Spirent_InputParam_2TAG_MC)
    StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_Mbps(1,0,**Spirent_InputParam_2TAG_MC)
    Spirent_L2_Gen.Generate_Traffic()
    Spirent_L2_Gen.Traffic_Collection()
    test_result['Spirent_MC_traffic'] = Spirent_L2_Gen.Validate_Traffic_Result2()

    Spirent_L2_Gen.Clean_Up_Spirent()
    test_result['CFM_Stats_Acc'] = my_config.mep_statistic_accedian()
    test_result['CFM_Stats_cisco'] = my_config.mep_statistic_cisco()
    my_config.check_QOS_counters_config()
    my_config.delete_config()
    my_config.disconnect_nodes()
    return test_result



#result['FF'] = onnet_CCM_Y1564_CCA('F','F')
#result['XX'] = onnet_CCM_Y1564_CCA('X','X')
# result['PP'] = onnet_CCM_Y1564_CCA('P','P')
# result['XP'] = onnet_CCM_Y1564_CCA('X','P')
# result['PX'] = onnet_CCM_Y1564_CCA('P','X')
# result['FY'] = onnet_CCM_Y1564_CCA('F','Y')
# result['YF'] = onnet_CCM_Y1564_CCA('Y','F')
result['YY'] = onnet_CCM_Y1564_CCA('Y','Y')

pprint(result)