import interactions
from commands.utils import get_emoji, getDefaultEmoji

# emojis
arrow_left = '\u2b05'
arrow_right = '\u27a1'
rewind = '\u23ee'
forward = '\u23ed'
attacks_toggle = getDefaultEmoji("crossed_swords")
counters_toggle = getDefaultEmoji("shield")
info_toggle = getDefaultEmoji("information_source")
adventurer_emoji = get_emoji("ad_filter")
assist_emoji = get_emoji("as_filter")
limitbreak_sub_emoji = get_emoji("square_off")
limitbreak_add_emoji = get_emoji("square_on")
hero_ascend_sub_emoji = get_emoji("star_off")
hero_ascend_add_emoji = get_emoji("star_on")

# buttons
previous_page = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label=arrow_left,
    custom_id="previous_page"
)
next_page = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label=arrow_right,
    custom_id="next_page"
)
to_start = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label=rewind,
    custom_id="to_start"
)
to_end = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label=forward,
    custom_id="to_end"
)
filter_adventurer = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    emoji=adventurer_emoji,
    custom_id="filter_adventurer"
)
filter_assist = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    emoji=assist_emoji,
    custom_id="filter_assist"
)
limitbreak_sub_button = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    emoji=limitbreak_sub_emoji,
    custom_id="limitbreak_sub"
)
limitbreak_add_button = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    emoji=limitbreak_add_emoji,
    custom_id="limitbreak_add"
)
hero_ascend_sub_button = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    emoji=hero_ascend_sub_emoji,
    custom_id="hero_ascend_sub"
)
hero_ascend_add_button = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    emoji=hero_ascend_add_emoji,
    custom_id="hero_ascend_add"
)
toggle_combat = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label=attacks_toggle,
    custom_id="toggle_combat"
)
toggle_counters = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label=counters_toggle,
    custom_id="toggle_counters"
)
toggle_effects = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label=info_toggle,
    custom_id="toggle_effects"
)
