import requests
import csv
import json
from bs4 import BeautifulSoup as BS

doc = "promo_html.html"
soup = BS(open(doc), 'html.parser')  # static file

# print(soup.prettify())
'''
[
{"promo_type": "desktop", "offer_banner": 1, "offer_url": "", "description":"", "offer_code": "SHIP39"},
{"promo_type": "desktop", "offer_banner": 2, "offer_url": "", "description":"", "offer_code": "SHIP40"},
{"promo_type": "mobile", "offer_banner": 1, "offer_url": "", "description":"", "offer_code": "SHIP39"},
{"promo_type": "mobile", "offer_banner": 2, "offer_url": "", "description":"", "offer_code": "SHIP40"}
]
'''

# promo_json = []
# promo_json_tmp = []

promo_type = ['desktop', 'mobile']  # desktop or mobile banner

# fetch available banner ids and load to list
banner_ids = list()

for promo in promo_type:

    for tag in soup.find_all(class_=str(promo)+'-offer-banner'):
        banner_ids.append(tag.get('id'))
# print(banner_ids)

    for x, item in enumerate(banner_ids):
        # for content in soup.find_all('div', attrs={'id': item}):
            # print(item)
            # pass

        for offer_url in soup.find_all('a', attrs={'id': str(promo)+"-offer-url-"+str(x+1)}):  # list indices start at 0
            # print("promo banner %s" %(x+1))
            print(str(promo)+" offer url "+str(x+1)+" : http://www.shutterfly.com%s" % offer_url['href'])
            # print(str(item)+" http://www.shutterfly.com"+offer_url['href'])
            # promo_json.append(offer_url['href'])
            pass

        for offer_details in soup.find_all('span', attrs={'id': str(promo)+"-offer-details-"+str(x+1)}):
            print(str(promo)+" offer details "+str(x+1)+": %s" % offer_details.text)
            # print(str(item)+" "+offer_details.text)
            # promo_json.append(offer_details.text)
            pass

        for offer_code in soup.find_all('span', attrs={'id': str(promo)+"-offer-code-"+str(x+1)}):
            print(str(promo)+" offer code "+str(x+1)+": %s" % offer_code.text.strip('Code :').strip('code :'))
            # print(str(item)+" "+offer_code.text.strip('Code :').strip('code :'))
            # promo_json.append(offer_code.text.strip('Code: '))
            pass
            print("---------------------\n")








