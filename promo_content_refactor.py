import requests
import csv
import json
from bs4 import BeautifulSoup as BS

doc = "promo_html.html"
soup = BS(open(doc), 'html.parser')  # static file

# print(soup.prettify())
'''
[
    {"device": "desktop", "offer_banner": 1, "offer_url": "", "description":"", "offer_code": "SHIP39"},
    {"device": "desktop", "offer_banner": 2, "offer_url": "", "description":"", "offer_code": "SHIP40"},
    {"device": "mobile", "offer_banner": 1, "offer_url": "", "description":"", "offer_code": "SHIP39"},
    {"device": "mobile", "offer_banner": 2, "offer_url": "", "description":"", "offer_code": "SHIP40"}
]
'''

promo_master = list()  # master list to store promo json

device_type = ['desktop', 'mobile']  # desktop or mobile banner
# chang to device_type
# fetch available banner ids and load to list
banner_ids = list()

for device in device_type:

    # print("promo = %s" % promo)
    banner_ids.clear()  # clear list before picking next promo type

    for tag in soup.find_all(class_=str(device) + '-offer-banner'):
        # print("id = %s" % tag.get('id'))
        banner_ids.append(tag.get('id'))

    for x, item in enumerate(banner_ids):
        # for content in soup.find_all('div', attrs={'id': item}):
        # print(item)
        # pass
        ofr_banner = x + 1
        # print("promo = %s" % device)
        # print("x = %d" % x)
        # print("item = %s"% item)
        # print("banner_ids = %s"% banner_ids)

        for offer_url in soup.find_all('a', attrs={
            'id': str(device) + "-offer-url-" + str(x + 1)}):  # list indices start at 0
            # print("promo banner %s" %(x+1))
            ofr_url = "https://www.shutterfly.com" + offer_url['href']
            # print(str(device) + " offer url " + str(x + 1) + " : "+ofr_url)
            # print(str(item)+" http://www.shutterfly.com"+offer_url['href'])
            # promo_json.append(offer_url['href'])
            pass

        for offer_details in soup.find_all('span', attrs={'id': str(device) + "-offer-details-" + str(x + 1)}):
            ofr_details = offer_details.text
            # print(str(device) + " offer details " + str(x + 1) + ": %s" % offer_details.text)
            # print(str(item)+" "+offer_details.text)
            # promo_json.append(offer_details.text)
            pass

        for offer_code in soup.find_all('span', attrs={'id': str(device) + "-offer-code-" + str(x + 1)}):
            ofr_code = offer_code.text.strip('Code :').strip('code :')
            # print(str(device) + " offer code " + str(x + 1) + ": %s" % offer_code.text.strip('Code :').strip('code :'))
            # print(str(item)+" "+offer_code.text.strip('Code :').strip('code :'))
            # promo_json.append(offer_code.text.strip('Code: '))
            pass
            # print("---------------------\n")

        promo_json = {"device": device, "offer_banner": ofr_banner, "offer_url": ofr_url, "offer_code": ofr_code,
                      "offer_details": ofr_details}
        promo_master.append(promo_json)

# print(promo_master)

# write json to file
with open('promo_data.json', 'w') as outfile:
    json.dump(promo_master, outfile)

f = open('promo_data.json')
data = json.load(f)
f.close()

f = csv.writer(open('promo_extract.csv', 'w+'))

# add header
f.writerow(['DEVICE'
               , 'OFFER_BANNER'
               , 'OFFER_URL'
               , 'OFFER_CODE'
               , 'OFFER_DETAILS'
            ])

# add content
for item in data:
    f.writerow([item['device']
                   , item['offer_banner']
                   , item['offer_url']
                   , item['offer_code']
                   , item['offer_details']]
               )

# file produced at local
