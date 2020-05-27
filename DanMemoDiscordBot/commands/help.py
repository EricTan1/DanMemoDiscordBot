import discord
import os

async def run(ctx):
    """direct message the help command to that user

    Arguments:
        ctx {discord.context} -- the message context object
    """
    temp_embed = discord.Embed()
    temp_embed.color = 3066993
    temp_embed.title = "Command List"
    with open('./help.txt') as fp:
        line = fp.readline()
        print(line.strip())
        
        while(line):
            print(line.strip())
            if(line.strip() =="F"):
                line = fp.readline()
                name = line
                value = ""
                line = fp.readline()
                while line.strip() !="F" and line.strip() !="E":
                    value = value + line
                    line = fp.readline()
                temp_embed.add_field(name=name, value=value, inline=False)
            elif(line.strip()=="E"):
                break;
        temp_embed.set_thumbnail(url="https://static.myfigurecollection.net/pics/figure/large/571996.jpg")
    await ctx.author.send(embed=temp_embed)
    await ctx.send("Sent info to your DM!")