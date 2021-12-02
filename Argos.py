import requests
from bs4 import BeautifulSoup as bs
import time
import discord
from discord_webhook import *
import threading

webhookurl = 'https://discord.com/api/webhooks/711261122673508454/6v3PfdBjIR2BxjG-BkU_IbSdaK4vsGS3nlDRMbov7o9jHFwi_y8IFJxzI4yE5ev5pvPz'

TOKEN = 'NzExMjU2NjU4NTkyMTM3MjM3.XsAXYQ.RsuGF9pIAtU3dguVz7-EclQRy34'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.30 Safari/537.36'}
client = discord.Client()
threads = []
s = requests.Session()

@client.event
async def on_ready():

    thread1 = threading.Thread(target=Argos, kwargs=dict(profilex=0,s = requests.Session()) )           
    thread2 = threading.Thread(target=Argos, kwargs=dict(profilex=1,s = requests.Session()) )         
    thread3 = threading.Thread(target=Argos, kwargs=dict(profilex=2,s = requests.Session()) )         
    
    
    thread1.start()
    time.sleep(10)
    thread2.start()
    time.sleep(10)
    thread3.start()

def Argos(s, profilex):
    Reservable = False
    productinstock = 0
    url = "https://www.argos.ie/webapp/wcs/stores/servlet/ArgosComparison?storeId=10152&catalogId=15051&categoryId=&langId=111&returnToURL=%2Fwebapp%2Fwcs%2Fstores%2Fservlet%2FSearch%3FstoreId%3D10152%26catalogId%3D15051%26langId%3D111%26searchTerms%3DCONSOLE%26authToken%3D431580815%25252CD%25252B0VuoF7dBOzCy%25252F72sepWW9iiDU%25253D&compIds=1846030&compIds=1840514&compIds=1846026"

    result = s.get(url,headers=headers).text
    soup = bs(result, 'lxml')
    while 1:
        hm = soup.find('table').find_all('tr')[13].find_all('td')
        #print(hm[profilex+1].get('class')) #PS5 Disk
        #print(hm[profilex+2].get('class')) #Xbox Series X
        #print(hm[profilex+3].get('class')) #PS5 Digital
        if("buyOrReservable" in hm[profilex+1].get('class')):
            
            product_title = soup.find('table').find_all('tr')[4].find_all('th')[profilex].a.text
            print(product_title+ " is reservable")
            webhook = DiscordWebhook(url=webhookurl, username="Argos", avatar_url='https://www.retailgazette.co.uk/wp-content/uploads/argos-e1556533610610-696x428.jpg') 
            embed = DiscordEmbed(title = product_title, url = url, color=0x00ff08)
            embed.add_embed_field(name='Status', value='Reservable', inline=True)
            embed.set_timestamp()
            webhook.add_embed(embed)
            if(Reservable == False):
                webhook.execute()
            Reservable = True
            time.sleep(45)
        else:
            product_title = soup.find('table').find_all('tr')[4].find_all('th')[profilex].a.text
            print(product_title+ " is not reservable")
            webhook = DiscordWebhook(url=webhookurl, username="Argos", avatar_url='https://www.retailgazette.co.uk/wp-content/uploads/argos-e1556533610610-696x428.jpg') 
            embed = DiscordEmbed(title = product_title, url = url, color=0xf22e1f)
            embed.add_embed_field(name='Status', value='No longer Reservable', inline=True)
            embed.set_timestamp()
            webhook.add_embed(embed)
            if(Reservable == True):
                webhook.execute()
            Reservable = False
            time.sleep(45)





client.run(TOKEN)