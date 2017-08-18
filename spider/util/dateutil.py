# encoding=utf-8#
__author__ = 'lism'

import re
import time
import logging


class DateUtil:
    default_format = '%Y-%m-%d %H:%M:%S'
    regs = [u"\\d{4}[年|\-|.|/]\\d{1,2}[月|\-|.|/]\\d{1,2}([号|日|\-|.|/])?(\\s*\\d{1,2}[:|时](\\d{1,2}([:|分]\\d{0,2})?秒?)?)?"]
    formats = [
        u"%Y年%m月%d日%H时%M分%S秒",
        u"%Y年%m月%d日 %H时%M分%S秒",
        u"%Y年%m月%d日%H时%M分",
        u"%Y年%m月%d日 %H时%M分",
        u"%Y年%m月%d日 %H时",
        u"%Y年%m月%d日%H时",
        u"%Y年%m月%d日",
        u"%Y年%m月%d日%H:%M:%S",
        u"%Y年%m月%d日 %H:%M:%S",
        u"%Y年%m月%d日%H:%M",
        u"%Y年%m月%d日 %H:%M",
        u"%Y年%m月%d日 %H",
        u"%Y年%m月%d日%H",
        u"%Y年%m月%d号%H时%M分%S秒",
        u"%Y年%m月%d号 %H时%M分%S秒",
        u"%Y年%m月%d号%H时%M分",
        u"%Y年%m月%d号 %H时%M分",
        u"%Y年%m月%d号 %H时",
        u"%Y年%m月%d号%H时",
        u"%Y年%m月%d号",
        u"%Y年%m月%d号%H:%M:%S",
        u"%Y年%m月%d号 %H:%M:%S",
        u"%Y年%m月%d号%H:%M",
        u"%Y年%m月%d号 %H:%M",
        u"%Y年%m月%d号 %H",
        u"%Y年%m月%d号%H",
        u"%Y-%m-%d %H时%M分%S秒",
        u"%Y-%m-%d %H时%M分",
        u"%Y-%m-%d %H时",
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H",
        u"%Y.%m.%d %H时%M分%S秒",
        u"%Y/%m/%d %H时%M分%S秒",
        u"%Y/%m/%d %H时%M分",
        u"%Y/%m/%d %H时",
        "%Y/%m/%d",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y/%m/%d %H",
        "%Y.%m.%d %H:%M:%S",
        "%Y.%m.%d %H:%M",
        "%Y.%m.%d %H",
        "%Y.%m.%d",
    ]

    @staticmethod
    def cut_date_str(str):
        date = DateUtil.cut_date(str)
        if (date == None):
            return None
        return time.strftime(DateUtil.default_format, date)

    @staticmethod
    def cut_date(str):
        date = None
        for reg in DateUtil.regs:
            pattern = re.compile(reg)
            match = pattern.search(str)
            if match:
                print(match.group())
                # logging.debug(match.group())
                date = DateUtil.format_date(match.group())
                break
        return date

    @staticmethod
    def format_date(date_str):
        date = None
        for format in DateUtil.formats:
            try:
                date = time.strptime(date_str, format)
                # print(format)
                logging.info(format)
                break
            except:
                pass
        return date

    @staticmethod
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

    @staticmethod
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


if __name__ == '__main__':
    # str = DateUtil.cut_date_str('分享1,312评论2017年08月18日11:04')
    str = DateUtil.cut_date_str('18/08/6 11:04')
    print(str)
