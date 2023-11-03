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
from sqlalchemy import Column, DateTime, Integer, String, create_engine, func
from sqlalchemy.orm import Session, declarative_base
from tabulate import tabulate

from .tomato_block import TomatoBlock
from .weekly_schedule import WeeklySchedule

BASE_DIR = pathlib.Path().home().joinpath('code', 'projects', 'python', 'tomato-blocks')
EXIT_MESSAGE = '\n\nTimer Cancelled'
SQLITE_DB = 'tomato.db'

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(message)s')
file_handler = logging.FileHandler('tomato.log')
file_handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

app = typer.Typer()


engine = create_engine('postgresql://localhost/tomato')

Base = declarative_base()


class Tomato(Base):  # type: ignore
	__tablename__ = 'tomato'

	id = Column(Integer, primary_key=True)
	uuid = Column(String, default=uuid.uuid4)
	title = Column(String)
	started_at = Column(DateTime, nullable=True)
	completed_at = Column(DateTime, nullable=True)
	cancelled_at = Column(DateTime, nullable=True)


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
	with Session(engine) as session:
		rows = (
			session.query(
				# func.extract('date', Tomato.started_at).label('date'),
				func.date(Tomato.started_at).label('date'),
				func.count(Tomato.started_at).label('started'),
				func.count(Tomato.completed_at).label('completed'),
				func.count(Tomato.cancelled_at).label('cancelled'),
			)
			.group_by(func.date(Tomato.started_at))
			.order_by(func.date(Tomato.started_at))
			.all()
		)
		print('[green]Daily Summary[/green]')
		print(tabulate(rows, headers=['Date', 'Started', 'Completed', 'Interrupted']))


@app.command()
def weekly():
	with Session(engine) as session:
		rows = (
			session.query(
				func.extract('week', Tomato.started_at).label('week'),
				func.count(Tomato.started_at).label('started'),
				func.count(Tomato.completed_at).label('completed'),
				func.count(Tomato.cancelled_at).label('cancelled'),
			)
			.group_by(func.extract('week', Tomato.started_at))
			.order_by(func.extract('week', Tomato.started_at))
			.all()
		)
		print('[green]Weekly Summary[/green]')
		print(tabulate(rows, headers=['Week', 'Started', 'Completed', 'Interrupted']))


@app.command()
def categories():
	with Session(engine) as session:
		rows = (
			session.query(
				Tomato.title,
				func.count(Tomato.started_at).label('started'),
				func.count(Tomato.completed_at).label('completed'),
				func.count(Tomato.cancelled_at).label('cancelled'),
			)
			.group_by(Tomato.title)
			.order_by(func.count(Tomato.started_at).desc())
			.all()
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
