import logging
import os
import pathlib
import subprocess
import sys
import time
import uuid
from datetime import datetime

import schedule
import typer
from rich import print
from sqlalchemy import (Boolean, Column, DateTime, Integer, String,
                        create_engine, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .tomato_block import TomatoBlock
from .weekly_schedule import WeeklySchedule

BASE_DIR = pathlib.Path().home().joinpath('code', 'projects', 'python', 'tomato-blocks')
EXIT_MESSAGE = '\n\nTimer Interrupted'
SQLITE_DB = 'tomato.db'

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(message)s')
file_handler = logging.FileHandler('tomato.log')
file_handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

app = typer.Typer()


engine = create_engine('sqlite:///tomato.db')
Base = declarative_base()


class Tomato(Base):
    __tablename__ = 'tomato'

    id = Column(Integer, primary_key=True)
    iso_8601 = Column(DateTime)
    uuid = Column(String)
    title = Column(String)
    started = Column(Boolean)
    completed = Column(Boolean)
    interrupted = Column(Boolean)


Base.metadata.create_all(engine)


def log_to_sql(iso_8601, uid, title, started=False, completed=False, interrupted=False):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()

        tomato_block = Tomato(
            iso_8601=datetime.strptime(iso_8601, '%Y-%m-%d %H:%M:%S'),
            uuid=uid,
            title=title,
            started=started,
            completed=completed,
            interrupted=interrupted,
        )
        session.add(tomato_block)
        session.commit()
    except Exception as e:
        print(f'[red]\n\nLogging to SQL crashed:\n{e}[/red]')


@app.command()
def timer(title):
    iso_8601 = datetime.now().isoformat(sep=' ', timespec='seconds')
    uid = uuid.uuid4()
    try:
        logger.info(f"{iso_8601} | {uid} | {title} | started")
        log_to_sql(iso_8601, str(uid), title, started=True)
        TomatoBlock(title).run()
        logger.info(f"{iso_8601} | {uid} | {title} | completed")
        log_to_sql(iso_8601, str(uid), title, completed=True)
    except KeyboardInterrupt:
        logger.info(f"{iso_8601} | {uid} | {title} | interrupted")
        log_to_sql(iso_8601, str(uid), title, interrupted=True)
        print(EXIT_MESSAGE)
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
    Session = sessionmaker(bind=engine)
    session = Session()

    rows = (
        session.query(
            func.date(Tomato.iso_8601).label('date'),
            func.sum(Tomato.started).label('started'),
            func.sum(Tomato.completed).label('completed'),
            func.sum(Tomato.interrupted).label('interrupted'),
        )
        .group_by(func.date(Tomato.iso_8601))
        .order_by(func.date(Tomato.iso_8601))
        .all()
    )

    print('[green]Daily Summary[/green]')
    print(f"| {'Date':<10} | {'Started':<8} | {'Completed':<9} | {'Interrupted':<10} |")
    print('-' * 71)
    for row in rows:
        print(f"| {row.date:<10} | {row.started:>8} | {row.completed:>9} | {row.interrupted:>11} |")


@app.command()
def weekly():
    Session = sessionmaker(bind=engine)
    session = Session()

    rows = (
        session.query(
            func.strftime('%W', Tomato.iso_8601).label('week'),
            func.sum(Tomato.started).label('started'),
            func.sum(Tomato.completed).label('completed'),
            func.sum(Tomato.interrupted).label('interrupted'),
        )
        .group_by(func.strftime('%W', Tomato.iso_8601))
        .order_by(func.strftime('%W', Tomato.iso_8601))
        .all()
    )

    print('[green]Weekly Summary[/green]')
    print(f"| {'Week':<10} | {'Started':<8} | {'Completed':<9} | {'Interrupted':<10} |")
    print('-' * 71)
    for row in rows:
        print(f"| {row.week:<10} | {row.started:>8} | {row.completed:>9} | {row.interrupted:>11} |")


@app.command()
def categories():
    Session = sessionmaker(bind=engine)
    session = Session()

    rows = (
        session.query(
            Tomato.title,
            func.sum(Tomato.started).label('started'),
            func.sum(Tomato.completed).label('completed'),
            func.sum(Tomato.interrupted).label('interrupted'),
        )
        .group_by(Tomato.title)
        .order_by(func.sum(Tomato.started).desc())
        .all()
    )

    print('[green]Categories Summary[/green]')
    print(f"| {'Category':<30} | {'Started':<8} | {'Completed':<9} | {'Interrupted':<10} |")
    print('-' * 71)
    for row in rows:
        print(f"| {row.title:<30} | {row.started:>8} | {row.completed:>9} | {row.interrupted:>11} |")


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
