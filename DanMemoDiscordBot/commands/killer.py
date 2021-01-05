import discord
import asyncio
import aiohttp

async def run(ctx):
    temp_embed = discord.Embed()
    temp_embed.color = 3066993
    temp_embed.set_author(name="Kami#6669",url="https://discordapp.com",icon_url="https://cdn.discordapp.com/avatars/204693066500538368/a_b277ff1da46965af78fe388cfa991e4c.gif?size=128")
    temp_embed.set_image(url="attachment://slayer.png")
    await ctx.send(embed=temp_embed, file=discord.File("./infographic/killer.png",filename="slayer.png"))