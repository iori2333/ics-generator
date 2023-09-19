from dataclasses import dataclass
from datetime import datetime, timedelta, time
from typing import Iterable, Self

from .base import Event, Schedule
from ..utils import Weekday, date_join, this_monday_of

MAX_WEEKS = 20


@dataclass
class MeetingSchedule(Schedule):
    weeks: Iterable[int]
    weekday: Weekday
    start: time
    lasting: timedelta

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
            start = date_join(weekday, self.start)
            end = start + self.lasting
            yield Schedule.Interval(start, end)


class Meeting(Event):
    @classmethod
    def of(
        cls,
        group: str,
        term_start: datetime,
        schedules: Iterable[Schedule] | Schedule,
        description: str | None = None,
    ) -> Self:
        if description is None:
            description = f"{group}会议"
        new_term_start = this_monday_of(term_start)
        if isinstance(schedules, Schedule):
            new_schedules = [schedules]
        else:
            new_schedules = list(schedules)

        for schedule in new_schedules:
            schedule.first_monday = new_term_start

        return cls(f"{group}会议", description, new_schedules)
