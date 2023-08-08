import json

from interactions import Embed, File, SlashContext

from commands.utils import Status, imageHorizontalConcat, imageVerticalConcat
from database.DBcontroller import DBConfig, DBcontroller


async def run(dbConfig: DBConfig, ctx: SlashContext, search_words: str):
    """searchs for the relevant dispatch quest

    Arguments:
        ctx -- context of the message
        search_words -- the dispatch quest to search for
    """
    with open("./dispatchQuest/dispatch.json", "r") as f:
        dispatch_dict = json.load(f)
    db = DBcontroller(dbConfig)

    search = search_words.split()
    my_search = ""
    for words in search:
        my_search += words + " "

    ret_list = db.dispatchSearch(my_search)
    discord_file_list = []
    temp_embed = Embed()
    for ret in ret_list[:23]:  # can only put 25 fields on Embed
        char_list = [ret[4], ret[5], ret[6], ret[7]]
        file_list = []
        for char in char_list:
            try:
                file_list.append("./lottery/" + dispatch_dict[char] + "/hex.png")
            except:
                file_list.append("./lottery/gac_dummy/hex.png")
        if ret[2] is None:
            temp_embed.add_field(
                name=f"{ret[1]} - {ret[3]}:",
                value=f"{ret[4]}, {ret[5]}, {ret[6]}, {ret[7]}",
            )
        else:
            temp_embed.add_field(
                name=f"{ret[1]} - {ret[2]} {ret[3]}:",
                value=f"{ret[4]}, {ret[5]}, {ret[6]}, {ret[7]}",
            )
        img = imageHorizontalConcat(file_list)
        discord_file_list.append(img)
    if len(ret_list) > 24:
        temp_embed.add_field(
            name="Cannot display more results",
            value="Please try a more specific search",
        )
    icons = imageVerticalConcat(discord_file_list)
    temp_embed.color = Status.OK.value
    temp_embed.title = f"{len(ret_list)} result(s) for {search}"
    temp_embed.set_image(url="attachment://temp.png")
    try:
        await ctx.send(embeds=temp_embed, files=File(icons, file_name="temp.png"))
    except:
        temp_embed = Embed()
        temp_embed.color = Status.KO.value
        temp_embed.title = "Unable to find dispatch quest or too many dispatch quests"
        temp_embed.description = "Please narrow it down further"
        await ctx.send(embeds=temp_embed)
