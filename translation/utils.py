from . import constants


def get_day_of_week(weekday: str, country_code=constants.UKRAINE_CODE):
    normalized = weekday.upper()
    
    if country_code == constants.UKRAINE_CODE:
        return constants.UKRAINIAN_WEEKDAYS.get(normalized, False)
