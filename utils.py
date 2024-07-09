import json

from electricity_schedule.constants import WEEKDAYS, LAST_SCHEDULE_UPDATE
from translation.utils import get_day_of_week


def get_token():
    with open('secrets.json') as file:
        secrets = json.load(file)

    return secrets.get('token')

def is_playtime_exists(playtime):
    for day in WEEKDAYS:
        if len(playtime[day]) > 0:
            return True
    return False

def format_playtime_output(playtime, groups, green_only=True):
    output = f'## Графіки оновлені: {LAST_SCHEDULE_UPDATE}\n'

    gree_or_not = 'зелені' if green_only else 'зелені i білі'
    exists_or_not = '' if is_playtime_exists(playtime) else ' - відсутні'
    
    output += f'## Спільні {gree_or_not} зони для груп: `{groups}`{exists_or_not}\n'

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
