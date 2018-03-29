from PageDecoder import *
from StockClass import *
from PushMessage import *
import time


my_interest = ['000651','600660','600887','600377','601012']
for interest in my_interest:
    data = GetTotalData(interest)
    istock = stock()
    istock.SetData(data)
    str1 = interest + '.CurPrice = ' + str(istock.CurPrice)
    print(str1)
    push(str1)
    time.sleep(1)
