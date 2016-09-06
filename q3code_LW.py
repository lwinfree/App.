# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 10:51:27 2016

@author: lillywinfree
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 12:24:02 2016

@author: lillywinfree
"""
#! usr/bin/env python3
from twitter import *
import sys
import csv
#set geo location, radius 5 km
latitude = 45.5
longitude = -122.67
max_range = 5
num_results = 700
outfile = "geoTweets2.csv"

#API creds
config= {}
exec(open("config.py").read(), config)

#create Twitter API object
twitter = Twitter(
        auth=OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))
    
#create CSV
csvfile=open(outfile, "w")
csvwriter=csv.writer(csvfile)
#add headers
row = ["user", "text", "latitude", "longitude"]
csvwriter.writerow(row)

#break up search into 10 pages of 100 tweets
result_count=0
last_id=None
while result_count < num_results:
    #perform our geo search
    query = twitter.search.tweets(q = "beer", geocode = "%f,%f,%dkm" % (latitude, longitude, max_range), count = 100, max_id = last_id)
    for result in query["statuses"]:
        if result["geo"]:    #only use results that have geolocation
            user = result["user"]["screen_name"]
            text = result["text"]
            text = text.encode('ascii', 'replace')
            latitude = result["geo"]["coordinates"][0]
            longitude = result["geo"]["coordinates"][1]
            #write to CSV file
            row = [ user, text, latitude, longitude ]
            csvwriter.writerow(row)
            result_count += 1
        last_id = result["id"]
    print("got %d results" % result_count) 
    #keep me posted about count
    
#close csv file
csvfile.close()

print("writen to %s" % outfile) 

import numpy as np
import pandas as pd
#read in data
data=pd.read_csv('geoTweets2.csv')
data.head()
data.columns
data['user'].count()
#will plot user tweet count as plot1
dataUC=data.groupby('user').agg([np.size])
dataUC=dataUC['text']['size']
dataUC=pd.DataFrame(dataUC)
dataUC_sorted = dataUC.sort_values(['size'], ascending=False)
#separate lat data
np.random.seed(1)
data['neighborhoodsNS']=pd.cut(data['latitude'], bins=[45.44, 45.53, 45.63], labels=False)
labels = np.array('South North'.split())
data['neighborhoodsNS']=labels[data['neighborhoodsNS']]
# long data
data.columnsnp.random.seed(1)
data['neighborhoodsECW']=pd.cut(data['abs_longitude'], bins=[122.50, 122.66, 122.68, 122.737], labels=False)
labels = np.array('East Central West'.split())
data['neighborhoodsECW']=labels[data['neighborhoodsECW']]
data.columns
data['neighborhoods']=data.neighborhoodsNS+data.neighborhoodsECW
data.head()

#get housing price data from Trulia website
import requests, bs4
res=requests.get('http://www.trulia.com/home_prices/Oregon/Portland-heat_map/')
type(res)
try:
    res.raise_for_status()
except Exception as exc:
    print('There is a problem: %s' % (exc))

price=bs4.BeautifulSoup(res.text)
type(price)

price1=price.select('td')
str(price1[174])
se=price1[174].getText()
se=se.strip('$')
se=se.replace(',','')
int(se)
cn=price1[204].getText() #use cn for pearl district
cn=cn.strip('$')
cn=cn.replace(',','')
int(cn)
nw=price1[284].getText()
nw=nw.strip('$')
nw=nw.replace(',','')
int(nw)
sw=price1[294].getText()
sw=sw.strip('$')
sw=sw.replace(',','')
int(sw)
sc=price1[434].getText()  #use sc for downtown
sc=sc.strip('$')
sc=sc.replace(',','')
int(sc)
ne=price1[94].getText()
ne=ne.strip('$')
ne=ne.replace(',','')
int(ne)

priceData=({'neighborhoods': pd.Series(['NorthCentral','NorthEast','NorthWest','SouthCentral','SouthEast','SouthWest'], index=['0','1','2','3','4','5']),
'price' : pd.Series([cn, ne, nw, sc, se, sw], index=['0','1','2','3','4','5'], dtype=int)})

#get num of texts mentioning beer per neighborhood
textNum=data.groupby('neighborhoods').agg({'text':[np.size]})
textNum
numCN=textNum['text']['size'][0]
numNE=textNum['text']['size'][1]
numNW=textNum['text']['size'][2]
numSC=textNum['text']['size'][3]
numSE=textNum['text']['size'][4]
numSW=textNum['text']['size'][5]
beerCount=numCN, numNE, numNW, numSC, numSE, numSW
priceData['beerCount']=beerCount
#portland average price and beerCount
priceData.describe()
meanPrice=priceData['price'].mean()
priceData['meanPrice']=meanPrice

#plot time
import matplotlib.pylab as plt

p1=dataUC_sorted.plot.bar(figsize=(20,20))
p1.set_xlabel('Users')
p1.set_ylabel('Tweet count')

p2=data.plot.scatter(x='abs_longitude', y='latitude', legend=False, title='Beer drinking tweets map', rot=25, color='blue')
p2.set_xlabel('Longitude')
p2.set_ylabel('Latitude')

p3=priceData.plot.bar(x='neighborhoods', y='beerCount', color=['grey', 'pink', 'yellow', 'blue', 'green', 'black'], legend=False, title='Beer drinking vs Neighborhood', rot=25)
p3.set_ylabel('Beer Count')
p3.set_xlabel('Neighborhoods')

p4=priceData.plot.bar(x='neighborhoods', y='price', color=['grey', 'pink', 'yellow', 'blue', 'green', 'black'], legend=False, title='House Prices per Neighborhood', rot=25)
p4.set_ylabel('Price')
p4.set_xlabel('Neighborhoods')