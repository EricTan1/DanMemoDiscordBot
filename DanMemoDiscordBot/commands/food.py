import discord

async def run(ctx):
    temp_embed = discord.Embed()
    temp_embed.color = 3066993
    temp_embed.title = "Here is your bento box for today!"
    temp_embed.set_image(url="attachment://texture.png")
    await ctx.send(embed=temp_embed, file=discord.File("./lottery/A Loving Lunch Syr Flover/texture.png"))
