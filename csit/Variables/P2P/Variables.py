#########################
##    NCS COMMANDS     ##
#########################

R1_interface_data = {
    'description': 'Ankit - Automation Test Service',
    'mtu': '9100',
    'output_policy': 'egr',
    'acc_value': '26'
}


R2_interface_data = {
    'description': 'Ankit - Automation Test Service',
    'mtu': '9100',
    'output_policy': 'egr',
    'acc_value': '26'
}


# service_type P = default   X = dot1ad/dot1q <Vlan-id>   Y = dot1q/dot1ad <Vlan-Id> second dot1q <Vlan-Id>   D = dot1q/dot1ad <Vlan-Id> second dot1q <Vlan-Id>   F = dot1ad/dot1q <Vlan-Id>

R1_sub_interface_data = {
    'description': 'Ankit - Automation Test Service',
    'service_type': 'P',            # P/F/X/Y/D
    'encapsulation1': 'dot1q 101',  #dot1q or dot1ad <vlan> // populate only for F/X/Y/D
    'encapsulation2': 'dot1q 102'   #dot1q or dot1ad <vlan> // populate only for Y/D
}

R2_sub_interface_data = {
    'description': 'Ankit - Automation Test Service',
    'service_type': 'P',            # P/F/X/Y/D
    'encapsulation1': 'dot1q 101',  # 'dot1q or dot1ad <vlan>' // populate only for F/X/Y/D
    'encapsulation2': 'dot1q 102'   # 'dot1q or dot1ad <vlan>' // populate only for Y/D
}

## Added on 5th June 2020


R1_sub_interface_X_data = {
    'description': 'Ankit - Automation Test Service X',
    'service_type': 'X',            # P/F/X/Y/D
    'encapsulation1': 'dot1q 49'  #dot1q or dot1ad <vlan> // populate only for F/X/Y/D
}

R1_sub_interface_F_data = {
    'description': 'Ankit - Automation Test Service F',
    'service_type': 'F',            # P/F/X/Y/D
    'encapsulation1': 'dot1q 49'  #dot1q or dot1ad <vlan> // populate only for F/X/Y/D
}


R1_sub_interface_Y_data = {
    'description': 'Ankit - Automation Test Service Y',
    'service_type': 'Y',            # P/F/X/Y/D
    'encapsulation1': 'dot1ad 50',  #dot1q or dot1ad <vlan> // populate only for F/X/Y/D
    'encapsulation2': 'dot1q 49'   #dot1q or dot1ad <vlan> // populate only for Y/D
}


R2_sub_interface_X_data = {
    'description': 'Ankit - Automation Test Service X',
    'service_type': 'X',            # P/F/X/Y/D
    'encapsulation1': 'dot1q 50'  #dot1q or dot1ad <vlan> // populate only for F/X/Y/D
}

R2_sub_interface_F_data = {
    'description': 'Ankit - Automation Test Service F',
    'service_type': 'F',            # P/F/X/Y/D
    'encapsulation1': 'dot1q 49'  #dot1q or dot1ad <vlan> // populate only for F/X/Y/D
}



Pol_map_egr_data = {
    'output_policy' : 'egr'
}

Ser_Pol_map_1G_data = {
    'ser_policy_map': 'BW-1Gbps-Class-test',
    'police_rate': '1000000 kbps',
    'burst': '100 kbytes',
    'traffic_class': '2',
    'qos_group': '2'
}

Ser_Pol_map_500M_data = {
    'ser_policy_map': 'BW-500M-Class-test',
    'police_rate': '500000 kbps',
    'burst': '100 kbytes',
    'traffic_class': '2',
    'qos_group': '2'
}

R1_evpn_data = {
    'evpn_id': '2100',
    'rd': '8220001:2100',
    'rt_import': '8220001:2100',
	'rt_export': '8220001:2100'
}

R2_evpn_data = {
    'evpn_id': '2100',
    'rd': '8220001:2100',
    'rt_import': '8220001:2100',
	'rt_export': '8220001:2100'
}

R1_l2vpn_data = {
    'xc_group': 'AR13_AR14_LE-500134',
    'p2p_xc_name': 'AR13_AR14_LE-500134',
    #'attch_ckt_intf': 'TenGigE0/0/0/30.4095',
	'evpn_id': '2100',
    'rmte_attc_ckt_id': '134',
    'src_attc_ckt_id': '143',
}

R2_l2vpn_data = {
    'xc_group': 'AR13_AR14_LE-500134',
    'p2p_xc_name': 'AR13_AR14_LE-500134',
    #'attch_ckt_intf': 'TenGigE0/0/0/30.4095',
	'evpn_id': '2100',
    'rmte_attc_ckt_id': '143',
    'src_attc_ckt_id': '134',
}


R1_cfm_data = {
    'domain_name': 'COLT-1',
    'domain_level': '1',
    'service_name': 'AR13_AR14_LE-500134',
	'xc_group': 'AR13_AR14_LE-500134',
    'p2p_xc_name': 'AR13_AR14_LE-500134',
    'ICC': 'LE',
    'UMC': 'XXX-500134',
	'local_mep_id': '1',
    'remote_mep_id': '2',
    'SLM': 'yes'  # if required= yes, not required= blank
}

##SLM parameter is not present as SLM config not required on other end
R2_cfm_data = {
    'domain_name': 'COLT-1',
    'domain_level': '1',
    'service_name': 'AR13_AR14_LE-500134',
	'xc_group': 'AR13_AR14_LE-500134',
    'p2p_xc_name': 'AR13_AR14_LE-500134',
    'ICC': 'LE',
    'UMC': 'XXX-500134',
	'local_mep_id': '2',
    'remote_mep_id': '1'
}

## Loopback L1
L1_Loopback_Internal_data = {
    'LoopbackType': 'internal'
}

L1_Loopback_External_data = {
    'LoopbackType': 'external'
}

L1_Loopback_Line_data = {
    'LoopbackType': 'line'
}

## Loopback L2
L2_Loopback_Internal_data = {
    'LoopbackType': 'internal'
}

L2_Loopback_External_data = {
    'LoopbackType': 'external'
}

# LLF config contain no variables. will be applied under intf/sub-intf
LLF_data = {}

# When ever new sub-interface is required, it will added here. No logic is developed to create sub-int from vlan (maybe in future we create that logic).
sub_interface_4095 = '4095'     # For encapsulation default
sub_interface_49 = '49'         # For X/Y/F
sub_interface_4097 = '4097'


# Data to be verified in NCS will be added here

local_mep_info = "Local MEPs: 1 total: all operational, no errors"
peer_mep_info = "Peer MEPs: 1 total: all operational, no errors"

intf_status = "up        up"    # 8 spaces

L2VPN_status = """UP        UP        UP"""     # 8 spaces

## make sure there is one space before Lost
SLM_status =""" Lost: 0 (0.0%); Corrupt: 0 (0.0%);
 Lost: 0 (0.0%); Corrupt: 0 (0.0%);
 Lost: 0 (0.0%); Corrupt: 0 (0.0%);
 Lost: 0 (0.0%); Corrupt: 0 (0.0%);"""





#########################
##  ACCEDIAN COMMANDS  ##
#########################

accedian_port_status = """Enabled        Up"""      # 8 spaces
mep_status = """Ok        False"""
#mep_status = """Failed        False"""


R3_port1_data = {
    'PortAliasName': '"Automation Test - UNI Port-Ankit"',
    'autoNegValue': 'disable',
    'portSpeed': '1G',
    'mtuValue': '10240'
}

R3_port5_data = {
    'PortAliasName': '"Automation Test - NNI Port-Ankit"',
    'autoNegValue': 'disable',
    'portSpeed': '10G',
    'mtuValue': '10240'
}

R3_1G_UNI_regulator_data = {
    'RegulatorName': 'U1_ANK_VER_LE-123456',
    'CirValue':  '1000000 ',
    'CirMax': '1000000',
    'CbsValue': '1024',
    'EirValue': '0',
    'EirMax': '1000000',
    'EbsValue': '10',
    'ColorMode': 'blind',
    'CouplingFlag': 'False'
}

R3_1G_NNI_regulator_data = {
    'RegulatorName': 'N1_ANK_VER_LE-123456',
    'CirValue':  '1000000 ',
    'CirMax': '1000000',
    'CbsValue': '1024',
    'EirValue': '0',
    'EirMax': '1000000',
    'EbsValue': '10',
    'ColorMode': 'blind',
    'CouplingFlag': 'False'
}

R3_Filter_Traffic5_data={
    'FilterType': 'l2',
    'FilterName': 'N1_ANK_VER_LE-123456',
    'vlan1EtherType': 'c-vlan',
    'vlan1Id': '1050'
}

#can be used for all type of traffic policy
R3_Traffic1_Policy_data = {
    'PortNumber': '1',
    'PolicyId': '3',
    'colour': 'green',
    'RegulatorName': 'U1_ANK_VER_LE-123456',
    'filterType': 'l2',
    'VidSetOrFilterName': '*default',
    'VlanAction': 'push',
    'firstVlanType': 'c-vlan',
    'firstVlanId': '1050',
    'secondVlanType': '',
    'secondVlanId': '',
    'greenPcpValue': '3',
    'yellowPcpValue': '0',
    'outPortName': 'PORT-5'
}
R3_Traffic5_Policy_data = {
    'PortNumber': '5',
    'PolicyId': '3',
    'colour': 'green',
    'RegulatorName': 'N1_ANK_VER_LE-123456',
    'filterType': 'l2',
    'VidSetOrFilterName': 'N1_ANK_VER_LE-123456',
    'VlanAction': 'pop',
    'firstVlanType': '',
    'firstVlanId': '',
    'secondVlanType': '',
    'secondVlanId': '',
    'greenPcpValue': '2',
    'yellowPcpValue': '0',
    'outPortName': 'PORT-1'
}


R3_CFM_MEG_Traffic5_Data = {
    'megName': 'LEXXX-101101',
    'ccmInterval': '1000',
    'megIndex': '1',
    'megLevel': '1',
    'rmepAutoDiscoveryOption': 'disable',
    'MepIdList': '1,2',
    'VidList': '1050',
    'VlanType': 'c-vlan'
}

R3_CFM_MEP_Traffic5_Data = {
    'mepName': 'LEXXX-101101|1|2',
    'active': 'yes',
    'mepIndex': '1',
    'direction': 'down',
    'cciEnable': 'yes',
    'ccmSeqNumber': 'enable',
    'megIndex': '1',
    'LowestAlarmPri': 'macRemErrXconAis',
    'mepId': '2',
    'PortName': 'PORT-5',
    'mepPriority': '2',
    'pvid': '1050'
}
