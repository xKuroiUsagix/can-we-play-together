import json

from electricity_schedule.constants import WEEKDAYS
from translation.utils import get_day_of_week


def get_token():
    with open('secrets.json') as file:
        secrets = json.load(file)

    return secrets.get('token')

def format_playtime_output(playtime, optimal=True):
    if optimal:
        output = '# Спільні зелені зони\n'
    else:
        output = '# Спільні зелені i білі зони\n'
    
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
