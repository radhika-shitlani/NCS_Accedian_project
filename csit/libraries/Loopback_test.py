##############################################################
# Loading HLTAPI for Python
##############################################################
from __future__ import print_function
import sth
import time
import json
import os
import sys
import yaml
import re
from pprint import pprint
from netmiko import Netmiko
import datetime
#from genie import testbed
from jinja2 import Template
import csv


class Loopback_test:

    def __init__(self,service_obj,spirent_obj,rfc_stream_handle,A,B):
        self.A_IP = service_obj.data['site_list'][0]['login']['host']
        self.B_IP = service_obj.data['site_list'][1]['login']['host']
        self.A_UNI = service_obj.data['site_list'][0]['main_interface']
        self.B_UNI = service_obj.data['site_list'][1]['main_interface']
        self.A_TEQ = spirent_obj.port_list[0]
        self.B_TEQ = spirent_obj.port_list[1]
        self.serv_type = f"{A}{B}"

        self.deviceA = {
            "host": self.A_IP,
            "username": "dshaw1",
            "password": "N0@ught33b0y",
            "device_type": "cisco_xr",
        }
        self.deviceB = {
            "host": self.B_IP,
            "username": "dshaw1",
            "password": "N0@ught33b0y",
            "device_type": "cisco_xr",
        }
        self.port_list = [self.A_TEQ, self.B_TEQ]
        self.interface_name = {
            "deviceA": self.A_UNI,
            "deviceB": self.B_UNI
        }
        self.device_list = [self.deviceA, self.deviceB]
        self.List1 = ['L2']
        self.List2 = ['Set', 'Release']
        self.dict_result = {}
        self.interface_name_list = []
        self.file_path = os.path.dirname(os.path.realpath(__file__))
        self.sub_interface = service_obj.data['item']
        self.F_vlan = service_obj.data['item']
        self.loop_id = 1
        self.deviceA_X_VLAN = service_obj.data['item']
        self.deviceB_X_VLAN = service_obj.data['item']
        self.deviceA_Y_VLAN = [service_obj.data['item'] + 100 ,service_obj.data['item']]
        self.deviceB_F_VLAN = service_obj.data['item']
        self.traffic_rate = service_obj.data['service_BW'] // 10000
        self.port_speed = spirent_obj.port_speed1[0]  # ether1000,ether10000
        self.copper_fiber = spirent_obj.port_mode1[0]  # copper,fiber
        # self.mac = {
        #     "DMAC": '00:10:94:00:01:13',
        #     "SMAC": '00:10:94:00:01:13'
        # }
        self.rfc_stream_handle = rfc_stream_handle

    def Execute_Loopback_Test(self,spirent_obj):
        def command_ouput(self, interface_name_list, device_list):
            print("**** statistic of traffic on both devices")
            for uni_port, device in zip(interface_name_list, device_list):
                net_connect = Netmiko(**device)
                command = 'show policy-map interface {}.{} | utility egrep "Match\|input\|output\|Drop"'.format(
                    uni_port, self.sub_interface)
                command_ouput = net_connect.send_command("show run hostname")
                command_ouput += net_connect.send_command(command)
                print(command_ouput)
                net_connect.disconnect()

        def clear_QOS_ouput(self, interface_name_list, device_list):
            print("**** clearing statistic on both devices")
            for uni_port, device in zip(interface_name_list, device_list):
                net_connect = Netmiko(**device)
                command = 'clear qos counters interface {}.{}'.format(uni_port, self.sub_interface)
                command_ouput = net_connect.send_command(command)
                print(command_ouput)
                net_connect.disconnect()

        def Command_Creation(self, filename, item1, item2, inter_exter, loop_id, **interface_name):
            if inter_exter == 'internal':
                dict_to_render = {
                    'main_inf': interface_name['deviceB'],
                    'sub_if': self.sub_interface,
                    'internal_external': inter_exter,
                    'Loop_id': loop_id
                }
            else:
                dict_to_render = {
                    'main_inf': interface_name['deviceA'],
                    'sub_if': self.sub_interface,
                    'internal_external': inter_exter,
                    'Loop_id': loop_id
                }
            with open(filename, 'r') as f:
                Temp = f.read()
                failure_command = Template(Temp).render(**dict_to_render)
                f.close()
                file_open = open(self.file_path + "/commands/loop_test/" + str(item1) + "_Loop_" + str(inter_exter) + "_" + str(
                    item2) + "_command.txt", 'w+')
                file_open.write(failure_command)
                file_open.write('\n')
                file_open.close()

        def netmiko_Set_config(self, item1, inter_exter):
            if inter_exter == 'internal':
                net_connect = Netmiko(**self.deviceB)
                print('***** log in to device {}'.format(self.deviceB['host']))
            else:
                net_connect = Netmiko(**self.deviceA)
                print('***** log in to device {}'.format(self.deviceA['host']))
            f = open(self.file_path + "/commands/loop_test/" + str(item1) + "_Loop_" + str(inter_exter) + "_Set_command.txt", 'r')
            f2 = f.readlines()
            clear_QOS_ouput(self, self.interface_name_list, self.device_list)
            output = net_connect.send_config_set(f2)
            net_connect.commit()
            net_connect.exit_config_mode()
            print(output)
            command = "show ethernet loopback active | include ID"
            show_output = net_connect.send_command(command)
            if item1 == "L2":
                show_output_list = show_output.split(" ")
                loop_id_to_render = show_output_list[-1]
                if loop_id_to_render != "1":
                    print("**** doing rendering one more time")
                    Command_Creation(self, location, item1, item2, inter_exter, loop_id_to_render, **self.interface_name)
            net_connect.disconnect()

        def netmiko_Release_config(self, item1, inter_exter):
            if inter_exter == 'internal':
                net_connect = Netmiko(**self.deviceB)
                print('***** log in to device {}'.format(self.deviceB['host']))
            else:
                net_connect = Netmiko(**self.deviceA)
                print('***** log in to device {}'.format(self.deviceA['host']))
            f = open(self.file_path + "/commands/loop_test/" + str(item1) + "_Loop_" + str(inter_exter) + "_Release_command.txt", 'r')
            f2 = f.readlines()
            time.sleep(15)
            command_ouput(self, self.interface_name_list, self.device_list)
            output = net_connect.send_config_set(f2)
            net_connect.commit()
            net_connect.exit_config_mode()
            print(output)
            net_connect.disconnect()

        def spirent_traffic(self, steam_name, item1, inter_exter):
            stream = steam_name['stream_id']
            print(stream)
            traffic_ctrl_ret = sth.traffic_control(
                stream_handle=[stream],
                action='run',
                traffic_start_mode='sync',
                duration='10')

            status = traffic_ctrl_ret['status']
            if (status == '0'):
                print("run sth.traffic_control failed")
                print(traffic_ctrl_ret)
            else:
                print("***** run sth.traffic started successfully")

            traffic_results_ret = sth.traffic_stats(
                port_handle=[spirent_obj.port_handle[0], spirent_obj.port_handle[1]],
                mode='all')

            status = traffic_results_ret['status']
            if (status == '0'):
                print("run sth.traffic_stats failed")
                print(traffic_results_ret)
            else:
                print("***** run sth.traffic_stats successfully, and results is:")
                pprint(traffic_results_ret)
                # pprint(traffic_results_ret1)


            deviceA_tx = traffic_results_ret[spirent_obj.port_handle[0]]['aggregate']['tx']['pkt_count']
            deviceA_rx = traffic_results_ret[spirent_obj.port_handle[0]]['aggregate']['rx']['pkt_count']
            deviceB_tx = traffic_results_ret[spirent_obj.port_handle[1]]['aggregate']['tx']['pkt_count']
            deviceB_rx = traffic_results_ret[spirent_obj.port_handle[1]]['aggregate']['rx']['pkt_count']

            test_result = 'Test Failed'
            if deviceA_rx == deviceA_tx:
                print("***************** " + str(item1) + " " + str(inter_exter) + "Test has Passed")
                print("**** No of Rx packets on deviceA are: " + str(deviceA_rx))
                print("**** No of Tx packets on deviceA are: " + str(deviceA_tx))
                test_result = 'Passed'
            elif deviceB_rx == deviceA_tx:
                print("***************** " + str(item1) + " " + str(inter_exter) + "Test has failed")
                print("**** No of Rx packets on deviceB are: " + str(deviceB_rx))
                print("**** No of Tx packets on deviceA are: " + str(deviceA_tx))
                print("**** No of Rx packets on deviceA are: " + str(deviceA_rx))
                print("**** No of Tx packets on deviceB are: " + str(deviceB_tx))
                test_result = 'Failed'

            else:
                print("something wrong")
                print("**** No of Rx packets on deviceB are: " + str(deviceB_rx))
                print("**** No of Tx packets on deviceA are: " + str(deviceA_tx))
                print("**** No of Rx packets on deviceA are: " + str(deviceA_rx))
                print("**** No of Tx packets on deviceB are: " + str(deviceB_tx))

            dict_name = '{}_{}_result'.format(item1, inter_exter)
            dict_local = {}
            dict_local['deviceA_tx'] = deviceA_tx
            dict_local['deviceA_rx'] = deviceA_rx
            dict_local['deviceB_tx'] = deviceB_tx
            dict_local['deviceB_rx'] = deviceB_rx
            dict_local['result'] = test_result
            dict_local['Traffic_rate'] = self.traffic_rate
            self.dict_result[dict_name] = dict_local

            traffic_ctrl_ret = sth.traffic_control(
                port_handle=[spirent_obj.port_handle[0], spirent_obj.port_handle[1]],
                action='clear_stats')

        for item1 in self.List1:
            if item1 == "L2":
                inter_exter_list = ['internal', 'external']
            else:
                inter_exter_list = ['internal', 'external', 'line']
            for inter_exter in inter_exter_list:
                for item2 in self.List2:
                    location = self.file_path + "/templates/loop_test/" + "tem_" + item1 + "_Loop_" + item2 + "_command.j2"
                    Command_Creation(self, location, item1, item2, inter_exter, self.loop_id, **self.interface_name)
                    print("**** Templateing Done for " + str(item1) + " " + str(inter_exter) + " & " + str(
                        item2) + " command")

        for item1 in self.List1:
            if item1 == "L2":
                inter_exter_list = ['internal']
            else:
                inter_exter_list = ['internal', 'external', 'line']

            for inter_exter in inter_exter_list:
                print("**** perform " + str(item1) + " " + str(inter_exter) + " Loop ")
                netmiko_Set_config(self, item1, inter_exter)
                spirent_traffic(self, self.rfc_stream_handle, item1, inter_exter)
                print("**** Release " + str(item1) + " " + str(inter_exter) + " Loop ")
                netmiko_Release_config(self, item1, inter_exter)
                time.sleep(30)

        ##############################################################
        # clean up the session, release the ports reserved and cleanup the dbfile
        ##############################################################
        spirent_obj.Clean_Up_Spirent()

        print(json.dumps(self.dict_result, indent=4))
        Final_Result = []
        for result in self.dict_result.values():
            Final_Result.append(result["result"])
        return(Final_Result)

def perform_spirent_loop_test(my_config,Spirent_L2_Gen,rfc_stream_handle,A,B):
    Loopback_Test_Handle = Loopback_test(my_config,Spirent_L2_Gen,rfc_stream_handle,A,B)
    Result = Loopback_Test_Handle.Execute_Loopback_Test(Spirent_L2_Gen)
    return (Result)