# -*- coding: utf-8 -*-
"""
Created on Fri Apr 07 15:21:40 2017
os.walk Reference - http://stackoverflow.com/questions/5817209/browse-files-and-subfolders-in-python
lxml scraping - http://python-guide-pt-br.readthedocs.io/en/latest/scenarios/scrape/
@author: Anish
"""
#import all necessary modules
import datetime
from lxml import html
import os
import pandas as pd

#Set the path for data files
path = 'data\\'

timedict = {}
tempios = {}

today = []
count = 0

#Walk through files in folders
for root, dirs, files in os.walk(path):
    for fname in files:
        
        count+=1
        osdict = {}
        dt = os.path.join(root,fname).split('\\')
        
        #Get the date and time from folder, file names
        date = dt[1].split('-')
        year = int(date[0])
        month = int(date[1])
        day = int(date[2])
        time = dt[2].split('_')
        hour = int(time[0])
        minute = int(time[1])
        
        #Create datetime object
        dto = datetime.datetime(year,month,day,hour,minute,0)
        try:
            
            #Scrape and store iOS values
            if 'ios' in fname:
                src_path = (os.path.join(root, fname))
                with open(src_path,'r') as f:
                    page = f.read()
                tree = html.fromstring(page)
                ios_file_size = tree.xpath('//*[@id="left-stack"]/div[1]/ul/li[5]/text()')
                osdict['ios_file_size'] = int(ios_file_size[0].split('M')[0].strip())
                ios_current_ratings = tree.xpath('//*[@id="left-stack"]/div[2]/div[2]/span[2]/text()')
                osdict['ios_current_ratings'] = int(ios_current_ratings[0].split()[0].strip())
                ios_all_ratings = tree.xpath('//*[@id="left-stack"]/div[2]/div[4]/span/text()')
                osdict['ios_all_ratings'] = int(ios_all_ratings[0].split()[0].strip())
                
            #Scrape and store android values
            if 'android' in fname:
                src_path = (os.path.join(root, fname))
                with open(src_path,'r') as f:
                    page = f.read()
                tree = html.fromstring(page)
                android_avg_rating = tree.xpath('//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div[1]/div[1]/text()')
                osdict['android_avg_rating'] = float(android_avg_rating[0])
                android_total_ratings = tree.xpath('//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div[1]/div[3]/span[2]/text()')
                osdict['android_total_ratings'] = int(android_total_ratings[0].replace(',',''))
                android_file_size = tree.xpath('//*[@id="body-content"]/div/div/div[1]/div[4]/div/div[2]/div[2]/div[2]/text()')
                osdict['android_file_size'] = int(android_file_size[0].split('M')[0].strip())
                android_ratings_5 = tree.xpath('//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div[2]/div[1]/span[3]/text()')
                osdict['android_ratings_5'] = int(android_ratings_5[0].replace(',',''))
                android_ratings_4 = tree.xpath('//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div[2]/div[2]/span[3]/text()')
                osdict['android_ratings_4'] = int(android_ratings_4[0].replace(',',''))
                android_ratings_3 = tree.xpath('//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div[2]/div[3]/span[3]/text()')
                osdict['android_ratings_3'] = int(android_ratings_3[0].replace(',',''))
                android_ratings_2 = tree.xpath('//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div[2]/div[4]/span[3]/text()')
                osdict['android_ratings_2'] = int(android_ratings_2[0].replace(',',''))
                android_ratings_1 = tree.xpath('//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div[2]/div[5]/span[3]/text()')
                osdict['android_ratings_1'] = int(android_ratings_1[0].replace(',',''))
                
        except:
                continue
        if dto not in timedict:
            timedict[dto] = osdict
        else:
            timedict[dto].update(osdict)
        print count

#transform the the dictionary into dataframe
df = pd.DataFrame.from_dict(timedict, orient='index')

#Save files in various formats
df.to_json(path_or_buf="data.json",orient='index',date_format='iso')
df.to_csv(path_or_buf="data.csv")
df.to_excel(excel_writer="data.xlsx")
#print timedict