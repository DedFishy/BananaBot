from discord.ext import commands
from funcs import msg, error, googlesearcherwordy
from pyfiglet import Figlet as figlet
from random import choice, shuffle, randint
from urllib.parse import quote

bot = None

def setup(bbot):
    bbot.add_cog(Fun())
    bot = bbot

class Fun(commands.Cog, name="fun"):
    """Some fun, useless commands!"""
    
    @commands.command("flip", brief="Flip a coin")
    async def flip(self, ctx):
        """Flip a coin that doesn't exist"""
        await ctx.send(embed=msg(title="You flipped that coin and got " + choice(['heads', 'tails']) + ".", thumbnail="https://media.giphy.com/media/a8TIlyVS7JixO/giphy.gif"))
    
    @commands.command("jumble", brief="Jumble up some text")
    async def jumble(self, ctx, *, text=""):
        """Jumble up each word in the text, but keep the order of the words"""
        arg = text
        if arg != "":
            phrase = arg
            phrase = phrase.split()
            finishedphrase  = []
            for i in range(0, len(phrase)):
                finishedphrase.append([char for char in phrase[i]])
            phrase = finishedphrase
            finishedphrase = []
            finalproduct = ""
            for i in range(0, len(phrase)):
                finishedphrase.append(shuffle(phrase[i]))
                finalproduct += " " + "".join(phrase[i])
            await ctx.send(embed=msg(title=finalproduct))
        else:
            await ctx.send(embed=error(title="Can't jumble nothing!", desc="Put in something to jumble if you want to jumble something!"))
    
    @commands.command("randoword", brief="Get a random word")
    async def randoword(self, ctx):
        """Get a random word!"""
        await ctx.send(embed=msg(title="Your word is: " + choice(words)))
    
    @commands.command("randosite", brief="Get a random website")
    async def randosite(self, ctx):
        """Get a random website, using the power of kindness and love"""
        keyword = choice(words)
        keyword = quote(keyword)
        loading = await ctx.send(embed=msg(thumbnail="https://media4.giphy.com/media/dOmQEMUbT2fWKy7hCA/giphy.gif"))
        site = await ctx.bot.loop.run_in_executor(None, googlesearcherwordy, keyword)
        print(str(site))
        await ctx.send(embed=msg(titleurl=site, title="Click for a site!", desc="*Warning: Although we use SafeSearch,  __BananaBot is not responsible for the content of this site!__*"))
        await loading.delete()
    
    @commands.command("say", brief="Make the bot say something!")
    async def saysomethin(self, ctx, *, thing=""):
        """Make BananaBot say stuff"""
        if thing == "":
            await ctx.send(embed=error(title="Nothing", desc="It's really hard to say nothing."))
            return
        await ctx.send(thing)
    
    @commands.command("roll", brief="Roll a die")
    async def roll(self, ctx, *, sides="6"):
        """Roll a die, and choose how many sides if you want"""
        arg = sides
        try:
            dienum = int(arg)
            roll = randint(1, int(arg))
            if dienum < 4:
                await ctx.send(embed=error(title="Foolish mortal", desc="I don't think a die can have that few sides..."))
            elif dienum > 9000:
                await ctx.send(embed=error(title="Foolish mortal", desc="IT'S OVER 9000 BABY (and it's too many sides)"))
            else:
                if str(roll).startswith("8") or (str(roll).endswith("8") and len(str(roll)) < 3):
                    if str(arg).startswith("8") or (str(roll).endswith("8") and len(str(roll)) < 3):
                        await ctx.send(embed=msg(title="You rolled an " + arg + "-sided die and got an " + str(roll), thumbnail="https://media.giphy.com/media/3oGRFlpAW4sIHA02NW/giphy.gif"))
                    else:
                        await ctx.send(embed=msg(title="You rolled a " + arg + "-sided die and got an " + str(roll), thumbnail="https://media.giphy.com/media/3oGRFlpAW4sIHA02NW/giphy.gif"))
                else:
                    if str(arg).startswith("8"):
                        await ctx.send(embed=msg(title="You rolled an " + arg + "-sided die and got a " + str(roll), thumbnail="https://media.giphy.com/media/3oGRFlpAW4sIHA02NW/giphy.gif"))
                    else:
                        await ctx.send(embed=msg(title="You rolled a " + arg + "-sided die and got a " + str(roll), thumbnail="https://media.giphy.com/media/3oGRFlpAW4sIHA02NW/giphy.gif"))
        except Exception as e:
            print(str(e))
            await ctx.send(embed=error(title="Foolish mortal", desc="Hey, that's not a number of sides! Gimme a number!"))
    
    @commands.command("circle", brief="Circle some text")
    async def circletext(self, ctx, *, text=""):
        """Circle some text!"""
        if text == "":
            await ctx.send(embed=error(title="Spinning in circles", desc="You need to put in some text to circle!"))
            return
        t = text
        t = t.lower()
        t = t.replace("0", "⓪")
        t = t.replace("1", "①")
        t = t.replace("2", "②")
        t = t.replace("3", "③")
        t = t.replace("4", "④")
        t = t.replace("5", "⑤")
        t = t.replace("6", "⑥")
        t = t.replace("7", "⑦")
        t = t.replace("8", "⑧")
        t = t.replace("9", "⑨")
        t = t.replace("a", "ⓐ")
        t = t.replace("b", "ⓑ")
        t = t.replace("c", "ⓒ")
        t = t.replace("d", "ⓓ")
        t = t.replace("e", "ⓔ")
        t = t.replace("f", "ⓕ")
        t = t.replace("g", "ⓖ")
        t = t.replace("h", "ⓗ")
        t = t.replace("i", "ⓘ")
        t = t.replace("j", "ⓙ")
        t = t.replace("k", "ⓚ")
        t = t.replace("l", "ⓛ")
        t = t.replace("m", "ⓜ")
        t = t.replace("n", "ⓝ")
        t = t.replace("o", "ⓞ")
        t = t.replace("p", "ⓟ")
        t = t.replace("q", "ⓠ")
        t = t.replace("r", "ⓡ")
        t = t.replace("s", "ⓢ")
        t = t.replace("t", "ⓣ")
        t = t.replace("u", "ⓤ")
        t = t.replace("v", "ⓥ")
        t = t.replace("w", "ⓦ")
        t = t.replace("x", "ⓧ")
        t = t.replace("y", "ⓨ")
        t = t.replace("z", "ⓩ")
        await ctx.send(embed=msg(title="Circles!", desc="```" + t + "```"))

    @commands.command("rps", brief="Play RPS!")
    async def rps(self, ctx, *, choice=""):
        """Play Rock, Paper, Scissors with the bot."""
        arg = choice
        if arg == "":
            await ctx.send(embed=error(title="REMATCH", desc="You need to put in rock, paper, scissors, or a corresponding ***NUMBER!***"))
        else:
            arg = arg.lower()
            arg = arg.strip()
            if arg == "rock":
                arg = "1"
            if arg == "paper":
                arg = "2"
            if arg == "scissors":
                arg = "3"
            
            ai = randint(1, 3)
            if not arg.isnumeric():
                await ctx.send(embed=error(title="You can't use 'gun' in RPS!", desc="Ya need to have either rock, paper, scissiors, or a number that corresponds to them, not " + arg + "!"))
                return
            elif int(arg) > 3 or int(arg) < 1:
                await ctx.send(embed=error(title="NO", desc="You need to put in a *corresponding* number, not just some silly-willy number."))
                return

            if arg == '2' and ai == 1:
                res = "You win!"
                
            elif arg == '3' and ai == 2:
                res='You win!'
                
            elif arg == "1" and ai == 3:
                res = "You win!"

            elif arg == '1' and ai == 2:
                res = "You lose!"

            elif arg == '2' and ai == 3:
                res = "You lose!"

            elif arg == '3' and ai == 1:
                res = "You lose!"

            elif arg == str(ai):
                res = "You tied!"
            
            else:
                res = "Oh no, an error!"
            
            await ctx.send(embed=msg(
                title="Rock, Paper, Scissors, Shoot!",
                desc="""RPS Results: \nYou picked: `""" + arg.replace("1", "rock").replace("2", "paper").replace("3", "scissors") + """` \nComputer picked: `""" + str(ai).replace("1", "rock").replace("2", "paper").replace("3", "scissors") + """`\nResult: `""" + res + """`"""))
            
    @commands.command("figlet", brief="Make ASCII art")
    async def figletif(self, ctx, *, text=""):
        """Make ASCII art out of the given text"""
        try:
            await ctx.send(embed=msg(title="Cool text has been served", desc="```" + figlet().renderText(text.replace(" ", "\n")) + "```"))
        except:
            await ctx.send(embed=error(title="No magic text", desc="It looks like either what you typed was too long or you didn't type anything! (or something else maybe...)"))

