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

`-h`  Help  
`-n --name` Bridge name  
`-f --file` Set config file
