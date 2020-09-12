import discord
from commands.utils import Status

async def run(ctx):
    embed = discord.Embed()
    embed.color = Status.KO.value
    embed.title = "Use this link to invite me!"
    embed.description = "https://top.gg/bot/671857934476509195"
    await ctx.send(embed=embed)
