import interactions

from commands.utils import Status


async def run(ctx: interactions.CommandContext, args: str = None):
    """direct message the help command to that user

    Arguments:
        ctx {interactions.context} -- the message context object
        args {str} -- "server" if help message should be sent to the server instead of the user.
    """
    temp_embed = interactions.Embed()
    temp_embed.color = Status.KO.value
    temp_embed.title = "Commands List"
    with open("./help.txt") as fp:
        line = fp.readline()
        # print(line.strip())

        while line:
            # print(line.strip())
            if line.strip() == "F":
                line = fp.readline()
                name = line
                value = ""
                line = fp.readline()
                while line.strip() != "F" and line.strip() != "E":
                    value = value + line
                    line = fp.readline()
                temp_embed.add_field(name=name, value=value, inline=False)
            elif line.strip() == "E":
                break
        temp_embed.set_thumbnail(
            url="https://static.myfigurecollection.net/pics/figure/large/571996.jpg"
        )

    if args == "server":
        await ctx.send(embeds=temp_embed)
    else:
        await ctx.author.send(embeds=temp_embed)
        await ctx.send("Sent info to your DM!")
