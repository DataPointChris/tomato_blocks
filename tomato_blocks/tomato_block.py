import contextlib
import os
import subprocess
import time
from datetime import datetime


class TomatoBlock:
    def __init__(self, title: str, duration: int = 50, max_width: int = int(os.get_terminal_size().columns * 0.9)):
        self.title = f"{datetime.now().strftime('%A %D %I:%M%p')} - {title}"
        self.duration = duration
        self.max_width = max_width

    def _tomato_timer(self) -> None:
        start_time = time.time()
        total_seconds = self.duration * 60
        bar_width = (self.max_width - 16) // 2
        while True:
            elapsed_seconds = int(time.time() - start_time)
            remaining_seconds = total_seconds - elapsed_seconds
            pct_complete = elapsed_seconds / total_seconds
            countdown = f'{int(remaining_seconds / 60):02}:{int(remaining_seconds % 60):02} ⏰'
            filled = int(pct_complete * bar_width)
            progress_bar = f'\r{"🍅" * filled}{"--" * (bar_width - filled)} [ {pct_complete:.0%} ] {countdown}'
            print(progress_bar, end='')

            if remaining_seconds <= 0:
                print()
                break
            time.sleep(1)

    def _notify(self, message: str):
        """
        # macos desktop notification
        terminal-notifier -> https://github.com/julienXX/terminal-notifier#download
        """
        with contextlib.suppress(Exception):  # pass if terminal-notifier is not installed
            subprocess.run(['terminal-notifier', '-title', 'Tomato Blocks', '-message', message])

    def _print_title(self):
        pad_size = 5
        space = self.max_width - len(self.title) - (pad_size * 2)
        left_pad = ('⎼' * (space // 2)) + (' ' * pad_size)
        right_pad = (' ' * pad_size) + ('⎼' * (space // 2))
        padded_title = f'{left_pad}{self.title}{right_pad}'
        top_border = '⎺' * len(padded_title)
        bottom_border = '⎽' * len(padded_title)
        print()
        print(top_border)
        print(padded_title)
        print(bottom_border)
        print()

    def _clear_screen(self):
        clear = 'cls' if os.name == 'nt' else 'clear'
        subprocess.call(clear, shell=True)

    def run(self):
        self._clear_screen()
        self._print_title()
        self._tomato_timer()
        self._notify(f'{self.title} Completed')
