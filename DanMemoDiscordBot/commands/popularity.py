from interactions import Client, Embed, File, SlashContext

from commands.utils import Status


async def run(client: Client, ctx: SlashContext):
    for guild in client.guilds:
        print(guild.name)
    embed = Embed()
    embed.color = Status.OK.value
    embed.title = "Popularity"
    embed.description = f"Ais is currently used in {str(len(client.guilds))} servers. Thank you for your support! ♡"
    embed.set_image(url="attachment://texture.png")
    await ctx.send(
        embeds=embed,
        files=File("./images/units/Ais (Girl) [Little Princess]/texture.png"),
    )
