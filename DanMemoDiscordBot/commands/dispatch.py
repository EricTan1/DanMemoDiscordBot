import interactions
from interactions.ext.files import CommandContext
import json

from database.DBcontroller import DBConfig, DBcontroller
from commands.utils import Status, imageHorizontalConcat, imageVerticalConcat


async def run(dbConfig: DBConfig, ctx: CommandContext, search_words: str):
    """searchs for the relevant dispatch quest

    Arguments:
        ctx {interactions.ext.files.CommandContext} -- context of the message
        search {string} -- the dispatch quest to search for
    """
    # to tell Discord this command may take longer than the default 3s timeout
    await ctx.defer()

    with open("./dispatchQuest/dispatch.json", "r") as f:
        dispatch_dict = json.load(f)
    db = DBcontroller(dbConfig)

    search = search_words.split()
    my_search = ""
    for words in search:
        my_search += words + " "

    ret_list = db.dispatchSearch(my_search)
    discord_file_list = []
    temp_embed = interactions.Embed()
    for ret in ret_list:
        char_list = [ret[4], ret[5], ret[6], ret[7]]
        file_list = []
        for char in char_list:
            try:
                file_list.append("./lottery/" + dispatch_dict.get(char) + "/hex.png")
            except:
                file_list.append("./lottery/gac_dummy/hex.png")
        if ret[2] == None:
            temp_embed.add_field(
                name=f"{ret[1]} - {ret[3]}:",
                value=f"{ret[4]}, {ret[5]}, {ret[6]}, {ret[7]}",
                inline=False,
            )
        else:
            temp_embed.add_field(
                name=f"{ret[1]} - {ret[2]} {ret[3]}:",
                value=f"{ret[4]}, {ret[5]}, {ret[6]}, {ret[7]}",
                inline=False,
            )
        img = imageHorizontalConcat(file_list)
        discord_file_list.append(img)
    icons = imageVerticalConcat(discord_file_list)
    temp_embed.color = Status.OK.value
    temp_embed.title = f"{len(ret_list)} result(s) for {search}"
    temp_embed.set_image(url="attachment://temp.png")
    try:
        await ctx.send(
            embeds=temp_embed, files=interactions.File(fp=icons, filename="temp.png")
        )
    except:
        temp_embed = interactions.Embed()
        temp_embed.color = Status.KO.value
        temp_embed.title = "Unable to find dispatch quest or too many dispatch quests"
        temp_embed.description = "Please narrow it down further"
        await ctx.send(embeds=temp_embed)
