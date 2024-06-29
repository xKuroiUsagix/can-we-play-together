import re

import discord
from discord import app_commands
from discord.ext import commands

from utils import get_token, format_playtime_output
from electricity_schedule import groups, constants, features


def main():
    bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
    dataframes = groups.read_electricity_schedules(constants.SCHEDULES_FILE_PATH)
    token = get_token()
    
    @bot.event
    async def on_ready():
        try:
            synced = await bot.tree.sync()
            total_commands = len(synced)
            print(f'Synced {total_commands} command(s)')
        except Exception as e:
            print(e)
    
    @bot.tree.command(name='hello')
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message('Hello World!')
    
    @bot.tree.command(name='can-we-play')
    @app_commands.describe(groups_input='Power outage of groups separated by space. For example: 2.1 1.1 3.3')
    async def can_we_play(interaction: discord.Interaction, groups_input: str):
        modified_input = groups_input.strip().lower()
        
        if not groups_valid(modified_input):
            await interaction.response.send_message('Your input was not valid.')
            return

        splited_groups = modified_input.split()

        try:
            best_playtime = groups.get_best_playtime(dataframes, splited_groups)
        except ValueError as e:
            await interaction.response.send_message(e)
            return
        
        combined = features.combine_timespans(best_playtime)
        formated = format_playtime_output(combined)
        
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
