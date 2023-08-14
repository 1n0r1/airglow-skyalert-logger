import requests
from time import sleep
from datetime import datetime

from get_IP import get_IP_from_MAC

## JJM: MIGHT WANT THIS TO BE COMMAND LINE INPUTS
#address='http://192.168.1.23:81'
skyAlertMAC = '2c:f7:f1:b8:10:73'
logfolder = './skyalert-logs/'
logfolder = '/home/airglow/airglow/skyalert-logger/skyalert-logs/'
site = 'blo'
index = 0

# get the SkyAlert IP address from the MAC address using ARP
SkyAlert_IP = get_IP_from_MAC(skyAlertMAC)
address = 'http://' + SkyAlert_IP + ':81'
print("Found skyalert on " + address)

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
                address = 'http://' + SkyAlert_IP + ':81'
                print("Found skyalert on " + address)
            sleep(5)

    print(arr)
    now = datetime.now()
    with open(logfolder + 'Cloud_%s_' % site + now.strftime('%Y%m%d.txt'), 'a+') as f:
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{timestamp} {arr}\n')
    sleep(20)

