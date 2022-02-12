import asyncio
from datetime import datetime, timedelta
import sys
import telegram
import json
import time

import set_environ
from global_vars import last_update_telegram_id
from handle_messeges import digest, handle_all, null_coro, digest_update
from telegram_utils import get_new_updates
from lock_running import is_running_locked, lock_running

period = 1


async def main(loop):
    digest_task = loop.create_task(null_coro())
    handling_task = loop.create_task(null_coro())
    await digest_task
    await handling_task

    i = 0
    datetime_is_alive = datetime.now()

    while True:
        lock_running()
        try:
            new_updates = get_new_updates()
        except telegram.error.TimedOut as e:
            print('error: telegram.error.TimedOut...\ncontinue requesting for updates')
            new_updates = []
        
        if len(new_updates)>0:
            print(f'found {len(new_updates)} new updates')
        if datetime.now() > datetime_is_alive:
            print(f'{datetime.now()} - is alive message...')
            datetime_is_alive += timedelta(seconds=30)
        
        if new_updates:
            digest_task = loop.create_task(digest(new_updates))
            if handling_task.done():
                handling_task = loop.create_task(handle_all())
        
        await asyncio.sleep(period)
        i += 1


try:
    arg = sys.argv[1]
except:
    arg = None

if is_running_locked() and arg != 'force':
    print('bot is already running in a different process...')
    time.sleep(5)
else:
    lock_running()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
