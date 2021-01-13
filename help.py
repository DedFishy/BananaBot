#This is the custom help command class so we can have a slick looking help command

#This is a map of cog names to "rich" cog names
#You should change the emojis because they're from the BananaBot Support server
cogmapping = {
    "basic": ":speech_balloon: Basic",
    "fun": ":grin: Fun",
    "helpful": ":grey_question: Helpful",
    "images": ":frame_photo: Images",
}

#Imports

import discord
from discord.ext.commands import HelpCommand
from discord.utils import oauth_url
import config
from funcs import msg, error

class HelpCommand(HelpCommand):
    #A function to generate the links and help command instructions
    def main_help(self):
        #Creating an invite for the bot
        invite = oauth_url(self.context.bot.user.id, permissions=discord.Permissions(67632192))
        #The support server link
        supportserver = config.supportserver
        #Getting the name of the bot
        name = self.context.bot.user.name
        #Getting the prefix
        pref = self.clean_prefix
        #The bot's website
        website = config.website
        
        #The beginning of the string
        final = f"""Items in [] are arguments. Use " " around each argument when an argument
                has spaces and there is more than one argument for that command.
                Use {pref}help [category] or {pref}help [command] for each.
                """
        #Adding the middle of the string, if applicable
        if config.invite:
            final += f"""[Invite {name}!]({invite} "Invite {name}")\n"""
        if website:
            final += f"""[{name} website]({website} "The {name} website")\n"""
        if supportserver:
            final += f"""[Support server]({supportserver} "The {name} support server")\n"""
        #The end of the string
        final += f"""
                Commands: {len(self.context.bot.commands)}
                Here are all the categories:"""

        return final
        
    #When a command is not found
    def command_not_found(self, cmd):
        return f"The command or category '{cmd}' was not found (make sure it's lowercase)."
    
    #Sending the help for a command
    async def send_command_help(self, cmd):
        dest = self.get_destination()

        embed = msg(
          title=self.get_command_signature(cmd) or "Whoops",
          desc=cmd.help or "No help found for this command or category (make sure it's lowercase)."
          )
        await dest.send(embed=embed)
    
    #Sending the main help
    async def send_bot_help(self, mapping):
        dest = self.get_destination()
        opening_note = self.main_help()
        embed = msg(title="Help", desc=opening_note)

        for cog in mapping.keys():
            if cog is not None:
                embed.add_field(name=cogmapping[cog.qualified_name], value=cog.description)
        
        helpmsg = await dest.send(embed=embed)
    
    #Sending the help for a subcommand
    async def send_group_help(self, group):
        dest = self.get_destination()
        commands = group.commands
        commandlist = "Subcommands:"
        for command in commands:
            commandlist += f'\n`{self.get_command_signature(command)}` - {command.brief or "No description"}'
        await dest.send(embed=msg(title="Subcommand " + group.qualified_name, desc=commandlist))
    
    #Sending the help for a cog
    async def send_cog_help(self, cog):
        dest = self.get_destination()
        cmds = cog.get_commands()

        if not cmds:
            embed = msg(title="You can't use any of these commands!")
            return await dest.send(embed=embed)

        desc = cog.description or "No category description"
        name = cog.qualified_name.capitalize()

        formatted_cmds = '\n'.join(
          f'`{self.get_command_signature(c)}` - {c.brief or "No description"}'
          for c in cmds
        )
        
        embed = msg(
          title=name,
          desc=f"""{desc}
                       There are `{len(cmds)}` in this category
                       Commands:
                       {formatted_cmds}"""
          )

        await dest.send(embed=embed)
    
    #When we get an error, oh no!
    async def send_error_message(self, err):
        dest = self.get_destination()
        await dest.send(embed=error(title="Aw man", desc=err))