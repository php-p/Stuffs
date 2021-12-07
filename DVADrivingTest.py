import re
import time
import requests
from twilio.rest import Client
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import smtplib
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

ref = '' #Enter your previous booking number
driver = '' #Enter driving license number
dob = '' #yyyy-mm-dd
s = requests.session()
datenew=None
counter = 0


def gettoken():
    while True:
        try:
            url = 'https://dva-bookings.nidirect.gov.uk/MyBookings/FindDriver'
            page = s.get(url, verify=False).text
            token = re.findall(r'__RequestVerificationToken" type="hidden" value="(.*?)"', page)[0]
            if len(token) > 0:
                return str(token)
        except:
            continue


def smtp_gmail(date):
    username = ""
    password = ""
    smtp_server = "smtp.gmail.com:587"
    email_from = ""
    email_to = ""
    email_body = str(date)
    server = smtplib.SMTP(smtp_server)
    server.starttls()
    server.login(username, password)
    server.sendmail(email_from, email_to, email_body)
    server.quit()


def text(date):
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body='Next Date for Newry is ' + str(date) + " " + "https://dva-bookings.nidirect.gov.uk/MyBookings/FindDriver",
        from_='',
        to=''
    )


def check():
    time.sleep(45)
    url = 'https://dva-bookings.nidirect.gov.uk/MyBookings/FindDriver'
    data = {"BookingReference": ref, "DriverNo": driver, 'DateOfBirth': dob, '__RequestVerificationToken': gettoken()}
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"}
    s.post(url, headers=headers, data=data, verify=False, allow_redirects=True)
    response1 = s.get('https://dva-bookings.nidirect.gov.uk/MyBookings/Change/Driver', verify=False, allow_redirects=True)
    text1 = response1.text
    try:
        global counter
        counter += 1
        date = re.findall(r'<option data-subtext="(.*?)" data-firstavailable=".*?" value=".*?">NEWRY</option>',text1)[0] #Change newry to your local center, CAPS REQURIED
        global datenew
        if date == datenew:
            print("Still same date - ", date)
        elif '2022' in date:
            print('Only Dates for 2022')
        else:
            text(date)
            smtp_gmail(date)
            print("WE FOUND A DATE FOR NEWRY! ", date)
            time.sleep(30)
        datenew = date
    except:
        print("No dates yet")
        #print(data['__RequestVerificationToken'])



while True:
    check()
#print(gettoken())

