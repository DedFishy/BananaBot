from discord.ext import commands
import discord
from io import BytesIO
from urllib.request import urlopen, urlretrieve
from urllib.parse import quote
import json
import config
from datetime import datetime
from funcs import msg, error, blurify, clayify, makebsod, getacat, loading
from funcs import makeclyde, stencilify, makediscord, getdoge, getaquackyboi, fuzzyimage, getgif, getapic, tshirter, rainbowimage, tvimage, makeqr, readqr

#Initializing the bot variable
bot = None

#Cog setup
def setup(bbot):
    bbot.add_cog(Images())
    bot = bbot

#Da class
class Images(commands.Cog, name="images"):
    """Commands related to images, like image generation and stuff."""
    #QR subcommand
    @commands.group(brief="QR code commands")
    async def qr(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=msg(title="You put the pixel in the wrong place", desc="That's an invalid QR command!"))
    @qr.command("make", brief="Create a QR code")
    async def createaqrboi(self, ctx, *, text=None):
        """Create a QR code, with [text] being what the QR code says."""
        if not text:
            await ctx.send(embed=error(title="COuld not read QR, get closer", desc="You need to put in some text to generate the QR from!"))
            return
        load = await loading(ctx)
        img = await ctx.bot.loop.run_in_executor(None, makeqr, text)
        await load.delete()
        await ctx.send(embed=msg(title="Cool QR", desc="We make QRs using [QRServer.com](http://qrserver.com/)!"), file=img)
        
    @qr.command("read", brief="Read a QR code")
    async def readaqrboi(self, ctx):
        """Read the QR code uploaded with the command"""
        try:
            qr = ctx.message.attachments[0].url
        except Exception as e:
            await ctx.send(embed=error(title="No, no, NO!", desc="You neeeeed to upload a QR code along with your message, you dumb moron! (Just kidding.)"))
            print(e)
            return
        load = await loading(ctx)
        text = await ctx.bot.loop.run_in_executor(None, readqr, qr)
        text = text['symbol'][0]["data"]
        await ctx.send(embed=msg(title="Cool QR", desc="We read QRs using [QRServer.com](http://qrserver.com/)!\nIt says:\n" + text))
        await load.delete()
    
    #The group for image editors
    @commands.group(brief="Image editing commands")
    async def edit(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=msg(title="You put the pixel in the wrong place (we reused this title haha)", desc="That's an invalid editor command!"))
    
    @edit.command("blur", brief="Blur an image")
    async def blurryboi(self, ctx):
        """Blur the uploaded image"""
        try:
            image = ctx.message.attachments[0].url
        except Exception as e:
            await ctx.send(embed=error(title="I found my glasses", desc="You gotta upload an image to blur"))
            print(e)
            return
        load = await loading(ctx)
        im = await ctx.bot.loop.run_in_executor(None, blurify, image)
        await load.delete()
        await ctx.send(file=im)
        
    @edit.command("clay", brief="Clayify an image")
    async def clayboi(self, ctx):
        """Clayify (???) the uploaded image"""
        try:
            image = ctx.message.attachments[0].url
        except Exception as e:
            await ctx.send(embed=error(title="There's no clay left", desc="You gotta upload an image to... clayify?"))
            print(e)
            return
        load = await loading(ctx)
        im = await ctx.bot.loop.run_in_executor(None, clayify, image)
        await load.delete()
        await ctx.send(file=im)
    
    @edit.command("outline", brief="Outline an image")
    async def outlineyboi(self, ctx):
        """Outline the uploaded image, like with a very thin marker"""
        try:
            image = ctx.message.attachments[0].url
        except Exception as e:
            await ctx.send(embed=error(title="Stenciled", desc="You gotta upload an image to ~~blur~~ outline"))
            print(e)
            return
        load = await loading(ctx)
        im = await ctx.bot.loop.run_in_executor(None, stencilify, image)
        await ctx.send(file=im)
        await load.delete()
    
    @commands.command("gif", brief="Search for a gif")
    async def findgif(self, ctx, *, query=""):
        """Search Giphy for a gif"""
        arg = query
        if arg == "":
            await ctx.send(embed=error(title="Then Thomas fell into a mine", desc="You didn't put in a search for a gif!"))
            return
        else:
            load = await loading(ctx)
            query = quote(arg)
            data= await ctx.bot.loop.run_in_executor(None, getgif, arg)
            data = dict(data)
            try:
                await ctx.send(embed=msg(title="Ooh, a shiny gif!", titleurl=data["data"][0]["images"]["original"]["url"], image=data["data"][0]["images"]["original"]["url"], thumbnail="https://raw.githubusercontent.com/SuperBoyne/bananabotfiles/main/Poweredby_100px-White_VertLogo.png", desc="Powered by [Giphy](https://giphy.com)"))
            except Exception as e:
                await ctx.send(embed=error(title="Giphy says NNNNNOOOPPEEE", desc="There were no results for your hopefully epic gif search."))
                print(str(e))
            await load.delete()
    
    @commands.command("pic", brief="Search for a picture")
    async def findpic(self, ctx, *, query=""):
        """Search Pixabay for a picture"""
        arg = query
        if arg == "":
            await ctx.send(embed=error(title="Pixel imperfect", desc="You didn't put in a search for a picture!"))
            return
        else:
            query = quote(arg)
            data= await ctx.bot.loop.run_in_executor(None, getapic, query)
            data = dict(data)
            try:
                await ctx.send(embed=msg(title="An image popped up", desc="Powered by [Pixabay](https://pixabay.com)", titleurl=data["hits"][0]["previewURL"], thumbnail="https://raw.githubusercontent.com/SuperBoyne/bananabotfiles/main/logo.png", image=data["hits"][0]["previewURL"]))
            except:
                await ctx.send(embed=error(title="Results? Nope.", desc="No results appeared for your image, apparently."))
    
    @commands.command("nasapic", brief="Get the NASA POTD")
    async def findnasapic(self, ctx):
        """Get the NASA Picture Of The Day"""
        data=await ctx.bot.loop.run_in_executor(None, json.loads, (urlopen("https://api.nasa.gov/planetary/apod?api_key=" + config.nasa + "&date=" + datetime.today().strftime('%Y-%m-%d')).read()))
        data = dict(data)
        await ctx.send(embed=msg(title="NASA Picture of The Day", desc="Powered by [NASA](https://nasa.gov)", titleurl=data["url"], image=data["url"]))
    
    @commands.group(brief="Image generation commands")
    async def generate(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=msg(title="WE put the pixel in the wrong place", desc="That's an invalid image generator command!"))
    
    @generate.command("fuzz", brief="Create an ugly image")
    async def fuzzimgyipee(self, ctx):
        """Create the ugliest image in the world"""
        arr = BytesIO()
        im = await ctx.bot.loop.run_in_executor(None, fuzzyimage)
        im.save(arr, format='PNG')
        arr.seek(0)
        file = discord.File(arr, filename="fuzzywuzzy.png")
        await ctx.send(file=file)
    
    @generate.command("tv", brief="Make a TVish image")
    async def tvimgwhupee(self, ctx):
        """Make an image that looks like one of those old TVs"""
        arr = BytesIO()
        im = await ctx.bot.loop.run_in_executor(None, tvimage)
        im.save(arr, format='PNG')
        arr.seek(0)
        file = discord.File(arr, filename="iturnedonthetubetv.png")
        await ctx.send(file=file)
    
    @generate.command("rainbow", brief="Make a rainbow image!")
    async def rainbowimgyay(self, ctx):
        """Make a RAAAAAAAAAAAINBOW image!"""
        arr = BytesIO()
        im = await ctx.bot.loop.run_in_executor(None, rainbowimage)
        im.save(arr, format='PNG')
        arr.seek(0)
        file = discord.File(arr, filename="raaaainbow.png")
        await ctx.send(file=file)
    
    @commands.command("cat", brief="Get a cat image")
    async def getacatyee(self, ctx):
        """Gat a picture of a kitty cat!"""
        cat = await ctx.bot.loop.run_in_executor(None, getacat)
        await ctx.send(embed=msg(title="Meow Meow Cat!", image=cat[0]["url"], titleurl=cat[0]["url"], desc="Cat pics are from [thecatapi.com](https://thecatapi.com)"))
    
    @generate.command("discord", brief="Make a Discord message")
    async def officialdiscordmessage(self, ctx, *, message=""):
        """Make a fake Discord message appear!"""
        arg = message
        if arg=="":
            await ctx.send(embed=error(title="Account terminated", desc="You need to put in text for Discord to say!"))
        else:
            load = await loading(ctx)
            try:
                file = await ctx.bot.loop.run_in_executor(None, makediscord, arg)
                await ctx.send(file=file)
                await load.delete()
            except Exception as e:
                print(str(e))
                await ctx.send(embed=error(title="Suspiscion arises", desc="For some reason we couldn't make Discord say that. Try again?"))
                await load.delete()
    
    @generate.command("bsod", brief="Make a fake BSOD")
    async def fakebsodohno(self, ctx, *, bsod=""):
        """Make a fake Windows BSOD!"""
        arg = bsod
        if arg=="":
            await ctx.send(embed=error(title="Account terminated", desc="You need to put in text to make an error!"))
        else:
            load = await loading(ctx)
            try:
                file = await ctx.bot.loop.run_in_executor(None, makebsod, bsod)
                await ctx.send(file=file)
                await load.delete()
            except Exception as e:
                print(str(e))
                await ctx.send(embed=error(title="Suspiscion arises", desc="For some reason there was an error making the error. *Errorception*."))
                await load.delete()
    
    @generate.command("tshirt", brief="Put text on a shirt")
    async def putonatshirt(self, ctx, *, text=""):
        """Put some text on a t-shirt!"""
        arg = text
        if arg=="":
            await ctx.send(embed=error(title="The shirt doesn't fit anymore", desc="You need to put in text so that it can be put on a *T*"))
        else:
            load = await loading(ctx)
            try:
                file = await ctx.bot.loop.run_in_executor(None, tshirter, text)
                await ctx.send(file=file)
                await load.delete()
            except Exception as e:
                print(str(e))
                await ctx.send(embed=error(title="Suspiscion arises", desc="For some reason we couldn't *put that on a t-shirt*. Maybe ***DO IT AGAIN***"))
                await load.delete()
    
    @commands.command("doge", brief="Get a dog pic")
    async def doggie(self, ctx):
        """Get a doggie picture!"""
        data = await ctx.bot.loop.run_in_executor(None, getdoge)
        await ctx.send(embed=msg(title="A doggo appeared!", desc="All our doggos are from [The Dog API](https://thedogapi.com)!", titleurl=data, image=data))
        
    @generate.command("clyde", brief="Make a Clyde message")
    async def clydemsg(self, ctx, *, message=""):
        """Make a message from Clyde appear!"""
        arg = message
        if arg=="":
            await ctx.send(embed=error(title="This user is not accepting DMs", desc="You need to put in text for Clyde to say!"))
        else:
            load = await loading(ctx)
            try:
                file = await ctx.bot.loop.run_in_executor(None, makeclyde, message)
                await ctx.send(file=file)
                await load.delete()
            except Exception as e:
                print(str(e))
                await ctx.send(embed=error(title="Suspiscion arises", desc="For some reason we couldn't make Clyde say that. Try again?"))
                await load.delete()

    @commands.command("duck", brief="Get a duck pic!")
    async def duckie(self, ctx):
        """Get a duckie picture!"""
        data = await ctx.bot.loop.run_in_executor(None, getaquackyboi)
        await ctx.send(embed=msg(title="QUACK QUACK!", desc="All the ducks are from [random-d.uk](https://random-d.uk/)!", titleurl=data, image=data))

