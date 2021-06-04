import time
import schedule
import block_schedule
import tomato_blocks

tomato_blocks.schedule_blocks(block_schedule.all_time_blocks)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)

except KeyboardInterrupt:
    print('\n'.join(['', '', 'Timer Quit', '👋 Good-bye']))
