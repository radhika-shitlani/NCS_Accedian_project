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

file_path = os.path.dirname(os.path.realpath(__file__))
result = {}



def get_rfc_stream_handle(A,B,Spirent_L2_Gen,**input_dict):
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
    rfc_stream_handle = []
    rfc_stream_handle.append(StreamHandle1)
    rfc_stream_handle.append(StreamHandle2)
    return rfc_stream_handle

def get_UC_BC_MC_stream_handle(A,B,tr,Spirent_L2_Gen,**input_dict):
    if A == 'Y':
        StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_Mbps(0,1,**input_dict['Spirent_2TAG_AZ'][tr])
    elif A == 'F' or A == 'X':
        StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Single_Tagged_VLAN_Mbps(0,1,**input_dict['Spirent_1TAG_AZ'][tr])
    else:                 
        StreamHandle1 = Spirent_L2_Gen.Stream_Config_Creation_Without_VLAN_Mbps(0,1,**input_dict['Spirent_0TAG_AZ'][tr])
    
    if B == 'Y':
        StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_Mbps(1,0,**input_dict['Spirent_2TAG_ZA'][tr])
    elif B == 'F' or B == 'X':
        StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Single_Tagged_VLAN_Mbps(1,0,**input_dict['Spirent_1TAG_ZA'][tr])
    else:
        StreamHandle2 = Spirent_L2_Gen.Stream_Config_Creation_Without_VLAN_Mbps(1,0,**input_dict['Spirent_0TAG_ZA'][tr])   
    UC_BC_MC_stream_handle = []
    UC_BC_MC_stream_handle.append(StreamHandle1)
    UC_BC_MC_stream_handle.append(StreamHandle2)
    return UC_BC_MC_stream_handle

def get_MT_VT_l2CP_stream_handle(mt_vt,Spirent_L2_Gen,**input_dict):
    if mt_vt == 'MT':
        StreamHandle1 = Spirent_L2_Gen.Spirent_MAC_Transperancy_Traffic_Testing_For_P2P_Service(0,1,**input_dict['Spirent_0TAG_AZ']['UC'])
        StreamHandle2 = Spirent_L2_Gen.Spirent_MAC_Transperancy_Traffic_Testing_For_P2P_Service(1,0,**input_dict['Spirent_0TAG_ZA']['UC'])
    elif mt_vt == 'VT':
        StreamHandle1 = Spirent_L2_Gen.Spirent_VLAN_Transperancy_Traffic_Testing_For_P2P_Service(0,1,**input_dict['Spirent_1TAG_AZ']['UC'])
        StreamHandle2 = Spirent_L2_Gen.Spirent_VLAN_Transperancy_Traffic_Testing_For_P2P_Service(1,0,**input_dict['Spirent_1TAG_ZA']['UC'])                    
    else:
        StreamHandle1 = Spirent_L2_Gen.Spirent_L2CP_Transperancy_Traffic_Testing_For_P2P_Service(0,1,**input_dict['Spirent_0TAG_AZ']['UC'])
        StreamHandle2 = Spirent_L2_Gen.Spirent_L2CP_Transperancy_Traffic_Testing_For_P2P_Service(1,0,**input_dict['Spirent_0TAG_ZA']['UC'])
    MT_VT_l2CP_stream_handle = []
    MT_VT_l2CP_stream_handle.append(StreamHandle1)
    MT_VT_l2CP_stream_handle.append(StreamHandle2)
    return MT_VT_l2CP_stream_handle

