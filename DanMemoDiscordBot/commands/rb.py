from interactions import Client, Embed, File, SlashContext

from commands.utils import Status

USER_ID = 141222596610883584


async def run(client: Client, ctx: SlashContext, character: str):
    akuno = await client.fetch_user(USER_ID)
    assert akuno
    temp_embed = Embed()
    temp_embed.color = Status.OK.value
    temp_embed.set_author(
        name="Akuno#8965",
        url=f"https://discordapp.com/users/{USER_ID}",
        icon_url=akuno.display_avatar.url,
    )
    temp_embed.set_image(url=f"attachment://{character}.png")
    await ctx.send(embeds=temp_embed, files=File(f"./rbguides/{character}.png"))
