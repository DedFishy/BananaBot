#This contains most of BananaBot's basic functions and functions for commands that take a bit to finish (for async)
from discord import Colour as color
from discord import Embed as embed
import discord
from datetime import timedelta
from PIL import Image, ImageFont, ImageDraw
from PIL import ImageFilter as filters
from io import BytesIO
from translate import Translator as trans
import lyricsgenius
from urllib.request import urlopen, urlretrieve
from random import randint
import requests
from time import time
from urllib.parse import quote, quote_plus
import googlesearch
import json
import config
lyrics = lyricsgenius.Genius(config.genius)
from profanity.profanity import censor, set_censor_characters

#Bot startup time
starttime = time()

yellow = color(0xfcca03)
red = color(0xff2600)

def makeqr(text):
    text = quote(text)
    response = requests.get("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=" + text)
    img = Image.open(BytesIO(response.content))
    arr = BytesIO()
    img.save(arr, format='png')
    arr.seek(0)
    file = discord.File(arr, filename="qr_" + text + ".png")
    return file

def readqr(img):
    data=json.loads(urlopen("https://api.qrserver.com/v1/read-qr-code/?fileurl=" + quote(img)).read())
    return dict(data[0])

def tshirter(text):
    response = requests.get("https://raw.githubusercontent.com/SuperBoyne/bananabotfiles/main/tshirt.jpg")
    img = Image.open(BytesIO(response.content))
    draw = ImageDraw.Draw(img)
    ImageDraw.Draw(img).text((40, 70), text, (0, 0, 0), font=ImageFont.truetype("font.ttf", size=14))
    arr = BytesIO()
    img.save(arr, format='png')
    arr.seek(0)
    file = discord.File(arr, filename="putthatonatshirt.png")
    return file

def getaquackyboi():
    data=json.loads(urlopen("https://random-d.uk/api/v2/random?format=json").read())
    return dict(data)["url"]

def getdoge():
    data=json.loads(urlopen("https://api.thedogapi.com/v1/images/search").read())
    data = list(data)
    data = dict(data[0])["url"]
    return data

def makediscord(text):
    response = requests.get("https://raw.githubusercontent.com/SuperBoyne/bananabotfiles/main/discord.png")
    img = Image.open(BytesIO(response.content))
    draw = ImageDraw.Draw(img)
    ImageDraw.Draw(img).text((70, 24), text, (255, 255, 255), font=ImageFont.truetype("font.ttf", size=15))
    arr = BytesIO()
    img.save(arr, format='png')
    arr.seek(0)
    file = discord.File(arr, filename="discordofficial.png")
    return file

def blurify(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.convert("RGB")
    img = img.filter(filters.BLUR)
    arr = BytesIO()
    img.save(arr, format='png')
    arr.seek(0)
    return discord.File(arr, filename="ineedmyglasses.png")

def clayify(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.convert("RGB")
    img = img.filter(filters.EMBOSS)
    arr = BytesIO()
    img.save(arr, format='png')
    arr.seek(0)
    return discord.File(arr, filename="whatclay.png")

def stencilify(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.convert("RGB")
    img = img.filter(filters.CONTOUR)
    arr = BytesIO()
    img.save(arr, format='png')
    arr.seek(0)
    return discord.File(arr, filename="likeafourthgrader.png")

def makeclyde(text):
    response = requests.get("https://raw.githubusercontent.com/SuperBoyne/bananabotfiles/main/clydesays.png")
    img = Image.open(BytesIO(response.content))
    draw = ImageDraw.Draw(img)
    ImageDraw.Draw(img).text((75, 30), text, (255, 255, 255), font=ImageFont.truetype("font.ttf", size=15))
    arr = BytesIO()
    img.save(arr, format='png')
    arr.seek(0)
    return discord.File(arr, filename="clydeisweird.png")

def msg(title="", desc="", image="", titleurl="", thumbnail="", color=yellow):
    title = censor(title)
    desc = censor(desc)
    embed = discord.Embed(title=title, description=desc, url=titleurl, color = color)
    if not image == "":
        embed.set_image(url=image)
    if not thumbnail == "":
        embed.set_thumbnail(url=thumbnail)
    return embed

def error(title="", desc=""):
    title = censor(title)
    desc = censor(desc)
    embed = discord.Embed(title=title, description=desc, color =  discord.Colour(0xff2600))
    embed.set_thumbnail(url="https://media4.giphy.com/media/NTddjTZTeOmXK/giphy.gif")
    return embed

def loadingembed():
    lembed = embed(color=yellow)
    lembed.set_embed("https://media4.giphy.com/media/dOmQEMUbT2fWKy7hCA/giphy.gif")
    return lembed

def getgif(query):
    return json.loads(urlopen("http://api.giphy.com/v1/gifs/search?q=" + query.replace(" ", "+") + "&api_key=" + config.giphy + "&limit=1&rating=g").read())

def getapic(query):
    return json.loads(urlopen("https://pixabay.com/api/?key=17168920-8e8630c50fb2d0013d3dd8822&per_page=3&image_type=photo&safesearch=true&q=" + query.replace(" ", "+") + "&api_key=" + config.pixabay + "&limit=1").read())

def googlesearcher(arg):
    results = []
    for j in googlesearch.search(arg, tld='com', lang='en', num=10, start=0, stop=10, pause=2.0, safe="on"):
        results.append(j)
    answer = ""
    for i in range(0, len(results)):
        answer += results[i] + "\n"
    if answer.replace(" ", "") == "":
        answer = "No Results (aww man)"
    return answer

def fuzzyimage():
    colortup = (255, 0, 0)
    testImage = Image.new("RGB", (200, 200), (255, 255, 255))
    for x in range(200):
        for y in range(200):
            colortup = (randint(0, 255), randint(0, 255), randint(0, 255))
            testImage.putpixel((x, y), colortup)
    return testImage

def getlyrics(title, artist):
    return lyrics.search_song(title, artist).lyrics

def tvimage():
    colortup = (255, 0, 0)
    testImage = Image.new("RGB", (200, 200), (255, 255, 255))
    for x in range(200):
        for y in range(200):
            color = randint(0, 255)
            colortup = (color, color, color)
            testImage.putpixel((x, y), colortup)
    return testImage

def rainbowimage():
        color = "red"
        colortup = (255, 0, 0)
        testImage = Image.new("RGB", (200, 200), (255, 255, 255))
        for x in range(200):
            for y in range(200):
                changecolor = randint(1, 100)
                if changecolor == 8:
                    changecolor = True
                else:
                    changecolor = False
                if changecolor:
                    if color == "red":
                        color = "green"
                        colortup = (0, 255, 0)
                    elif color == "green":
                        color = "blue"
                        colortup = (0, 0, 255)
                    else:
                        color = "red"
                        colortup = (255, 0, 0)
                testImage.putpixel((x, y), colortup)
        return testImage

def getacat():
    url = 'https://api.thecatapi.com/v1/images/search'
    headers = {'x-api-key': config.catapi}
    req = requests.get(url, headers=headers)
    cat = json.loads(req.text)
    return cat

def makebsod(bsod):
    response = requests.get("https://raw.githubusercontent.com/SuperBoyne/bananabotfiles/main/win10bsod.png")
    img = Image.open(BytesIO(response.content))
    draw = ImageDraw.Draw(img)
    ImageDraw.Draw(img).text((100, 180), bsod, (255, 255, 255), font=ImageFont.truetype("font.ttf", size=15))
    arr = BytesIO()
    img.save(arr, format='png')
    arr.seek(0)
    file = discord.File(arr, filename="bsod.png")
    return file

def googlesearcherwordy(arg):
    results = []
    for j in googlesearch.search(arg, tld='com', lang='en', num=1, start=0, stop=10, pause=2.0, safe="on"):
        results.append(j)
    try:
        answer = results[0]
    except:
        answer = ""
    if answer.replace(" ", "") == "":
        answer = choice(links)
    return answer

def statmsg(bot):
    embed = discord.Embed(title="BananaBot Stats!", color = yellow)
    embed.add_field(name="Servers", value="BananaBot is in `" + str(len(list(bot.guilds))) + "` servers! Yay! [?](https://www.pcmag.com/how-to/what-is-discord-and-how-do-you-use-it \"What's Discord?\")")
    embed.add_field(name="Uptime", value="BananaBot has been online for `" + str(timedelta(seconds=int("%.0f" % int(time() - starttime)))) + "`. [?](https://www.pickaweb.co.uk/kb/what-is-uptime/ \"What is uptime?\")")
    embed.add_field(name="Ping", value="BananaBot's ping is `%.3f` seconds! [?](https://blog.stackpath.com/latency/ \"What is latency?\")"%bot.latency)
    return embed
