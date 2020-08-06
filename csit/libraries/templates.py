#########################
##    NCS COMMANDS     ##
#########################

# NCS_int_template= when sub intf need to be configured
NCS_int_template = '''
interface {{ component.interface }}
 description {{ component.description }}
 mtu {{ component.mtu }}
 service-policy output {{ component.output_policy }} account user-defined {{ component.acc_value }}
 lldp
  receive disable
  transmit disable
  no shutdown
 !
 negotiation auto
 load-interval 30
 #loopback internal
!
'''
# loopback internal - only for testing. will be removed in actual test.

# NCS_main_int_template= when main intf need to be configured
NCS_main_int_template = '''
interface {{ component.interface }}
 description {{ component.description }}
 mtu {{ component.mtu }}
 lldp
  receive disable
  transmit disable
  no shutdown
 !
 negotiation auto
 load-interval 30
 #loopback internal
!
 l2transport
 service-policy output {{ component.output_policy }} account user-defined {{ component.acc_value }}
'''


Del_NCS_int_template = '''
no interface {{ component.interface }}
'''

# Sub-intf type = P/F/D/X/Y & below possible values should be defined in Variables.py for encapsulation
# encapsulation type P = default   X = dot1ad/dot1q <Vlan-id>   Y = dot1q/dot1ad <Vlan-Id> second dot1q <Vlan-Id>   D = dot1q/dot1ad <Vlan-Id> second dot1q <Vlan-Id>   F = dot1ad/dot1q <Vlan-Id>

NCS_sub_int_template = """
interface {{ component.sub_interface }} l2transport
 description {{ component.description }}
 {% if component.service_type == 'P' %}
 encapsulation default
 {% elif component.service_type == 'F' %}
 encapsulation {{ component.encapsulation1 }}
 {% elif component.service_type == 'X' %}
 encapsulation {{ component.encapsulation1 }} 
 rewrite ingress tag pop 1 symmetric 
 {% elif component.service_type == 'Y' %}
 encapsulation {{ component.encapsulation1 }} {{ component.encapsulation2 }}
 rewrite ingress tag pop 1 symmetric 
 {% elif component.service_type == 'D' %}
 encapsulation {{ component.encapsulation1 }} {{ component.encapsulation2 }}
 {% endif %}
 no shutdown
"""

# this template was created earlier. now using NCS_sub_int_template.
# will remove in future if everything works well.
NCS_sub_int_PFD_template = """
interface {{ component.sub_interface }} l2transport
 description {{ component.description }}
 encapsulation {{ component.encapsulation }}
 no shutdown
"""
# this template was created earlier. now using NCS_sub_int_template.
# will remove in future if everything works well.
NCS_sub_int_XY_template = """
interface {{ component.sub_interface }} l2transport
 description {{ component.description }}
 encapsulation {{ component.encapsulation }}
 rewrite ingress tag pop 1 symmetric 
 no shutdown
"""


Del_NCS_sub_int_template = """
no interface {{ component.sub_interface }}
"""



Pol_map_egr_template = """
policy-map {{ component.output_policy }}
 class class-default
  bandwidth percent 100 
 ! 
 end-policy-map
"""

Del_Pol_map_egr_template = """
no policy-map {{ component.output_policy }}
"""

Ser_Pol_map_template = """
policy-map {{ component.ser_policy_map }}
class class-default
police rate {{ component.police_rate }} burst {{ component.burst }}
set traffic-class {{ component.traffic_class }}
set qos-group {{ component.qos_group }}
end-policy-map

"""

Del_Ser_Pol_map_template = """
no policy-map {{ component.ser_policy_map }}
"""

Ser_Pol_map_intf_template = """
interface {{ component.policy_intf }} l2transport
no service-policy input
service-policy input {{ component.ser_policy_map }}
"""

Ser_Pol_map_main_intf_template = """
interface {{ component.policy_intf }}
 l2transport
 no service-policy input
 service-policy input {{ component.ser_policy_map }}
"""

EVPN_template = """
evpn
 evi {{ component.evpn_id }}
  bgp
   rd {{ component.rd }}
   route-target import {{ component.rt_import }}
   route-target export {{ component.rt_export }}
"""

Del_EVPN_template = """
no evpn evi {{ component.evpn_id }}
"""

L2VPN_template = """
l2vpn
 xconnect group {{ component.xc_group }}
  p2p {{ component.p2p_xc_name }}
   interface {{ component.attch_ckt_intf }}
   neighbor evpn evi {{ component.evpn_id }} target {{ component.rmte_attc_ckt_id }} source {{ component.src_attc_ckt_id }}
"""
#attach_ckt_intf can be main or sub-interface in robot frame work

Del_L2VPN_template = """
l2vpn 
no xconnect group {{ component.xc_group }}
"""

CFM_template = """
ethernet cfm
 domain {{ component.domain_name }} level {{ component.domain_level }} id null
  service {{ component.service_name }} xconnect group {{ component.xc_group }} p2p {{ component.p2p_xc_name }} id icc-based {{ component.ICC }} {{ component.UMC }}
   continuity-check interval 1s
   mep crosscheck
    mep-id {{ component.remote_mep_id }}
   !
   log continuity-check errors
   log crosscheck errors
   log continuity-check mep changes
"""

Del_CFM_template = """
ethernet cfm
 domain {{ component.domain_name }} level {{ component.domain_level }} id null
  no service {{ component.service_name }} xconnect group {{ component.xc_group }} p2p {{ component.p2p_xc_name }} id icc-based {{ component.ICC }} {{ component.UMC }}
"""

## SLM/DMM also configured with CFM when SLM = 'yes'
CFM_intf_template = """
interface {{ component.cfm_ckt_intf }}
 ethernet cfm
  mep domain {{ component.domain_name }} service {{ component.service_name }} mep-id {{ component.local_mep_id }}
   cos 2
   {% if component.SLM == 'yes' %}
   sla operation profile DMM2 target mep-id {{ component.remote_mep_id }}
   sla operation profile SLM2 target mep-id {{ component.remote_mep_id }}
   {% endif %}
"""


LLF_template = """
interface {{ component.llf_intf }}
l2transport
propagate remote-status
"""


L1_loopback_template = """
int {{ component.interface }}
{% if component.LoopbackType == 'internal'-%}
loopback internal
{% elif component.LoopbackType == 'line' -%}
loopback line
{% else -%}
loopback external
{% endif %}
"""

Del_L1_loopback_template = """
int {{ component.interface }}
{% if component.LoopbackType == 'internal'-%}
no loopback internal
{% elif component.LoopbackType == 'line' -%}
no loopback line
{% else -%}
no loopback external
{% endif %}
"""



L2_loopback_template ="""
int {{ component.sub_interface }} l2transport
{% if component.LoopbackType == 'internal'-%}
ethernet loopback permit internal
{% else -%}
ethernet loopback permit external
{% endif -%}
commit
exit
exit
{% if component.LoopbackType == 'internal'-%}
ethernet loopback start local interface {{ component.sub_interface }} internal destination mac-address 0010.9400.0113 timeout 1800
{% else -%}
ethernet loopback start local interface {{ component.sub_interface }} external destination mac-address 0010.9400.0113 timeout 1800
{% endif -%}
"""


Del_L2_loopback_template = """
exit
ethernet loopback stop local interface {{ component.sub_interface }} id 1
configure terminal
interface {{ component.sub_interface }} l2transport
no ethernet loopback

"""

show_interface_template = """show interface {{ component.interface }} brief"""
# intf_status = """up        up"""

show_L2VPN_template = """show l2vpn xconnect group {{ component.xc_group }}"""
# L2VPN_status = """UP        UP        UP"""

show_eth_cfm_template = """show ethernet cfm services domain {{ component.domain_name }} service {{ component.service_name }}"""
# local_mep_info = "Local MEPs: 1 total: all operational, no errors"
# peer_mep_info = "Peer MEPs: 1 total: all operational, no errors"

show_SLA_template = """show ethernet sla statistics interface {{ component.interface }}"""
# SLA_status =""" Lost: 0 (0.0%); Corrupt: 0 (0.0%);
#  Lost: 0 (0.0%); Corrupt: 0 (0.0%);
#  Lost: 0 (0.0%); Corrupt: 0 (0.0%);
#  Lost: 0 (0.0%); Corrupt: 0 (0.0%);
#  Lost: 0 (0.0%); Corrupt: 0 (0.0%);"""

show_pol_map_int = """show policy-map interface {{ component.interface }}"""

#########################
##  ACCEDIAN COMMANDS  ##
#########################

port_enable_template = """port edit {{ component.port_name }} alias {{ component.PortAliasName }} state enable auto-nego {{ component.autoNegValue }} speed {{ component.portSpeed }} mtu {{ component.mtuValue }} lldp-state disable"""

port_show_template = """port show status {{ component.port_name }}"""
# accedian_port_status = """Enabled        Up"""


bw_regulator_template = """
bandwidth-regulator add regulator {{ component.RegulatorName }} cir {{ component.CirValue }} cir-max {{ component.CirMax }} cbs {{ component.CbsValue }} eir {{ component.EirValue }} eir-max {{ component.EirMax }} ebs {{ component.EbsValue }} color-mode {{ component.ColorMode }} coupling-flag {{ component.CouplingFlag }}
"""
Del_bw_regulator_template = """
bandwidth-regulator delete regulator {{ component.RegulatorName }}
"""

bw_regulator_show_template = """bandwidth-regulator show regulator configuration {{ component.RegulatorName }}"""

filter_template ="""
filter add {{ component.FilterType }} {{ component.FilterName }} vlan1-ethertype {{component.vlan1EtherType}} vlan1-id {{component.vlan1Id}} enable
"""

Del_filter_template = """
filter delete l2 {{ component.FilterName }}
"""

filter_show_template = """filter show {{ component.FilterType }} {{ component.FilterName }}"""

vid_set_template ="""
vid-set add {{ component.PortVidSetName }} policy-list Traffic-{{ component.PortNumber }} vlan-type {{ component.vlanType }} vid-list {{ component.vidList }}
"""

Del_vid_set_template = """
vid-set delete {{ component.PortVidSetName }}
"""

vid_set_show_template ="""
vid-set show set name {{ component.PortVidSetName }}
"""

policy_template = """
{% set var = component.VlanAction  %}
{% if var == 'none' %}
policy edit Traffic-{{ component.PortNumber }} {{ component.PolicyId }} state enable action permit pre-marking {{ component.colour }} regulator enable {{ component.RegulatorName }} filter {{ component.filterType }} {{ component.VidSetOrFilterName }} evc-encapsulation none cos-mapping direct green-cfi 0 green-pcp {{ component.greenPcpValue }} yellow-cfi 0 yellow-pcp {{ component.yellowPcpValue }} out-port {{ component.uniPortName }}
{% elif var == 'push' %}
policy edit Traffic-{{ component.PortNumber }} {{ component.PolicyId }} state enable action permit pre-marking {{ component.colour }} regulator enable {{ component.RegulatorName }} filter {{ component.filterType }} {{ component.VidSetOrFilterName }} evc-encapsulation push evc-ethertype {{ component.firstVlanType }} evc-vlan-id {{ component.firstVlanId }} cos-mapping direct green-cfi 0 green-pcp {{ component.greenPcpValue }} yellow-cfi 0 yellow-pcp {{ component.yellowPcpValue }} out-port {{ component.outPortName }}
{% elif var == 'pop' %}
policy edit Traffic-{{ component.PortNumber }} {{ component.PolicyId }} state enable action permit pre-marking {{ component.colour }} regulator enable {{ component.RegulatorName }} filter {{ component.filterType }} {{ component.VidSetOrFilterName }} evc-encapsulation pop cos-mapping direct green-cfi 0 green-pcp {{ component.greenPcpValue }} yellow-cfi 0 yellow-pcp {{ component.yellowPcpValue }} out-port {{ component.outPortName }}
{% elif var == 'replace' %}
policy edit Traffic-{{ component.PortNumber }} {{ component.PolicyId }} state enable action permit pre-marking {{ component.colour }} regulator enable {{ component.RegulatorName }} filter {{ component.filterType }} {{ component.VidSetOrFilterName }} evc-encapsulation replace evc-ethertype {{ component.firstVlanType }}  evc-vlan-id {{ component.firstVlanId }} cos-mapping direct green-cfi 0 green-pcp {{ component.greenPcpValue }} yellow-cfi 0 yellow-pcp {{ component.yellowPcpValue }} out-port {{ component.outPortName }}
{% elif var == 'pop-replace' %}
policy edit Traffic-{{ component.PortNumber }} {{ component.PolicyId }} state enable action permit pre-marking {{ component.colour }} regulator enable {{ component.RegulatorName }} filter {{ component.filterType }} {{ component.VidSetOrFilterName }} evc-encapsulation pop-replace evc-ethertype {{ component.firstVlanType }}  evc-vlan-id {{ component.firstVlanId }} cos-mapping direct green-cfi 0 green-pcp {{ component.greenPcpValue }} yellow-cfi 0 yellow-pcp {{ component.yellowPcpValue }} out-port {{ component.outPortName }}
{% elif var == 'push-replace' %}
policy edit Traffic-{{ component.PortNumber}} {{ component.PolicyId}} state enable action permit pre-marking {{ component.colour}} regulator enable {{ component.RegulatorName}} filter {{ component.filterType }} {{ component.VidSetOrFilterName }} evc-encapsulation push-replace evc-ethertype {{ component.firstVlanType}}  evc-vlan-id {{ component.firstVlanId }} evc-ethertype2 {{ component.secondVlanType }} evc-vlan-id2 {{ component.secondVlanId }} cos-mapping direct green-cfi 0 green-pcp {{ component.greenPcpValue }} yellow-cfi 0 yellow-pcp {{ component.yellowPcpValue }} out-port {{ component.outPortName }}
{% elif var == 'pop-pop' %}
policy edit Traffic-{{ component.PortNumber }} {{ component.PolicyId }} state enable action permit pre-marking {{ component.colour }} regulator enable {{ component.RegulatorName }} filter {{ component.filterType }} {{ component.VidSetOrFilterName }} evc-encapsulation pop-pop cos-mapping direct green-cfi 0 green-pcp {{ component.greenPcpValue }} yellow-cfi 0 yellow-pcp {{ component.yellowPcpValue }} out-port {{ component.outPortName }}
{% endif %}
"""

Del_policy_template ="""
policy edit Traffic-{{ component.PortNumber }} {{ component.PolicyId }} state disable action permit pre-marking green regulator disable monitor disable map1-state disable map2-state disable evc-encapsulation none evc-ethertype c-vlan evc-vlan-id 0 evc-ethertype2 c-vlan evc-vlan-id2 0 cos-mapping preserve map1-type pcp-vlan map2-type pcp-vlan map1-regulator-set disable green-cfi 0 green-pcp 0 yellow-cfi 0 yellow-pcp 0  
"""

CFM_MEG_accedian_template ="""
cfm add meg name {{ component.megName }} name-format icc-based ccm-interval {{ component.ccmInterval }} index {{ component.megIndex }} mhf-creation none sndr-id-perm none  level {{ component.megLevel }} rmep-auto-discovery {{ component.rmepAutoDiscoveryOption }} mepid-list {{ component.MepIdList }} vid-list {{ component.VidList }} vlan-type {{ component.VlanType }}
"""

Del_CFM_MEG_accedian_template = """
cfm delete meg {{ component.megIndex }}
"""

CFM_MEP_accedian_template ="""
cfm add mep name {{ component.mepName }} active {{ component.active }} index {{ component.mepIndex }} direction {{ component.direction }} cci-enable {{ component.cciEnable }} ccm-seq-number {{ component.ccmSeqNumber }} meg-idx {{ component.megIndex }} lowest-alarm-pri {{ component.LowestAlarmPri }} mep-id {{ component.mepId }} port {{ component.PortName }} priority {{ component.mepPriority }} pvid {{ component.pvid }}
"""

Del_CFM_MEP_accedian_template ="""
cfm delete mep {{ component.mepName }}
"""

cfm_show_mep_database_template ="""
cfm show mep database {{ component.mepName }}
"""
