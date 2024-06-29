import json

from electricity_schedule.constants import WEEKDAYS
from translation.utils import get_day_of_week


def get_token():
    with open('secrets.json') as file:
        secrets = json.load(file)

    return secrets.get('token')

def format_playtime_output(playtime, groups, green_only=True):
    if green_only:
        output = f'## Спільні зелені зони для груп: `{groups}`\n'
    else:
        output = f'## Спільні зелені i білі зони для груп: `{groups}`\n'
    
    for day in WEEKDAYS:
        if len(playtime[day]) == 0:
            continue
        
        translated_day = get_day_of_week(day)
        if translated_day == False:
            translated_day = day

        output += f'> **{translated_day.capitalize()}**\n'
        output += '```'
        for timespans in playtime[day]:
            start = str(timespans[0])[:5]
            finish = str(timespans[1])[:5]
            output += f'{start} - {finish}\n'
        output += '```\n'
    
    return output
