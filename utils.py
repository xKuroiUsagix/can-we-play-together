import json

from electricity_schedule.constants import WEEKDAYS


def get_token():
    with open('secrets.json') as file:
        secrets = json.load(file)

    return secrets.get('token')

def format_playtime_output(playtime):
    output = '# Оптимальний час щоб пограти, на кожен день тижня:\n'
    
    for day in WEEKDAYS:
        output += f'## {day.capitalize()}:\n'

        for timespans in playtime[day]:
            start = str(timespans[0])[:5]
            finish = str(timespans[1])[:5]
            output += f'{start}  - {finish}\n'
    
    return output
