import discord
from commands.utils import Status

async def run(ctx):
    embed = discord.Embed()
    embed.color = Status.KO.value
    embed.title = "Use this link to join our support server!\n Also check out our patreon!"
    embed.description = "Support Server: https://discord.gg/b8xGHhm \nPatreon:https://www.patreon.com/aisbot"
    await ctx.send(embed=embed)
