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
def onnet_CCM_Y1564_FF():

    print("!"*1)
    print("!"*2)
    print("************** Test FF type EP ************* ")
    print("!!"*3)
    dict1 = yaml.load(open(file_path + '/../Topology/inputfile.yml'),Loader=yaml.Loader)
    dict1['site_list'][0]['port_type'] = 'F-type'
    dict1['site_list'][1]['port_type'] = 'F-type'
    dict1['site_list'][2]['port_type'] = 'F-type'
    my_config = Service(**dict1)
    my_config.connect_nodes()
    my_config.parse_accedian()
    my_config = Service(**dict1)
    my_config.Command_Creation()
    my_config.push_config()
    # my_config.parse_accedian()
    # my_config.Command_Creation()
    test_result = {}
    test_result['ccm_status'] = my_config.Validate_ccm()
    test_result['Loop_test'] = my_config.Y1564_test()
    my_config.check_QOS_counters_config()
    my_config.delete_config()
    my_config.disconnect_nodes()
    return test_result
def onnet_CCM_Y1564_XX():

    print("!"*1)
    print("!"*2)
    print("************** Test XX type EP ************* ")
    print("!!"*3)
    dict1 = yaml.load(open(file_path + '/../Topology/inputfile.yml'),Loader=yaml.Loader)
    dict1['site_list'][0]['port_type'] = 'X-type'
    dict1['site_list'][1]['port_type'] = 'X-type'
    dict1['site_list'][2]['port_type'] = 'X-type'
    my_config = Service(**dict1)
    my_config.parse_accedian()
    my_config = Service(**dict1)
    my_config.Command_Creation()
    my_config.push_config()
    # my_config.parse_accedian()
    # my_config.Command_Creation()
    test_result = {}
    test_result['ccm_status'] = my_config.Validate_ccm()
    test_result['Loop_test'] = my_config.Y1564_test()
    my_config.check_QOS_counters_config()
    my_config.delete_config()
    return test_result
def onnet_CCM_Y1564_PP():

    print("!"*1)
    print("!"*2)
    print("************** Test PP type EP ************* ")
    print("!!"*3)
    dict1 = yaml.load(open(file_path + '/../Topology/inputfile.yml'),Loader=yaml.Loader)
    dict1['site_list'][0]['port_type'] = 'P-type'
    dict1['site_list'][1]['port_type'] = 'P-type'
    dict1['site_list'][2]['port_type'] = 'P-type'
    my_config = Service(**dict1)
    my_config.parse_accedian()
    my_config = Service(**dict1)
    my_config.Command_Creation()
    my_config.push_config()
    my_config.parse_accedian()
    my_config.Command_Creation()
    test_result = {}
    test_result['ccm_status'] = my_config.Validate_ccm()
    test_result['Loop_test'] = my_config.Y1564_test()
    my_config.check_QOS_counters_config()
    my_config.delete_config()
    return test_result
def onnet_CCM_Y1564_XP():

    print("!"*1)
    print("!"*2)
    print("************** Test XP type EP ************* ")
    print("!!"*3)
    dict1 = yaml.load(open(file_path + '/../Topology/inputfile.yml'),Loader=yaml.Loader)
    dict1['site_list'][0]['port_type'] = 'X-type'
    dict1['site_list'][1]['port_type'] = 'P-type'
    dict1['site_list'][2]['port_type'] = 'P-type'
    my_config = Service(**dict1)
    my_config.parse_accedian()
    my_config = Service(**dict1)
    my_config.Command_Creation()
    my_config.push_config()
    my_config.parse_accedian()
    my_config.Command_Creation()
    test_result = {}
    test_result['ccm_status'] = my_config.Validate_ccm()
    test_result['Loop_test'] = my_config.Y1564_test()
    my_config.check_QOS_counters_config()
    my_config.delete_config()
    return test_result
def onnet_CCM_Y1564_PX():

    print("!"*1)
    print("!"*2)
    print("************** Test PX type EP ************* ")
    print("!!"*3)
    dict1 = yaml.load(open(file_path + '/../Topology/inputfile.yml'),Loader=yaml.Loader)
    dict1['site_list'][0]['port_type'] = 'P-type'
    dict1['site_list'][1]['port_type'] = 'X-type'
    dict1['site_list'][2]['port_type'] = 'X-type'
    my_config = Service(**dict1)
    my_config.parse_accedian()
    my_config = Service(**dict1)
    my_config.Command_Creation()
    my_config.push_config()
    my_config.parse_accedian()
    my_config.Command_Creation()
    test_result = {}
    test_result['ccm_status'] = my_config.Validate_ccm()
    test_result['Loop_test'] = my_config.Y1564_test()
    my_config.check_QOS_counters_config()
    my_config.delete_config()
    return test_result
def onnet_CCM_Y1564_FY():

    print("!"*1)
    print("!"*2)
    print("************** Test FY type EP ************* ")
    print("!!"*3)
    dict1 = yaml.load(open(file_path + '/../Topology/inputfile.yml'),Loader=yaml.Loader)
    dict1['site_list'][0]['port_type'] = 'F-type'
    dict1['site_list'][1]['port_type'] = 'Y-type'
    dict1['site_list'][2]['port_type'] = 'Y-type'
    my_config = Service(**dict1)
    my_config.parse_accedian()
    my_config = Service(**dict1)
    my_config.Command_Creation()
    my_config.push_config()
    my_config.parse_accedian()
    my_config.Command_Creation()
    test_result = {}
    test_result['ccm_status'] = my_config.Validate_ccm()
    test_result['Loop_test'] = my_config.Y1564_test()
    my_config.check_QOS_counters_config()
    my_config.delete_config()
    return test_result
def onnet_CCM_Y1564_YF():

    print("!"*1)
    print("!"*2)
    print("************** Test YF type EP ************* ")
    print("!!"*3)
    dict1 = yaml.load(open(file_path + '/../Topology/inputfile.yml'),Loader=yaml.Loader)
    dict1['site_list'][0]['port_type'] = 'Y-type'
    dict1['site_list'][1]['port_type'] = 'F-type'
    dict1['site_list'][2]['port_type'] = 'F-type'
    my_config = Service(**dict1)
    my_config.parse_accedian()
    my_config = Service(**dict1)
    my_config.Command_Creation()
    my_config.push_config()
    my_config.parse_accedian()
    my_config.Command_Creation()
    test_result = {}
    test_result['ccm_status'] = my_config.Validate_ccm()
    test_result['Loop_test'] = my_config.Y1564_test()
    my_config.check_QOS_counters_config()
    my_config.delete_config()
    return test_result
def onnet_CCM_Y1564_YY():

    print("!"*1)
    print("!"*2)
    print("************** Test YY type EP ************* ")
    print("!!"*3)
    dict1 = yaml.load(open(file_path + '/../Topology/inputfile.yml'),Loader=yaml.Loader)
    dict1['site_list'][0]['port_type'] = 'Y-type'
    dict1['site_list'][1]['port_type'] = 'Y-type'
    dict1['site_list'][2]['port_type'] = 'Y-type'
    my_config = Service(**dict1)
    my_config.parse_accedian()
    my_config = Service(**dict1)
    my_config.Command_Creation()
    my_config.push_config()
    my_config.parse_accedian()
    my_config.Command_Creation()
    test_result = {}
    test_result['ccm_status'] = my_config.Validate_ccm()
    test_result['Loop_test'] = my_config.Y1564_test()
    my_config.check_QOS_counters_config()
    my_config.delete_config()
    return test_result


result['FF'] = onnet_CCM_Y1564_FF()
# result['XX'] = onnet_CCM_Y1564_XX()
# result['PP'] = onnet_CCM_Y1564_PP()
# result['XP'] = onnet_CCM_Y1564_XP()
# result['PX'] = onnet_CCM_Y1564_PX()
# result['FY'] = onnet_CCM_Y1564_FY()
# result['YF'] = onnet_CCM_Y1564_YF()
# result['YY'] = onnet_CCM_Y1564_YY()

pprint(result)