# ICS-Generator

## Usage

You may start with modifying `example.py`, which is a simple example of how to use the generator.

```python
async def main():
    fetcher = MasterFetcher("Your XK_TOKEN Here")
    events = [
        # extra meetings and courses here
    ]
    cal = await generate("ICS Name", fetchers=[fetcher], events=events)
    with open("my-events.ics", "wb") as f:
        f.write(cal.to_ical())
```

If you want to fetch courses from `yjsxk.nju.edu.cn`, please log in and get your `XK_TOKEN` from browser cookies.
Additional events, namely courses and meetings, can be added to the `events` list.
The `events` list should contain `Event` objects from `ics.events` package. You can add customized events by
subclassing `ics.events.Event` and adding your own properties.
