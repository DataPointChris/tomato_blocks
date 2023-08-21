import os
import subprocess
from dataclasses import dataclass
from datetime import datetime

import schedule

from .tomato_block import TomatoBlock


@dataclass
class ScheduleBlock:
    day: str
    time: str
    timer: TomatoBlock


DEFAULT_SCHEDULE = {
    'Monday': [],
    'Tuesday': [
        ScheduleBlock('Tuesday', *args)
        for args in [
            ('06:00', TomatoBlock('Breakfast', 50)),
            ('07:00', TomatoBlock('Yoga', 50)),
            ('08:00', TomatoBlock('Book', 50)),
            ('09:00', TomatoBlock('SQL', 50)),
            ('10:00', TomatoBlock('Book', 50)),
            ('11:00', TomatoBlock('SQL', 50)),
            ('12:00', TomatoBlock('Lunch', 50)),
            ('13:00', TomatoBlock('Misc', 50)),
            ('14:00', TomatoBlock('Project', 50)),
            ('15:00', TomatoBlock('Project', 50)),
            ('16:00', TomatoBlock('Project', 50)),
            ('17:00', TomatoBlock('Project', 50)),
            ('18:00', TomatoBlock('Dinner', 50)),
            ('19:00', TomatoBlock('Social', 50)),
            ('20:00', TomatoBlock('Special', 50)),
            ('21:00', TomatoBlock('Play', 50)),
            ('22:00', TomatoBlock('Bed', 50)),
        ]
    ],
    'Wednesday': [
        ScheduleBlock('Wednesday', *args)
        for args in [
            ('06:00', TomatoBlock('Breakfast', 50)),
            ('07:00', TomatoBlock('Yoga', 50)),
            ('08:00', TomatoBlock('Class', 50)),
            ('09:00', TomatoBlock('Zoom', 50)),
            ('10:00', TomatoBlock('Zoom', 50)),
            ('11:00', TomatoBlock('Zoom', 50)),
            ('12:00', TomatoBlock('Zoom', 50)),
            ('13:00', TomatoBlock('Gym', 50)),
            ('14:00', TomatoBlock('Gym', 50)),
            ('15:00', TomatoBlock('Class', 50)),
            ('16:00', TomatoBlock('Class', 50)),
            ('17:00', TomatoBlock('Special', 50)),
            ('18:00', TomatoBlock('Dinner', 50)),
            ('19:00', TomatoBlock('Project', 50)),
            ('20:00', TomatoBlock('Project', 50)),
            ('21:00', TomatoBlock('Play', 50)),
            ('22:00', TomatoBlock('Bed', 50)),
        ]
    ],
    'Thursday': [
        ScheduleBlock('Thursday', *args)
        for args in [
            ('08:00', TomatoBlock('Breakfast', 50)),
            ('09:00', TomatoBlock('Yoga', 50)),
            ('10:00', TomatoBlock('Book', 50)),
            ('11:00', TomatoBlock('SQL', 50)),
            ('12:00', TomatoBlock('Lunch', 50)),
            ('13:00', TomatoBlock('Misc', 50)),
            ('14:00', TomatoBlock('Project', 50)),
            ('15:00', TomatoBlock('Project', 50)),
            ('16:00', TomatoBlock('Book', 50)),
            ('17:00', TomatoBlock('SQL', 50)),
            ('18:00', TomatoBlock('Dinner', 50)),
            ('19:00', TomatoBlock('Social', 50)),
            ('20:00', TomatoBlock('Special', 50)),
            ('21:00', TomatoBlock('Project', 50)),
            ('22:00', TomatoBlock('Project', 50)),
            ('23:00', TomatoBlock('Play', 50)),
        ]
    ],
    'Friday': [
        ScheduleBlock('Friday', *args)
        for args in [
            ('08:00', TomatoBlock('Breakfast', 50)),
            ('09:00', TomatoBlock('Yoga', 50)),
            ('10:00', TomatoBlock('Book', 50)),
            ('11:00', TomatoBlock('SQL', 50)),
            ('12:00', TomatoBlock('Lunch', 50)),
            ('13:00', TomatoBlock('Gym', 50)),
            ('14:00', TomatoBlock('Gym', 50)),
            ('15:00', TomatoBlock('Book', 50)),
            ('16:00', TomatoBlock('SQL', 50)),
            ('17:00', TomatoBlock('Class', 50)),
            ('18:00', TomatoBlock('Class', 50)),
            ('19:00', TomatoBlock('Special', 50)),
            ('20:00', TomatoBlock('Dinner', 50)),
            ('21:00', TomatoBlock('Project', 50)),
            ('22:00', TomatoBlock('Project', 50)),
            ('23:00', TomatoBlock('Play', 50)),
        ]
    ],
    'Saturday': [
        ScheduleBlock('Saturday', *args)
        for args in [
            ('08:00', TomatoBlock('Breakfast', 50)),
            ('09:00', TomatoBlock('Yoga', 50)),
            ('10:00', TomatoBlock('Project', 50)),
            ('11:00', TomatoBlock('Project', 50)),
            ('12:00', TomatoBlock('Lunch', 50)),
            ('13:00', TomatoBlock('Misc', 50)),
            ('14:00', TomatoBlock('Book', 50)),
            ('15:00', TomatoBlock('SQL', 50)),
            ('16:00', TomatoBlock('Project', 50)),
            ('17:00', TomatoBlock('Project', 50)),
            ('18:00', TomatoBlock('Dinner', 50)),
            ('19:00', TomatoBlock('Book', 50)),
            ('20:00', TomatoBlock('SQL', 50)),
            ('21:00', TomatoBlock('Social', 50)),
            ('22:00', TomatoBlock('Special', 50)),
            ('23:00', TomatoBlock('Play', 50)),
        ]
    ],
    'Sunday': [
        ScheduleBlock('Sunday', *args)
        for args in [
            ('06:00', TomatoBlock('Breakfast', 50)),
            ('07:00', TomatoBlock('Yoga', 50)),
            ('08:00', TomatoBlock('Book', 50)),
            ('09:00', TomatoBlock('SQL', 50)),
            ('10:00', TomatoBlock('Book', 50)),
            ('11:00', TomatoBlock('SQL', 50)),
            ('12:00', TomatoBlock('Lunch', 50)),
            ('13:00', TomatoBlock('Class', 50)),
            ('14:00', TomatoBlock('Gym', 50)),
            ('15:00', TomatoBlock('Gym', 50)),
            ('16:00', TomatoBlock('Class', 50)),
            ('17:00', TomatoBlock('Special', 50)),
            ('18:00', TomatoBlock('Dinner', 50)),
            ('19:00', TomatoBlock('Project', 50)),
            ('20:00', TomatoBlock('Project', 50)),
            ('21:00', TomatoBlock('Play', 50)),
            ('22:00', TomatoBlock('Bed', 50)),
        ]
    ],
}


class WeeklySchedule:
    def __init__(self, weekly_schedule: dict[str, list[ScheduleBlock]] = DEFAULT_SCHEDULE):
        self.weekly_schedule = weekly_schedule

    def _convert_time(self, time: str) -> str:
        return datetime.strptime(time, "%H:%M").strftime("%I:%M%p")

    def create(self):
        for sch in self.weekly_schedule.values():
            for block in sch:
                getattr(schedule.every(), block.day.lower()).at(block.time).do(block.timer.run())

    def print_day(self, day: str):
        separator = '-' * 20
        day = day.capitalize()
        if day == 'Today':
            day = datetime.today().strftime("%A")
        schedule = self.weekly_schedule.get(day)
        if schedule is not None:
            print()
            print(day)
            print(separator)
            for block in schedule:
                print(f'{self._convert_time(block.time)}  {block.timer.title}')
            print()
        else:
            print('Invalid day selection: ', day)

    def print_weekly(self):
        separator = '-' * 20
        print()
        print(separator)
        print('WEEKLY SCHEDULE')
        print(separator)
        print()
        for day in self.weekly_schedule:
            self.print_day(day)

    def _clear_screen(self):
        clear = 'cls' if os.name == 'nt' else 'clear'
        subprocess.call(clear, shell=True)
