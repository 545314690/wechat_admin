import time


def timestamp_datetime(ts, type='ms'):
    """
    输入时间戳，将时间戳转换为GMT0日期时间输出
    :param ts: int整型或int字符串，默认毫秒时间
    :param type: 时间类型，输入的数据为ms或s。默认ms
    :return: GMT0的time_struct类型(但time_struct其实不含tz信息)
    """
    ts = int(ts)
    if type.lower() == 'ms':
        ts = ts / 1000
    elif type.lower() == 's':
        pass
    else:
        print('错误！时间戳请选择s或ms')
        return

    str_format = '%Y-%m-%d %H:%M:%S'
    dt0 = time.strftime(str_format, time.gmtime(ts))  # GMT0的日期
    return dt0


def datetime_timestamp(dt0, type='ms'):
    """
    输入GMT0时间的日期(或日期字符串)，输出int型时间戳。默认毫秒级
    :param dt0: GMT0的时间
    :param type: 输出的时间戳类型，ms级还是s级
    :return: int型时间戳
    """
    if isinstance(dt0, str):
        ts = time.mktime(time.strptime(dt0, '%Y-%m-%d %H:%M:%S'))
    else:
        ts = time.mktime(dt0)

    delta = time.timezone  # mktime默认时间是本地时间，需用 ts+delta 调整时区
    if type.lower() == 'ms':
        ts0 = int(ts) * 1000 - delta * 1000
    elif type.lower() == 's':
        ts0 = int(ts) - delta
    else:
        print('错误！时间戳请选择s或ms')
        return

    return ts0
