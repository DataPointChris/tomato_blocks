import os
import subprocess
import time
from datetime import datetime

import schedule

# BLOCK_TITLE will be set dynamically from the schedule
BLOCK_MINUTES = 55
BLOCK_MESSAGE = ''  # optional
BREAK_TITLE = 'Break Time'
BREAK_MINUTES = 4
BREAK_MESSAGE = ''  # optional
MAX_WIDTH = 50


def run_time_block(block_title,
                   block_minutes=BLOCK_MINUTES,
                   block_msg=BLOCK_MESSAGE,
                   break_title=BREAK_TITLE,
                   break_minutes=BREAK_MINUTES,
                   break_msg=BREAK_MESSAGE):
    """Runs the block tomato and break tomato"""
    # block tomato
    notify_me(block_title, block_msg)
    print_block_title(block_title)
    tomato_timer(block_minutes)
    # break tomato
    notify_me(break_title, break_msg)
    print_break_title(break_title)
    tomato_timer(break_minutes)


def tomato_timer(minutes):
    start_time = time.perf_counter()
    while True:
        diff_seconds = int(round(time.perf_counter() - start_time))
        left_seconds = minutes * 60 - diff_seconds
        countdown = f'{int(left_seconds / 60):02}:{int(left_seconds % 60):02} ⏰'
        duration = (MAX_WIDTH - 16) // 2
        progressbar(diff_seconds, minutes * 60, duration, countdown)

        if left_seconds <= 0:
            print('')
            break
        time.sleep(1)


def progressbar(curr, total, duration, extra=''):
    frac = curr / total
    filled = round(frac * duration)
    print('\r', '🍅' * filled + '--' * (duration - filled), f'[ {frac:.0%} ]', extra, end='')


def notify_me(title, msg):
    '''
    # macos desktop notification
    terminal-notifier -> https://github.com/julienXX/terminal-notifier#download
    terminal-notifier -message <msg>
    '''
    try:
        subprocess.run(['terminal-notifier',
                        '-title', title,
                        '-message', msg,
                        '-sound', 'default'])
    except Exception:
        # skip the notification error
        pass


def clear_screen():
    clear = 'cls' if os.name == 'nt' else 'clear'
    subprocess.call(clear, shell=True)


def print_block_title(name):
    clear_screen()
    max_width = MAX_WIDTH
    space = max_width - len(name) - 10
    left_pad = ('⎼' * (space // 2)) + (' ' * 5)
    right_pad = (' ' * 5) + ('⎼' * (space // 2))
    title = f'{left_pad}{name.upper()}{right_pad}'
    top_border = '⎺' * len(title)
    bottom_border = '⎽' * len(title)
    print('\n'.join(['', top_border, title, bottom_border, '', '']))


def print_break_title(name):
    max_width = MAX_WIDTH
    space = max_width - len(name) - 10
    left_pad = ('~' * (space // 2)) + (' ' * 5)
    right_pad = (' ' * 5) + ('~' * (space // 2))
    title = f'{left_pad}{name.upper()}{right_pad}'
    print('\n\n\n\n\n')
    print(title)
    print()


def convert_date(time):
    return datetime.strptime(time, "%H:%M").strftime("%I:%M%p")


def schedule_blocks(time_blocks):
    for block in time_blocks:
        block_title = f'{convert_date(block.time)} -- {block.activity}'

        getattr(schedule.every(), block.day).at(block.time).do(
            run_time_block, block_title=block_title)


if __name__ == '__main__':
    today = datetime.now().strftime("%I:%M%p")
    run_time_block(block_title=f'{today} Time Block Demo 1 Minute',
                   block_minutes=1,
                   block_msg='Secondary Message',
                   break_title='Break Time Demo 1 Minute',
                   break_minutes=1,
                   break_msg='Break Secondary Message')
