def format_remaining_time(remaining_time):  # Pass in seconds, returns string
    if remaining_time <= 0:
        return 'EXPIRED'
    elif remaining_time // 31536000:  # Year
        years = int(remaining_time / 31536000)
        remainder = remaining_time - years * 31536000
        if remainder >= 2628000:
            months = int(remainder / 2628000)
            return f"{pluralize(years, 'year')} {pluralize(months, 'month')}"
        else:
            return f"{pluralize(years, 'year')}"
    elif remaining_time // 2628000:  # Month
        months = int(remaining_time / 2628000)
        remainder = remaining_time - months * 2628000
        if remainder >= 604800:
            weeks = int(remainder / 604800)
            return f"{pluralize(months, 'month')} {pluralize(weeks, 'week')}"
        else:
            return f"{pluralize(months, 'month')}"
    elif remaining_time // 604800:  # Week
        weeks = int(remaining_time / 604800)
        remainder = remaining_time - weeks * 604800
        if remainder >= 86400:
            days = int(remainder / 86400)
            return f"{pluralize(weeks, 'week')} {pluralize(days, 'day')}"
        else:
            return f"{pluralize(weeks, 'week')}"
    elif remaining_time // 86400:  # Day
        days = int(remaining_time / 86400)
        remainder = remaining_time - days * 86400
        if remainder >= 3600:
            hours = int(remainder / 3600)
            return f"{pluralize(days, 'day')} {pluralize(hours, 'hour')}"
        else:
            return f"{pluralize(days, 'day')}"
    elif remaining_time // 3600:  # Hour
        hours = int(remaining_time / 3600)
        remainder = remaining_time - hours * 3600
        if remainder >= 60:
            minutes = int(remainder / 60)
            return f"{pluralize(hours, 'hour')} {pluralize(minutes, 'minute')}"
        else:
            return f"{pluralize(hours, 'hour')}"
    elif remaining_time // 60:  # Minute
        minutes = int(remaining_time / 60)
        remainder = remaining_time - minutes * 60
        if remainder >= 1:
            seconds = int(remainder)
            return f"{pluralize(minutes, 'minute')} {pluralize(seconds, 'second')}"
        else:
            return f"{pluralize(minutes, 'minute')}"
    else:  # Seconds
        return f"{pluralize(remaining_time, 'second')}"


def parse_duration(duration):
    try:
        number = eval(duration[:-1])
    except (NameError, SyntaxError):
        return False
    if not isinstance(number, int):
        return False
    if number < 0:
        return False
    symbol = duration[-1]
    if symbol not in {'m', 'h', 'd', 'w'}:
        return False
    if symbol == 'm':
        return number * 60
    elif symbol == 'h':
        return number * 3600
    elif symbol == 'd':
        return number * 86400
    elif symbol == 'w':
        return number * 604800


def pluralize(value, string):
    if value > 1:
        return f'{value} {string}s'
    else:
        return f'{value} {string}'
