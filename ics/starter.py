from typing import Iterable

import httpx
import icalendar

from .utils import DEFAULT_USER_AGENT
from .fetchers import Fetcher
from .events import Event


async def generate(
    name: str,
    events: Iterable[Event] = (),
    fetchers: Iterable[Fetcher] = (),
) -> icalendar.Calendar:
    ics = icalendar.Calendar()
    ics.add("version", "2.0")
    ics.add("prodid", f"-//me.iori2333//{name}//EN")

    all_events = list(events)
    async with httpx.AsyncClient(headers={"User-Agent": DEFAULT_USER_AGENT}) as client:
        for fetcher in fetchers:
            all_events.extend(await fetcher.fetch(client))
    for event in all_events:
        for ics_event in event.to_ics_events():
            ics.add_component(ics_event)

    return ics
