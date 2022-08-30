import interactions
from commands.utils import Status


async def run(ctx: interactions.CommandContext):
    embed = interactions.Embed()
    embed.color = Status.KO.value
    embed.title = (
        "Use this link to join our support server!\nAlso check out our patreon!"
    )
    embed.description = "Support Server: https://discord.gg/b8xGHhm \nPatreon: https://www.patreon.com/aisbot"
    await ctx.send(embeds=embed)
