import datetime
from enum import Enum
from typing import Sequence, Self


class Weekday(Enum):
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6

    @classmethod
    def from_chinese(cls, word: str) -> Self:
        if word == "一":
            return Weekday.MON
        elif word == "二":
            return Weekday.TUE
        elif word == "三":
            return Weekday.WED
        elif word == "四":
            return Weekday.THU
        elif word == "五":
            return Weekday.FRI
        elif word == "六":
            return Weekday.SAT
        elif word == "日":
            return Weekday.SUN
        else:
            raise ValueError(f"Unknown weekday: {word}")


class Weeks:
    @staticmethod
    def odds(begin: int, end: int) -> Sequence[int]:
        if begin % 2 == 0:
            begin += 1
        return range(begin, end + 1, 2)

    @staticmethod
    def evens(begin: int, end: int) -> Sequence[int]:
        if begin % 2 == 1:
            begin += 1
        return range(begin, end + 1, 2)

    @staticmethod
    def every(begin: int, end: int) -> Sequence[int]:
        return range(begin, end + 1)


def date_join(date: datetime.datetime, time: datetime.time) -> datetime.datetime:
    return datetime.datetime.combine(date.date(), time, tzinfo=date.tzinfo)


def this_monday_of(date: datetime.datetime) -> datetime.datetime:
    return date - datetime.timedelta(days=date.weekday())


def next_monday_of(date: datetime.datetime) -> datetime.datetime:
    if date.weekday() == 0:
        return date
    return this_monday_of(date) + datetime.timedelta(weeks=1)


DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
)
