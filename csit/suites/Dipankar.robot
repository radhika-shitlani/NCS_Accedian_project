*** Settings ***
Documentation     A test suite with tests for P2P conenctivity between Cisco-Cisco-Accedian
...               Topology:-
...               Cisco-Cisco_accedian
...
#Suite Setup       Setup Actions
#Suite Teardown    Teardown Actions
Metadata          Version    1.0\nMore Info For more information about Robot Framework see http://robotframework.org\nAuthor Sathishkumar murugesan\nDate 12 Dec 2017\nExecuted At HOST\nTest Framework Robot Framework Python
Variables         ${CURDIR}/../Variables/P2P/Variables.py
Variables         ${CURDIR}/../libraries/templates.py
Library           Collections
Library           String
Library           OperatingSystem
Library           ${CURDIR}/../libraries/CCA.py
Resource          ../libraries/Resource.robot
Resource          ../libraries/Resource.robot

*** Test Cases ***

onnet_CCA
    ${test_result}    onnet_CCA    P    P
    log to console    ${test_result}
    run keyword and continue on failure    dictionary should not contain value    ${test_result['ccm_status']}    fail
    #run keyword and continue on failure    dictionary should not contain value    ${test_result['Loop_test']}    fail
    #run keyword and continue on failure    dictionary should not contain value    ${test_result['PP']['Spirent_MT_traffic']}    fail
    #run keyword and continue on failure    dictionary should not contain value    ${test_result['PP']['Spirent_VT_traffic']}    fail
    #run keyword and continue on failure    dictionary should not contain value    ${test_result}    fail



*** Keywords ***
