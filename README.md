# dlm-utility-factory

This is DLM utilities using at Moxa Factory

## Requirement: 
Install Python 3.X</br>
Install Python packages
```bash
pip install -r requirements.txt
```

## Program: factoryEnroll.py
This program reads input parameters (mac, modelName, serialNumber), invokes PIC Proxy Server to fetch device's certificate and private key, and output them to caller via **standard output**.
### How to run?
```bash
python factoryEnroll.py -m {mac address} -M {model name} -s {serial number}
```

### Return Code
| No  |Code   |Note   |
|---|---|---|
| 1  | 0  |Success   |
| 2  | 100  |Wrong MAC address   |
| 3  | 101  |Cannot find project   |
| 4  | 108  |Not support this model name   |
| 5 | 109 |Pproject id can't be null |
| 6 | 111  |ProjectId is not match   |
| 7 | 112  |Exceed the max device limit   |
| 8 | 131  |Using: factoryEnroll.py -m {mac address} -M {model name} -s {serial number}   |
| 9 | 132  |Using: factoryEnroll.py -m {mac address} -M {model name} -s {serial number}   |
| 10 | 104 |Can't Reach PIC Proxy Server|
| 11 | 160 |Can't write data to file|
| 12 | 161 |Can't crate tar file|
| 13 | 162 |Can't read tar File|
| 14 | 199  |Unknow Error from PIC Server|

### Output
Content Type: .tar.gz</br>
Data Type: bytes

# Production Environment
You shall modify PIC Proxy Sever IP and port which defined in factoryEnroll.py
