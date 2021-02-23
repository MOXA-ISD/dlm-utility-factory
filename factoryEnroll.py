# -*- coding: utf-8 -*-
import getopt, sys, io, os, json
import requests
from pathlib import Path
import tarfile

# External Configuration
_picProxy1 = '192.168.8.4'                          # Define first PIC Proxy IP
_picProxy2 = '192.168.8.5'                          # Define second PIC Proxy IP
_picProxyPort = '8000'                              # Define PIC Proxy Port

# Internal Global Variable
_outputFolder = Path('device')                      # Content working folder
_keyFileName = _outputFolder / 'device.key'         # device private key output location
_certFileName = _outputFolder / 'device.cer'        # device certification output location
_archiveName = "device.tar.gz"                      # tar file to be create
_outputFile = Path(_archiveName)                    # tar file for output to std

#
# Valid Input parameters
# factoryEnroll.py -m {mac address} -M {model name} -s {serial number}
# 
def validInputParameters():
    macAddress=None
    modelName=None
    serialNumber=None
    short_options = "m:M:s:"
    long_options = ["macAddress=", "modelName=", "serialNumber="]
    returnCode = 999

    try:
        argument_list = sys.argv[1:]
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        returnCode = 301        # Unknow error on Get Opt
        sys.exit(returnCode)

    for current_argument, current_value in arguments:
        if current_argument in ("-m", "--macAddress"):
            macAddress = current_value            
        elif current_argument in ("-M", "--modelName="):
            modelName = current_value            
        elif current_argument in ("-s", "--serialNumber"):
            serialNumber = current_value            

    if (macAddress == None) or (modelName == None) or (serialNumber == None):
        returnCode = 302        # Using: factoryEnroll.py -m {mac address} -M {model name} -s {serial number}
        sys.exit(returnCode)
    
    return macAddress, modelName, serialNumber

#
# Call PIC Proxy Server to enroll device 
# Input: MAC, modelName, serialNo
# Output: X.509 Cert (string), Private Key (string)
# Exit with None-0 code, if specific error return from PIC Proxy Server
# 
def requestCAfromDLMProxy(MAC, modelName, serialNo, proxyId):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}        
        data = {'mac': MAC.replace(':',''), 'serialNumber': serialNo, 'modelName':modelName}
        returnCode = 999

        if proxyId == 1:
            picProxy = _picProxy1
        else:
            picProxy = _picProxy2

        try:
            r = requests.post('http://' + picProxy + ':' + _picProxyPort + '/api/v1/dlmProxy/enroll', headers=headers, data=json.dumps(data), verify=False, timeout=(5,5))            
            result = json.loads(r.text)
            if "data" in result:
                return result['data']['enrollCert'], result['data']['enrollPK']
            else: 
                if "error" in result:
                    returnCode = int(result['error']['code'])       # Error from PIC Server
                    sys.exit(returnCode)
                else:
                    sys.exit(returnCode)        # Unknow Error from PIC Server, 500
        except Exception as error:            
            return None, None

#
# Output device.tar.gz to stdout
#   - create certificate file
#   - create private key file
#   - tar these two files as device.tar.gz
#   - output device.tar.gz to stdout
# 
def outputCertificate(Cert, PK):  
    returnCode = 999

    try:                        # Save PK and Cert Files
        if not _outputFolder.exists():
            _outputFolder.mkdir()

        _keyFileName.write_text(PK)
        _certFileName.write_text(Cert)
    except Exception as error:
        returnCode = 600        # Can't write data to file
        sys.exit(returnCode)

    try:                        # Create tar File
        tar = tarfile.open(_archiveName, "w:gz")
        for file_name in _outputFolder.glob('**/*'):
            tar.add(file_name, os.path.basename(file_name))
        tar.close()
    except Exception as error:
        returnCode = 601        # Can't crate tar file
        sys.exit(returnCode)

    try:                        # Output tar content to stdout        
        #print(_outputFile.read_bytes(), file = sys.stdout)     
        sys.stdout.buffer.write(_outputFile.read_bytes())   
    except Exception as error:
        returnCode = 602        # Can't read tar file
        sys.exit(returnCode)

#
# Clean files and folder
# 
def cleanData():
    try:
        os.remove(_outputFile)
        os.remove(_keyFileName)
        os.remove(_certFileName)
        os.rmdir(_outputFolder)
    except Exception as error:
        returnCode = 0        # Ignore this Error
        sys.exit(returnCode)

#
# Main Program Start
#
cert = None
counter = 0
#macAddress = '00:90:e8:44:22:11'
#modelName = 'UC-8112A-ME-T-LX'
#serialNumber = 'A12345678'

macAddress, modelName, serialNumber = validInputParameters()

while cert == None and counter < 3:
    cert, pk = requestCAfromDLMProxy(macAddress, modelName, serialNumber, 1)
    counter = counter + 1

if (cert == None):
    counter = 0
    while cert == None and counter < 3:
        cert, pk = requestCAfromDLMProxy(macAddress, modelName, serialNumber, 2)
        counter = counter + 1
    
    if (cert == None):
        returnCode = 404                # Can't Reach PIC Proxy Server
        sys.exit(returnCode)            # Exit
    

outputCertificate(cert, pk)
cleanData()

sys.exit(0)            # Exit success




