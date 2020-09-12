import discord
from commands.utils import Status

async def run(client,ctx):
    author = str(ctx.message.author)
    authorUniqueId = str(ctx.message.author.id)
    content = ctx.message.content
    
    print("\nReceived message from '"+author+"("+authorUniqueId+")' with content '"+content+"'")

    for guild in client.guilds:
        print(guild.name)
    embed = discord.Embed()
    embed.color = Status.KO.value
    embed.title = "Popularity"
    embed.description= "Ais is currently used in "+str(len(client.guilds))+" servers. Thank you for your support! ♡"
    embed.set_image(url="attachment://texture.png")
    await ctx.send(embed=embed, file=discord.File("./images/units/Ais (Girl) [Little Princess]/texture.png"))

