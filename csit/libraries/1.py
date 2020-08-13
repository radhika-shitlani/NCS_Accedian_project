
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

output = '''
Domain COLT-1 (level 1), Service ALX_NCS_LE-102305
Up MEP on TenGigE0/0/0/5.2305 MEP-ID 2
================================================================================
  Interface state: Up      MAC address: 0032.1705.b414
  Peer MEPs: 1 up, 0 with errors, 0 timed out (archived)
  Cross-check errors: 0 missing, 0 unexpected

  CCM generation enabled:  Yes, 1s (Remote Defect detected: No)
                           CCM processing offloaded to hardware
  AIS generation enabled:  No
  Sending AIS:             No
  Receiving AIS:           No

  Packet        Sent      Received
  ------  ----------  ---------------------------------------------------------
  DMM            172           297
  DMR            297           171
  SLM           1719          2969
  SLR           2969          1718
 '''

dict3 = {}
file_path = os.path.dirname(os.path.realpath(__file__))
def mep_statistic_accedian():
    dict3['tx'] = {}
    dict3['rx'] = {}
    print(type(output))
    for dm_sl in ['DM','SL']:
        for M in ['M','R']:                
                X = re.findall("{}{}\s+\w+\s+\w+".format(dm_sl,M), output)
                print(X[0].split())
                id = '{}{}'.format(dm_sl,M)
                dict3['tx'][id] = X[0].split()[1]
                dict3['rx'][id] = X[0].split()[-1]
                # id = '{}{}'.format(dm_sl,M)
                # if '{}{}'.format(dm_sl,M) == 'DMM' or '{}{}'.format(dm_sl,M) == 'SLM':
                #     if int(X[0].split()[-1]) > 0:
                #         dict3['tx'][id] = int(X[0].split()[-1])
                #     if int(X[1].split()[-1]) > 0:
                #         dict3['rx'][id] = int(X[1].split()[-1])
                # else:
                #     if int(X[1].split()[-1]) > 0:
                #         dict3['tx'][id] = int(X[1].split()[-1])
                #     if int(X[0].split()[-1]) > 0:
                #         dict3['rx'][id] = int(X[0].split()[-1])
    pprint(dict3)
mep_statistic_accedian()

