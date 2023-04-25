import requests
from time import sleep
from datetime import datetime

## JJM: MIGHT WANT THIS TO BE COMMAND LINE INPUTS
address='http://192.168.1.2:81'
logfolder = './skyalert-logs/'
logfolder = '/home/airglow/airglow/skyalert-logger/skyalert-logs/'
site = 'uao'
index = 0
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
            sleep(5)

    print(arr)
    now = datetime.now()
    with open(logfolder + 'Cloud_%s_' % site + now.strftime('%Y%m%d.txt'), 'a+') as f:
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{timestamp} {arr}\n')
    sleep(20)

