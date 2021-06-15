import discord
from discord.ext import commands
import asyncio
import json
import datetime
import logging

# Setting up logging
logger = logging.getLogger('discord')
#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Loading config.json file
with open('./config.json','r') as c_json:
    config = json.load(c_json)
c_json.close()


# Setting up the Bot
desc = '''katy bot v2'''
prefix = '!'
bot = commands.Bot(command_prefix = prefix, description = desc)
bot.allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True)

# Defining cogs
cogs = [
    'cogs.greetings',
    'cogs.vote',
]

# Loading Cogs
for cog in cogs:
    try:
        bot.load_extension(cog)
    except Exception as e:
        print('{} failed to load.\n{}: {}'.format(cog, type(e).__name__, e))

# Introductory message
@bot.event
async def on_ready():
    for server in bot.guilds:
        print("[{}] has started in server [{}] with [{:,}] members.".format(
        bot.user.name, server.name, server.member_count))

# Run the Bot
bot.run(config['disc']['token'])
