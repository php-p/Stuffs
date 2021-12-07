import smtplib
import requests
import json
import re

#edit smtp function as needed. Recommended to use NSSM (Non sucking service manager), add python script as a service + sleep command for 1 day etc or create scheduled task to run as required


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


def getgainers():
    string=""
    reply=requests.get('https://coinmarketcap.com/gainers-losers/').text
    dict1=re.findall(r'"gainersLosers":(.*?),"trendingCoins":',reply)[0]
    dict1=json.loads(dict1)
    for x in range(11):
        string+=dict1['gainers'][x]['name']
        string += '-'
        string += (format(dict1['gainers'][x]['priceChange']['price'],'.6f'))
        string += '\n'
    return string


smtp_gmail(getgainers())
