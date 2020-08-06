from __future__ import print_function

import socket

import subprocess

import re

import sys

import os

import select

import platform



TRUE = 1

FALSE = 0

tclserversocket=''

socket_buffer = 1024

pythonver=0

log_dir=""
logname=""

GRetDict = {}

#################STC Native APIs implementation################
class StcPython(object):

    def apply(self):
        return _private_invoke('stc::apply')

    def config(self, _object, **kwargs):
        argList=''
        cmd="stc::config "+_object
        svec = []
        StcPython._packKeyVal(svec, kwargs)
        for svec_ele in svec:
            if svec_ele == "":
                svec_ele='""'
            elif svec_ele.find(" ") != -1:
                svec_ele='"'+svec_ele+'"'
            argList=argList+" "+svec_ele
        cmd=cmd+' '+argList
        return _private_invoke(cmd)

    def connect(self, *hosts):
        cmd=''
        svec = StcPython._unpackArgs(*hosts)
        for svec_ele in svec:
            cmd=cmd+' '+svec_ele
        return _private_invoke("stc::connect"+cmd)

    def create(self, _type, **kwargs):
        argList=''
        cmd="stc::create "+_type
        svec = []
        if _type != 'project':
            svec.append('-under')
            svec.append(kwargs.pop('under'))
        StcPython._packKeyVal(svec, kwargs)
        for svec_ele in svec:
            argList=argList+" "+svec_ele
        cmd=cmd+' '+argList
        return _private_invoke(cmd)

    def delete(self, handle):
        return _private_invoke("stc::delete"+' '+handle)

    def disconnect(self, *hosts):
        cmd=''
        svec = StcPython._unpackArgs(*hosts)
        for svec_ele in svec:
            cmd=cmd+' '+svec_ele
        return _private_invoke("stc::disconnect"+cmd)

    def get(self, handle, *args):
        svec = StcPython._unpackArgs(*args)
        svecDashes = ""
        for svec_ele in svec:
            svecDashes=svecDashes+" -"+svec_ele
        ret=_private_invoke("set ret [stc::get"+' '+handle+svecDashes+"]")
        if len(ret.split(' '))==1:
            return ret
        ret=_private_invoke("array set varArray $ret")
        varKeys=_private_invoke("set keys [array names varArray]")
        tempDic={}
        for items in varKeys.split(' '):
            tempDic[items]=_private_invoke("set values $varArray("+items+")")
            newItem=items.replace('-','',1)
            tempDic[newItem] = tempDic.pop(items)
        return tempDic

    def perform(self, _cmd, **kwargs):
        argList=''
        cmd="stc::perform "+_cmd
        svec = []
        StcPython._packKeyVal(svec, kwargs)
        for svec_ele in svec:
            argList=argList+" "+svec_ele
        cmd=cmd+' '+argList
        ret=_private_invoke("set ret ["+cmd+"]")
        if len(ret.split(' '))==1:
            return ret
        ret=_private_invoke("array set varArray $ret")
        varKeys=_private_invoke("set keys [array names varArray]")
        tempDic={}
        for items in varKeys.split(' '):
            tempDic[items]=_private_invoke("set values $varArray("+items+")")
            newItem=items.replace('-','',1)
            tempDic[newItem] = tempDic.pop(items)
        return tempDic

    def release(self, *csps):
        cmd=''
        svec = StcPython._unpackArgs(*csps)
        for svec_ele in svec:
            cmd=cmd+' '+svec_ele
        return _private_invoke("stc::release"+' '+cmd);

    def reserve(self, *csps):
        cmd=''
        svec = StcPython._unpackArgs(*csps)
        for svec_ele in svec:
            cmd=cmd+' '+svec_ele
        return _private_invoke("stc::reserve"+' '+cmd);

    def sleep(self, seconds):
        import time
        time.sleep(seconds)

    def subscribe(self, **kwargs):
        argList=''
        svec = []
        StcPython._packKeyVal(svec, kwargs)
        for svec_ele in svec:
            argList=argList+" "+svec_ele
        return _private_invoke("stc::subscribe "+argList)

    def unsubscribe(self, rdsHandle):
        return _private_invoke("stc::unsubscribe "+rdsHandle)

    def waitUntilComplete(self, **kwargs):
        argList=''
        svec = []
        if 'timeout' in kwargs:
            argList = '-timeout'+' '+str(kwargs['timeout'])
        return _private_invoke("stc::waitUntilComplete "+argList)

    def log(self, level, msg):
        return _private_invoke("stc::log "+level+' '+msg)


    def help(self, topic=''):
        if topic == '' or topic.find(' ') != -1:
            return 'Usage: \n' + \
                    '  stc.help(\'commands\')\n' + \
                    '  stc.help(<handle>)\n' + \
                    '  stc.help(<className>)\n' + \
                    '  stc.help(<subClassName>)'

        if topic == 'commands':
            allCommands = []
            for commandHelp in StcIntPythonHelp.HELP_INFO.values():
                allCommands.append(commandHelp['desc'])
            allCommands.sort()
            return '\n'.join(allCommands)

        info = StcIntPythonHelp.HELP_INFO.get(topic)
        if info != None:
            return 'Desc: ' + info['desc'] + '\n' + \
                   'Usage: ' + info['usage'] + '\n' + \
                   'Example: ' + info['example'] + '\n'

        return _private_invoke("stc::help "+topic)

    @staticmethod
    def _unpackArgs(*args):
         svec = []
         for arg in args:
            if type(arg) is list:
                svec.extend(arg)
            else:
                svec.append(arg)
         return svec

    @staticmethod
    def _packKeyVal(svec, hash):
        for key, val in hash.items():
            svec.append('-' + str(key))
            if type(val) is list:
                svec.append(' '.join(map(str, val)))
            else:
                svec.append(str(val));

# internal help info
class StcIntPythonHelp(object):

    def __init__(self):
        pass

    HELP_INFO = dict(    create =            dict(desc    = "create: -Creates an object in a test hierarchy",
                                                  usage   = "stc.create( className, under = parentObjectHandle, propertyName1 = propertyValue1, ... )",
                                                  example = 'stc.create( \'port\', under=\'project1\', location = "#{mychassis1}/1/2" )'),

                         config =            dict(desc    = "config: -Sets or modifies the value of an attribute",
                                                  usage   = "stc.config( objectHandle, propertyName1 = propertyValue1, ... )",
                                                  example = "stc.config( stream1, enabled = true )"),

                         get =               dict(desc    = "get: -Retrieves the value of an attribute",
                                                  usage   = "stc.get( objectHandle, propertyName1, propertyName2, ... )",
                                                  example = "stc.get( stream1, 'enabled', 'name' )"),

                         perform =           dict(desc    = "perform: -Invokes an operation",
                                                  usage   = "stc.perform( commandName, propertyName1 = propertyValue1, ... )",
                                                  example = "stc.perform( 'createdevice', parentHandleList = 'project1' createCount = 4 )"),

                         delete  =           dict(desc    = "delete: -Deletes an object in a test hierarchy",
                                                  usage   = "stc.delete( objectHandle )",
                                                  example = "stc.delete( stream1 )"),

                         connect =           dict(desc    = "connect: -Establishes a connection with a Spirent TestCenter chassis",
                                                  usage   = "stc.connect( hostnameOrIPaddress, ... )",
                                                  example = "stc.connect( mychassis1 )"),

                         disconnect =        dict(desc    = "disconnect: -Removes a connection with a Spirent TestCenter chassis",
                                                  usage   = "stc.disconnect( hostnameOrIPaddress, ... )" ,
                                                  example = "stc.disconnect( mychassis1 )") ,

                         reserve =           dict(desc    = "reserve: -Reserves a port group",
                                                  usage   = "stc.reserve( CSP1, CSP2, ... )",
                                                  example = 'stc.reserve( "//#{mychassis1}/1/1", "//#{mychassis1}/1/2" )'),

                         release =           dict(desc    = "release: -Releases a port group",
                                                  usage   = "stc.release( CSP1, CSP2, ... )",
                                                  example = 'stc.release( "//#{mychassis1}/1/1", "//#{mychassis1}/1/2" )'),

                         apply =             dict(desc    = "apply: -Applies a test configuration to the Spirent TestCenter firmware",
                                                  usage   = "stc.apply()",
                                                  example = "stc.apply()"),

                         log  =              dict(desc    = "log: -Writes a diagnostic message to the log file",
                                                  usage   = "stc.log( logLevel, message )",
                                                  example = "stc.log( 'DEBUG', 'This is a debug message' )"),

                         waitUntilComplete = dict(desc    = "waitUntilComplete: -Suspends your application until the test has finished",
                                                  usage   = "stc.waitUntilComplete()",
                                                  example = "stc.waitUntilComplete()"),

                         subscribe =         dict(desc    = "subscribe: -Directs result output to a file or to standard output",
                                                  usage   = "stc.subscribe( parent=parentHandle, resultParent=parentHandles, configType=configType, resultType=resultType, viewAttributeList=attributeList, interval=interval, fileNamePrefix=fileNamePrefix )",
                                                  example = "stc.subscribe( parent='project1', configType='Analyzer', resulttype='AnalyzerPortResults', filenameprefix='analyzer_port_counter' )"),

                         unsubscribe =       dict(desc    = "unsubscribe: -Removes a subscription",
                                                  usage   = "stc.unsubscribe( resultDataSetHandle )",
                                                  example = "stc.unsubscribe( resultDataSet1 )"))

#################END OF STC Native APIs implementation################

def _hlpyapi_env():

    global pythonver,logname,log_dir

	#To get python version

    if (sys.version.split(' ')[0]).split('.')[0]=='3':

	    pythonver=3

    print('Current OS: '+platform.system()+','+platform.release()+','+platform.version()+';'+' python version: ' + sys.version.split(' ')[0])



    # spawn and connect to a server running on the local host

    # for a remote server, this will have to be changed somewhat

    # todo: implement a connection to a remote server

    global tclserversocket

    HOST = 'localhost'

    PORT = 0

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    srv.bind((HOST, PORT))

    srv.listen(1)

    HOST,PORT = srv.getsockname()

    portstr = '%d' %PORT

    if 'STC_TCL' in os.environ:

        tcl_path = os.environ['STC_TCL']

    else :

        print('HLPy Error: need set system environ variable STC_TCL firstly\n')

        sys.exit()

    if 'HLPYAPI_LOG' in os.environ:

        log_dir = os.environ['HLPYAPI_LOG']

    else :

        log_dir = os.getcwd()

    logname = "hlpyapi.hltlog"

    try:

        if sys.argv[0]:

            logname = os.path.basename(sys.argv[0])

            logname = logname.split('.py')[0]

            logname = logname + '.hltlog'

    except:

        logname = "hlpyapi.hltlog"

    basedir = os.path.dirname(os.path.realpath(__file__))

    filedir = os.path.join(basedir, "hltapiserver.srv")

    stcserver = tcl_path +" "+filedir+ " "+portstr+" 120 log "+ log_dir +" "+ logname +" INFO"

    subprocess.Popen(stcserver.split())



    connection, address = srv.accept()



    newport = connection.recv(socket_buffer)

    if pythonver == 3:

        newport = newport.decode("utf-8")

    match = re.search('[0-9]*',newport)

    newport = match.group(0)

    import locale

    newport = locale.atoi(newport)

    print("Connecting Tcl server via port", newport)

    tclserversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    tclserversocket.connect((HOST, newport))

    #To set tcllibpath
    srcdir = "/".join(str(basedir).split('\\'))+"/SourceCode"
    if os.path.exists(srcdir):
        print("Setting HltApi TCLLIBPATH...")
        srcdir="set auto_path [linsert $auto_path 0 " +srcdir+"] \n"
        if pythonver == 3:
            tclserversocket.send(bytes(srcdir, 'UTF-8'))
        else:
            tclserversocket.send(srcdir)
        tclserversocket.recv(socket_buffer)

    print("Loading SpirentHltApi...")

    if pythonver == 3:

        tclserversocket.send(bytes("package require SpirentHltApi\n", 'UTF-8'))

    else:

        tclserversocket.send("package require SpirentHltApi\n")

    if pythonver == 3:

        result = (tclserversocket.recv(socket_buffer)).decode("utf-8")

    else:

        result = tclserversocket.recv(socket_buffer)

    print("Loaded SpirentHltApi:",result)

    return TRUE;



def invoke(cmd):
    print ("Native call : " + cmd)

    ret = _private_invoke(cmd)

    return ret;


def _private_invoke(cmd):

    global tclserversocket

    if pythonver == 3:

        tclserversocket.send(bytes(cmd+'\n','UTF-8'))

    else:

        tclserversocket.send(cmd+'\n')

    ret = ''

    flag = 1

    socket_list = [tclserversocket]

    read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])



    while flag:

        for sock in read_sockets:

            if sock == tclserversocket:

                if pythonver == 3:

                    data = (tclserversocket.recv(socket_buffer)).decode("utf-8")

                else:

                    data = tclserversocket.recv(socket_buffer)

                ret += data

                if len(data) < socket_buffer :

                    flag = 0

                elif ('\r' == data[len(data) -2]) :

                    if('\n' == data[len(data) -1]):

                        flag = 0
                        
                        data = tclserversocket.recv(socket_buffer)

                        ret += data

    #removal of whitespaces at end of line

    ret = re.sub(r'\s+$', '', ret)
    
    ret = re.sub(r'\r', '', ret)
    
    ret = re.sub(r'\n', '', ret)

    #check ret: STCSERVER_RET_SUCCESS:/STCSERVER_RET_ERROR:/invalid rest

    ret = ret.replace('STCSERVER_RET_SUCCESS:', ' ')
    
    ret = re.sub(r'\s+', ' ', ret)

    if ret.find('STCSERVER_RET_ERROR') >= 0 :
        
        print('HLPy',cmd,'\nError:',ret)
        
        sys.exit()
        
    return ret;


def _hltpy_sequencer_config(tcl_str, **arg):
    mytcl_str = ''
    for key in list(arg.keys()):
        mytcl_str += _pydict2tclstr(key, arg[key], '')
    
    mytcl_str += tcl_str
    tclarray = mytcl_str.split('\n')
    for i in range(0, len(tclarray)):
        mytcl = tclarray[i].strip()
        if (mytcl != ""):
            _private_invoke(mytcl)
            ret_dict = _hlt_result_conv()

    if isinstance(ret_dict, dict) and ret_dict == {}:
        return ""
    return ret_dict


def _pydict2tclstr(handle_ret_py, dict_ret_py, key_str):
    tcl_str = ''
    handle_ret = re.sub(r'^py_', '', handle_ret_py)
    if re.match('^py_port', handle_ret_py, flags=re.I) is not None:
        tcl_str = 'set handle_ret $' + handle_ret_py
    else:
        for (key, value) in dict_ret_py.items():
            mykey_str = key_str+'.'+key
            if key_str == '':
                mykey_str = key
            else:
                mykey_str = key_str+'.'+key
            if isinstance(value, dict):
                tcl_str += _pydict2tclstr(handle_ret_py, value, mykey_str)
            else:
                tcl_str += 'keylset ' + handle_ret + ' ' + mykey_str + ' ' + value + '\n'
    return tcl_str

def _hlt_params_conv(**arg):

    ret = ''

    for key in list(arg.keys()):

        if type(arg[key]) is int:

            arg[key]= str(arg[key])

        elif type(arg[key]) is list:

            tcllist = '"'

            for element in arg[key]:

                tcllist = tcllist + ' ' +element

            tcllist += '"'

            tcllist = tcllist.replace('" ','"')

            arg[key]= tcllist

        elif type(arg[key]) is str:

            if arg[key].find(' ') >= 0:

                arg[key]= '"' + arg[key] + '"'

        else:

            print("HLPY: hlpyapi only accept int,list and string as parameters. ",key,type(arg[key]))

        keybak = key

        keybak = keybak.replace('python_','')

        ret = ret+ ' -' + keybak + ' ' + arg[key]

    return ret;





def _init_dict_recursive(keysList, value) :

    dict_key = {}

    keyarray = keysList.split('.')

    mylen = len(keyarray)

    if mylen > 0 and keyarray[0] != '' :

        key = keyarray[0]

        newList = keysList.replace(key, '',1)

        newList = newList.lstrip('.')

        dict_key[key] = _init_dict_recursive(newList, value)

        return dict_key

    else :

        return value



def _merge_dict_recursive(a, b):

    '''recursively merges dict's. not just simple a['key'] = b['key'], if

    both a and bhave a key who's value is a dict then dict_merge is called

    on both values and the result stored in the returned dictionary.'''

    if not isinstance(b, dict):

        return b

    result = dict(a)

    if pythonver == 3:

        for k, v in b.items():

            if k in result and isinstance(result[k], dict):

                result[k] = _merge_dict_recursive(result[k], v)

            else:

                result[k] = v

    else:

        for k, v in b.iteritems():

            if k in result and isinstance(result[k], dict):

                result[k] = _merge_dict_recursive(result[k], v)

            else:

                result[k] = v

    return result



def _hlt_result_conv():

    mydict = {}

    #catch the make sure error also can pass this function

    try:

        _private_invoke("set hashkey \"\"; set hashvalue \"\"; set nested_hashkey \"\"")

        _private_invoke("ret_hash ret hashkey hashvalue nested_hashkey")



        keys = _private_invoke("set hashkey")

        values = _private_invoke("set hashvalue")



        keysbackup = keys

        valuesbackup = values



        #delete '\r\n'

        keys = keys.replace('\r\n','')

        values = values.replace('\r\n','')

        values = values.replace('{{}}','{}')

        keys = keys.replace(' . ','.')

        keys = keys.replace('{','')

        keys = keys.replace('}','')

        valuesList = list(values)

        values = []

        listflag = 0

        valuetemp = ''

        for char in valuesList:

            if char == '{':

                listflag = 1

            elif char == '}':

                listflag = 0

                #output list

                values.append(valuetemp)

                valuetemp = ''

            elif char == ' ':

                if listflag == 0:

                    #output single value

                    if valuetemp != '':

                        values.append(valuetemp)

                    valuetemp = ''

                else:

                    #buffer value

                    valuetemp+= char

            else :

                #buffer value

                valuetemp+= char

        if valuetemp != '':

            values.append(valuetemp)



        keysList = keys.split()

        for i in range(0,len(keysList)):

            subdict = _init_dict_recursive(keysList[i], values[i])

            mydict = _merge_dict_recursive(mydict, subdict)

    except:

        print("HLPY: error happened when converting keys-values:",keysbackup,valuesbackup)

    return mydict



#used be emulation_lldp_optional_tlv_config and emulation_lldp_dcbx_tlv_config

def _hlt_result_conv_special(ret):

    returnval = {}

    returnval['status'] = '1'

    ret = ret.replace('\r\n','')

    ret = ret.replace('{handle {','')

    ret = ret.replace('}} {status 1}','')

    ret = ret.replace('{','\{')

    ret = ret.replace('}','\}')

    returnval['handle'] = ret

    return returnval



def connect(**arg):

    #print "HLPY: connect:",
    port_names = ''
    if 'my_return_handle' in arg.keys():
        port_names = arg['my_return_handle']
        del arg['my_return_handle']

    cmdline = _hlt_params_conv(**arg)

    #print cmdline

    #execute the HLT command

    ret = _private_invoke("sth::connect"+cmdline)

    #convert the HLT return value keyed list into Dict and return

    #connect need special handle

    #{offline 0} {port_handle {{10 {{61 {{44 {{2 {{6/8 port1}}}}}}}}}}} {status 1}

    ret = ret.replace('{','')

    ret = ret.replace('}','')

    ret = ret.split()

    retnew = {}

    index = 0

    chassis_port = {}

    ports = {}

    for element in ret:

        index += 1

        if element == 'offline':

            retnew['offline'] = ret[index]

            index1 = index + 1

        if element == 'status':

            retnew['status'] = ret[index]

            index2 = index - 1

    port_handle = ret[index1]
    ipTemp=['$']*4
    indexRet=index1+1
    ipIdx=0
    strFlag=0
    chassis_port={}
    portDetail={}
    completeFlag=0
    keepIp=[]
    while(indexRet<index2):
        if "/" in str(ret[indexRet]):
                if completeFlag!=1 and strFlag!=1:
                    firstIdx=0
                    for startIdx in range(ipTemp.count("$"),4):
                        if ipTemp[firstIdx]!="$":
                            keepIp[startIdx]=ipTemp[firstIdx]
                            firstIdx=firstIdx+1
                    ipIdx=0
                if strFlag!=1:
                    ipKeyStr='.'.join(str(ipStr) for ipStr in keepIp)
                else:
                    ipKeyStr=strIP
                portDetail[ret[indexRet]]=ret[indexRet+1]
                if ipKeyStr in chassis_port.keys():
                    chassis_port[ipKeyStr].update(portDetail)
                else:
                    chassis_port.update({ipKeyStr:portDetail})
                portDetail={}
                indexRet=indexRet+2
                continue
        if ret[indexRet].isdigit():
            completeFlag=0
            ipTemp[ipIdx]=ret[indexRet]
            ipIdx=ipIdx+1
            if ipIdx==4:
                completeFlag=1
                keepIp=ipTemp
                ipTemp=['$']*4
                ipIdx=0
            strFlag=0
        else:
            #when ip is given as string
            strIP=ret[indexRet]
            strFlag=1
        indexRet=indexRet+1

    retnew[port_handle] = chassis_port

    #Update Global return variable
    if port_names:
        device = arg['device']
        port_list = arg['port_list']
        port_names_dict = {}
    
        if 'connect' in GRetDict.keys():
            port_names_dict = GRetDict['connect']
    
        for i in range(len(port_names)):
            port_names_dict.update({port_names[i]: retnew['port_handle'][device][port_list[i]]})
    
        GRetDict.update({ 'connect' : port_names_dict })

    return retnew



#####sth.device_info#####

def device_info(**arg):

    #print "HLPY: device_info:",

    cmdline = _hlt_params_conv(**arg)

    #print cmdline

    #execute the HLT command

    ret = _private_invoke("sth::device_info"+cmdline)

    #convert the HLT return value keyed list into hash and return

    #this is not same as other functions

    ret = ret.replace('{','')

    ret = ret.replace('}','')

    ret = ret.split()

    newret = {}

    newret[ret[0]] = ret[1]

    chassis = ret[2]+'.'+ret[3]+'.'+ret[4]+'.'+ret[5]

    chassisdict = {}

    availabledcit = {}

    inusedict = {}

    if ret.count('available') != 0:

        availableindex = ret.index('available')

        if ret.count('inuse') != 0:

            inusedindex = ret.index('inuse')

            i = availableindex+1

            while i < inusedindex :

                availabledcit[ret[i]] = {ret[i+1]:ret[i+2]}

                i += 3

    if ret.count('inuse') != 0:

        inusedindex = ret.index('inuse')

        if ret.count('port_handle') != 0:

            port_handleindex = ret.index('port_handle')

            i = inusedindex+1

            while i < port_handleindex :

                inusedict[ret[i]] = {ret[i+1]:ret[i+2],ret[i+3]:ret[i+4]}

                i += 5

    newret[chassis] = {'available':availabledcit,'inuse':inusedict}

    if ret.count('status') != 0:

        statusindex = ret.index('status')

        newret['status'] = ret[statusindex+1]

    return newret



#################################generate by tool################
#####sth.emulation_gre_config#####

def emulation_gre_config(**arg):

    #print "HLPY: emulation_gre_config:",

    cmdline = _hlt_params_conv(**arg)

    #print cmdline

    #execute the HLT command

    ret = _private_invoke("set ret [sth::emulation_gre_config" + cmdline + "]")

    #convert the HLT return value keyed list into hash and return

    ret = ret.replace('\r\n','')

    return ret


#####sth.emulation_lldp_dcbx_tlv_config#####

def emulation_lldp_dcbx_tlv_config(**arg):

    #print "HLPY: emulation_lldp_dcbx_tlv_config:",

    cmdline = _hlt_params_conv(**arg)

    #print cmdline

    #execute the HLT command

    ret = _private_invoke("set ret [sth::emulation_lldp_dcbx_tlv_config" + cmdline + "]")

    #convert the HLT return value keyed list into hash and return

    return _hlt_result_conv_special(ret)


#####sth.emulation_lldp_optional_tlv_config#####

def emulation_lldp_optional_tlv_config(**arg):

    #print "HLPY: emulation_lldp_optional_tlv_config:",

    cmdline = _hlt_params_conv(**arg)

    #print cmdline

    #execute the HLT command

    ret = _private_invoke("set ret [sth::emulation_lldp_optional_tlv_config" + cmdline + "]")

    #convert the HLT return value keyed list into hash and return

    return _hlt_result_conv_special(ret)

#####sth.cleanup_session#####
def cleanup_session(**arg):
    if 'my_port_handle' in arg.keys() :
        portList = arg['my_port_handle']
        for i in range(len(portList)):
            portHnd = GRetDict['connect'][portList[i]]
        arg.update({'port_handle' : portHnd})
        del arg['my_port_handle']
    
    cmdline = _hlt_params_conv(**arg)
    if "clean_logs" in arg.keys() and int(arg["clean_logs"])==1:
        ret = _private_invoke("stcserver::close_file")
        os.remove(os.path.join(log_dir,logname))
    #execute the HLT command
    ret = _private_invoke("set ret [sth::cleanup_session" + cmdline + "]")
    #convert the HLT return value keyed list into hash and return
    return _hlt_result_conv()

def _str_to_list(dict_input):
    for keyName in list(dict_input):
        if keyName != "status" and len(dict_input[keyName].split())!=1:
            dict_input[keyName]=dict_input[keyName].split()
    return dict_input


#listing all APIs
def _process_cmd(cmd_name,**arg):

    if 'my_return_handle' in arg.keys() or 'my_port_handle' in arg.keys() or 'my_handle' in arg.keys() :
        retVal = _process_handles(cmd_name,**arg)
    else :
        cmdline=_hlt_params_conv(**arg)
        retVal=_private_invoke("set ret [sth::"+cmd_name+cmdline+"]")
        retVal = _hlt_result_conv()
    
    return retVal


def _process_handles(cmd_name,**arg):
    
    device_names = ''
    if 'my_return_handle' in arg.keys() :
        device_names = arg['my_return_handle']
        del arg['my_return_handle']

    if 'my_port_handle' in arg.keys() :
        portList = arg['my_port_handle']
        for i in range(len(portList)):
            portHnd = GRetDict['connect'][portList[i]]
        arg.update({'port_handle' : portHnd})
        del arg['my_port_handle']

    if 'my_handle' in arg.keys() :
        if 'emulation_dhcp_group_config' in cmd_name :
            hnd = GRetDict['emulation_dhcp_config'][arg['my_handle']]
        arg.update({'handle' : hnd})
        del arg['my_handle']

    cmdline=_hlt_params_conv(**arg)
    ret=_private_invoke("set ret [sth::"+cmd_name+cmdline+"]")
    ret = _hlt_result_conv()


    if device_names :
        names_dict = {}
        if cmd_name in GRetDict.keys():
            names_dict = GRetDict[cmd_name]
        if 'emulation_dhcp_server_config' in cmd_name:
            names_dict.update({device_names: ret['handle']['dhcp_handle']})
        elif 'emulation_dhcp_group_config' in cmd_name:
            temp_dict = {}
            temp_dict.update({'handles': ret['handles']})
            temp_dict.update({'handle': ret['handle']})
            names_dict.update({device_names: temp_dict})
        else :
            names_dict.update({device_names: ret['handles']})            
    
        GRetDict.update({cmd_name : names_dict })
    
    return ret


def alarms_control(**arg):
    return _process_cmd("alarms_control",**arg)

def alarms_stats(**arg):
    return _process_cmd("alarms_stats",**arg)

def emulation_ancp_config(**arg):
    return _process_cmd("emulation_ancp_config",**arg)

def emulation_ancp_subscriber_lines_config(**arg):
    return _process_cmd("emulation_ancp_subscriber_lines_config",**arg)

def emulation_ancp_control(**arg):
    return _process_cmd("emulation_ancp_control",**arg)

def emulation_ancp_stats(**arg):
    return _process_cmd("emulation_ancp_stats",**arg)

def emulation_bfd_config(**arg):
    return _process_cmd("emulation_bfd_config",**arg)

def emulation_bfd_control(**arg):
    return _process_cmd("emulation_bfd_control",**arg)

def emulation_bfd_info(**arg):
    return _process_cmd("emulation_bfd_info",**arg)

def emulation_bfd_session_config(**arg):
    return _process_cmd("emulation_bfd_session_config",**arg)

def emulation_bgp_config(**arg):
    return _process_cmd("emulation_bgp_config",**arg)

def emulation_bgp_control(**arg):
    return _process_cmd("emulation_bgp_control",**arg)

def emulation_bgp_info(**arg):
    return _process_cmd("emulation_bgp_info",**arg)

def emulation_bgp_route_config(**arg):
    return _process_cmd("emulation_bgp_route_config",**arg)

def emulation_bgp_route_generator(**arg):
    return _process_cmd("emulation_bgp_route_generator",**arg)

def emulation_bgp_custom_attribute_config(**arg):
    return _process_cmd("emulation_bgp_custom_attribute_config",**arg)

def emulation_bgp_route_info(**arg):
    return _process_cmd("emulation_bgp_route_info",**arg)

def emulation_bgp_route_element_config(**arg):
    return _process_cmd("emulation_bgp_route_element_config",**arg)

def emulation_convergence_config(**arg):
    return _process_cmd("emulation_convergence_config",**arg)

def emulation_convergence_control(**arg):
    return _process_cmd("emulation_convergence_control",**arg)

def emulation_convergence_info(**arg):
    return _process_cmd("emulation_convergence_info",**arg)

def emulation_device_config(**arg):
    return _process_cmd("emulation_device_config",**arg)

def emulation_dhcp_config(**arg):
    return _process_cmd("emulation_dhcp_config",**arg)

def emulation_dhcp_group_config(**arg):
    return _process_cmd("emulation_dhcp_group_config",**arg)

def emulation_dhcp_control(**arg):
    return _process_cmd("emulation_dhcp_control",**arg)

def emulation_dhcp_stats(**arg):
    return _process_cmd("emulation_dhcp_stats",**arg)

def emulation_dhcp_server_config(**arg):
    return _process_cmd("emulation_dhcp_server_config",**arg)

def emulation_dhcp_server_relay_agent_config(**arg):
    return _process_cmd("emulation_dhcp_server_relay_agent_config",**arg)

def emulation_dhcp_server_control(**arg):
    return _process_cmd("emulation_dhcp_server_control",**arg)

def emulation_dhcp_server_stats(**arg):
    return _process_cmd("emulation_dhcp_server_stats",**arg)

def emulation_dot1x_config(**arg):
    return _process_cmd("emulation_dot1x_config",**arg)

def emulation_dot1x_control(**arg):
    return _process_cmd("emulation_dot1x_control",**arg)

def emulation_dot1x_stats(**arg):
    return _process_cmd("emulation_dot1x_stats",**arg)

def emulation_oam_config_msg(**arg):
    return _process_cmd("emulation_oam_config_msg",**arg)

def emulation_oam_config_ma_meg(**arg):
    return _process_cmd("emulation_oam_config_ma_meg",**arg)

def emulation_oam_config_topology(**arg):
    return _process_cmd("emulation_oam_config_topology",**arg)

def emulation_oam_control(**arg):
    return _process_cmd("emulation_oam_control",**arg)

def emulation_oam_info(**arg):
    return _process_cmd("emulation_oam_info",**arg)

def fc_config(**arg):
    return _process_cmd("fc_config",**arg)

def fc_control(**arg):
    return _process_cmd("fc_control",**arg)

def fc_stats(**arg):
    return _process_cmd("fc_stats",**arg)

def fcoe_config(**arg):
    return _process_cmd("fcoe_config",**arg)

def fcoe_control(**arg):
    return _process_cmd("fcoe_control",**arg)

def fcoe_stats(**arg):
    return _process_cmd("fcoe_stats",**arg)

def fcoe_traffic_config(**arg):
    return _process_cmd("fcoe_traffic_config",**arg)

def fip_traffic_config(**arg):
    return _process_cmd("fip_traffic_config",**arg)

def pcs_error_config(**arg):
    return _process_cmd("pcs_error_config",**arg)

def random_error_config(**arg):
    return _process_cmd("random_error_config",**arg)

def pcs_error_control(**arg):
    return _process_cmd("pcs_error_control",**arg)

def random_error_control(**arg):
    return _process_cmd("random_error_control",**arg)

def forty_hundred_gig_l1_results(**arg):
    return _process_cmd("forty_hundred_gig_l1_results",**arg)

def emulation_http_profile_config(**arg):
    return _process_cmd("emulation_http_profile_config",**arg)

def emulation_http_phase_config(**arg):
    return _process_cmd("emulation_http_phase_config",**arg)

def emulation_http_config(**arg):
    return _process_cmd("emulation_http_config",**arg)

def emulation_http_control(**arg):
    return _process_cmd("emulation_http_control",**arg)

def emulation_http_stats(**arg):
    return _process_cmd("emulation_http_stats",**arg)

def emulation_igmp_querier_config(**arg):
    return _process_cmd("emulation_igmp_querier_config",**arg)

def emulation_igmp_querier_control(**arg):
    return _process_cmd("emulation_igmp_querier_control",**arg)

def emulation_igmp_querier_info(**arg):
    return _process_cmd("emulation_igmp_querier_info",**arg)

def emulation_ipv6_autoconfig(**arg):
    return _process_cmd("emulation_ipv6_autoconfig",**arg)

def emulation_ipv6_autoconfig_control(**arg):
    return _process_cmd("emulation_ipv6_autoconfig_control",**arg)

def emulation_ipv6_autoconfig_stats(**arg):
    return _process_cmd("emulation_ipv6_autoconfig_stats",**arg)

def emulation_isis_config(**arg):
    return _process_cmd("emulation_isis_config",**arg)

def emulation_isis_control(**arg):
    return _process_cmd("emulation_isis_control",**arg)

def emulation_isis_topology_route_config(**arg):
    return _process_cmd("emulation_isis_topology_route_config",**arg)

def emulation_isis_lsp_generator(**arg):
    return _process_cmd("emulation_isis_lsp_generator",**arg)

def emulation_isis_info(**arg):
    return _process_cmd("emulation_isis_info",**arg)

def l2tp_config(**arg):
    return _process_cmd("l2tp_config",**arg)

def l2tp_control(**arg):
    return _process_cmd("l2tp_control",**arg)

def l2tp_stats(**arg):
    return _process_cmd("l2tp_stats",**arg)

def l2tpv3_config(**arg):
    return _process_cmd("l2tpv3_config",**arg)

def l2tpv3_control(**arg):
    return _process_cmd("l2tpv3_control",**arg)

def l2tpv3_stats(**arg):
    return _process_cmd("l2tpv3_stats",**arg)

def emulation_lag_config(**arg):
    return _process_cmd("emulation_lag_config",**arg)

def emulation_lacp_config(**arg):
    return _process_cmd("emulation_lacp_config",**arg)

def emulation_lacp_control(**arg):
    return _process_cmd("emulation_lacp_control",**arg)

def emulation_lacp_info(**arg):
    return _process_cmd("emulation_lacp_info",**arg)

def emulation_ldp_config(**arg):
    return _process_cmd("emulation_ldp_config",**arg)

def emulation_ldp_control(**arg):
    return _process_cmd("emulation_ldp_control",**arg)

def emulation_ldp_info(**arg):
    return _process_cmd("emulation_ldp_info",**arg)

def emulation_ldp_route_config(**arg):
    return _process_cmd("emulation_ldp_route_config",**arg)

def emulation_lsp_switching_point_tlvs_config(**arg):
    return _process_cmd("emulation_lsp_switching_point_tlvs_config",**arg)

def emulation_ldp_route_element_config(**arg):
    return _process_cmd("emulation_ldp_route_element_config",**arg)

def emulation_efm_config(**arg):
    return _process_cmd("emulation_efm_config",**arg)

def emulation_efm_control(**arg):
    return _process_cmd("emulation_efm_control",**arg)

def emulation_efm_stat(**arg):
    return _process_cmd("emulation_efm_stat",**arg)

def emulation_lldp_config(**arg):
    return _process_cmd("emulation_lldp_config",**arg)

def emulation_lldp_control(**arg):
    return _process_cmd("emulation_lldp_control",**arg)

def emulation_lldp_info(**arg):
    return _process_cmd("emulation_lldp_info",**arg)

def emulation_mld_config(**arg):
    return _process_cmd("emulation_mld_config",**arg)

def emulation_mld_control(**arg):
    return _process_cmd("emulation_mld_control",**arg)

def emulation_mld_group_config(**arg):
    return _process_cmd("emulation_mld_group_config",**arg)

def emulation_mld_info(**arg):
    return _process_cmd("emulation_mld_info",**arg)

def emulation_mpls_tp_config(**arg):
    return _process_cmd("emulation_mpls_tp_config",**arg)

def emulation_mpls_tp_port_config(**arg):
    return _process_cmd("emulation_mpls_tp_port_config",**arg)

def emulation_mpls_tp_control(**arg):
    return _process_cmd("emulation_mpls_tp_control",**arg)

def emulation_lsp_ping_info(**arg):
    return _process_cmd("emulation_lsp_ping_info",**arg)

def emulation_mpls_l2vpn_pe_config(**arg):
    return _process_cmd("emulation_mpls_l2vpn_pe_config",**arg)

def emulation_mpls_l2vpn_site_config(**arg):
    return _process_cmd("emulation_mpls_l2vpn_site_config",**arg)

def emulation_mpls_l3vpn_pe_config(**arg):
    return _process_cmd("emulation_mpls_l3vpn_pe_config",**arg)

def emulation_mpls_l3vpn_site_config(**arg):
    return _process_cmd("emulation_mpls_l3vpn_site_config",**arg)

def emulation_mpls_vpn_control(**arg):
    return _process_cmd("emulation_mpls_vpn_control",**arg)

def emulation_mvpn_provider_port_config(**arg):
    return _process_cmd("emulation_mvpn_provider_port_config",**arg)

def emulation_mvpn_config(**arg):
    return _process_cmd("emulation_mvpn_config",**arg)

def emulation_mvpn_customer_port_config(**arg):
    return _process_cmd("emulation_mvpn_customer_port_config",**arg)

def emulation_mvpn_vrf_config(**arg):
    return _process_cmd("emulation_mvpn_vrf_config",**arg)

def emulation_mvpn_vrf_route_config(**arg):
    return _process_cmd("emulation_mvpn_vrf_route_config",**arg)

def emulation_mvpn_vrf_traffic_config(**arg):
    return _process_cmd("emulation_mvpn_vrf_traffic_config",**arg)

def emulation_mvpn_control(**arg):
    return _process_cmd("emulation_mvpn_control",**arg)

def emulation_mvpn_info(**arg):
    return _process_cmd("emulation_mvpn_info",**arg)

def emulation_openflow_config(**arg):
    return _process_cmd("emulation_openflow_config",**arg)

def emulation_openflow_control(**arg):
    return _process_cmd("emulation_openflow_control",**arg)

def emulation_openflow_stats(**arg):
    return _process_cmd("emulation_openflow_stats",**arg)

def emulation_ospf_lsa_config(**arg):
    return _process_cmd("emulation_ospf_lsa_config",**arg)

def emulation_ospf_tlv_config(**arg):
    return _process_cmd("emulation_ospf_tlv_config",**arg)

def emulation_ospf_config(**arg):
    return _process_cmd("emulation_ospf_config",**arg)

def emulation_ospf_control(**arg):
    return _process_cmd("emulation_ospf_control",**arg)

def emulation_ospfv2_info(**arg):
    return _process_cmd("emulation_ospfv2_info",**arg)

def emulation_ospfv3_info(**arg):
    return _process_cmd("emulation_ospfv3_info",**arg)

def emulation_ospf_route_info(**arg):
    return _process_cmd("emulation_ospf_route_info",**arg)

def emulation_ospf_lsa_generator(**arg):
    return _process_cmd("emulation_ospf_lsa_generator",**arg)

def packet_config_buffers(**arg):
    return _process_cmd("packet_config_buffers",**arg)

def packet_control(**arg):
    return _process_cmd("packet_control",**arg)

def packet_stats(**arg):
    return _process_cmd("packet_stats",**arg)

def packet_config_filter(**arg):
    return _process_cmd("packet_config_filter",**arg)

def packet_config_pattern(**arg):
    return _process_cmd("packet_config_pattern",**arg)

def packet_config_triggers(**arg):
    return _process_cmd("packet_config_triggers",**arg)

def packet_info(**arg):
    return _process_cmd("packet_info",**arg)

def packet_decode(**arg):
    return _process_cmd("packet_decode",**arg)

def emulation_pcep_config(**arg):
    return _process_cmd("emulation_pcep_config",**arg)

def emulation_pcep_control(**arg):
    return _process_cmd("emulation_pcep_control",**arg)

def emulation_pcep_stats(**arg):
    return _process_cmd("emulation_pcep_stats",**arg)

def emulation_pim_config(**arg):
    return _process_cmd("emulation_pim_config",**arg)

def emulation_pim_control(**arg):
    return _process_cmd("emulation_pim_control",**arg)

def emulation_pim_group_config(**arg):
    return _process_cmd("emulation_pim_group_config",**arg)

def emulation_pim_info(**arg):
    return _process_cmd("emulation_pim_info",**arg)

def emulation_ping(**arg):
    return _process_cmd("emulation_ping",**arg)

def ppp_config(**arg):
    return _process_cmd("ppp_config",**arg)

def ppp_stats(**arg):
    return _process_cmd("ppp_stats",**arg)

def pppox_config(**arg):
    return _process_cmd("pppox_config",**arg)

def pppox_control(**arg):
    return _process_cmd("pppox_control",**arg)

def pppox_stats(**arg):
    return _process_cmd("pppox_stats",**arg)

def pppox_server_config(**arg):
    return _process_cmd("pppox_server_config",**arg)

def pppox_server_control(**arg):
    return _process_cmd("pppox_server_control",**arg)

def pppox_server_stats(**arg):
    return _process_cmd("pppox_server_stats",**arg)

def emulation_ptp_config(**arg):
    return _process_cmd("emulation_ptp_config",**arg)

def emulation_ptp_control(**arg):
    return _process_cmd("emulation_ptp_control",**arg)

def emulation_ptp_stats(**arg):
    return _process_cmd("emulation_ptp_stats",**arg)

def test_rfc2889_config(**arg):
    return _process_cmd("test_rfc2889_config",**arg)

def test_rfc2544_config(**arg):
    return _process_cmd("test_rfc2544_config",**arg)

def test_rfc2544_control(**arg):
    return _process_cmd("test_rfc2544_control",**arg)

def test_rfc2544_info(**arg):
    return _process_cmd("test_rfc2544_info",**arg)

def test_rfc3918_config(**arg):
    return _process_cmd("test_rfc3918_config",**arg)

def test_rfc3918_control(**arg):
    return _process_cmd("test_rfc3918_control",**arg)

def test_rfc3918_info(**arg):
    return _process_cmd("test_rfc3918_info",**arg)

def emulation_rip_config(**arg):
    return _process_cmd("emulation_rip_config",**arg)

def emulation_rip_control(**arg):
    return _process_cmd("emulation_rip_control",**arg)

def emulation_rip_route_config(**arg):
    return _process_cmd("emulation_rip_route_config",**arg)

def emulation_rip_info(**arg):
    return _process_cmd("emulation_rip_info",**arg)

def emulation_rsvp_config(**arg):
    return _process_cmd("emulation_rsvp_config",**arg)

def emulation_rsvp_control(**arg):
    return _process_cmd("emulation_rsvp_control",**arg)

def emulation_rsvp_info(**arg):
    return _process_cmd("emulation_rsvp_info",**arg)

def emulation_rsvp_tunnel_info(**arg):
    return _process_cmd("emulation_rsvp_tunnel_info",**arg)

def emulation_rsvp_tunnel_config(**arg):
    return _process_cmd("emulation_rsvp_tunnel_config",**arg)

def emulation_rsvpte_tunnel_control(**arg):
    return _process_cmd("emulation_rsvpte_tunnel_control",**arg)

def emulation_rsvp_custom_object_config(**arg):
    return _process_cmd("emulation_rsvp_custom_object_config",**arg)

def labserver_connect(**arg):
    return _process_cmd("labserver_connect",**arg)

def labserver_disconnect(**arg):
    return _process_cmd("labserver_disconnect",**arg)

def interface_config(**arg):
    return _process_cmd("interface_config",**arg)

def interface_stats(**arg):
    return _process_cmd("interface_stats",**arg)

def interface_control(**arg):
    return _process_cmd("interface_control",**arg)

def start_devices(**arg):
    return _process_cmd("start_devices",**arg)

def stop_devices(**arg):
    return _process_cmd("stop_devices",**arg)

def load_xml(**arg):
    return _process_cmd("load_xml",**arg)

def save_xml(**arg):
    if not arg:
        arg = {"filename" : os.path.splitext(os.path.abspath(sys.argv[0]))[0]+".xml"}
    else:
        arg['filename'] = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), arg['filename'])
    if os.name == 'nt':
        arg['filename'] = arg['filename'].replace('\\', '/')    
    print ("Saving the configuration to "+arg['filename'])
    return _process_cmd("save_xml",**arg)
    
def fill_global_variables(**arg):
    return _process_cmd("fill_global_variables",**arg)

def get_handles(**arg):
    retRes=_process_cmd("get_handles",**arg)
    return _str_to_list(retRes)

def link_config(**arg):
    return _process_cmd("link_config",**arg)

def arp_control(**arg):
    return _process_cmd("arp_control",**arg)

def sequencer_control(**arg):
    return _process_cmd("sequencer_control",**arg)

def arp_nd_config(**arg):
    return _process_cmd("arp_nd_config",**arg)

def emulation_sip_config(**arg):
    return _process_cmd("emulation_sip_config",**arg)

def emulation_sip_control(**arg):
    return _process_cmd("emulation_sip_control",**arg)

def emulation_sip_stats(**arg):
    return _process_cmd("emulation_sip_stats",**arg)

def emulation_stp_config(**arg):
    return _process_cmd("emulation_stp_config",**arg)

def emulation_mstp_region_config(**arg):
    return _process_cmd("emulation_mstp_region_config",**arg)

def emulation_msti_config(**arg):
    return _process_cmd("emulation_msti_config",**arg)

def emulation_stp_control(**arg):
    return _process_cmd("emulation_stp_control",**arg)

def emulation_stp_stats(**arg):
    return _process_cmd("emulation_stp_stats",**arg)

def test_config(**arg):
    return _process_cmd("test_config",**arg)

def test_control(**arg):
    return _process_cmd("test_control",**arg)

def traffic_control(**arg):
    return _process_cmd("traffic_control",**arg)

def traffic_stats(**arg):
    return _process_cmd("traffic_stats",**arg)

def drv_stats(**arg):
    return _process_cmd("drv_stats",**arg)

def create_csv_file(**arg):
    return _process_cmd("create_csv_file",**arg)

def traffic_config(**arg):
    return _process_cmd("traffic_config",**arg)

def imix_config(**arg):
    return _process_cmd("imix_config",**arg)

def traffic_config_ospf(**arg):
    return _process_cmd("traffic_config_ospf",**arg)

def emulation_twamp_config(**arg):
    return _process_cmd("emulation_twamp_config",**arg)

def emulation_twamp_session_config(**arg):
    return _process_cmd("emulation_twamp_session_config",**arg)

def emulation_twamp_control(**arg):
    return _process_cmd("emulation_twamp_control",**arg)

def emulation_twamp_stats(**arg):
    return _process_cmd("emulation_twamp_stats",**arg)

def emulation_l2vpn_pe_config(**arg):
    return _process_cmd("emulation_l2vpn_pe_config",**arg)

def emulation_vpls_site_config(**arg):
    return _process_cmd("emulation_vpls_site_config",**arg)

def emulation_vxlan_config(**arg):
    return _process_cmd("emulation_vxlan_config",**arg)

def emulation_vxlan_control(**arg):
    return _process_cmd("emulation_vxlan_control",**arg)

def emulation_vxlan_stats(**arg):
    return _process_cmd("emulation_vxlan_stats",**arg)

def emulation_vxlan_port_config(**arg):
    return _process_cmd("emulation_vxlan_port_config",**arg)

def emulation_nonvxlan_port_config(**arg):
    return _process_cmd("emulation_nonvxlan_port_config",**arg)

def emulation_vxlan_wizard_config(**arg):
    return _process_cmd("emulation_vxlan_wizard_config",**arg)

def emulation_multicast_group_config(**arg):
    return _process_cmd("emulation_multicast_group_config",**arg)

def emulation_multicast_source_config(**arg):
    return _process_cmd("emulation_multicast_source_config",**arg)

def emulation_igmp_config(**arg):
    return _process_cmd("emulation_igmp_config",**arg)

def emulation_igmp_control(**arg):
    return _process_cmd("emulation_igmp_control",**arg)

def emulation_igmp_group_config(**arg):
    return _process_cmd("emulation_igmp_group_config",**arg)

def emulation_igmp_info(**arg):
    return _process_cmd("emulation_igmp_info",**arg)

def emulation_ospf_topology_route_config(**arg):
    return _process_cmd("emulation_ospf_topology_route_config",**arg)

def emulation_evpn_config(**arg):
    return _process_cmd("emulation_evpn_config",**arg)

def emulation_iptv_config(**arg):
    return _process_cmd("emulation_iptv_config",**arg)

def emulation_iptv_channel_viewing_profile_config(**arg):
    return _process_cmd("emulation_iptv_channel_viewing_profile_config",**arg)

def emulation_iptv_viewing_behavior_profile_config(**arg):
    return _process_cmd("emulation_iptv_viewing_behavior_profile_config",**arg)

def emulation_iptv_channel_block_config(**arg):
    return _process_cmd("emulation_iptv_channel_block_config",**arg)

def emulation_iptv_control(**arg):
    return _process_cmd("emulation_iptv_control",**arg)

def emulation_iptv_stats(**arg):
    return _process_cmd("emulation_iptv_stats",**arg)

def emulation_video_config(**arg):
    return _process_cmd("emulation_video_config",**arg)

def emulation_video_stats(**arg):
    return _process_cmd("emulation_video_stats",**arg)

def emulation_video_server_streams_config(**arg):
    return _process_cmd("emulation_video_server_streams_config",**arg)

def emulation_vqa_port_config(**arg):
    return _process_cmd("emulation_vqa_port_config",**arg)

def emulation_profile_config(**arg):
    return _process_cmd("emulation_profile_config",**arg)

def emulation_video_control(**arg):
    return _process_cmd("emulation_video_control",**arg)

def emulation_video_clips_manage(**arg):
    return _process_cmd("emulation_video_clips_manage",**arg)

def emulation_client_load_phase_config(**arg):
    return _process_cmd("emulation_client_load_phase_config",**arg)

def emulation_vqa_config(**arg):
    return _process_cmd("emulation_vqa_config",**arg)

def emulation_vqa_global_config(**arg):
    return _process_cmd("emulation_vqa_global_config",**arg)

def emulation_vqa_stats(**arg):
    return _process_cmd("emulation_vqa_stats",**arg)

def emulation_vqa_host_config(**arg):
    return _process_cmd("emulation_vqa_host_config",**arg)

def emulation_vqa_control(**arg):
    return _process_cmd("emulation_vqa_control",**arg)
    
def system_settings(**arg):
    return _process_cmd("system_settings",**arg)
	
def start_test(**arg):
    return _process_cmd("start_test",**arg)
#################################################
#############close the socket manually###########
#####sth.close#####
def close(**arg):
    global tclserversocket
    tclserversocket.close()
    tclserversocket=''

#as default, hlpyapi_env need be called as initial

try:

    _hlpyapi_env()

except:

    print("HLPY: error happened when connecting hltapiserver and loading hltapi.")

