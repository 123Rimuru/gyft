from __future__ import print_function

from icalendar import Calendar, Event
from datetime import datetime, timedelta
from timetable import Course
from utils import dates, build_event_duration, generate_india_time, next_weekday

WORKING_DAYS = dates.get_dates()


def generate_ics(courses: list[Course], output_filename):
    """
    Creates an ICS file `timetable.ics` with the timetable data present inside the 'timetable' parameter.
    """
    cal = Calendar()
    cal.add("prodid", "-//Your Timetable generated by GYFT//mxm.dk//")
    cal.add("version", "1.0")
    for course in courses:
        start_dates = []
        end_dates = []
        for x in WORKING_DAYS:
            if next_weekday(x[0], course.day) <= x[1]:
                start_dates.append(
                    next_weekday(x[0], course.day)
                )  # work only in the interval 'x' of WORKING_DAYS, avoiding recurring outside of it.
                end_dates.append(x[1])
        lecture_begins_stamps = [
            generate_india_time(
                start.year, start.month, start.day, course.start_time, 0
            )
            for start in start_dates
        ]

        for lecture_begin, end in zip(lecture_begins_stamps, end_dates):
            event = build_event_duration(
                course.title,
                course.code,
                lecture_begin,
                course.duration,
                course.get_location(),
                "weekly",
                end,
            )

            cal.add_component(event)

    # add holidays
    for holiday in dates.holidays:
        event = Event()
        event.add("summary", "INSTITUTE HOLIDAY : " + holiday[0])
        event.add("dtstart", holiday[1])
        event.add("dtend", holiday[1] + timedelta(days=1))
        cal.add_component(event)

    with open(output_filename, "wb") as f:
        f.write(cal.to_ical())
        print("\nYour timetable has been written to %s" % output_filename)
