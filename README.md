# homekit-knx-bridge

>WIP!!!

quick and dirty hack of a pure python HomeKit KNX Bridge

## Installation

### Requirements

* python3 > 3.5
* HAP-python (https://github.com/ikalchev/HAP-python)
* xnkx (https://github.com/XKNX/xknx)  

`pip3 install --user HAP-python[QRCode] xknx`

### Clone repo

`git clone https://github.com/uweswrtz/homekit-knx-bridge.git`

## Run

* adapt xknx.yaml to your needs or create a copy

`./homekit-knx-bridge -h`  
`./homekit-knx-bridge --name "My HomeKit KNX Bridge"` --file myhome.yaml

### Command line options

```
-n --name                   Set bridge name (Default: HomeKit KNX Bridge)
-f --file                   Set config file (Default: xknx.yaml)
-p --port                   Set port to listen (Default: 51826)
-u --updates                Enable XNKX device udpates
-h --help                   Print help
```
