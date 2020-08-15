
def spirent_call(A,B):
    trafficname = []
    if A == 'F' or A == 'X':
        trafficname.append('Stream_Config_Creation_Single_Tagged_VLAN_Mbps')
    elif A == 'Y':
        trafficname.append('Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_Mbps')
    elif A == 'P':
        trafficname.append('Stream_Config_Creation_Without_VLAN_Mbps')
    else:
        pass
    
    if B == 'F' or B == 'X':
        trafficname.append('Stream_Config_Creation_Single_Tagged_VLAN_Mbps')
    elif B == 'Y':
        trafficname.append('Stream_Config_Creation_Dual_Tagged_VLAN_dot1ad_Mbps')
    elif B == 'P':
        trafficname.append('Stream_Config_Creation_Without_VLAN_Mbps')
    else:
        pass

    return trafficname

x = spirent_call('F','P')
print(x)
