import discord
import asyncio
import json
import sys
import os
import aiohttp
from discord.ext import commands

TOKEN = os.environ.get("DISCORD_TOKEN_DANMEMO")
_command_prefix = '$'
client = commands.Bot(command_prefix=_command_prefix, help_command=None)

@client.event
async def on_ready():
    ''' () -> None
    This function initializes the bot.
    '''
    print("Bot is ready!")

@client.command()
async def close(ctx):
    # embeded message to show that the bot is shut down
    temp_embed = discord.Embed()
    temp_embed.color = 3066993
    temp_embed.title = "Closed"
    temp_embed.description = "Bot has been successfully closed"
    await ctx.send(embed=temp_embed)
    # shut down the bot
    await client.close()



if __name__ == "__main__":
    # Run the bot
    client.run(TOKEN)
