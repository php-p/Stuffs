import re
import requests
from prettytable import PrettyTable
from termcolor import colored
import collections
from datetime import datetime

starttime=datetime.now(tz=None)
dictmain=collections.defaultdict(list)
top10old=[]


def conversion():
  base='https://www.xe.com/currencyconverter/convert/?Amount=1&From=GBP&To=USD'
  get=requests.get(base).text
  usdtogbp=float(re.findall(r'lass="result__BigRate-sc-1bsijpp-1 iGrAod">(.*?)<span',get)[0])
  return  usdtogbp


def tops():
  top10current = []
  top10new = []
  global top10old
  url = 'https://coinmarketcap.com/gainers-losers/'
  x=requests.get(url).text
  y=re.findall(r'sc-1eb5slv-0 iworPT">(.*?)<',x)[:15]
  price=re.findall(r'right"><span>(.*?)<',x)[:15]
  percent=re.findall(r'span class="icon-Caret-up"></span>(.*?)<',x)[:15]
  link=re.findall(r'a href="(/currencies/.*?/)',x)[:15]
  z=zip(y,price,percent,link)
  t = PrettyTable(['Crypto (24hr)', 'Price', 'Increase %', 'Link', 'Contract', 'Status', 'Increase from-' + str(starttime)[10:16]])
  for x in list(z):
    price=str(x[1])
    if ',' in price:
      price =str(x[1]).replace(',','')
    top10current.append(x[0])
    if x[0] in top10old:
      reply = requests.get('https://coinmarketcap.com' + x[3]).text
      try:
        contract = re.findall(r'"contractAddress":"(.*?)"', reply)[0]
      except:
        contract='No Contract'
      try:
        Platform = re.findall(r'"contractPlatform":"(.*?)"', reply)[0]
      except:
        Platform='No Contract'
      t.add_row([colored(x[0],'red'), colored(format(float(price[1:]) / conversion(),'.10f'),'red'),colored(x[2],'red'),'https://coinmarketcap.com' + x[3], colored(Platform,'red') + ' ' + colored(contract,'red'), colored('old','red'),str(build_dict(x)) + '%'])
    else:
      reply = requests.get('https://coinmarketcap.com' + x[3]).text
      try:
        contract = re.findall(r'"contractAddress":"(.*?)"', reply)[0]
      except:
        contract = 'No Contract'
      try:
        Platform = re.findall(r'"contractPlatform":"(.*?)"', reply)[0]
      except:
        Platform='No Contract'
      t.add_row([colored(x[0],'green'), colored(format(float(price[1:]) / conversion(),'.10f'),'green'),colored(x[2],'green'),colored(('https://coinmarketcap.com' + x[3]),'green'), colored(Platform,'green') + ' ' + colored(contract,'green'), colored('***NEW***','green'),str(build_dict(x))+'%'])
      top10new.append(x)
  print(t)
  top10old = top10current.copy()
  newlist=zip(y,price,percent,link)
  return list(newlist)


def build_dict(input):
    name=input[0]
    price=input[1][1:]
    dictmain[name]+=[price]
    try:
      first = dictmain[name][:1][0]
      last = dictmain[name][-2::][1:2:][0]
      return diff(first,last)
    except:
      return None


def diff(one,two):
  try:
    xy = round(((float(two) - float(one)) / float(one)) * 100, 5)
    return format(xy, '.4f')
  except ZeroDivisionError:
    return '0%'
  except:
    return None


#Below isfor possible future developments, with multiproccesing, allows user to add crypto trades into the prorams and tickers to monitor

# def keyin():
#   keyinput=input('What to do? \n')
#   if 'buy' not in keyinput:
#     print('Regenerating Table')
#     pass
#   else:
#     addbuy(watchlist(keyinput))
#
#
# def watchlist(key1):
#   listthing=key1.split(',')
#   coin=listthing[1].strip()
#   amount=listthing[2].strip()
#   cake=listthing[3].strip()
#   return coin,amount,cake

#
# def addbuy(LOADS):
#   url = LOADS[0]
#   x=requests.get(url).text
#   name=re.findall(r',"name":"(.*?)","currency":',x)[0]
#   price=float(re.findall(r'"price":(.*?),"priceCurrency"',x)[0]) / conversion()
#   cake=getcake()
#   PRICEBUY = format(cake/float(LOADS[1]),'.8f')
#   t = PrettyTable(['Crypto', 'Amount', 'Price Bought', 'Price Now', '% Change', 'Value Change','Link',])
#   t.add_row([colored(name, 'yellow'), colored(LOADS[1], 'yellow'), colored(PRICEBUY, 'yellow'), colored(format(price,'.8f'), 'yellow'), colored(diff(PRICEBUY,price), 'yellow') , colored(format((float(price)-float(PRICEBUY)) * int(LOADS[1]), '.8f'), 'yellow'), colored(url, 'yellow')])
#   print(t)


# def getcake():
#   base='https://www.coingecko.com/en/coins/pancakeswap/gbp'
#   get=requests.get(base).text
#   price=re.findall(r'price.price">£(.*?)</span>',get)[0]
#   return float(price)
#
#



while True:
  tops()


