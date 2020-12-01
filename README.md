# dlm-utility-factory

This is DLM utilities using at Moxa Factory

## Requirement: 
Install Python 3.X</br>
Install Python packages
```bash
pip install -r requirements.txt
```

## Program: factoryEnroll.py
This program reads input parameters (mac, modelName, serialNumber), invokes PIC Proxy Server to fetch device's certificate and private key, and output them to caller by standard output.
### How to run?
```bash
python factoryEnroll.py -m {mac address} -M {model name} -s {serial number}
```

## Program: call_factoryEnroll.py
This program shows how to invoke factoryEnroll.py program, and prints out return code and return data from factoryEnroll.py
### How to run?
```bash
python call_factoryEnroll.py
```

### Return Code
| No  |   |   |
|---|---|---|
| 1  | 0  |Success   |
| 2  | 100  |Wrong MAC address   |
| 3  | 101  |Cannot find project   |
| 4  | 108  |Not support this model name   |
| 5  | 111  |ProjectId is not match   |
| 6  | 112  |Exceed the max device limit   |
| 7  | 301  |Using: factoryEnroll.py -m {mac address} -M {model name} -s {serial number}   |
| 8  | 302  |Using: factoryEnroll.py -m {mac address} -M {model name} -s {serial number}   |
| 9  | 400  |Can't Reach PIC Proxy Server|
| 10  | 600  |Can't Write Data to File|
| 11 | 601  |Can't Create tar File|
| 12  | 999  |Unknow Error from PIC Server|

### Output
Content Type: .tar.gz</br>
Data Type: bytes

# Production Environment
You shall modify PIC Proxy Sever IP and port which defined in factoryEnroll.py
