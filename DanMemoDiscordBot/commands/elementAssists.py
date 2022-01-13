import discord

async def run(ctx):
    temp_embed = discord.Embed()
    temp_embed.color = 3066993
    temp_embed.set_image(url="attachment://slayer.png")
    await ctx.send(embed=temp_embed, file=discord.File("./infographic/elementAssists.png",filename="slayer.png"))