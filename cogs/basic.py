#Imports
from discord.ext import commands
import discord
from datetime import timedelta
from discord.ext import commands
from funcs import msg, error, statmsg
import requests
import discord
import textwrap
from contextlib import redirect_stdout
import traceback
import io
from time import time

#Initializing the bot variable
bot = None

#Setting up the cog
def setup(bbot):
    global bot
    bbot.add_cog(Basic())
    bot = bbot

#Developer check
async def devcheck(ctx):
    """A check that is applied to every command in this cog."""

    if await bot.is_owner(ctx.author):
        return True

    raise commands.NotOwner  # if the author is not the owner

#The actual class
class Basic(commands.Cog, name="basic"):
    """Some basic commands that can sometimes be found in other bots!"""
    
    def __init__(self):
      self._last_result = None
      
    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        return content.strip('` \n')  # remove `foo`
    
    @commands.group(checks=[devcheck], brief="Commands only the bot developers can use!")
    async def dev(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=msg(title="Traceback most recent call last", desc="That's an invalid developer command!"))
    
    @dev.command("execute", brief="Execute a Python snippet")
    async def execute(self, ctx, *, body=None):
        """Execute some Python code"""
        
        if not body:
            await ctx.send(embed=error(title="Nerp", desc="You need to actually put in some code!"))
            return
        
        env = {
            'bot': bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception:
            value = stdout.getvalue()
            await ctx.send(embed=error(desc=f'```py\n{value}{traceback.format_exc()}\n```'))
        else:
            value = stdout.getvalue()

            if ret is None:
                if value:
                    await ctx.send(embed=msg(desc=f'```py\n{value}\n```'))
                else:
                    await ctx.send(embed=msg(desc="```no output```"))
            else:
                self._last_result = ret
                await ctx.send(embed=msg(desc=f'```py\n{value}{ret}\n```'))
    
    @dev.command("reload", brief="Reload a category")
    async def reloadyboi(self, ctx, *, category=""):
        """Reloads a category"""
        try:
            bot.reload_extension(category)
        except Exception as e:
            await ctx.send(embed=error(title="NOPED", desc="Yo, you need an actual category!"))
            print(e)  
    @dev.command("servercount", brief="Get a list of servers")
    async def servercount(self, ctx):
        """Get a list of servers the bot is on"""
        if ctx.author.id == 645264167623983124:
            servers = list(bot.guilds)
            await ctx.send(embed=msg(title=f"Connected to {str(len(servers))} servers:", desc='\n'.join(server.name for server in servers)))
        else:
            await ctx.send(embed=error(title="The hacker has been caught", desc="For privacy reasons, this command is only available to the owner of the bot."))

    @dev.command("pres", brief="Change the bot's presence")
    async def changezepres(self, ctx, text="", prestype=""):
        """Change the bot's presence"""
        arg1 = text
        arg2 = prestype
        if arg1 == "" or arg2 == "" or not arg2.isnumeric():
            await ctx.send(embed=error(title="That's no good, sir", desc="You need to put in a status and a status type (the type is a number)!"))
        elif ctx.author.id == 645264167623983124:
            await bot.change_presence(activity=discord.Activity(name=arg1, type=int(arg2)))
            await ctx.send(embed=msg(title="Yessir", desc="The presence has been set, sir"))
        else:
            await ctx.send(embed=error(title="No can do, sir", desc="Hey, you're not the captain! You're an *Imposter!* (You can't use this command lol)"))
            
    @dev.command("stop", brief="Stop the bot")
    async def stopthebot(self, ctx):
        """Stop the bot"""
        if ctx.author.id == 645264167623983124:
            await ctx.send(embed=msg(title="Stopping..."))
            quit()
        else:
            await ctx.send(embed=error(title="You can't stop me", desc="You don't own the bot, so you can't stop the bot. Fair's fair."))
    @commands.command("uptime", brief="Get the bot's uptime")
    async def uptime(self, ctx):
        """Get the bot's uptime (how long it's been online)"""
        await ctx.send(embed=msg(desc="Uptime is " + str(timedelta(seconds=int("%.0f" % int(time() - bot.starttime)))) + ""))
    
    @commands.command("stats", brief="Get various bot stats")
    async def botstats(self, ctx):
        """Get some bot stats such as uptime and server count"""
        await ctx.send(embed=statmsg(bot))

    @commands.command("ping", brief="Get BananaBot's ping")
    async def ping(self, ctx):
        """Get BananaBot's ping (how many seconds it takes to do stuff"""
        await ctx.send(embed=msg(desc="Ping received! I'm not really a 'pong' type of guy. Latency is %.3f seconds."%bot.latency))

    @commands.command("credits", brief="Show the credits")
    async def credits(self, ctx):
        """It's the end of the movie, show the credits (who made BananaBot)"""
        await ctx.send(embed=msg(title="Credits", desc="Created by the owner of [The Epical Programming Server](https://teps.ml)"))
