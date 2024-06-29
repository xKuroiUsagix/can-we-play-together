import pandas as pd

from .constants import POWER_ON, POWER_UKNOWN, START, FINISH, GROUP_NAMES


def _select_timespans(dataframe: pd.DataFrame, power_states=[POWER_ON]):
    """
    This function creates a dictionary where keys are weekdays and values 
    are lists of timespans (tuples) of hours when power state is in power_states list.
    
    Args:
        dataframe (DataFrame): A pandas dataframe of electricity schedule
        power_states (list): An acceptable power states. There are 3 possible states: POWER_OFF, POWER_ON, POWER_UKNOWN
    
    Returns:
        dict: A dictionary of time spans for each weekday where power state is acceptable
        
        dict format:
            {
                'DAY_OF_WEEK': [
                    (datetime.time, datetime.time),
                ],
            }
    """
    playtime = {}

    for row in dataframe.iloc:
        for column in dataframe.columns[2:]:
            if row[column] in power_states:
                timespan = (row[START], row[FINISH])
                playtime.setdefault(column, []).append(timespan)

    return playtime

def _validate_groups(groups: list[str]):
    """
    This function validates groups
    
    Args:
        groups (list): A list of strings, where each string represent a group of electricity schedule
    
    Raises (ValueError):
        if there are less than 2 groups total
        
        if there are group duplicates
        
        if there is no such group as given one(s)
    """
    if len(groups) < 2:
        raise ValueError(f'Need at least 2 different groups. Current groups: {groups}')
    if len(groups) > len(set(groups)):
        raise ValueError('Groups must be unique')
    for group in groups:
        if group.lower() not in GROUP_NAMES:
            raise ValueError(f'Incorrect group: {group}. Avaliable groups are: {GROUP_NAMES}')

def _get_playtime(dataframes: dict, groups: list[str], power_states=[POWER_ON]):
    _validate_groups(groups)
    playtime = _select_timespans(dataframes[groups[0]], power_states)

    for group in groups[1:]:
        for row in dataframes[group].iloc:
            for column in dataframes[group].columns[2:]:
                timespan = (row[START], row[FINISH])
                if (row[column] not in power_states) and (timespan in playtime[column]):
                    playtime[column].remove(timespan)
    
    return playtime

def read_electricity_schedules(file: str) -> dict:
    """
    This function reads excel file with electricity schedules.

    Expected table format:
    ----------------------
    | START_TIME | END_TIME | MONDAY | TUESDAY | WEDNESDAY | THURSDAY | FRIDAY | SATURDAY | SUNDAY |
    | time       | time     | int    | int     | int       | int      | int    | int      | int    |
    
    Args:
        file (str): A path to .excel file with schedules.
    
    Returns:
        dict: A list of pandas.dataframes for each page of excel file
    
    """
    dataframes = {}
    for name in GROUP_NAMES:
        dataframes[name] = pd.read_excel(file, sheet_name=name)
    
    return dataframes

def get_best_playtime(dataframes: dict, groups: list[str]) -> dict:
    """
    This function gives intersections of electricity schedules of different groups
    when there is electricity turned on in all groups at the same time if any.
    
    Args:
        dataframes (dict): A list of pandas.dataframes of electricity schedules
        groups (list): A list of strings of schedule groups
    
    Returns:
        dict: A dictionary of time spans for each weekday where people from groups can play with each other
        
        dict format:
            {
                'DAY_OF_WEEK': [
                    (datetime.time, datetime.time),
                ],
            }
    """
    return _get_playtime(dataframes, groups)

def get_possible_playtime(dataframes: dict, groups: list[str]) -> dict:
    """
    This function gives intersections of electricity schedules of different groups
    when there is electricity turned on or uknown in all groups at the same time if any.
    
    Args:
        dataframes (dict): A list of pandas.dataframes of electricity schedules
        groups (list): A list of strings of schedule groups
    
    Returns:
        dict: A dictionary of time spans for each weekday where people from groups can possibly play with each other
        
        dict format:
            {
                'DAY_OF_WEEK': [
                    (datetime.time, datetime.time),
                ],
            }
    """
    return _get_playtime(dataframes, groups, power_states=[POWER_ON, POWER_UKNOWN])
