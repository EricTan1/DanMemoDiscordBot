import discord
import asyncio
import aiohttp

async def run(ctx, character):
    rb_list = ["ottarl","revis","riveria", "finn","ottar"]
    if character.lower() in rb_list:
        if(character.lower() == "ottar"):
            character = "ottarl"
        temp_embed = discord.Embed()
        temp_embed.color = 3066993
        temp_embed.set_author(name="Akuno#8965",url="https://discordapp.com",icon_url="https://cdn.discordapp.com/avatars/141222596610883584/0e51b4be33b83b17a4c98ceb381bda85.png?size=128")
        temp_embed.set_image(url="attachment://rb.png")
        await ctx.send(embed=temp_embed, file=discord.File("./rbguides/" + character.lower()+ ".png",filename="rb.png"))
    else:
        temp_embed = discord.Embed()
        temp_embed.color = 16203840
        temp_embed.title = "No character found"
        temp_embed.description= "There doesn't exist an RB for this character. Please search either: Ottar/Otarrl, Revis, Riveria or Finn"
        await ctx.send(embed=temp_embed)
        