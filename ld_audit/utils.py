import time


# All timestamp functions return in milliseconds
def get_timestamp_for_now():
    return int(time.time()) * 1000


def get_timestamp_for_beginning_of_current_month():
    now = get_timestamp_for_now() / 1000
    current_time_struct = time.localtime(now)
    beginning_of_month = time.struct_time(
        (current_time_struct.tm_year, current_time_struct.tm_mon, 1, 0, 0, 0, 0, 0, 0)
    )
    return int(time.mktime(beginning_of_month)) * 1000


def get_timestamp_for_n_days_ago(num_days: int):
    now = get_timestamp_for_now()
    n_days_ago = now - num_days * 24 * 60 * 60 * 1000
    return n_days_ago
