import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Type

from tomato_blocks import clear_screen, convert_date


@dataclass
class Block:
    day: str
    time: str
    activity: str
    duration: int


monday_schedule = []

tuesday_schedule = [
    ('06:00', 'Breakfast', 50),
    ('07:00', 'Yoga', 50),
    ('08:00', 'Book', 50),
    ('09:00', 'SQL', 50),
    ('10:00', 'Book', 50),
    ('11:00', 'SQL', 50),
    ('12:00', 'Lunch', 50),
    ('13:00', 'Misc', 50),
    ('14:00', 'Project', 50),
    ('15:00', 'Project', 50),
    ('16:00', 'Project', 50),
    ('17:00', 'Project', 50),
    ('18:00', 'Dinner', 50),
    ('19:00', 'Social', 50),
    ('20:00', 'Special', 50),
    ('21:00', 'Play', 50),
    ('22:00', 'Bed', 50),
]

wednesday_schedule = [
    ('06:00', 'Breakfast', 50),
    ('07:00', 'Yoga', 50),
    ('08:00', 'Class', 50),
    ('09:00', 'Zoom', 50),
    ('10:00', 'Zoom', 50),
    ('11:00', 'Zoom', 50),
    ('12:00', 'Zoom', 50),
    ('13:00', 'Gym', 50),
    ('14:00', 'Gym', 50),
    ('15:00', 'Class', 50),
    ('16:00', 'Class', 50),
    ('17:00', 'Special', 50),
    ('18:00', 'Dinner', 50),
    ('19:00', 'Project', 50),
    ('20:00', 'Project', 50),
    ('21:00', 'Play', 50),
    ('22:00', 'Bed', 50),
]

thursday_schedule = [
    ('06:00', 'Breakfast', 50),
    ('07:00', 'Yoga', 50),
    ('08:00', 'Book', 50),
    ('09:00', 'SQL', 50),
    ('10:00', 'Book', 50),
    ('11:00', 'SQL', 50),
    ('12:00', 'Lunch', 50),
    ('13:00', 'Misc', 50),
    ('14:00', 'Project', 50),
    ('15:00', 'Project', 50),
    ('16:00', 'Project', 50),
    ('17:00', 'Project', 50),
    ('18:00', 'Dinner', 50),
    ('19:00', 'Social', 50),
    ('20:00', 'Special', 50),
    ('21:00', 'Play', 50),
    ('22:00', 'Bed', 50),
]

friday_schedule = [
    ('06:00', 'Breakfast', 50),
    ('07:00', 'Yoga', 50),
    ('08:00', 'Book', 50),
    ('09:00', 'SQL', 50),
    ('10:00', 'Book', 50),
    ('11:00', 'SQL', 50),
    ('12:00', 'Lunch', 50),
    ('13:00', 'Gym', 50),
    ('14:00', 'Gym', 50),
    ('15:00', 'Class', 50),
    ('16:00', 'Class', 50),
    ('17:00', 'Special', 50),
    ('18:00', 'Dinner', 50),
    ('19:00', 'Project', 50),
    ('20:00', 'Project', 50),
    ('21:00', 'Play', 50),
    ('22:00', 'Bed', 50),
]

saturday_schedule = [
    ('06:00', 'Breakfast', 50),
    ('07:00', 'Yoga', 50),
    ('08:00', 'Project', 50),
    ('09:00', 'Project', 50),
    ('10:00', 'Project', 50),
    ('11:00', 'Project', 50),
    ('12:00', 'Lunch', 50),
    ('13:00', 'Misc', 50),
    ('14:00', 'Book', 50),
    ('15:00', 'SQL', 50),
    ('16:00', 'Book', 50),
    ('17:00', 'SQL', 50),
    ('18:00', 'Dinner', 50),
    ('19:00', 'Social', 50),
    ('20:00', 'Special', 50),
    ('21:00', 'Play', 50),
    ('22:00', 'Bed', 50),
]

sunday_schedule = [
    ('06:00', 'Breakfast', 50),
    ('07:00', 'Yoga', 50),
    ('08:00', 'Book', 50),
    ('09:00', 'SQL', 50),
    ('10:00', 'Book', 50),
    ('11:00', 'SQL', 50),
    ('12:00', 'Lunch', 50),
    ('13:00', 'Class', 50),
    ('14:00', 'Gym', 50),
    ('15:00', 'Gym', 50),
    ('16:00', 'Class', 50),
    ('17:00', 'Special', 50),
    ('18:00', 'Dinner', 50),
    ('19:00', 'Project', 50),
    ('20:00', 'Project', 50),
    ('21:00', 'Play', 50),
    ('22:00', 'Bed', 50),
]

daily_schedules = {'Monday': monday_schedule,
                   'Tuesday': tuesday_schedule,
                   'Wednesday': wednesday_schedule,
                   'Thursday': thursday_schedule,
                   'Friday': friday_schedule,
                   'Saturday': saturday_schedule,
                   'Sunday': sunday_schedule}

monday_blocks = [Block('monday', time, activity, duration) for time, activity, duration in monday_schedule]
tuesday_blocks = [Block('tuesday', time, activity, duration) for time, activity, duration in tuesday_schedule]
wednesday_blocks = [Block('wednesday', time, activity, duration) for time, activity, duration in wednesday_schedule]
thursday_blocks = [Block('thursday', time, activity, duration) for time, activity, duration in thursday_schedule]
friday_blocks = [Block('friday', time, activity, duration) for time, activity, duration in friday_schedule]
saturday_blocks = [Block('saturday', time, activity, duration) for time, activity, duration in saturday_schedule]
sunday_blocks = [Block('sunday', time, activity, duration) for time, activity, duration in sunday_schedule]

all_time_blocks = monday_blocks \
    + tuesday_blocks \
    + wednesday_blocks \
    + thursday_blocks \
    + friday_blocks \
    + saturday_blocks \
    + sunday_blocks


def print_schedule(daily_schedules, day=None):
    if day:
        day = day.capitalize()
        if day == 'Today':
            day = datetime.today().strftime("%A")
        try:
            schedule = daily_schedules[day]        
            print()
            print('-' * 20)
            print(f'{day}')
            print('-' * 20)
            for item in schedule:
                print(f'{convert_date(item[0])}  {item[1]}')
            print()
        except KeyError:
            print('Please enter a valid day of the week or today')
    else:
        print()
        print('-' * 20)
        print('WEEKLY SCHEDULE')
        print('-' * 20)
        print()
        for day, schedule in daily_schedules.items():
            print(day)
            print('-' * 20)
            for item in schedule:
                print(f'{convert_date(item[0])}  {item[1]}')
            print()


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        clear_screen()
        print_schedule(daily_schedules)

    else:
        day = sys.argv[1]
        clear_screen()
        print_schedule(daily_schedules, day)
