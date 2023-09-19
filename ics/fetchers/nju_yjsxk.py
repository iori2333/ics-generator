# Fetcher for https://yjsxk.nju.edu.cn
from datetime import datetime
from typing import Collection
import re

import httpx
import pytz
from pydantic import BaseModel, Field

from .base import Fetcher
from ..utils import next_monday_of, Weeks, Weekday
from ..events import Event, Course as CourseEvent, CourseSchedule


TIME_LOC_REG = re.compile(r"(\d+)-(\d+)周 星期(\w)\[(\d+)-(\d+)节](.*)")
COURSE_API = (
    "https://yjsxk.nju.edu.cn/yjsxkapp/sys/xsxkapp/xsxkCourse/loadStdCourseInfo.do"
)


class Course(BaseModel):
    name: str = Field(alias="KCMC")
    category: str = Field(alias="KCLBMC")
    time_location: str = Field(alias="PKSJDD")
    campus: str = Field(alias="XQMC")
    teachers: str = Field(alias="RKJS")
    department: str = Field(alias="KCKKDWMC")
    term: str = Field(alias="XNXQDM")
    credit: float = Field(alias="XF")
    language: str = Field(alias="SKYYMC")

    def parse_time_location(self) -> Collection[CourseSchedule]:
        entries = self.time_location.split("<br>")
        schedules = []
        for entry in entries:
            match = TIME_LOC_REG.search(entry)
            if match is None:
                continue
            begin, end, weekday, begin_time, end_time, location = match.groups()

            every_week = True
            if m := re.search(r"单周：(\w+)", location):
                new_location = m.group(1)
                weeks = Weeks.odds(int(begin), int(end))
                schedules.append(
                    CourseSchedule(
                        weeks=weeks,
                        weekday=Weekday.from_chinese(weekday),
                        begin=int(begin_time),
                        end=int(end_time),
                        location=new_location,
                    )
                )
                every_week = False

            if m := re.search(r"双周：(\w+)", location):
                new_location = m.group(1)
                weeks = Weeks.evens(int(begin), int(end))
                schedules.append(
                    CourseSchedule(
                        weeks=weeks,
                        weekday=Weekday.from_chinese(weekday),
                        begin=int(begin_time),
                        end=int(end_time),
                        location=new_location,
                    )
                )
                every_week = False

            if every_week:
                schedules.append(
                    CourseSchedule(
                        weeks=Weeks.every(int(begin), int(end)),
                        weekday=Weekday.from_chinese(weekday),
                        begin=int(begin_time),
                        end=int(end_time),
                        location=location,
                    )
                )

        return schedules

    def to_event(self) -> CourseEvent:
        year, term = int(self.term[:4]), int(self.term[4])
        if term == 1:
            begin = datetime(
                year=year, month=9, day=1, tzinfo=pytz.timezone("Asia/Shanghai")
            )
        else:
            begin = datetime(
                year=year, month=3, day=1, tzinfo=pytz.timezone("Asia/Shanghai")
            )
        first_monday = next_monday_of(begin)

        description = (
            f"学分：{self.credit}；课程类别：{self.category}；开课单位：{self.department}；"
            f"授课语言：{self.language}；校区：{self.campus}"
        )
        return CourseEvent.of(
            name=self.name,
            term_start=first_monday,
            description=description,
            teachers=self.teachers.split(","),
            schedules=self.parse_time_location(),
        )


class MasterFetcher(Fetcher):
    def __init__(self, xk_token: str):
        self.xk_token = xk_token

    async def fetch(self, client: httpx.AsyncClient) -> Collection[Event]:
        client.cookies.set("XK_TOKEN", self.xk_token, domain="yjsxk.nju.edu.cn")
        resp = await client.get(COURSE_API)
        resp.raise_for_status()
        courses_raw = resp.json()["results"]
        courses = [Course.model_validate(course) for course in courses_raw]
        return [course.to_event() for course in courses]
