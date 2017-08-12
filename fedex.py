import requests
import json
from collections import OrderedDict
from datetime import datetime
import sys

tracking_number = int(input('Enter Fedex Tracking Id:'))

data = requests.post('https://www.fedex.com/trackingCal/track', data={
    'data': json.dumps({
        'TrackPackagesRequest': {
            'appType': 'wtrk',
            'uniqueKey': '',
            
            'trackingInfoList': [{
                'trackNumberInfo': {
                    'trackingNumber': tracking_number,
                    
                }
            }]
        }
    }),
    'action': 'trackpackages',
    'locale': 'en_US',
    'format': 'json',
    'version': 99
}).json()
i=0
for a in data['TrackPackagesResponse']['packageList'][0]['scanEventList']:
    if(a['status']==''):
        print("Invalid Tracking No.")
        sys.exit()
    if(i==0):
        status=a['status']
        scheduled_delivery=a['date']
        time=a['time']
    if(i==len(data['TrackPackagesResponse']['packageList'][0]['scanEventList'])-2):
        fedex=a['status']
        ship_date=a['date']
    i=i+1
time=time[:-3]
scheduled_delivery=scheduled_delivery.replace("-","")
scheduled_day=datetime.strptime(scheduled_delivery, '%Y%m%d').strftime('%a')
scheduled_delivery=datetime.strptime(scheduled_delivery, '%Y%m%d').strftime('%d/%m/%Y')

ship_date=ship_date.replace("-","")
ship_day=datetime.strptime(ship_date, '%Y%m%d').strftime('%a')
ship_date = datetime.strptime(ship_date, '%Y%m%d').strftime('%d/%m/%Y')

output=OrderedDict([("Tracking no",tracking_number), ("Ship date",ship_day +' '+ ship_date),("Status",status),("scheduled delivery",scheduled_day +' '+ scheduled_delivery +' '+time)])
output=json.dumps(output)
print(output)
