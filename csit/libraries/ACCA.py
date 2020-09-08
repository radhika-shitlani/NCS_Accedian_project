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
def onnet_CCM_Y1564_ACCA(A,B):

    print("!"*1)
    print("!"*2)
    print("************** Test {}{} type EP ************* ".format(A,B))
    print("!!"*3)
    dict1 = yaml.load(open(file_path + '/../Topology/inputfile_ACCA.yml'),Loader=yaml.Loader)
    dict1['site_list'][0]['port_type'] = '{}-type'.format(A)
    dict1['site_list'][1]['port_type'] = '{}-type'.format(B)
    dict1['site_list'][2]['port_type'] = '{}-type'.format(A)
    dict1['site_list'][3]['port_type'] = '{}-type'.format(B)
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
    my_config.disconnect_nodes()
    # input_dict = {}
    # input_dict = my_config.create_spirent_input_dict()
    # Spirent_L2_Gen = Create_Spirent_L2_Gen()
    # Spirent_L2_Gen.Port_Init()

    #### perform rfc Test
    if A == 'Y':
        StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_Mbps(0,1,**input_dict['Spirent_2TAG_AZ']['UC'])
    elif A == 'F' or A == 'X':
        StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Single_Tagged_VLAN_Mbps(0,1,**input_dict['Spirent_1TAG_AZ']['UC'])
    else:                 
        StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Without_VLAN_Mbps(0,1,**input_dict['Spirent_0TAG_AZ']['UC'])
    if B == 'Y':
        StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_Mbps(1,0,**input_dict['Spirent_2TAG_ZA']['UC'])
    elif B == 'F' or B == 'X':
        StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Single_Tagged_VLAN_Mbps(1,0,**input_dict['Spirent_1TAG_ZA']['UC'])
    else:
        StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Without_VLAN_Mbps(1,0,**input_dict['Spirent_0TAG_ZA']['UC'])
    # test_result['rfc_tput_test'] = Spirent_L2_Gen.rfc_2544_throughput_test(StreamHandle1,StreamHandle2)
    test_result['rfc_fl_test'] = Spirent_L2_Gen.rfc_2544_frameloss_test(StreamHandle1,StreamHandle2)
    # test_result['rfc_b2b_test'] = Spirent_L2_Gen.rfc_2544_backtoback_test(StreamHandle1,StreamHandle2)
    # test_result['rfc_latency_test'] = Spirent_L2_Gen.rfc_2544_latency_test(StreamHandle1,StreamHandle2)
    Spirent_L2_Gen.delete_streams_clear_counters()

    ### test UC,MC,BC Traffic, with % of total BW( default MTU is 9100)        
    # for tr in ['UC','BC','MC']:
    #     if A == 'Y':
    #         StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_Mbps(0,1,**input_dict['Spirent_2TAG_AZ'][tr])
    #     elif A == 'F' or A == 'X':
    #         StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Single_Tagged_VLAN_Mbps(0,1,**input_dict['Spirent_1TAG_AZ'][tr])
    #     else:                 
    #         StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Without_VLAN_Mbps(0,1,**input_dict['Spirent_0TAG_AZ'][tr])
        
    #     if B == 'Y':
    #         StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_Mbps(1,0,**input_dict['Spirent_2TAG_ZA'][tr])
    #     elif B == 'F' or B == 'X':
    #         StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Single_Tagged_VLAN_Mbps(1,0,**input_dict['Spirent_1TAG_ZA'][tr])
    #     else:
    #         StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Without_VLAN_Mbps(1,0,**input_dict['Spirent_0TAG_ZA'][tr])   
        
    #     Spirent_L2_Gen.Generate_Traffic()
    #     Spirent_L2_Gen.Traffic_Collection()
    #     test_result['Spirent_{}_traffic'.format(tr)] = Spirent_L2_Gen.Validate_Traffic_Result2()
    #     Spirent_L2_Gen.delete_streams_clear_counters()

    # # if A == 'P' and B == 'P':
    # #     for mt_vt in ['MT','VT','L2CP']:
    # #         print("**** {} traffic is going to run".format(mt_vt))
    # #         if mt_vt == 'MT':
    # #             StreamHandleMT1 = Spirent_L2_Gen.Spirent_MAC_Transperancy_Traffic_Testing_For_P2P_Service(0,1,**input_dict['Spirent_0TAG_AZ']['UC'])
    # #             StreamHandleMT2 = Spirent_L2_Gen.Spirent_MAC_Transperancy_Traffic_Testing_For_P2P_Service(1,0,**input_dict['Spirent_0TAG_ZA']['UC'])
    # #         elif mt_vt == 'VT':
    # #             StreamHandleVT1 = Spirent_L2_Gen.Spirent_VLAN_Transperancy_Traffic_Testing_For_P2P_Service(0,1,**input_dict['Spirent_1TAG_AZ']['UC'])
    # #             StreamHandleVT2 = Spirent_L2_Gen.Spirent_VLAN_Transperancy_Traffic_Testing_For_P2P_Service(1,0,**input_dict['Spirent_1TAG_ZA']['UC'])                    
    # #         else:
    # #             StreamHandlel2CP1 = Spirent_L2_Gen.Spirent_L2CP_Transperancy_Traffic_Testing_For_P2P_Service(0,1,**input_dict['Spirent_0TAG_AZ']['UC'])
    # #             StreamHandleL2CP2 = Spirent_L2_Gen.Spirent_L2CP_Transperancy_Traffic_Testing_For_P2P_Service(1,0,**input_dict['Spirent_0TAG_ZA']['UC'])
    # #         Spirent_L2_Gen.Generate_Traffic()
    # #         Spirent_L2_Gen.Traffic_Collection()
    # #         test_result['Spirent_{}_traffic'.format(mt_vt)] = Spirent_L2_Gen.Validate_Traffic_Result2()
    # #         Spirent_L2_Gen.delete_streams_clear_counters()
   

    #Spirent_L2_Gen.Clean_Up_Spirent()
    my_config.connect_nodes()
    test_result['CFM_Stats_ACC'] = my_config.mep_statistic_accedian()
    my_config.check_QOS_counters_config()
    my_config.delete_config()
    my_config.disconnect_nodes()
    return test_result

#result['FF'] = onnet_CCM_Y1564_ACCA('F','F')
result['XX'] = onnet_CCM_Y1564_ACCA('X','X')
# result['PP'] = onnet_CCM_Y1564_ACCA('P','P')
# result['XP'] = onnet_CCM_Y1564_ACCA('X','P')
# result['PX'] = onnet_CCM_Y1564_ACCA('P','X')
# result['FY'] = onnet_CCM_Y1564_ACCA('F','Y')
# result['YF'] = onnet_CCM_Y1564_ACCA('Y','F')
# result['YY'] = onnet_CCM_Y1564_ACCA('Y','Y')

pprint(result)