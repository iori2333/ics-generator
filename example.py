from ics import MasterFetcher, generate


async def main():
    fetcher = MasterFetcher("Your XK_TOKEN Here")
    events = [
        # extra meetings and courses here
    ]
    cal = await generate("ICS Name", fetchers=[fetcher], events=events)
    with open("my-events.ics", "wb") as f:
        f.write(cal.to_ical())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
