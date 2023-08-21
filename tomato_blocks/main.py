import sys
import time

import typer
import schedule
from rich import print
import os
import subprocess
import pathlib

from .tomato_block import TomatoBlock
from .weekly_schedule import WeeklySchedule

BASE_DIR = pathlib.Path().home().joinpath('code', 'projects', 'python', 'tomato-blocks')
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


@app.command()
def update():
    print('[blue]Updating tomato-blocks...[/blue]')
    print(BASE_DIR)
    os.chdir(BASE_DIR)

    print('[green]Building new wheel...[/green]')
    subprocess.call('deactivate', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call('poetry build', shell=True)

    wheel_path = next(BASE_DIR.joinpath('dist').glob('*.whl'))
    print(f'[green]Installing new wheel...[/green]')
    print(f'[green]{wheel_path.name}[/green]')
    subprocess.call(f'pip install --quiet --user {wheel_path} --force-reinstall', shell=True)
    print('[green]Done![/green]')


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
