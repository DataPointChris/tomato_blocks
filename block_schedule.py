from dataclasses import dataclass
from datetime import datetime
import sys

from schedule import clear
from tomato_blocks import convert_date, clear_screen


@dataclass
class Block:
    day: str
    time: str
    activity: str


monday_schedule = []

tuesday_schedule = [
    ('06:00', 'Breakfast'),
    ('07:00', 'Yoga'),
    ('08:00', 'Book'),
    ('09:00', 'SQL'),
    ('10:00', 'Book'),
    ('11:00', 'SQL'),
    ('12:00', 'Lunch'),
    ('13:00', 'Misc'),
    ('14:00', 'Project'),
    ('15:00', 'Project'),
    ('16:00', 'Project'),
    ('17:00', 'Project'),
    ('18:00', 'Dinner'),
    ('19:00', 'Social'),
    ('20:00', 'Special'),
    ('21:00', 'Play'),
    ('22:00', 'Bed'),
]

wednesday_schedule = [
    ('06:00', 'Breakfast'),
    ('07:00', 'Yoga'),
    ('08:00', 'Class'),
    ('09:00', 'Zoom'),
    ('10:00', 'Zoom'),
    ('11:00', 'Zoom'),
    ('12:00', 'Zoom'),
    ('13:00', 'Gym'),
    ('14:00', 'Gym'),
    ('15:00', 'Class'),
    ('16:00', 'Class'),
    ('17:00', 'Special'),
    ('18:00', 'Dinner'),
    ('19:00', 'Project'),
    ('20:00', 'Project'),
    ('21:00', 'Play'),
    ('22:00', 'Bed'),
]

thursday_schedule = [
    ('06:00', 'Breakfast'),
    ('07:00', 'Yoga'),
    ('08:00', 'Book'),
    ('09:00', 'SQL'),
    ('10:00', 'Book'),
    ('11:00', 'SQL'),
    ('12:00', 'Lunch'),
    ('13:00', 'Misc'),
    ('14:00', 'Project'),
    ('15:00', 'Project'),
    ('16:00', 'Project'),
    ('17:00', 'Project'),
    ('18:00', 'Dinner'),
    ('19:00', 'Social'),
    ('20:00', 'Special'),
    ('21:00', 'Play'),
    ('22:00', 'Bed'),
]

friday_schedule = [
    ('06:00', 'Breakfast'),
    ('07:00', 'Yoga'),
    ('08:00', 'Book'),
    ('09:00', 'SQL'),
    ('10:00', 'Book'),
    ('11:00', 'SQL'),
    ('12:00', 'Lunch'),
    ('13:00', 'Gym'),
    ('14:00', 'Gym'),
    ('15:00', 'Class'),
    ('16:00', 'Class'),
    ('17:00', 'Special'),
    ('18:00', 'Dinner'),
    ('19:00', 'Project'),
    ('20:00', 'Project'),
    ('21:00', 'Play'),
    ('22:00', 'Bed'),
]

saturday_schedule = [
    ('06:00', 'Breakfast'),
    ('07:00', 'Yoga'),
    ('08:00', 'Book'),
    ('09:00', 'SQL'),
    ('10:00', 'Book'),
    ('11:00', 'SQL'),
    ('12:00', 'Lunch'),
    ('13:00', 'Misc'),
    ('14:00', 'Project'),
    ('15:00', 'Project'),
    ('16:00', 'Project'),
    ('17:00', 'Project'),
    ('18:00', 'Dinner'),
    ('19:00', 'Social'),
    ('20:00', 'Special'),
    ('21:00', 'Play'),
    ('22:00', 'Bed'),
]

sunday_schedule = [
    ('06:00', 'Breakfast'),
    ('07:00', 'Yoga'),
    ('08:00', 'Book'),
    ('09:00', 'SQL'),
    ('10:00', 'Book'),
    ('11:00', 'SQL'),
    ('12:00', 'Lunch'),
    ('13:00', 'Class'),
    ('14:00', 'Gym'),
    ('15:00', 'Gym'),
    ('16:00', 'Class'),
    ('17:00', 'Special'),
    ('18:00', 'Dinner'),
    ('19:00', 'Project'),
    ('20:00', 'Project'),
    ('21:00', 'Play'),
    ('22:00', 'Bed'),
]

daily_schedules = {'Monday': monday_schedule,
                   'Tuesday': tuesday_schedule,
                   'Wednesday': wednesday_schedule,
                   'Thursday': thursday_schedule,
                   'Friday': friday_schedule,
                   'Saturday': saturday_schedule,
                   'Sunday': sunday_schedule}

monday_blocks = [Block('monday', time, activity) for time, activity in monday_schedule]
tuesday_blocks = [Block('tuesday', time, activity) for time, activity in tuesday_schedule]
wednesday_blocks = [Block('wednesday', time, activity) for time, activity in wednesday_schedule]
thursday_blocks = [Block('thursday', time, activity) for time, activity in thursday_schedule]
friday_blocks = [Block('friday', time, activity) for time, activity in friday_schedule]
saturday_blocks = [Block('saturday', time, activity) for time, activity in saturday_schedule]
sunday_blocks = [Block('sunday', time, activity) for time, activity in sunday_schedule]

all_time_blocks = monday_blocks \
    + tuesday_blocks \
    + wednesday_blocks \
    + thursday_blocks \
    + friday_blocks \
    + saturday_blocks \
    + sunday_blocks


def print_schedule(daily_schedules, today=None):
    if today:
        print('-' * 20)
        print(today)
        print('-' * 20)
        for item in daily_schedules.get(today):
            print(f'{convert_date(item[0])}  {item[1]}')
        print()
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

    elif sys.argv[1] == '--today':
        clear_screen()
        today = datetime.today().strftime("%A")
        print_schedule(daily_schedules, today=today)
