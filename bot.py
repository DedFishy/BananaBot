#The Banana() class, a subclass of Bot

#Imports
from discord.ext.commands import Bot
from discord.ext import commands
from socket import gethostname
from help import HelpCommand
from time import time
import config
from funcs import error
import sys
import traceback
 
#The actual class
class Banana(Bot):
    #Starting the bot class
    def __init__(self):
        #Switching the prefix for dev mode
        if gethostname() == config.devpc:
            prefix = config.devprefix
        else:
            prefix = config.prefix
        #Setting up the parent class
        super().__init__(
          activity=config.activity,
          command_prefix=prefix,
          help_command=HelpCommand(),
          token=config.token
          )
        
        #Getting the startup time
        self.starttime = time()

    #When a command errors out
    async def on_command_error(self, ctx, err):
        """Overridden ``on_command_error`` to send some useful information
        to the context command's author."""

        #https://docs.python.org/3/library/functions.html#hasattr
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        err = getattr(err, 'original', err)
        embed = error()

        if isinstance(err, commands.CommandNotFound):
            return

        elif isinstance(err, commands.CommandOnCooldown):
            embed.title = f"You need to take a chill pill, phil. Try again in ``{round(err.retry_after)}`` second(s)."

        elif isinstance(err, commands.BadArgument):
            embed.title = "You passed a bad argument, noob!!"
            embed.description = err

        elif isinstance(err, commands.MissingRequiredArgument):
            embed.title = f"Hey you're missing the \"{err.param.name}\" argument for that command!"

        elif isinstance(err, commands.NotOwner):
            embed.title = "Nooope"
            embed.description = "You ain't allowed to use that command"

        else:
            embed.title = "Something went wrong with that command!"
            embed.description = F"{err.__class__.__name__}: {err}"
            embed.set_footer(text=f"You can help by suggesting the error be fixed by using {ctx.prefix}suggest.")

            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(err), err, err.__traceback__, file=sys.stderr)

        await ctx.send(embed=embed)