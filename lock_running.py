import os
import psutil

lock_file = 'current_running_pid.lock'

def is_running_locked():
    ret = False
    if os.path.isfile(lock_file):
        with open(lock_file, 'r') as f:
            current_pid = int(f.read())
        
        ret = psutil.pid_exists(current_pid)
    
    return ret


def lock_running():
    with open(lock_file, 'w') as f:
        f.write(str(os.getpid()))
