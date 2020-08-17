    streamblock_ret1 = sth.traffic_config(
        mode='create',
        port_handle=self.port_handle[src_port_handle_index],
        l2_encap='ethernet_ii',
        mac_src='00:10:94:00:00:02',
        mac_dst='01:80:C2:00:00:02',
        enable_control_plane='0',
        l3_length='537',
        name='LACP_Stream_/Slow_Protocol',
        fill_type='prbs',
        fcs_error='0',
        fill_value='0',
        frame_size='555',
        traffic_state='1',
        high_speed_result_analysis='1',
        length_mode='fixed',
        tx_port_sending_traffic_to_self_en='false',
        disable_signature='0',
        enable_stream_only_gen='1',
        pkts_per_burst='1',
        inter_stream_gap_unit='bytes',
        burst_loop_count='30',
        transmit_mode='continuous',
        inter_stream_gap='12',
        rate_pps='9275');

    status = streamblock_ret1['status']
    if (status == '0'):
        print("run sth.traffic_config failed")
        print(streamblock_ret1)
    else:
        print("***** run sth.traffic_config successfully")

    streamblock_ret2 = sth.traffic_config(
        mode='create',
        port_handle=self.port_handle[src_port_handle_index],
        l2_encap='ethernet_ii',
        mac_src='00:10:94:00:00:02',
        ether_type='888E',
        mac_dst='01:80:C2:00:00:03',
        enable_control_plane='0',
        l3_length='537',
        name='Port_Authentication',
        fill_type='constant',
        fcs_error='0',
        fill_value='0',
        frame_size='555',
        traffic_state='1',
        high_speed_result_analysis='1',
        length_mode='fixed',
        tx_port_sending_traffic_to_self_en='false',
        disable_signature='0',
        enable_stream_only_gen='1',
        pkts_per_burst='1',
        inter_stream_gap_unit='bytes',
        burst_loop_count='30',
        transmit_mode='continuous',
        inter_stream_gap='12',
        rate_pps='9164');

    status = streamblock_ret2['status']
    if (status == '0'):
        print("run sth.traffic_config failed")
        print(streamblock_ret2)
    else:
        print("***** run sth.traffic_config successfully")

    streamblock_ret3 = sth.traffic_config(
        mode='create',
        port_handle=self.port_handle[src_port_handle_index],
        l2_encap='ethernet_ii',
        mac_src='00:10:94:00:00:02',
        ether_type='88EE',
        mac_dst='01:80:C2:00:00:07',
        enable_control_plane='0',
        l3_length='537',
        name='E-LMI',
        fill_type='constant',
        fcs_error='0',
        fill_value='0',
        frame_size='555',
        traffic_state='1',
        high_speed_result_analysis='1',
        length_mode='fixed',
        tx_port_sending_traffic_to_self_en='false',
        disable_signature='0',
        enable_stream_only_gen='1',
        pkts_per_burst='1',
        inter_stream_gap_unit='bytes',
        burst_loop_count='30',
        transmit_mode='continuous',
        inter_stream_gap='12',
        rate_pps='9148');

    status = streamblock_ret3['status']
    if (status == '0'):
        print("run sth.traffic_config failed")
        print(streamblock_ret3)
    else:
        print("***** run sth.traffic_config successfully")

    streamblock_ret4 = sth.traffic_config(
        mode='create',
        port_handle=self.port_handle[src_port_handle_index],
        l2_encap='ethernet_ii',
        mac_src='00:10:94:00:00:02',
        mac_dst='01:80:C2:00:00:0E',
        enable_control_plane='0',
        l3_length='982',
        name='LLDP',
        fill_type='constant',
        fcs_error='0',
        fill_value='0',
        frame_size='1000',
        traffic_state='1',
        high_speed_result_analysis='1',
        length_mode='fixed',
        tx_port_sending_traffic_to_self_en='false',
        disable_signature='0',
        enable_stream_only_gen='1',
        pkts_per_burst='1',
        inter_stream_gap_unit='bytes',
        burst_loop_count='30',
        transmit_mode='continuous',
        inter_stream_gap='12',
        rate_pps='9199');

    status = streamblock_ret4['status']
    if (status == '0'):
        print("run sth.traffic_config failed")
        print(streamblock_ret4)
    else:
        print("***** run sth.traffic_config successfully")

    streamblock_ret5 = sth.traffic_config(
        mode='create',
        port_handle=self.port_handle[src_port_handle_index],
        l2_encap='ethernet_ii',
        mac_dst_mode='increment',
        mac_dst_repeat_count='0',
        mac_dst_count='16',
        mac_src='00:10:94:00:00:02',
        mac_dst='01:80:C2:00:00:20',
        enable_control_plane='0',
        l3_length='537',
        name='GARP/GMRP_StreamBlock',
        fill_type='constant',
        fcs_error='0',
        fill_value='0',
        frame_size='555',
        traffic_state='1',
        high_speed_result_analysis='1',
        length_mode='fixed',
        tx_port_sending_traffic_to_self_en='false',
        disable_signature='0',
        enable_stream_only_gen='1',
        pkts_per_burst='1',
        inter_stream_gap_unit='bytes',
        burst_loop_count='30',
        transmit_mode='continuous',
        inter_stream_gap='12',
        rate_pps='9147',
        enable_stream='false');

    status = streamblock_ret5['status']
    if (status == '0'):
        print("run sth.traffic_config failed")
        print(streamblock_ret5)
    else:
        print("***** run sth.traffic_config successfully")

    streamblock_ret6 = sth.traffic_config(
        mode='create',
        port_handle=self.port_handle[src_port_handle_index],
        l2_encap='ethernet_ii',
        mac_src='00:10:94:00:00:02',
        mac_dst='01:80:C2:00:00:02',
        enable_control_plane='0',
        l3_length='138',
        name='LACP_MARKER',
        fill_type='constant',
        fcs_error='0',
        fill_value='0',
        frame_size='156',
        traffic_state='1',
        high_speed_result_analysis='1',
        length_mode='fixed',
        tx_port_sending_traffic_to_self_en='false',
        disable_signature='0',
        enable_stream_only_gen='1',
        pkts_per_burst='1',
        inter_stream_gap_unit='bytes',
        burst_loop_count='30',
        transmit_mode='continuous',
        inter_stream_gap='12',
        rate_pps='9203');

    status = streamblock_ret6['status']
    if (status == '0'):
        print("run sth.traffic_config failed")
        print(streamblock_ret6)
    else:
        print("***** run sth.traffic_config successfully")

    streamblock_ret7 = sth.traffic_config(
        mode='create',
        port_handle=self.port_handle[src_port_handle_index],
        enable_control_plane='0',
        l3_length='128',
        name='Link_OAM',
        fill_type='constant',
        fcs_error='0',
        fill_value='0',
        frame_size='128',
        traffic_state='1',
        high_speed_result_analysis='1',
        length_mode='fixed',
        tx_port_sending_traffic_to_self_en='false',
        disable_signature='0',
        enable_stream_only_gen='1',
        pkts_per_burst='1',
        inter_stream_gap_unit='bytes',
        burst_loop_count='30',
        transmit_mode='continuous',
        inter_stream_gap='12',
        rate_pps='9100');

    status = streamblock_ret7['status']
    if (status == '0'):
        print("run sth.traffic_config failed")
        print(streamblock_ret7)
    else:
        print("***** run sth.traffic_config successfully")

    streamblock_ret8 = sth.traffic_config(
        mode='create',
        port_handle=self.port_handle[src_port_handle_index],
        l2_encap='ethernet_8023_snap',
        custom_pattern='ABCDEFABCDEF',
        mac_src='00:10:94:00:00:02',
        mac_dst='01:00:0C:CC:CC:CC',
        llc_control='03',
        llc_ssap='AA',
        llc_dsap='AA',
        snap_oui_id='00000C',
        snap_ether_type='2000',
        enable_control_plane='0',
        l3_length='555',
        name='Cisco_CDP_VTP',
        fill_type='constant',
        fcs_error='0',
        fill_value='0',
        frame_size='555',
        traffic_state='1',
        high_speed_result_analysis='1',
        length_mode='fixed',
        tx_port_sending_traffic_to_self_en='false',
        disable_signature='0',
        enable_stream_only_gen='1',
        pkts_per_burst='1',
        inter_stream_gap_unit='bytes',
        burst_loop_count='30',
        transmit_mode='continuous',
        inter_stream_gap='12',
        rate_pps='9116');

    status = streamblock_ret8['status']
    if (status == '0'):
        print("run sth.traffic_config failed")
        print(streamblock_ret8)
    else:
        print("***** run sth.traffic_config successfully")

    streamblock_ret9 = sth.traffic_config(
        mode='create',
        port_handle=self.port_handle[src_port_handle_index],
        l2_encap='ethernet_ii',
        mac_src='00:10:94:00:00:02',
        ether_type='0802',
        mac_dst='01:00:0C:CC:CC:CC',
        enable_control_plane='0',
        l3_length='110',
        name='Cicso_Shared_STP_',
        fill_type='constant',
        fcs_error='0',
        fill_value='0',
        frame_size='128',
        traffic_state='1',
        high_speed_result_analysis='1',
        length_mode='fixed',
        tx_port_sending_traffic_to_self_en='false',
        disable_signature='0',
        enable_stream_only_gen='1',
        pkts_per_burst='1',
        inter_stream_gap_unit='bytes',
        burst_loop_count='30',
        transmit_mode='continuous',
        inter_stream_gap='12',
        rate_pps='9223');

    status = streamblock_ret9['status']
    if (status == '0'):
        print("run sth.traffic_config failed")
        print(streamblock_ret9)
    else:
        print("***** run sth.traffic_config successfully")

    streamblock_ret10 = sth.traffic_config(
        mode='create',
        port_handle=self.port_handle[src_port_handle_index],
        l2_encap='ethernet_ii',
        l3_protocol='ipv4',
        l4_protocol='igmp',
        igmp_max_response_time='0',
        igmp_version='2',
        igmp_type='16',
        igmp_msg_type='report',
        igmp_group_addr='225.0.0.1',
        ip_id='0',
        ip_src_addr='192.85.1.2',
        ip_dst_addr='224.0.0.1',
        ip_ttl='255',
        ip_hdr_length='5',
        ip_protocol='2',
        ip_fragment_offset='0',
        ip_mbz='0',
        ip_precedence='0',
        ip_tos_field='0',
        mac_src='00:10:94:00:00:02',
        ether_type='0800',
        mac_dst='01:00:5E:00:00:01',
        enable_control_plane='0',
        l3_length='110',
        name='IPV4_IGMP_multicast',
        fill_type='constant',
        fcs_error='0',
        fill_value='0',
        frame_size='128',
        traffic_state='1',
        high_speed_result_analysis='1',
        length_mode='fixed',
        tx_port_sending_traffic_to_self_en='false',
        disable_signature='0',
        enable_stream_only_gen='1',
        pkts_per_burst='1',
        inter_stream_gap_unit='bytes',
        burst_loop_count='30',
        transmit_mode='continuous',
        inter_stream_gap='12',
        rate_pps='9100',
        mac_discovery_gw='192.85.1.1');

    status = streamblock_ret10['status']
    if (status == '0'):
        print("run sth.traffic_config failed")
        print(streamblock_ret10)
    else:
        print("***** run sth.traffic_config successfully")
    streamblock_ret11 = sth.traffic_config(
        mode='create',
        port_handle=self.port_handle[src_port_handle_index],
        l2_encap='ethernet_ii',
        custom_pattern='ABCDEFABCDEF',
        mac_src='00:10:94:00:00:02',
        ether_type='0000',
        mac_dst='01:00:0C:00:00:01',
        enable_control_plane='0',
        l3_length='110',
        name='Cisco_Inter_Switch_Protocol_(ISL)',
        fill_type='constant',
        fcs_error='0',
        fill_value='0',
        frame_size='128',
        traffic_state='1',
        high_speed_result_analysis='1',
        length_mode='fixed',
        tx_port_sending_traffic_to_self_en='false',
        disable_signature='0',
        enable_stream_only_gen='1',
        pkts_per_burst='1',
        inter_stream_gap_unit='bytes',
        burst_loop_count='30',
        transmit_mode='continuous',
        inter_stream_gap='12',
        rate_pps='9100');

    status = streamblock_ret11['status']
    if (status == '0'):
        print("run sth.traffic_config failed")
        print(streamblock_ret11)
    else:
        print("***** run sth.traffic_config successfully")

    streamblock_ret12 = sth.traffic_config(
        mode='create',
        port_handle=self.port_handle[src_port_handle_index],
        l2_encap='ethernet_ii',
        mac_src='00:10:94:00:00:02',
        ether_type='8902',
        mac_dst='01:80:C2:00:00:35',
        enable_control_plane='0',
        l3_length='537',
        name='SOAM_CCM_Level_5',
        fill_type='constant',
        fcs_error='0',
        fill_value='0',
        frame_size='555',
        traffic_state='1',
        high_speed_result_analysis='1',
        length_mode='fixed',
        tx_port_sending_traffic_to_self_en='false',
        disable_signature='0',
        enable_stream_only_gen='1',
        pkts_per_burst='1',
        inter_stream_gap_unit='bytes',
        burst_loop_count='30',
        transmit_mode='continuous',
        inter_stream_gap='12',
        rate_pps='9116');

    status = streamblock_ret12['status']
    if (status == '0'):
        print("run sth.traffic_config failed")
        print(streamblock_ret12)
    else:
        print("***** run sth.traffic_config successfully")

    streamblock_ret13 = sth.traffic_config(
        mode='create',
        port_handle=self.port_handle[src_port_handle_index],
        l2_encap='ethernet_ii',
        mac_src='00:10:94:00:00:02',
        mac_dst='01:80:C2:00:00:0E',
        enable_control_plane='0',
        l3_length='110',
        name='PTP_Delay_Request',
        fill_type='constant',
        fcs_error='0',
        fill_value='0',
        frame_size='128',
        traffic_state='1',
        high_speed_result_analysis='1',
        length_mode='fixed',
        tx_port_sending_traffic_to_self_en='false',
        disable_signature='0',
        enable_stream_only_gen='1',
        pkts_per_burst='1',
        inter_stream_gap_unit='bytes',
        burst_loop_count='30',
        transmit_mode='continuous',
        inter_stream_gap='12',
        rate_pps='9100');

    status = streamblock_ret13['status']
    if (status == '0'):
        print("run sth.traffic_config failed")
        print(streamblock_ret13)
    else:
        print("***** run sth.traffic_config successfully")

    streamblock_ret14 = sth.traffic_config(
        mode='create',
        port_handle=self.port_handle[src_port_handle_index],
        l2_encap='ethernet_ii',
        mac_dst_mode='increment',
        mac_dst_repeat_count='0',
        mac_dst_count='16',
        mac_src='00:10:94:00:00:02',
        mac_dst='01:80:C2:00:00:00',
        enable_control_plane='0',
        l3_length='110',
        name='L2CP_MAC_Frame',
        fill_type='constant',
        fcs_error='0',
        fill_value='0',
        frame_size='128',
        traffic_state='1',
        high_speed_result_analysis='1',
        length_mode='fixed',
        tx_port_sending_traffic_to_self_en='false',
        disable_signature='0',
        enable_stream_only_gen='1',
        pkts_per_burst='1',
        inter_stream_gap_unit='bytes',
        burst_loop_count='30',
        transmit_mode='continuous',
        inter_stream_gap='12',
        rate_pps='9100',
        enable_stream='false');

    status = streamblock_ret14['status']
    if (status == '0'):
        print("run sth.traffic_config failed")
        print(streamblock_ret14)
    else:
        print("***** run sth.traffic_config successfully")

    streamblock_ret15 = sth.traffic_config(
        mode='create',
        port_handle=self.port_handle[src_port_handle_index],
        l2_encap='ethernet_ii',
        mac_src='00:10:94:00:00:02',
        mac_dst='01:80:C2:00:00:DD',
        enable_control_plane='0',
        l3_length='110',
        name='Provider_Bridge_MVRP_Address',
        fill_type='constant',
        fcs_error='0',
        fill_value='0',
        frame_size='128',
        traffic_state='1',
        high_speed_result_analysis='1',
        length_mode='fixed',
        tx_port_sending_traffic_to_self_en='false',
        disable_signature='0',
        enable_stream_only_gen='1',
        pkts_per_burst='1',
        inter_stream_gap_unit='bytes',
        burst_loop_count='30',
        transmit_mode='continuous',
        inter_stream_gap='12',
        rate_pps='9100');

    status = streamblock_ret15['status']
    if (status == '0'):
        print("run sth.traffic_config failed")
        print(streamblock_ret15)
    else:
        print("***** run sth.traffic_config successfully")