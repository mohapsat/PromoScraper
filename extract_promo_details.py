import requests
import csv
import json
from bs4 import BeautifulSoup

url = "https://www.shutterfly.com/promotions_details/?esch=1#crm"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

promo_codes = []

headlines = soup.find_all('div', attrs={'class':'headline'})

promo_descriptions = []

for promoTxt in soup.find_all('div',attrs={'class':'promoTxt'}):
    promo_cd = promoTxt.find('span')
    if promo_cd is None: # handle null promo codes
        # promo_cd.text = 'Not Provided'
        # promo_codes_list.append(promo_cd.text)
        continue
    else:
        # print(promo_cd.text)
        promo_codes.append(promo_cd.text)

    description = promoTxt.find('p')
    if description is None:
        continue
    else:
        promo_descriptions.append(description.text)


discalimers = soup.find_all('div', attrs={'class':'disclaimer'})


final_json_tmp = {}
final_json = []

for promo_code in promo_codes:
    for headline in headlines:
        for description in promo_descriptions:
            for disclaimer in discalimers:
                final_json_tmp.update({ "promo_code": promo_code
                                      ,"headline": headline.text
                                      ,"description": description
                                      ,"disclaimer": disclaimer.text})
                final_json.append(final_json_tmp.copy())


# final_json = [{"promo_code":"hello","headline":1},{"promo_code":"No","headline":4}]
# write json to file
with open('promo_data.json', 'w') as outfile:
    json.dump(final_json, outfile)

f = open('promo_data.json')
data = json.load(f)
f.close()

f = csv.writer(open('promo_extract.csv','w+'))

# add header
f.writerow(['PROMO_CODE'
               ,'HEADLINE'
               ,'DESCRIPTION'
               ,'DISCLAIMER'
            ])

# add content
for item in data:
    f.writerow([item['promo_code'],item['headline'],item['description'],item['disclaimer']])