from interactions import Button, ButtonStyle

# emojis
from commands.emojis import (
    adventurer_emoji,
    arrow_left,
    arrow_right,
    assist_emoji,
    attacks_toggle,
    counters_toggle,
    forward,
    hero_ascend_add_emoji,
    hero_ascend_sub_emoji,
    info_toggle,
    limitbreak_add_emoji,
    limitbreak_sub_emoji,
    rewind,
)

previous_page = Button(
    style=ButtonStyle.PRIMARY, label=arrow_left, custom_id="previous_page"
)
next_page = Button(style=ButtonStyle.PRIMARY, label=arrow_right, custom_id="next_page")
to_start = Button(style=ButtonStyle.PRIMARY, label=rewind, custom_id="to_start")
to_end = Button(style=ButtonStyle.PRIMARY, label=forward, custom_id="to_end")
filter_adventurer = Button(
    style=ButtonStyle.PRIMARY,
    emoji=adventurer_emoji,
    custom_id="filter_adventurer",
)
filter_assist = Button(
    style=ButtonStyle.PRIMARY,
    emoji=assist_emoji,
    custom_id="filter_assist",
)
limitbreak_sub_button = Button(
    style=ButtonStyle.PRIMARY,
    emoji=limitbreak_sub_emoji,
    custom_id="limitbreak_sub",
)
limitbreak_add_button = Button(
    style=ButtonStyle.PRIMARY,
    emoji=limitbreak_add_emoji,
    custom_id="limitbreak_add",
)
hero_ascend_sub_button = Button(
    style=ButtonStyle.PRIMARY,
    emoji=hero_ascend_sub_emoji,
    custom_id="hero_ascend_sub",
)
hero_ascend_add_button = Button(
    style=ButtonStyle.PRIMARY,
    emoji=hero_ascend_add_emoji,
    custom_id="hero_ascend_add",
)
toggle_combat = Button(
    style=ButtonStyle.PRIMARY,
    label=attacks_toggle,
    custom_id="toggle_combat",
)
toggle_counters = Button(
    style=ButtonStyle.PRIMARY,
    label=counters_toggle,
    custom_id="toggle_counters",
)
toggle_effects = Button(
    style=ButtonStyle.PRIMARY,
    label=info_toggle,
    custom_id="toggle_effects",
)
