import sys
import time

import typer
import schedule

from .tomato_block import TomatoBlock
from .weekly_schedule import WeeklySchedule

EXIT_MESSAGE = '\n\nTimer Quit\n👋\nGood-bye'

app = typer.Typer()


@app.callback(invoke_without_command=True)
@app.command()
def main(ctx: typer.Context, title=None):
    if ctx.invoked_subcommand is None:
        try:
            if title:
                TomatoBlock(title).run()
            else:
                TomatoBlock().run()
        except KeyboardInterrupt:
            print(EXIT_MESSAGE)
            sys.exit(0)


sched = typer.Typer()


@sched.command()
def run():
    sch = WeeklySchedule()
    sch.create()
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)

    except KeyboardInterrupt:
        print(EXIT_MESSAGE)
        sys.exit(0)


@sched.command(name='weekly')
def print_weekly():
    sch = WeeklySchedule()
    sch.print_weekly()


@sched.command(name='day')
def print_day(day: str = typer.Argument('Today')):
    sch = WeeklySchedule()
    sch.print_day(day)


app.add_typer(sched, name='schedule')
