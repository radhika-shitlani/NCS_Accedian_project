#!/bin/sh
echo "
************
set env variables
***********
"
export STC_TCL=/opt/ActiveTcl-8.5/bin/tclsh
export STC_INSTALL_DIR=/opt/Spirent_TestCenter_4.70/Spirent_TestCenter_Application_Linux/
export TCLLIBPATH="/opt/Spirent_TestCenter_4.70/Spirent_TestCenter_Application_Linux /opt/ActiveTcl-8.5/lib/SpirentHltApi"
export PYTHONPATH=/opt/ActiveTcl-8.5/lib/SpirentHltApi/hltapiForPython
