from dataclasses import dataclass
from datetime import time, datetime, timedelta
from typing import Iterable, Self

from .base import Event, Schedule
from ..utils import date_join, this_monday_of, Weekday

COURSE_BEGIN_END = {
    1: (time(8, 0), time(8, 50)),
    2: (time(9, 0), time(9, 50)),
    3: (time(10, 10), time(11, 0)),
    4: (time(11, 10), time(12, 0)),
    5: (time(14, 0), time(14, 50)),
    6: (time(15, 0), time(15, 50)),
    7: (time(16, 10), time(17, 0)),
    8: (time(17, 10), time(18, 0)),
    9: (time(18, 30), time(19, 20)),
    10: (time(19, 30), time(20, 20)),
    11: (time(20, 30), time(21, 20)),
    12: (time(21, 30), time(22, 20)),
}
MAX_WEEKS = 20


@dataclass
class CourseSchedule(Schedule):
    weeks: Iterable[int]
    weekday: Weekday
    begin: int
    end: int

    first_monday: datetime | None = None

    @property
    def dates(self) -> Iterable[Schedule.Interval]:
        assert self.first_monday is not None, "first_monday is not set"

        for week in self.weeks:
            if week > MAX_WEEKS:
                continue
            weekday = (
                self.first_monday
                + timedelta(days=self.weekday.value)
                + timedelta(weeks=week - 1)
            )
            start = date_join(weekday, COURSE_BEGIN_END[self.begin][0])
            end = date_join(weekday, COURSE_BEGIN_END[self.end][1])

            yield Schedule.Interval(start, end)


class Course(Event):
    @classmethod
    def of(
        cls,
        name: str,
        term_start: datetime,
        description: str,
        teachers: Iterable[str],
        schedules: Iterable[Schedule] | Schedule,
    ) -> Self:
        new_description = f"课程：{name}；教师：{'、'.join(teachers)}。{description}"
        new_term_start = this_monday_of(term_start)
        if isinstance(schedules, Schedule):
            new_schedules = [schedules]
        else:
            new_schedules = list(schedules)

        for schedule in new_schedules:
            schedule.first_monday = new_term_start

        return cls(name, new_description, new_schedules)
