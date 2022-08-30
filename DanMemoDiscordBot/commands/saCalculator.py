from types import SimpleNamespace
from typing import Optional, List
import interactions
from interactions.ext.wait_for import WaitForClient
from interactions.ext.files import CommandContext

# WANT TO CONNECT THIS TO DB SO CAN BE ANY SA_GAUGE
from commands.cache import Cache
from commands.utils import Status


async def run(
    client: WaitForClient,
    ctx: CommandContext,
    config_file: Optional[interactions.Attachment],
):
    # check if there is attachment if not send them a template attachment
    if not config_file:
        await ctx.send(
            "For this to work, you need to download the file, edit it, and reupload it into the channel with ais bot in it with the description /sa-calculator",
            files=interactions.File("sacalc.txt"),
        )
    else:
        # if template attached start to verify it
        # attachment object only contains the URL, so have to download it first
        async with client._http._req._session.get(config_file.url) as request:
            contents = await request.content.read()
        contents_decode = contents.decode("utf-8").split("\n")
        positions: List[List[int]] = [[], [], [], []]
        errors = ""
        turns = 0
        for line in contents_decode:
            print(line)
            # buff wipe verify
            stripped_line = line.strip()
            if stripped_line.startswith("BUFF_WIPE="):
                stripped_line = stripped_line.replace("BUFF_WIPE=", "")
                # do you want the buffs to be wiped
                if stripped_line.lower() == "false":
                    is_revis = True
                elif stripped_line.lower() == "true":
                    is_revis = False
                else:
                    errors += "Buff wipe is not True or False\n"
            # adventurer title format list
            elif stripped_line.startswith("ADVENTURER="):
                stripped_line = stripped_line.replace("ADVENTURER=", "")
                adventurer_order = stripped_line.split(",")
                if len(adventurer_order) != 6:
                    errors += "Unable to read adventurer, make sure there are exactly 5 commas\n"
            # assist title format list
            elif stripped_line.startswith("ASSIST="):
                stripped_line = stripped_line.replace("ASSIST=", "")
                assists_order = stripped_line.split(",")
                if len(assists_order) != 6:
                    errors += (
                        "Unable to read assist, make sure there are exactly 5 commas\n"
                    )
            elif stripped_line.startswith("TURNS="):
                stripped_line = stripped_line.replace("TURNS=", "")
                try:
                    turns = int(stripped_line)
                except:
                    errors += "Make sure turns are numeric"
            # Turn orders for non sacs
            else:
                for position in range(4):
                    line_start = f"P{position+3}="
                    if stripped_line.startswith(line_start):
                        stripped_line = stripped_line.replace(line_start, "").replace(
                            "||", ","
                        )
                        try:
                            positions[position] = verifyAndCast(
                                stripped_line.split(",")
                            )
                            if len(positions[position]) != turns:
                                errors += f"Unable to read turn order, make sure there are exactly {turns-1} commas you specify TURNS before the turn order\n"
                        except:
                            errors += "Make sure turn orders are numeric and it is either separated by commas or \|\|\n"
        # error handling
        if errors == "":
            await calculate(
                ctx, is_revis, adventurer_order, assists_order, positions, turns
            )
        else:
            temp_embed = interactions.Embed()
            temp_embed.color = Status.KO.value
            temp_embed.title = "ERROR"
            temp_embed.description = errors
            await ctx.send(embeds=temp_embed)


def verifyAndCast(my_list: List[str]) -> List[int]:
    ret = []
    print(my_list)
    for items in my_list:
        ret.append(int(items))
    return ret


# Speed Tier needs to be added and calcs need to happen at buff phase
async def calculate(
    ctx: CommandContext,
    is_revis: bool,
    adventurer_turns: List[str],
    assist_turns: List[str],
    positions: List[List[int]],
    turns: int,
):
    curr_message = ""
    cache = Cache()
    # 1,2 = sacs in order aka index 0 and 1
    current_turn = 0
    mlb_assists = [False, False, False, False, False, False]
    assist_order: List[List[SimpleNamespace]] = []
    adventurer_order: List[List[SimpleNamespace]] = []

    for x in range(len(assist_turns)):
        temp_order = assist_turns[x].lower()
        if "mlb" in temp_order:
            mlb_assists[x] = True
            temp_order = temp_order.replace("mlb", "").strip()

        skill = [
            skilleffect
            for skilleffect in cache.get_assist_sa_gauge()
            if temp_order == skilleffect.title.lower().strip()
        ]
        if len(skill) > 0:
            assist_order.append(skill)
        else:
            assist_order.append([])

    for x in range(len(adventurer_turns)):
        skill = [
            skilleffect
            for skilleffect in cache.get_adventurer_sa_gauge()
            if adventurer_turns[x].lower().strip() == skilleffect.title.lower().strip()
        ]
        if len(skill) > 0:
            adventurer_order.append(skill)
        else:
            adventurer_order.append([])

    # party members turn order
    add_on = [0] * turns
    p1 = [1] + add_on
    p2 = [2] + add_on

    turn_orders = [p1, p2] + positions
    # base sa gauge current buffs
    sa_gauge_adv = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    sa_gauge_as = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    # every 14 = 1 full charge
    current_sa_gauge = 0.0
    while current_turn < turns:
        curr_message = curr_message + f"**Start of turn {current_turn+1}**\n"
        # WIPE BUFFS FOR FINN,OTTARL,RIVERIA TURN 4/8
        if (current_turn == 3 or current_turn == 7) and is_revis == False:
            print("buffs wiped")
            sa_gauge_adv = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        # first sac
        if current_turn == 0:
            # APPLY ASSIST BUFFS t1 (first 4 assists) 0 = not mlb 1 = mlb
            for index in [0, 2, 3, 4]:
                calculate_assist_sa_gauge(
                    assist_order, mlb_assists, sa_gauge_as, [0, 2, 3, 4], index
                )
        # second sac
        elif current_turn == 1:
            calculate_assist_sa_gauge(
                assist_order, mlb_assists, sa_gauge_as, list(range(1, 5)), 1
            )
        # last person comes in
        elif current_turn == 2:
            calculate_assist_sa_gauge(
                assist_order, mlb_assists, sa_gauge_as, list(range(2, 6)), 5
            )
        # calculate adventurers SA gauge
        for index in range(len(adventurer_order)):
            if adventurer_order[index]:
                adv_skill = adventurer_order[index][0]
                adv_mod = int(adv_skill.modifier) / 100
                if adv_skill.target.lower() == "self":
                    if not (
                        turn_orders[index][current_turn] != 4
                        and adv_skill.skilltype.lower() == "special"
                    ):
                        if sa_gauge_adv[index] < adv_mod:
                            sa_gauge_adv[index] = adv_mod
                elif adv_skill.target.lower() == "allies":
                    if current_turn == 0 and index == 0:
                        for x in [0, 2, 3, 4]:
                            if sa_gauge_adv[x] < adv_mod:
                                sa_gauge_adv[x] = adv_mod
                        if sa_gauge_adv[0] < adv_mod:
                            sa_gauge_adv[0] = adv_mod
                    elif current_turn == 1 and index == 1:
                        for x in range(1, 5):
                            if sa_gauge_adv[x] < adv_mod:
                                sa_gauge_adv[x] = adv_mod
                        if sa_gauge_adv[1] < adv_mod:
                            sa_gauge_adv[1] = adv_mod
                    # ignore first and second adv now since not their turn
                    elif index != 0 and index != 1:
                        for x in range(2, 6):
                            if sa_gauge_adv[x] < adv_mod:
                                sa_gauge_adv[x] = adv_mod
        if current_turn == 0:
            current_sa_gauge = current_sa_gauge + sa_gauge_adv[0] + sa_gauge_as[0] + 1
            current_sa_gauge = round(current_sa_gauge, 1)
        if current_turn == 1:
            current_sa_gauge = current_sa_gauge + sa_gauge_adv[1] + sa_gauge_as[1] + 1
            current_sa_gauge = round(current_sa_gauge, 1)

        for x in range(2, 5):
            if turn_orders[x][current_turn] != 4:
                current_sa_gauge = (
                    current_sa_gauge + sa_gauge_adv[x] + sa_gauge_as[x] + 1
                )
                current_sa_gauge = round(current_sa_gauge, 1)
            else:
                curr_message = curr_message + f"MEMBER {x+1} SA THIS TURN\n"
                current_sa_gauge = current_sa_gauge - 14
        # last person who comes in after 2 sacs
        if turn_orders[-1][current_turn] != 4 and current_turn > 1:
            current_sa_gauge = current_sa_gauge + sa_gauge_adv[5] + sa_gauge_as[5] + 1
            current_sa_gauge = round(current_sa_gauge, 1)
        elif turn_orders[-1][current_turn] == 4 and current_turn > 1:
            curr_message = curr_message + "MEMBER 6 SA THIS TURN\n"
            current_sa_gauge = current_sa_gauge - 14
        # 4 SA hard cap
        if current_sa_gauge > 56:
            current_sa_gauge = 56
        curr_message = curr_message + f"Adv: {sa_gauge_adv}\n"
        curr_message = curr_message + f"As: {sa_gauge_as}\n"
        curr_message = (
            curr_message
            + f"End of turn {current_turn+1} with SA gauge charge {round(current_sa_gauge/14,2)}\n\n"
        )
        current_turn = current_turn + 1
    # SA CALC
    temp_embed = interactions.Embed()
    temp_embed.color = Status.OK.value
    temp_embed.title = "SA Calculator"
    temp_embed.description = curr_message
    await ctx.send(embeds=temp_embed)


def calculate_assist_sa_gauge(
    assists_order: List[List[SimpleNamespace]],
    mlb_assists: List[bool],
    charge_buffs: List[float],
    positions: List[int],
    self_pos: int,
):
    if assists_order[self_pos]:
        if mlb_assists[self_pos]:
            assist_skill = assists_order[self_pos][1]
        else:
            assist_skill = assists_order[self_pos][0]
        curr_mod = int(assist_skill.modifier) / 100
        if assist_skill.target.lower() == "self":
            if charge_buffs[self_pos] < curr_mod:
                charge_buffs[self_pos] = curr_mod
        elif assist_skill.target.lower() == "allies":
            for x in positions:
                if charge_buffs[x] < curr_mod:
                    charge_buffs[x] = curr_mod
