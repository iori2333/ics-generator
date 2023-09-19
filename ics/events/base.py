from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Collection, Iterable, NamedTuple

from icalendar import Event as ICSEvent


@dataclass
class Schedule(ABC):
    class Interval(NamedTuple):
        start: datetime
        end: datetime

    location: str

    @property
    @abstractmethod
    def dates(self) -> Iterable[Interval]:
        raise NotImplementedError()


class Event:
    def __init__(self, name: str, description: str, schedules: Iterable[Schedule]):
        self.name = name
        self.description = description
        self.schedules = schedules

    def to_ics_events(self) -> Collection[ICSEvent]:
        events = list[Event]()

        base_event = ICSEvent()
        base_event.add("summary", self.name)
        base_event.add("description", self.description)
        base_event.add("dtstamp", datetime.now())
        base_event.add("status", "CONFIRMED")

        for schedule in self.schedules:
            for interval in schedule.dates:
                event = base_event.copy()
                event.add("dtstart", interval.start)
                event.add("dtend", interval.end)
                event.add("location", schedule.location)
                events.append(event)

        return events
