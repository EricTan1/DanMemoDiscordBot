from interactions.ext.files import CommandContext


async def run(ctx: CommandContext):
    clan_list_name = []
    clan_list_id = []
    # loop for everyone in the list imanity discord server member list and check for role: 803388556180455424
    for member in ctx.guild.members:
        # record their names and player id
        for roles in member.roles:
            if roles.id == 708008774140690473:
                if member.nick is None:
                    # clan_list.append([member.id,member.name])
                    clan_list_name.append([member.name])
                else:
                    # clan_list.append([member.id,member.nick])
                    clan_list_name.append([member.nick])
                clan_list_id.append([str(member.id)])

    print(clan_list_name)
    for names in clan_list_name:
        print(names[0])
    for ids in clan_list_id:
        print(ids[0])
    print(clan_list_id)

    print(len(clan_list_name))

    await ctx.send("Command executed successfully", ephemeral=True)
