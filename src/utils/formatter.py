from models.activity import Activity
from discord import ActivityType
from datetime import datetime
from loguru import logger

# timeline symbols
TIMELINE_SYMBOL = "-"
TIMELINE_POINTER = "●"
TIMELINE_NUM_SEGMENTS = 20

def get_message_text(act: Activity):
    prefix = get_prefix(act.type)

    if (act.end_time):
        return format_tl_act(act)
    else:
        return format_act(act, prefix)

def get_prefix(type: ActivityType):
    prefix = "⌚"
    if type == ActivityType.playing:
        prefix = "🎮"
    if type == ActivityType.watching:
        prefix = "📺"
    if type == ActivityType.listening:
        prefix = "🎵"
    return prefix
    
def format_act(act: Activity, time_prefix: str) -> str:
    result = []
    
    if act.details:
        result.append(f"- {act.details}")
    if act.state:
        result.append(f"- {act.state}")
    if act.large_text:
        if act.large_url:
            result.append(f"<a href='{act.large_url}'>&gt; {act.large_text}</a>")
        else:
            result.append(f"- {act.large_text}")
    
    result.append(f"\r\n<b>{time_prefix} {act.get_elapsed_time()}</b>")
    
    logger.trace("Activity formatted.")
    return "\n".join(result)


def format_tl_act(act: Activity) -> str:
    parts = []
    
    for _ in range(TIMELINE_NUM_SEGMENTS):
        parts.append(TIMELINE_SYMBOL)
    
    now = datetime.now(act.start_time.tzinfo)
    
    segment_duration = act.track_length // TIMELINE_NUM_SEGMENTS
    pointer_index = (now - act.start_time) // segment_duration
    if pointer_index > len(parts) - 1:
        pointer_index = len(parts) - 1
    parts[pointer_index] = TIMELINE_POINTER
    timeline = "".join(parts)

    result = [f"{act.get_elapsed_time()} {timeline} {act.get_track_length()}"]

    if act.details:
        result.append(f"- {act.details}")
    if act.state:
        result.append(f"- {act.state}")
    if act.large_text:
        if act.large_url:
            result.append(f"<a href='{act.large_url}'>&gt; {act.large_text}</a>")
        else:
            result.append(f"- {act.large_text}")
    
    logger.trace("Activity with timeline formatted.")
    return "\n".join(result)