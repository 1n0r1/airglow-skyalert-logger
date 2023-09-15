import requests
from time import sleep
from datetime import datetime

from powercontrol import PowerControl
from get_IP import get_IP_from_MAC
from config import config

## JJM: MIGHT WANT THIS TO BE COMMAND LINE INPUTS
#address='http://192.168.1.126:81'
skyAlertMAC = config['skyAlertMAC']
logfolder = './skyalert-logs/'
logfolder = '/home/airglow/airglow/skyalert-logger/skyalert-logs/'
site = config['site']
index = 0

powerControl = PowerControl(config['powerSwitchAddress'], config['powerSwitchUser'], config['powerSwitchPassword'])
    
# get the SkyAlert IP address from the MAC address using ARP
SkyAlert_IP = get_IP_from_MAC(skyAlertMAC)
if SkyAlert_IP is None:
    # Try rebooting
    print("Cannot find skyalert; rebooting")
    powerControl.turnOff(config['CloudSensorPowerPort'])
    sleep(5)
    powerControl.turnOn(config['CloudSensorPowerPort'])
    sleep(60)
    SkyAlert_IP = get_IP_from_MAC(config['skyAlertMAC'])
    if SkyAlert_IP is not None:
        address = 'http://' + SkyAlert_IP + ':81'
        print('Found SkyAlert at %s' % SkyAlert_IP)
    else:
        print('Could not find SkyAlert after power cycle')
else:
    address = 'http://' + SkyAlert_IP + ':81'
    print("Found SkyAlert on " + address)

while 1:
    count = 5
    while count != 0:
        try:
            arr = requests.post(url=address, timeout=10).text.strip()  
            count = 0
        except:
            count = count - 1
            if count == 0:
                print("failed to connect to skyalert")

                # Try to find the SkyAlert (maybe add reboot capability?
                print("Trying to find the IP of skyalert")
                SkyAlert_IP = get_IP_from_MAC(skyAlertMAC)
                if SkyAlert_IP is None:
                    # Try rebooting
                    print("Cannot find skyalert; rebooting")
                    powerControl.turnOff(config['CloudSensorPowerPort'])
                    sleep(5)
                    powerControl.turnOn(config['CloudSensorPowerPort'])
                    sleep(60)
                    SkyAlert_IP = get_IP_from_MAC(config['skyAlertMAC'])
                    if SkyAlert_IP is not None:
                        address = 'http://' + SkyAlert_IP + ':81'
                        print('Found SkyAlert at %s' % SkyAlert_IP)
                    else:
                        print('Could not find SkyAlert after power cycle')
                else:
                    address = 'http://' + SkyAlert_IP + ':81'
                    print("Found skyalert on " + address)
            sleep(5)

    print(arr)
    now = datetime.now()
    with open(logfolder + 'Cloud_%s_' % site.lower() + now.strftime('%Y%m%d.txt'), 'a+') as f:
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{timestamp} {arr}\n')
    sleep(20)

