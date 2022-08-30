import interactions
from interactions.ext.files import CommandContext
from interactions.ext.wait_for import WaitForClient
from commands.utils import Status


async def run(client: WaitForClient, ctx: CommandContext):
    for guild in client.guilds:
        print(guild.name)
    embed = interactions.Embed()
    embed.color = Status.OK.value
    embed.title = "Popularity"
    embed.description = f"Ais is currently used in {str(len(client.guilds))} servers. Thank you for your support! ♡"
    embed.set_image(url="attachment://texture.png")
    await ctx.send(
        embeds=embed,
        files=interactions.File(
            "./images/units/Ais (Girl) [Little Princess]/texture.png"
        ),
    )
