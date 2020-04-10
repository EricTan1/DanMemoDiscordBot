import discord
import json

from database.DBcontroller import DBcontroller
from commands.utils import imageHorizontalConcat, imageVerticalConcat

async def run(dbConfig, client, ctx, *search):
    with open('./dispatchQuest/dispatch.json', 'r') as f:
        dispatch_dict = json.load(f)
    db = DBcontroller(dbConfig)
    message = ""
    my_search = ""
    for words in search:
        my_search= my_search + words + " "
    ret_list = db.dispatchSearch(my_search)
    discord_file_list = []
    temp_embed = discord.Embed()    
    for ret in ret_list:
        char_list = [ret[4],ret[5],ret[6],ret[7]]
        file_list = []
        for char in char_list:
            print(dispatch_dict)
            print(char)
            try:
                file_list.append("./lottery/"+dispatch_dict.get(char)+"/hex.png")
            except:
                file_list.append("./lottery/gac_dummy/hex.png")
        if(ret[2]== None):
            temp_embed.add_field(name="{} - {}:".format(ret[1],ret[3]), value="{}, {}, {}, {}".format(ret[4],ret[5],ret[6],ret[7]), inline=False)
        else:
            #message = message + "{} - {} {}: {}, {}, {}, {}\n".format(ret[1],ret[2],ret[3],ret[4],ret[5],ret[6],ret[7])
            temp_embed.add_field(name="{} - {} {}:".format(ret[1],ret[2],ret[3]), value="{}, {}, {}, {}".format(ret[4],ret[5],ret[6],ret[7]), inline=False)
        await imageHorizontalConcat(client,file_list,discord_file_list)
    icons = await imageVerticalConcat(client,discord_file_list)
    temp_embed.color = 3066993
    temp_embed.title = "{} results for {}".format(len(ret_list),search)
    #temp_embed.description = message
    temp_embed.set_image(url="attachment://temp.png")
    try:
        msg = await ctx.send(embed=temp_embed, file=discord.File(icons, filename="temp.png"))
    except:
        temp_embed = discord.Embed()
        temp_embed.color = 16203840
        temp_embed.title = "Unable to find dispatch quest or too many dispatch quests"
        temp_embed.description= "Please narrow it down further"
        await ctx.send(embed=temp_embed)        
