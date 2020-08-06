*** Settings ***
Documentation     Resource file containing all the PYTHON API implementations.
Library           String
Library           Collections
Library           ${CURDIR}//Connect_devices.py
Library           ${CURDIR}//Commands.py
Resource          ${CURDIR}//Resource.robot    #Resource    Resource.robot

*** Variables ***

*** Keywords ***
#Setup Actions
    # Log To Console    Setup Actions done here
    # #    log to console    ${CURDIR}
    # ${Topo_data}    Get Data
    # #log to console    ${Topo_data}
    # ${DEV_DICT}    get from dictionary    ${Topo_data}    Device_Details    #get all device details
    # ${PORT_DICT}    get from dictionary    ${Topo_data}    Port_Details     #get all port details

    # ## Details for NCS devices ##

    # ## NCS_R1 ##
    # ${NCS_R1_DICT}    get from dictionary    ${DEV_DICT}    NCS_R1    #NCS_R1 dictionary
    # ${NCS_R1_net_connect}    Make Connection    ${NCS_R1_DICT}    #ssh to NCS_R1
    # Builtin.Set_Suite_Variable    ${NCS_R1_net_connect}
    # Log To Console    Connection Establihed to NCS_R1
    # # Port Details
    # ${PORT_NCS_R1}    get from dictionary    ${PORT_DICT}    NCS_R1    #get NCS_R1 link dictionary
    # ${NCS_R1_P1}    get from dictionary    ${PORT_NCS_R1}    P1    #get NCS_R1_P1 link
    # ${NCS_R1_P2}    get from dictionary    ${PORT_NCS_R1}    P2    #get NCS_R1_P2 link
    # Builtin.Set_Suite_Variable    ${NCS_R1_P1}    #global variable
    # Builtin.Set_Suite_Variable    ${NCS_R1_P2}    #global variable

    # ## NCS_R2 ##
    # ${NCS_R2_DICT}    get from dictionary    ${DEV_DICT}    NCS_R2    #NCS_R2 dictionary
    # ${NCS_R2_net_connect}    Make Connection    ${NCS_R2_DICT}    #ssh to NCS_R2
    # Builtin.Set_Suite_Variable    ${NCS_R2_net_connect}
    # Log To Console    Connection Establihed to NCS_R2
    # # Port Details
    # ${PORT_NCS_R2}    get from dictionary    ${PORT_DICT}    NCS_R2    #get NCS_R2 link dictionary
    # ${NCS_R2_P1}    get from dictionary    ${PORT_NCS_R2}    P1    #get NCS_R2_P1 link
    # ${NCS_R2_P2}    get from dictionary    ${PORT_NCS_R2}    P2    #get NCS_R2_P2 link
    # Builtin.Set_Suite_Variable    ${NCS_R2_P1}    #global variable
    # Builtin.Set_Suite_Variable    ${NCS_R2_P2}    #global variable


#    ## Details for Accedian devices ##
#
#    ## ACC_R1 ##
#    ${ACC_R1_DICT}    get from dictionary    ${DEV_DICT}    ACC_R1    #ACC_R1 dictionary
#    ${ACC_R1_net_connect}    Make Connection Accedian    ${ACC_R1_DICT}    #ssh to ACC_R1
#    Builtin.Set_Suite_Variable    ${ACC_R1_net_connect}
#    Log To Console    Connection Establihed to ACC_R1
#    # Port Details
#    ${PORT_ACC_R1}    get from dictionary    ${PORT_DICT}    ACC_R1    #get NCS_R4 link dictionary
#    ${ACC_R1_P1}    get from dictionary    ${PORT_ACC_R1}    P1    #get ACC_R1_P1 link
#    ${ACC_R1_P2}    get from dictionary    ${PORT_ACC_R1}    P2    #get ACC_R1_P2 link
#    Builtin.Set_Suite_Variable    ${ACC_R1_P1}    #global variable
#    Builtin.Set_Suite_Variable    ${ACC_R1_P2}    #global variable

Teardown Actions
    Log To Console    Teardown Actions done here

    Close Connection    ${NCS_R1_net_connect}
	Close Connection    ${NCS_R2_net_connect}

#    Close Connection    ${ACC_R1_net_connect}


CONFIGURE POLICY-MAP-EGR
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}   template_data=${template_data}
    should not contain    ${commit_result}    fail

## NCS config ##
CONFIGURE SERVICE-POLICY-MAP
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

CONFIGURE SERVICE-POLICY-MAP-INTF
    [Arguments]    ${connect_id}    ${intf_name}    ${template_name}    ${template_data}
    set to dictionary    ${template_data}    policy_intf=${intf_name}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

CONFIGURE INTERFACE
    [Arguments]    ${connect_id}    ${intf_name}    ${template_name}    ${template_data}
    set to dictionary    ${template_data}    interface=${intf_name}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

CONFIGURE SUB-INTERFACE
    [Arguments]    ${connect_id}    ${sub_intf_name}    ${template_name}    ${template_data}
    set to dictionary    ${template_data}    sub_interface=${sub_intf_name}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

CONFIGURE L2VPN
    [Arguments]    ${connect_id}    ${sub_intf_name}    ${template_name}    ${template_data}
    set to dictionary    ${template_data}    attch_ckt_intf=${sub_intf_name}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

CONFIGURE EVPN
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

CONFIGURE CFM
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

CONFIGURE CFM-INTF
    [Arguments]    ${connect_id}    ${intf_name}    ${template_name}    ${template_data}
    set to dictionary    ${template_data}    cfm_ckt_intf=${intf_name}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

CONFIGURE LLF
    [Arguments]    ${connect_id}    ${intf_name}    ${template_name}    ${template_data}
    set to dictionary    ${template_data}    llf_intf=${intf_name}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

CONFIGURE L1-LOOPBACK
    [Arguments]    ${connect_id}    ${intf_name}    ${template_name}    ${template_data}
    set to dictionary    ${template_data}    interface=${intf_name}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

CONFIGURE L2-LOOPBACK
    [Arguments]    ${connect_id}    ${sub_intf_name}    ${template_name}    ${template_data}
    set to dictionary    ${template_data}    sub_interface=${sub_intf_name}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail


SHOW COMMAND
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${show_cmd_result}    Show Commands    ${connect_id}    template_name=${${template_name}}    template_data=${template_data}    textfsm_template=${template_name}
    [Return]    ${show_cmd_result}


UNCONFIGURE CFM
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

UNCONFIGURE EVPN
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

UNCONFIGURE L2VPN
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

UNCONFIGURE SUB-INTF
    [Arguments]    ${connect_id}    ${sub_intf_name}    ${template_name}    ${template_data}
    set to dictionary    ${template_data}    sub_interface=${sub_intf_name}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

UNCONFIGURE INTF
    [Arguments]    ${connect_id}    ${intf_name}    ${template_name}    ${template_data}
    set to dictionary    ${template_data}    interface=${intf_name}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

UNCONFIGURE SERVICE-POLICY-MAP
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

UNCONFIGURE L1-LOOPBACK
    [Arguments]    ${connect_id}    ${intf_name}    ${template_name}    ${template_data}
    set to dictionary    ${template_data}    interface=${intf_name}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

UNCONFIGURE L2-LOOPBACK
    [Arguments]    ${connect_id}    ${sub_intf_name}    ${template_name}    ${template_data}
    set to dictionary    ${template_data}    sub_interface=${sub_intf_name}
    ${commit_result}    Configure Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
    should not contain    ${commit_result}    fail

## Accedian Config ## LTS ##

ENABLE ACCEDIAN-PORT
    [Arguments]    ${connect_id}    ${port_name}    ${template_name}    ${template_data}
    set to dictionary    ${template_data}    port_name=${port_name}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error

CONFIGURE ACCEDAIN-REGULATOR
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error

UNCONFIGURE ACCEDAIN-REGULATOR
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error

CONFIGURE ACCEDAIN-FILTER
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error

UNCONFIGURE ACCEDAIN-FILTER
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error

CONFIGURE VID-SET
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error

UNCONFIGURE VID-SET
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error

CONFIGURE TRAFFIC-POLICY
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error

UNCONFIGURE TRAFFIC-POLICY
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error

CONFIGURE CFM-MEG-ACCEDIAN
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error

UNCONFIGURE CFM-MEG-ACCEDIAN
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error

CONFIGURE CFM-MEP-ACCEDIAN
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error

UNCONFIGURE CFM-MEP-ACCEDIAN
    [Arguments]    ${connect_id}    ${template_name}    ${template_data}
    ${result}    Configure Accedian Commands    ${connect_id}    template_name=${template_name}    template_data=${template_data}
#    should not contain    ${result}    Error
