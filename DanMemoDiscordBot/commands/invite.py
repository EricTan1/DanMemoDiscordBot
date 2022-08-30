import interactions
from commands.utils import Status


async def run(ctx: interactions.CommandContext):
    embed = interactions.Embed()
    embed.color = Status.KO.value
    embed.title = "Use this link to invite me!"
    embed.description = "https://discord.com/api/oauth2/authorize?client_id=671857934476509195&permissions=378944&scope=bot%20applications.commands"
    await ctx.send(embeds=embed)
