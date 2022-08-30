import interactions
from interactions.ext.files import CommandContext
from interactions.ext.wait_for import WaitForClient
from commands.utils import Status

USER_ID = 141222596610883584


async def run(client: WaitForClient, ctx: CommandContext, character: str):
    akuno = await client._http.get_user(USER_ID)
    avatar_url = f"https://cdn.discordapp.com/avatars/{USER_ID}/{akuno['avatar']}.png"
    temp_embed = interactions.Embed()
    temp_embed.color = Status.OK.value
    temp_embed.set_author(
        name="Akuno#8965",
        url=f"https://discordapp.com/users/{USER_ID}",
        icon_url=avatar_url,
    )
    temp_embed.set_image(url=f"attachment://{character}.png")
    await ctx.send(
        embeds=temp_embed, files=interactions.File(f"./rbguides/{character}.png")
    )
