import asyncio
import unittest

import httpx
import icalendar

from .nju_yjsxk import MasterFetcher


class TestMasterFetcher(unittest.TestCase):
    def test_something(self):
        ics = icalendar.Calendar()
        ics.add("version", "2.0")
        ics.add("prodid", "-//me.iori2333//NJU Master Course//EN")

        async def _test():
            async with httpx.AsyncClient() as client:
                fetcher = MasterFetcher(xk_token="")
                events = await fetcher.fetch(client)
                for event in events:
                    for ics_event in event.to_ics_events():
                        ics.add_component(ics_event)

            with open("test.ics", "wb") as f:
                f.write(ics.to_ical())

        asyncio.run(_test())


if __name__ == "__main__":
    unittest.main()
