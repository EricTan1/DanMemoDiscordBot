import discord

async def run(ctx):
    embed = discord.Embed()
    embed.color = 16203840
    embed.title = "Use this link to invite me!"
    embed.description= "https://top.gg/bot/671857934476509195"
    await ctx.send(embed=embed)
