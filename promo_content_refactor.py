import requests
import csv
import json
import teradata
import time
from bs4 import BeautifulSoup as BS


doc = "promo_html.html"
soup = BS(open(doc), 'html.parser')  # static file

# stage_uri = "https://www.stage.shutterfly.com/"
prod_uri = "https://www.shutterfly.com/"

response = requests.get(prod_uri)
soup = BS(response.text, 'html.parser')

# print(soup.prettify())
'''
[
  {'device': 'desktop', 'promo_location': 'desktop-offer-banner-1', 'offer_banner': 1, 'offer_code': 'SHIP39', 'offer_details': 'FREE SHIPPING', 'promo_start': '20-AUG-2018', 'promo_end': '21-AUG-2018', 'offer_url': 'https://www.shutterfly.com/promotions_details/#economy', 'offer_terms': 'really long text', 'offer_template': 'MASTER_TEMPLATE_001'},
  {'device': 'desktop', 'promo_location': 'desktop-offer-banner-2', 'offer_banner': 2, 'offer_code': 'SUMMERTIME', 'offer_details': '50% OFF HARDCOVER BOOKS, GIFTS, & HOME DECOR + 40% ALL ELSE* ', 'promo_start': '22-AUG-2018', 'promo_end': '22-AUG-2018', 'offer_url': 'https://www.shutterfly.com/promotions_details/#economy', 'offer_terms': 'long long text', 'offer_template': 'MASTER_TEMPLATE_002'}, 
  {'device': 'mobile', 'promo_location': 'mobile-offer-banner-1', 'offer_banner': 1, 'offer_code': 'SHIP39', 'offer_details': 'Free shipping on $39+', 'promo_start': '', 'promo_end': '', 'offer_url': 'https://www.shutterfly.com/special-offers', 'offer_terms': '', 'offer_template': ''}
]
'''

promo_master = list()  # master list to store promo json

device_type = ['desktop']  # desktop or mobile banner, add 'mobile later
# chang to device_type
# fetch available banner ids and load to list
banner_ids = list()
data = list()
data_tup = tuple()

for device in device_type:

    # clear out contents
    banner_ids.clear()  # clear list before picking next promo type
    ofr_template = ''
    ofr_terms = ''
    ofr_exp = ''
    ofr_start = ''
    ofr_code = ''
    ofr_details = ''
    ofr_url = ''

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

        for offer_code in soup.find_all('span',
                                        attrs={'id': str(device) + "-offer-code-" + str(x + 1), 'class': 'hidden'}):
            ofr_code = offer_code.text
            # print("offer code: %s" % ofr_code)

        for offer_start in soup.find_all('span', attrs={'id': str(device) + "-offer-start-" + str(x + 1)}):
            # if offer_start.text == '':
            #     ofr_start = '01-Jan-1900' # default null date to something
            # else:
            ofr_start = offer_start.text
            # print("offer start: %s" % ofr_start)

        for offer_exp in soup.find_all('span', attrs={'id': str(device) + "-offer-expiration-" + str(x + 1)}):
            # if offer_exp.text == '' or offer_exp.text  None:
            #     ofr_exp = '31-Dec-9999'
            # else:
            ofr_exp = offer_exp.text
            # print("offer expiration: %s" % ofr_exp)

        for offer_terms in soup.find_all('span', attrs={'id': str(device) + "-offer-terms-" + str(x + 1)}):
            ofr_terms = offer_terms.text
            # print("offer terms = %s" % ofr_terms)

        for offer_template in soup.find_all('span', attrs={'id': str(device) + "-offer-template-" + str(x + 1)}):
            ofr_template = offer_template.text

            # print("offer template = %s" % ofr_template)

            # print("---------------------\n")

        # promo_json = {"device": device, "promo_location": item, "promo_banner": ofr_banner, "promo_code": ofr_code,
        #               "promo_details": ofr_details, "promo_start": ofr_start, "promo_end": ofr_exp, "promo_url": ofr_url,
        #               "promo_terms": ofr_terms, "promo_template": ofr_template}
        # promo_master.append(promo_json)

        data_part = (device, item, ofr_banner, ofr_code, ofr_details,
                     ofr_start, ofr_exp, ofr_url, ofr_terms, ofr_template)
        data.append(data_part)
        data_tup = tuple(data)

'''
data_tup = (
            ('desktop', 'desktop-offer-banner-1', 1, 'SHIP39', 'FREE SHIPPING', '29-SEP-2018', '31-DEC-9999', 'https://www.shutterfly.com/promotions_details/#economy', 'Terms and conditions, really long text', '1'),
            ('desktop', 'desktop-offer-banner-2', 2, 'no code needed', '50% off Hardcover Photo Books Plus, 30-50% Off Everything Else*', '29-SEP-2018', '02-OCT-2018', 'https://www.shutterfly.com/promotions_details/#economy', 'Terms and conditions, really long text', '2'),
            ('mobile', 'mobile-offer-banner-1', 1, 'SHIP39', 'Free shipping on $39+', '', '', 'https://www.shutterfly.com/special-offers', '', '')
            )
'''

print(data_tup)
print("parsing completed")

# print(promo_master)

# Prep teradata insert

# insert_data = data_tup
dsn = 'TDDB'

udaExec = teradata.UdaExec(appName="tdPyInterface", version="1.0",
                           logConsole=False, appConfigFile="tdPyInterface.ini")

session = udaExec.connect(dsn)

# CRIPT_PROMO_STG
'''
CT CRMP.CRIPT_PROMO_STG (
DEVICE varchar(32), 
PROMO_LOCATION varchar(64), 
PROMO_BANNER integer, 
PROMO_CODE varchar(128), 
PROMO_DETAILS varchar(4000), 
PROMO_START DATE format 'dd-MMM-YYYY' DEFAULT CURRENT_DATE,
PROMO_END DATE format 'dd-MMM-YYYY' DEFAULT DATE '9999-01-01',
PROMO_DETAILS_URL varchar(1024), 
PROMO_TERMS varchar(4000), 
PROMO_TEMPLATE varchar(512), 
CREATED_DATE date DEFAULT CURRENT_DATE, 
MODIFIED_DATE date DEFAULT NULL, 
CREATED_BY VARCHAR(64) DEFAULT 'CRIPT_SCRAPER', 
MODIFIED_BY VARCHAR(64) DEFAULT 'CRIPT_SCRAPER'
);

CT CRMP.CRIPT_PROMO_STG (
DEVICE varchar(32), 
PROMO_LOCATION varchar(64), 
PROMO_BANNER integer, 
PROMO_CODE varchar(128), 
PROMO_DETAILS varchar(4000), 
PROMO_START VARCHAR(64),
PROMO_END VARCHAR(64) DEFAULT '9999-01-01',
PROMO_DETAILS_URL varchar(1024), 
PROMO_TERMS varchar(4000), 
PROMO_TEMPLATE varchar(512), 
CREATED_DATE date DEFAULT CURRENT_DATE, 
MODIFIED_DATE date DEFAULT NULL, 
CREATED_BY VARCHAR(64) DEFAULT 'CRIPT_SCRAPER', 
MODIFIED_BY VARCHAR(64) DEFAULT 'CRIPT_SCRAPER'
);

'''

print("Deleting CRMP.CRIPT_PROMO_STG")

del_stg = "delete CRMP.CRIPT_PROMO_STG"

cursor = session.execute(del_stg)

time.sleep(3)

ins_stg = """INSERT INTO CRMP.CRIPT_PROMO_STG (DEVICE, PROMO_LOCATION, PROMO_BANNER, PROMO_CODE, PROMO_DETAILS, 
                     PROMO_START, PROMO_END, PROMO_DETAILS_URL, PROMO_TERMS, PROMO_TEMPLATE) VALUES (?, ?, ?, ?, ?, ?,
                      ?, ?, ?, ?)"""

cursor = session.executemany(ins_stg, data_tup, batch=True)  # batch insert

# CRIPT_PROMO_MASTER
'''
CREATE SET TABLE CRMP.CRIPT_PROMO_MASTER ,NO FALLBACK ,
     NO BEFORE JOURNAL,
     NO AFTER JOURNAL,
     CHECKSUM = DEFAULT,
     DEFAULT MERGEBLOCKRATIO
     (
      ID INTEGER GENERATED ALWAYS AS IDENTITY
           (START WITH 1 
            INCREMENT BY 1 
            MINVALUE 1 
            MAXVALUE 2147483647 
            NO CYCLE),
      DEVICE VARCHAR(32) CHARACTER SET LATIN NOT CASESPECIFIC,
      PROMO_LOCATION VARCHAR(64) CHARACTER SET LATIN NOT CASESPECIFIC,
      PROMO_BANNER INTEGER,
      PROMO_CODE VARCHAR(128) CHARACTER SET LATIN NOT CASESPECIFIC,
      PROMO_DETAILS VARCHAR(4000) CHARACTER SET LATIN NOT CASESPECIFIC,
      PROMO_START VARCHAR(32) CHARACTER SET LATIN NOT CASESPECIFIC,
      PROMO_END VARCHAR(32) CHARACTER SET LATIN NOT CASESPECIFIC,
      PROMO_DETAILS_URL VARCHAR(1024) CHARACTER SET LATIN NOT CASESPECIFIC,
      PROMO_TERMS VARCHAR(4000) CHARACTER SET LATIN NOT CASESPECIFIC,
      PROMO_TEMPLATE VARCHAR(512) CHARACTER SET LATIN NOT CASESPECIFIC,
      CREATED_DATE DATE FORMAT 'YY/MM/DD' DEFAULT DATE ,
      MODIFIED_DATE DATE FORMAT 'YY/MM/DD',
      CREATED_BY VARCHAR(64) CHARACTER SET LATIN NOT CASESPECIFIC DEFAULT 'CRIPT_SCRAPER',
      MODIFIED_BY VARCHAR(64) CHARACTER SET LATIN NOT CASESPECIFIC DEFAULT 'CRIPT_SCRAPER')
PRIMARY INDEX ( PROMO_CODE );
'''

time.sleep(3)

print("Merging into CRMP.CRIPT_PROMO_MASTER ")

merge_master = """
MERGE INTO 
  CRMP.CRIPT_PROMO_MASTER AS TGT
USING
  (SELECT DEVICE, PROMO_LOCATION, PROMO_BANNER, PROMO_CODE, PROMO_DETAILS, PROMO_START, PROMO_END, PROMO_DETAILS_URL, PROMO_TERMS, PROMO_TEMPLATE, CREATED_DATE, MODIFIED_DATE
  FROM CRMP.CRIPT_PROMO_STG) AS SRC
ON
    ( 
        TGT.PROMO_CODE = SRC.PROMO_CODE 
        and  TGT.CREATED_DATE = SRC.CREATED_DATE
        and  TGT.DEVICE = SRC.DEVICE
    )
WHEN MATCHED THEN 
  UPDATE SET
  MODIFIED_DATE = CURRENT_TIMESTAMP
WHEN NOT MATCHED THEN
  INSERT
  (DEVICE, PROMO_LOCATION, PROMO_BANNER, PROMO_CODE, 
  PROMO_DETAILS, PROMO_START, PROMO_END, PROMO_DETAILS_URL, 
  PROMO_TERMS, PROMO_TEMPLATE)
  VALUES
  (SRC.DEVICE, SRC.PROMO_LOCATION, SRC.PROMO_BANNER, SRC.PROMO_CODE, 
  SRC.PROMO_DETAILS, SRC.PROMO_START, SRC.PROMO_END, SRC.PROMO_DETAILS_URL, 
  SRC.PROMO_TERMS, SRC.PROMO_TEMPLATE);
"""

cursor = session.execute(merge_master)

print("Merge into  CRMP.CRIPT_PROMO_MASTER complete.")

'''
# write json to file
with open('promo_data.json', 'w') as outfile:
    json.dump(promo_master, outfile)

f = open('promo_data.json')
data = json.load(f)
f.close()

f = csv.writer(open('promo_extract.csv', 'w+'))

# add header
f.writerow(['DEVICE'
               , 'PROMO_LOCATION'
               , 'PROMO_BANNER'
               , 'PROMO_CODE'
               , 'PROMO_DETAILS'
               , 'PROMO_START'
               , 'PROMO_END'
               , 'PROMO_DETAILS_URL'
               , 'PROMO_TERMS'
               , 'PROMO_TEMPLATE'
            ])

# add content
for item in data:
    f.writerow([item['device']
                   , item['promo_location']
                   , item['promo_banner']
                   , item['promo_code']
                   , item['promo_details']
                   , item['promo_start']
                   , item['promo_end']
                   , item['promo_url']
                   , item['promo_terms']
                   , item['promo_template']]
               )

# file produced at local
'''
