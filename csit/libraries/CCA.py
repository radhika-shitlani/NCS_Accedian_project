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

def onnet_CCM_Y1564():

    dict1 = yaml.load(open(file_path + '/../Topology/inputfile.yml'),Loader=yaml.Loader)
    my_config = Service(**dict1)
    meg_index = my_config.parse_accedian()
    my_config = Service(**dict1)
    my_config.Command_Creation()
    my_config.push_config()
    test_result = {}
    test_result['ccm_status'] = my_config.Validate_ccm()
    test_result['Loop_test'] = my_config.Y1564_test()
  
    # Spirent_InputParam = {
    #     'Frame_Size':9100, 
    #     'Rate_Mbps': 400,
    #     'vlan_id' : 2301,
    #     'vlan_user_priority': 1,
    #     'VLAN_EtherType': 8100
    
    #     }
    # Spirent_L2_Gen = Create_Spirent_L2_Gen()
    # Spirent_L2_Gen.Port_Init()
    # print("Just Before Stream Creation-1")
    # StreamHandle = Spirent_L2_Gen.Stream_Config_Creation_Single_Tagged_VLAN_Mbps(0,1,**Spirent_InputParam)
    # #Spirent_L2_Gen.Generate_Stream_Traffic(StreamHandle)
    # print("Just Before Stream Creation-2")
    # StreamHandle = Spirent_L2_Gen.Stream_Config_Creation_Single_Tagged_VLAN_Mbps(1,0,**Spirent_InputParam)
    # #Spirent_L2_Gen.Generate_Stream_Traffic(StreamHandle)
    # Spirent_L2_Gen.Generate_Traffic()
    # Spirent_L2_Gen.Traffic_Collection()
    # test_result['spirent_test'] = Spirent_L2_Gen.Validate_Traffic_Result()
    my_config.delete_config()
    return test_result

result = onnet_CCM_Y1564()
pprint(result)