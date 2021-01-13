#This is BananaBot's configuration.

#Imports
from discord import Activity

#This is the bot's main token. If you don't have a token, BananaBot won't work.
token = "my-epic-token"

#This is the bot's developer token, for if the bot is running on the development PC. Set it to None (and set "devpc" to None) if you don't want a dev PC.
devtoken = "another-epic-token"

#This is the name of the computer that launches the development bot instead of the main one. Set it to None if you don't want a development bot.
#Use "socket.gethostname()" to find the name of your computer
devpc = "a-nice-computer"

#This is the support server link. Set it to None fSor no support server.
supportserver = "https://discord.gg/yee"

#This is the bot's website. Set it to None for no website.
website = "https://www.youtube.com/watch?v=DLzxrzFCyOs"

#This toggles whether you want the bot invite to be displayd on the help page.
invite = False

#This is the prefix, or prefixes. It can be a string, or a list of strings.
prefix = [">", "bb "]

#This is the developer prefix, for the developer bot. It can be a string, or a list of strings.
devprefix = ">>"

#This is the Discord webhook URL where suggestions will be sent.
sugurl = "https://ptb.discord.com/api/webhooks/lorem/ipsum/dolor/sit/amet"

#This is BananaBot's startup activity
activity = Activity(name=">help", type=3)

#This is your Genius API token.
genius = "geniuscuzimsmart"

#This is your Pixabay API token
pixabay = "thebayofpixes"

#This is your Giphy API token
giphy = "ihatetenor"

#This is your cat API (thecatapi.com) token
catapi = 'meeeeeeeeow'

#This your NASA API token
nasa = "nasaiscool"
