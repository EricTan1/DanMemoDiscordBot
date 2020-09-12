import discord
from commands.utils import Status

async def run(ctx):
    embed = discord.Embed()
    embed.color = Status.KO.value
    embed.title = "Use this link to join our support server!"
    embed.description = "https://discord.gg/b8xGHhm"
    await ctx.send(embed=embed)
