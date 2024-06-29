import re

import discord
from discord import app_commands
from discord.ext import commands

from electricity_schedule import schedule, features
from electricity_schedule.constants import SCHEDULES_FILE_PATH

from utils import get_token, format_playtime_output
from descriptions import GROUPS_DECSRIPTION, GREEN_ONLY_DESCRIPTION


def main():
    bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
    dataframes = schedule.read_electricity_schedules(SCHEDULES_FILE_PATH)
    token = get_token()

    @bot.event
    async def on_ready():
        try:
            synced = await bot.tree.sync()
            print(f'Synced {len(synced)} command(s)')
        except Exception as e:
            print(e)

    @bot.tree.command(name='compare')
    @app_commands.describe(groups=GROUPS_DECSRIPTION, green_only=GREEN_ONLY_DESCRIPTION)
    async def compare_schedules(interaction: discord.Interaction, groups: str, green_only: bool=True):
        modified_input = groups.strip().lower()

        if not groups_valid(modified_input):
            await interaction.response.send_message('Your input was not valid.')
            return

        splited_groups = modified_input.split()

        try:
            if green_only:
                playtime = schedule.get_best_playtime(dataframes, splited_groups)
            else:
                playtime = schedule.get_possible_playtime(dataframes, splited_groups)
        except ValueError as e:
            await interaction.response.send_message(e)
            return

        combined = features.combine_timespans(playtime)
        formated = format_playtime_output(combined, groups, green_only)

        await interaction.response.send_message(formated)

    bot.run(token)

def groups_valid(groups_input: str) -> bool:
    # Pattern Explanation:
    # Select decimal numbers with singular digits like 1.1, 1.2, 1.3 ...
    # Also select whitespace after first occurance of that decimal number + another decimal number of that format
    # This regexp should have full match for string like: "1.2 2.3 3.1 1.1"
    pattern = re.compile(r'([0-9]{1}\.[0-9]{1}( [0-9]{1}\.[0-9]{1})+)')
    
    return True if re.fullmatch(pattern, groups_input) else False

if __name__ == '__main__':
    main()
