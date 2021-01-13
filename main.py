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
from pymongo import MongoClient

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

#Getting the word list
try:
    readwords = open("words.txt", "r") #Trying to open the word list
    wordlist = readwords.read() #Reading the word list
    if wordlist == "": #If the word list is empty, meaning there was an error creating it, raise an error so we can redownload it
        raise SyntaxError()
except: #If finding the word list doesn't work
    try:
        readwords.close() #Just in case
    except:
        pass
    print("Creating word list")
    print("Step 1: Create file")
    wordsfile = open("words.txt", "w+") #Initializing a file for the word list to live in
    print("Step 2: Download list")
    while True: #So we can retry
        try:
            wordsfile.write(requests.get("https://raw.githubusercontent.com/SuperBoyne/wordlist/main/words.txt").text) #Downloading the word list
            break #Breaking out of the while True so we don't download again
        except:
            print("Couldn't download the list, retrying in 3 seconds...")
            sleep(3)
    print("Step 3: Close file")
    wordsfile.close() #Closing the file
    readwords = open("words.txt", "r") #Opening the fresh new file
    wordlist = readwords.read() #Reading the word list
readwords.close() #Finally closing the word list
words = wordlist.splitlines() #Splitting the word list into an actual list

#Just a notification
print("Connecting to Discord...")

bot.load_extension('cogs.basic')
bot.load_extension('cogs.fun')
bot.load_extension('cogs.helpful')
bot.load_extension('cogs.images')


bot.run(token)