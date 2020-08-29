import discord

async def run(ctx):
    embed = discord.Embed()
    embed.color = 16203840
    embed.title = "Use this link to join our support server!"
    embed.description= "https://discord.gg/b8xGHhm"
    await ctx.send(embed=embed)
