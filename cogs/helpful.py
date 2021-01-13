from discord.ext import commands
from funcs import msg, error, getlyrics, googlesearcher
from urllib.request import urlopen, urlretrieve
from urllib.parse import quote, quote_plus
import discord
import asyncio
import json
from time import time
import requests
from datetime import timedelta
import config
from translate import Translator as trans

bot = None
def setup(bbot):
    global bot
    bbot.add_cog(Helpful())
    bot = bbot

sugurl = config.sugurl

class Helpful(commands.Cog, name="helpful"):
    """Some helpful commands that aren't actually useless oh yeah"""

    @commands.command("search", brief="Search Google")
    async def search(self, ctx, *, query=""):
        """Search Google for something"""
        arg = query
        if arg == "":
            await ctx.send(embed=error(title="No Query", desc="You need to put in what you want to search"))
            return
        else:
            loading = await ctx.send(embed=msg(thumbnail="https://media4.giphy.com/media/dOmQEMUbT2fWKy7hCA/giphy.gif"))
            result = await ctx.bot.loop.run_in_executor(None, googlesearcher, arg)
            await ctx.send(embed=msg(title="Search results", desc=result + "\n Most relevant results at the top."))
            await loading.delete()

    @commands.command("conv", brief="Convert between languages")
    async def convtoenglish(self, ctx, fromlang="", tolang="", *, text=""):
        """Convert from one language to another"""
        arg1 = fromlang
        arg2 = tolang
        arg3 = text
        if arg1 == "" or arg2 == "" or arg3=="":
            await ctx.send(embed=error(title="No hablo estúpido", desc="You need to put in a language to convert to *and* a language to convert from *AND* some text to convert!"))
        else:
            res = trans(from_lang=arg1, to_lang=arg2).translate(arg3)
            if "IS AN INVALID TARGET LANGUAGE" in res or "IS AN INVALID SOURCE LANGUAGE" in res:
                await ctx.send(embed=error(title="Whoops", desc="The language you put in is invalid. Put in something like 'Spanish'."))
            else:
                await ctx.send(embed=msg(title="Conversion!", desc=res))
 
    @commands.command("lyrics", brief="Get the lyrics to a song")
    async def lyricgrabber(self, ctx, title="", artist=""):
        """Get the lyrics to a song"""
        if title == "" or artist == "":
            await ctx.send(embed=error(title="Not enough infos", desc="You need to specify a title *and* an artist, like this: >lyrics Immortals \"Fall Out Boy\" (wrap it in quotes if you have spaces)"))
        else:
            loading = await ctx.send(embed=msg(thumbnail="https://media4.giphy.com/media/dOmQEMUbT2fWKy7hCA/giphy.gif"))
            try:
                lyric = await ctx.bot.loop.run_in_executor(None, getlyrics, title, artist)
                lyriclist = [(lyric[i:i+2000]) for i in range(0, len(lyric), 2000)]
                for i in range(0, len(lyriclist)):
                    await ctx.send(embed=msg(desc=lyriclist[i]))
                    await ctx.send(embed=msg(title="\nPowered by [Genius](https://genius.com)"))
                await loading.delete()
            except Exception as e:
                await ctx.send(embed=error(title="No musics for you", desc="Coundn't get the lyrics. Most likely we couldn't find the lyrics."))
                print(str(e))
                await loading.delete()
    
    @commands.command("dict", brief="Get the definition of a word")
    async def dictionarysearch(self, ctx, *, word=""):
        """Get the dictionary definition of a word"""
        arg = word
        if arg == "":
            await ctx.send(embed=error(title="'' is not in the dictionary", desc="You need to specify a word to get the definition of!"))
            return
        try:
            data=json.loads(urlopen("https://api.dictionaryapi.dev/api/v2/entries/en/" + quote(arg)).read())
            err = False
        except Exception as e:
            if "Error 404:" in str(e):
                await ctx.send(embed=error(title="Not feelin' smart today, eh?", desc="Couldn't find that word in our immense database"))
            else:
                await ctx.send(embed=error(title="Aw man", desc="An unknown error occurred."))
                print(str(e))
            err = True

        if not err:
            data = list(data)
            data = list(dict(data[0])["meanings"])
            meanings = ""
            for i in range(0, len(data)):
                meanings += str(data[i]["partOfSpeech"]) + ": " + str(data[i]["definitions"][0]['definition'] + "\n")
            await ctx.send(embed=msg(title=arg, desc=meanings + "\nPowered by [dictionaryapi.dev](https://dictionaryapi.dev)"))

    @commands.command("me", brief="Get info about yourself")
    async def me(self, ctx):
        """Get some info about yourself"""
        if isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.send(embed=error(title="Noob.", desc="Haha, you can't use this command in DMs."))
            return
        member = ctx.author
        await ctx.send(embed=msg(title=member.name + "'s info", desc="Account created on " + str(member.created_at.date()) + "\nJoined the server on " + str(member.joined_at.date()) + "\n Top role: " + str(member.top_role), thumbnail=member.avatar_url))
     
    @commands.command("suggest", brief="Suggest something!")
    async def suggest(self, ctx, *, suggestion=""):
        """Suggest something  to the BananaBot Team"""
        arg = suggestion
        if arg == "":
            await ctx.send(embed=error(title="I suggest you try harder", desc="You need to put in something to suggest!"))
        elif ctx.author.id in []:
            await ctx.send(embed=error(title="403 - Forbidden", desc="You've been blocked by the BananaBot devs from using certain commands, such as this one! Be a good boy next time."))
        else:
            requests.post(sugurl, data={"username": "Suggestion", "content":"*User **" + str(ctx.author.id) + "** made a suggestion:*\n" + arg})
            await ctx.send(embed=msg(title="Boom, done.", desc="Suggestion sent, maybe we'll do it!"))
            
    @commands.command("searchmsg", brief="Search all sent messages")
    async def searchmessages(self, ctx, *, query=""):
        """Search all of the sent messages in the channel"""
        arg=query
        if arg == "":
            await ctx.send(embed=error(title="Oops, we dropped the magnifying glass", desc="You need to put in a search!"))
            return
        messages = await ctx.channel.history(limit=200).flatten()
        res = ""
        hasfound = False
        for i in range(1, len(messages)):
            if arg.lower() in messages[i].content and messages[i].content.startswith(">msgsearch") == False:
                await ctx.send(embed=msg(title="Found a message!", desc="Found a message that matches or is related to `" + arg + "`. [Jump to message](" + messages[i].jump_url + ")"))
                hasfound = True
        if not hasfound:
            await ctx.send(embed=error(title="Empathy banana is here for you", desc="Couldn't find a matching message!"))


