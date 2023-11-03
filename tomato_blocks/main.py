import logging
import os
import pathlib
import subprocess
import sys
import time
import uuid
from datetime import datetime, timedelta

import schedule
import typer
from rich import print
from sqlalchemy import Date, DateTime, Integer, String, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from tabulate import tabulate

from .tomato_block import TomatoBlock
from .weekly_schedule import WeeklySchedule

BASE_DIR = pathlib.Path().home().joinpath('code', 'projects', 'python', 'tomato-blocks')
EXIT_MESSAGE = '\n\nTimer Cancelled'
SQLITE_DB = 'tomato.db'
DEFAULT_DURATION = 50

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(message)s')
file_handler = logging.FileHandler('tomato.log')
file_handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

app = typer.Typer()


engine = create_engine('postgresql://localhost/tomato')


class Base(DeclarativeBase):
    pass


class Tomato(Base):
    __tablename__ = 'tomato'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid: Mapped[str] = mapped_column(String, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    cancelled_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)


Base.metadata.create_all(engine)


@app.command()
def timer(title):
    with Session(engine) as session:
        tomato = Tomato(title=title, started_at=datetime.now())
        session.add(tomato)
        session.commit()
        session.refresh(tomato)
        try:
            TomatoBlock(title).run()
            tomato.completed_at = datetime.now()
            session.add(tomato)
            session.commit()
            session.refresh(tomato)
        except KeyboardInterrupt:
            tomato.cancelled_at = datetime.now()
            session.add(tomato)
            session.commit()
            print(f'[red]{EXIT_MESSAGE}[/red]')
            sys.exit(0)


@app.command()
def update():
    print('[blue]Updating tomato-blocks...[/blue]')
    print(BASE_DIR)
    os.chdir(BASE_DIR)

    print('[green]Building new wheel...[/green]')
    subprocess.call('poetry build', shell=True)

    wheel_path = next(BASE_DIR.joinpath('dist').glob('*.whl'))
    print('[green]Installing new wheel...[/green]')
    print(f'[green]{wheel_path.name}[/green]')
    subprocess.call(f'pip install --quiet --user {wheel_path} --force-reinstall', shell=True)
    print('[green]Done![/green]')


@app.command()
def daily():
    with Session(engine) as session:
        rows = session.execute(
            select(
                func.date(Tomato.started_at).label('date'),
                func.count(Tomato.started_at),
                func.count(Tomato.completed_at),
                func.count(Tomato.cancelled_at),
            )
            .group_by('date')
            .order_by('date')
        )
        print('[green]Daily Summary[/green]')
        print(tabulate(rows, headers=['Date', 'Started', 'Completed', 'Cancelled']))


@app.command()
def weekly():
    with Session(engine) as session:
        week_start_string = func.cast(func.cast(func.date_trunc('week', Tomato.started_at), Date), String)
        week_end_string = func.cast(
            func.cast(func.date_trunc('week', Tomato.started_at) + timedelta(days=6), Date), String
        )
        week_range_string = week_start_string + ' - ' + week_end_string
        rows = session.execute(
            select(
                week_range_string.label('week'),
                func.count(Tomato.started_at),
                func.count(Tomato.completed_at),
                func.count(Tomato.cancelled_at),
            )
            .group_by('week')
            .order_by('week')
        )
        print('[green]Weekly Summary[/green]')
        print(tabulate(rows, headers=['Week', 'Started', 'Completed', 'Cancelled']))


@app.command()
def categories():
    with Session(engine) as session:
        rows = session.execute(
            select(
                Tomato.title,
                func.count(Tomato.started_at),
                func.count(Tomato.completed_at),
                func.count(Tomato.cancelled_at),
            )
            .group_by(Tomato.title)
            .order_by(func.count(Tomato.started_at).desc())
        )
        print('[green]Categories Summary[/green]')
        print(tabulate(rows, headers=['Category', 'Started', 'Completed', 'Interrupted']))


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
