# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 11:46:06 2017
urlretrieve - http://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python
@author: Anish
"""
#import all necessary modules
import os
from lxml import html
import urllib

#set path and initiate various variables
path = 'data\\'
uimgs = set()
uaimgs = set()

#walk through files and extract image links for iOS
for root, dirs, files in os.walk(path):
    for fname in files:
        if 'ios' in fname:
            src_path = (os.path.join(root, fname))
            with open(src_path,'r') as f:
                page = f.read()
            tree = html.fromstring(page)
            uimgs.update(tree.xpath('//*[@id="content"]/div/div[2]/div[4]/div[2]/div[1]/div/div[1]/img/@src'))
            uimgs.update(tree.xpath('//*[@id="content"]/div/div[2]/div[4]/div[2]/div[1]/div/div[2]/img/@src'))
            uimgs.update(tree.xpath('//*[@id="content"]/div/div[2]/div[4]/div[2]/div[1]/div/div[3]/img/@src'))
            uimgs.update(tree.xpath('//*[@id="content"]/div/div[2]/div[4]/div[2]/div[1]/div/div[4]/img/@src'))
            uimgs.update(tree.xpath('//*[@id="content"]/div/div[2]/div[4]/div[2]/div[1]/div/div[5]/img/@src'))
            uimgs.update(tree.xpath('//*[@id="content"]/div/div[2]/div[4]/div[2]/div[2]/div/div[1]/img/@src'))
            uimgs.update(tree.xpath('//*[@id="content"]/div/div[2]/div[4]/div[2]/div[2]/div/div[2]/img/@src'))

#walk through files and extract image links for Android
for root, dirs, files in os.walk(path):
    for fname in files:
        try:
            if 'android' in fname:
                src_path = (os.path.join(root, fname))
                with open(src_path,'r') as f:
                    page = f.read()
                tree = html.fromstring(page)
                uaimgs.update(tree.xpath('//*[@id="body-content"]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div/img[1]/@src'))
                uaimgs.update(tree.xpath('//*[@id="body-content"]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div/img[2]/@src'))
                uaimgs.update(tree.xpath('//*[@id="body-content"]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div/img[3]/@src'))
                uaimgs.update(tree.xpath('//*[@id="body-content"]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div/img[4]/@src'))
                uaimgs.update(tree.xpath('//*[@id="body-content"]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div/img[5]/@src'))
        except:
            print ("Error at",src_path)
            continue

#Using the extracted links, retrieve the images and store them in folders
cwd = os.getcwd()
count = 0
nwd = os.getcwd()+r'\android'
if not os.path.exists(nwd):
    os.makedirs('android_images')
os.chdir(nwd)
for img in uaimgs:
    img = r'http:'+img
    nwd = os.getcwd()+"\\a{}".format(count)+".png"
    urllib.urlretrieve(img,nwd)
    count+=1
 
count1 = 0
os.chdir(cwd)
if not os.path.exists(nwd):
    os.makedirs('iOS_images')
os.chdir(nwd)
for img in uimgs:
    img = r'http:'+img
    nwd = os.getcwd()+"\\a{}".format(count1)+".png"
    urllib.urlretrieve(img,nwd)
    count1+=1