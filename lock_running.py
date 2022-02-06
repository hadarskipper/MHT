from marshal import load
import os
import json
import psutil
from datetime import datetime

lock_file = 'current_running_pid.lock'

def is_running_locked():
    ret = False
    if os.path.isfile(lock_file):
        lock_dict = json.load(lock_file)
        
        current_pid = lock_dict['current_pid']
        datetime_alive = lock_dict['datetime_alive']
        ret = psutil.pid_exists(current_pid)
    
    return ret


def lock_running():
    lock_dict = {}
    current_pid = os.getpid()
    datetime_alive = datetime.now()

    json.dump(lock_dict, lock_file)
