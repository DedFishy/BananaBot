#coding: utf-8
'''
BananaBot
Created by SuperBoyne

'''

#Imports

#Getting the configuration
import config
from socket import gethostname
from bot import Banana
from os.path import exists
from urllib.request import urlretrieve
from time import sleep
import requests

if gethostname() == config.devpc:
    devmode = True
else:
    devmode = False

#Setting the token
token = config.token
if devmode:
    #Setting the development token (in case we're on the development PC)
    token = config.devtoken

bot = Banana()

#Checking if we have the BananaBot font and if not downloading it
if not exists("font.ttf"):
    print("Getting font...")
    urlretrieve("https://github.com/SuperBoyne/bananabotfiles/blob/main/ARI.ttf?raw=true", "font.ttf")

#Just a notification
print("Connecting to Discord...")

bot.load_extension('cogs.basic')
bot.load_extension('cogs.fun')
bot.load_extension('cogs.helpful')
bot.load_extension('cogs.images')


bot.run(token)