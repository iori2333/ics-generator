import unittest
from datetime import datetime, timedelta, time

import icalendar

from ics.events import Course, CourseSchedule
from ics.events.meeting import Meeting, MeetingSchedule
from ics.utils import Weekday, Weeks


class TestAddCourse(unittest.TestCase):
    def test_course(self):
        ics = icalendar.Calendar()
        course = Course.of(
            name="测试课程",
            term_start=datetime(2021, 9, 6),
            description="我是一个测试课程",
            teachers=["测试教师1", "测试教师2"],
            schedules=[
                CourseSchedule(
                    weeks=Weeks.odds(1, 17),
                    weekday=Weekday.MON,
                    begin=1,
                    end=2,
                    location="测试教室",
                ),
                CourseSchedule(
                    weeks=Weeks.evens(1, 17),
                    weekday=Weekday.MON,
                    begin=3,
                    end=4,
                    location="测试教室2",
                ),
            ],
        )
        for event in course.to_ics_events():
            ics.add_component(event)

        with open("test.ics", "wb") as f:
            f.write(ics.to_ical())

    def test_meeting(self):
        ics = icalendar.Calendar()
        meeting = Meeting.of(
            group="测试组",
            description="测试组周会",
            term_start=datetime(2021, 9, 6),
            schedules=MeetingSchedule(
                weeks=Weeks.every(1, 17),
                weekday=Weekday.TUE,
                start=time(10, 10),
                lasting=timedelta(minutes=50),
                location="测试会议室",
            ),
        )
        for event in meeting.to_ics_events():
            ics.add_component(event)

        with open("test.ics", "wb") as f:
            f.write(ics.to_ical())


if __name__ == "__main__":
    unittest.main()
