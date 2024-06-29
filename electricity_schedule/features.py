import datetime
import copy


def selected_time(playtime: dict, start_time: datetime.time):
    """
    This function filter timespans by given start and end time.
    
    Args:
        playtime (dict): A dictionary where keys are days of week and
        values are lists of tuples with format (datetime.time, datetime.time)
        
        start_time (datetime.time): A time value in 24-hour format
        
    """
    filtered_timespans = {}

    for day_of_week, timespan in playtime.items():
        new_timespans = []

        for ts in timespan:
            if ts[0] >= start_time:
                new_timespans.append(ts)

        filtered_timespans[day_of_week] = new_timespans
    
    return filtered_timespans

def combine_timespans(playtime: dict):
    """
    This function combines close timespans for each day of week.

    For example with timespans like: [(9, 12), (12, 15)]
    Result will be: [(9, 15)]
    
    Args:
        playtime (dict): A dictionary where keys are days of week and
        values are lists of tuples with format (datetime.time, datetime.time)
    
    Returns:
        dict: New dictionary of the same format as input dictionary with combined timespans
        
    """
    combined_playtime = copy.deepcopy(playtime)

    for timespans in combined_playtime.values():
        if len(timespans) > 1:
            i = 0
            while i < len(timespans) - 1:
                start_value = timespans[i][0]

                if timespans[i][1] == timespans[i + 1][0]:
                    end_value = timespans[i + 1][1]
                else:
                    i += 1
                    continue

                del timespans[i]
                del timespans[i]    

                combined = (start_value, end_value)
                timespans.insert(i, combined)

    return combined_playtime
