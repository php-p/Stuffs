import re
import requests
import smtplib
from datetime import datetime

timenow=datetime.now(tz=None)
alreadysent=[]
emails=['yourmeail@gmail.com']



def smtp_gmail(text1):
    username = "" #gmail address
    password = "" #add gmail application password
    smtp_server = "smtp.gmail.com:587"
    email_from = "" #your gmail address
    email_to = "" #assuming your email
    email_body = 'Subject: {}\n\n{}'.format('Top 10 Cryptos!', text1)
    server = smtplib.SMTP(smtp_server)
    server.starttls()
    server.login(username, password)
    server.sendmail(email_from, email_to, email_body)
    server.quit()


def newlist():
    reply=requests.get('https://coinmarketcap.com/new/').text
    name=re.findall(r'"sc-1eb5slv-0 iworPT">(.*?)</p><div',reply)[:7]
    added=re.findall(r'(\d*?)( day | hours | minutes )ago',reply)[:7]
    links=re.findall(r'a href="/currencies/(.*?)/',reply)[:7]
    added=[x[0] + x[1] for x in added]
    price=re.findall(r'style="text-align:right"><span>(.*?)</span></td><td style="text-a',reply)[:7]
    combined=zip(name,added,links,price)
    for x in combined:
        if x[0] not in alreadysent:
            if 'minutes' in x[1]:
                replynew = requests.get('https://coinmarketcap.com/currencies/' + x[2]).text
                try:
                    contractplatform = re.findall(r'"contractPlatform":"(.*?)"', replynew)[0]
                    contract = re.findall(r'"contractAddress":"(.*?)"', replynew)[0]
                    message = "New Crypto - " + str(x[0]) + " - $" + format(float(x[3][1:]), '.8f') + " - " + str(contractplatform) + " - " + str(contract) + " - " + str('coinmarketcap.com/currencies/' + x[2])
                    alreadysent.append(x[0])
                    print(message)
                    smtp_gmail(message)
                except:
                    message = "New Crypto - " + str(x[0]) + " - $" + format(float(x[3][1:]), '.8f') + " - " + "currently no contract, keep checking" + " - " + str('coinmarketcap.com/currencies/' + x[2])
                    alreadysent.append(x[0])
                    print(message)
                    continue


while True:
    newlist()


