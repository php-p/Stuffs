import re
import time
import requests
from twilio.rest import Client
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

property_count=0


def text(messagetext):
    account_sid = '' #Get from twilio api account
    auth_token = '' #Get from twilio api account
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=messagetext,
        from_='', #Get from twilio api account
        to=''
    )


def rostrevor():
    for i in range(1440):
        base = 'https://www.propertypal.com/property-to-rent/rostrevor'
        headers={
                 'Cookie': 'bt=ecf46a01-297d-4dbb-83a1-cbadfd05a2cc.65bf6139-629b-4991-b687-3060898e88c7..17d4c61e3fd.8039e1dadaaf97a2faec8af5e21eb4d80354ee56; Expires=Thu, 01-Jan-1970 00:00:10 GMT, bt=ecf46a01-297d-4dbb-83a1-cbadfd05a2cc.65bf6139-629b-4991-b687-3060898e88c7..17d4c61e3fd.8039e1dadaaf97a2faec8af5e21eb4d80354ee56; Expires=Sun, 22-Nov-2026 10:40:23 GMT; Path=/, pp.geo=MmEwMDoyM2M0OmY5OTc6YzYwMToyYzg2OmNhYTg6NjE3YzozZTIxLUdCUi1HQlA; Version=1; Comment="Location data"; Max-Age=259200; Expires=Fri, 26-Nov-2021 10:40:23 GMT; Path=/, JSESSIONID=9649181C22C176DDE5DC153D0C18EDD8; Path=/; Secure; HttpOnly',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
                 'Referer': 'https://www.propertypal.com/'
                                                            }
        x=requests.get(base,headers=headers)
        global property_count
        num=int(re.findall(r'PropertyPal Lists (.*?) Results For Property To Rent in Rostrevor,',x.text)[0])
        if num != property_count:
            property_count=num
            text('Propertypal has ' + str(num) + " " + "properties for rostrevor")
        time.sleep(58)
    text('Script is still running')




while True:
    rostrevor()



