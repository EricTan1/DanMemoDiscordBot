from commands.utils import getCustomEmoji, getDefaultEmoji

arrow_left = "\u2b05"
arrow_right = "\u27a1"
rewind = "\u23ee"
forward = "\u23ed"
star_emoji = "\u2b50"

attacks_toggle = getDefaultEmoji("crossed_swords")
counters_toggle = getDefaultEmoji("shield")
info_toggle = getDefaultEmoji("information_source")

adventurer_emoji = getCustomEmoji("ad_filter")
assist_emoji = getCustomEmoji("as_filter")
limitbreak_sub_emoji = getCustomEmoji("square_off")
limitbreak_add_emoji = getCustomEmoji("square_on")
hero_ascend_sub_emoji = getCustomEmoji("star_off")
hero_ascend_add_emoji = getCustomEmoji("star_on")
crepe_emoji = getCustomEmoji("crepe")
adventurer_emoji = getCustomEmoji("ad_filter")
assist_emoji = getCustomEmoji("as_filter")
limitbreak_emojis = [getCustomEmoji(f"limitbreak_{number}") for number in range(1, 6)]
