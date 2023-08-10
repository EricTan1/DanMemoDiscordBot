from interactions import Embed, SlashContext

from commands.utils import Status


async def run(ctx: SlashContext):
    """direct message the help command to that user"""
    temp_embed = Embed()
    temp_embed.color = Status.KO.value
    temp_embed.title = "Commands List"
    with open("./help.txt") as fp:
        line = fp.readline()

        while line:
            if line.strip() == "F":
                line = fp.readline()
                name = line
                value = ""
                line = fp.readline()
                while line.strip() != "F" and line.strip() != "E":
                    value = value + line
                    line = fp.readline()
                temp_embed.add_field(name=name, value=value)
            elif line.strip() == "E":
                break
        temp_embed.set_thumbnail(
            url="https://static.myfigurecollection.net/pics/figure/large/571996.jpg"
        )

    await ctx.author.send(embeds=temp_embed)
    await ctx.send("Sent info to your DM!")
