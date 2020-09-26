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
import ast
from Class_Based_Spirent_Code_Generation import Spirent_L2_Traffic_Gen,Get_Spirent_Config,Create_Spirent_L2_Gen
from get_stream_handle import *
file_path = os.path.dirname(os.path.realpath(__file__))
result = {}


def lag_test(service_obj,spirent_obj,A,B,iter):
    test_result = {}
    # pprint(service_obj.data)
    for node in service_obj.data["site_list"]:
        if node['login']['device_type'] == 'cisco_xr' and 'Bun' in node['main_interface']:
            if node['Lag_test_eligible']:
                service_obj.connect_nodes()
                test_result[node['Node_name']] = {}
                test_result[node['Node_name']]['failure'] = {}
                test_result[node['Node_name']]['repair'] = {}
                input_dict1 = {}
                input_dict1 = service_obj.create_spirent_input_dict_PPS(**node)
                # pprint(input_dict1)
                switchover_stream_handle = get_switchover_stream_handle(A,B,spirent_obj,**input_dict1)
                # print(switchover_stream_handle)                      
                for i in range(iter):
                    for fail_repair in ['failure','repair']:          
                        print(f"*** iteration {i} , {fail_repair} test")
                        spirent_obj.Generate_Traffic_port_based()
                        time.sleep(spirent_obj.sw_test_duration / 10)
                        output = node['connect_obj'].send_config_set(node[f'{fail_repair}_command'])
                        print(output)
                        node['connect_obj'].commit()
                        node['connect_obj'].exit_config_mode()
                        print("**** waiting for the Traffic to stop")
                        time.sleep(spirent_obj.sw_test_duration + 10)
                        spirent_obj.Stop_Traffic_port_based()
                        spirent_obj.Traffic_Collection()
                        test_result[node['Node_name']][fail_repair][i] = spirent_obj.Validate_Traffic_Result2()
                        spirent_obj.Clear_counters_port_based()
                spirent_obj.delete_streams_clear_counters()
                service_obj.disconnect_nodes()
    pprint(test_result)
    return test_result