import time

import psutil

from CineWinx.misc import _boot_
from .formatters import get_readable_time


async def bot_sys_stats():
    bot_uptime = int(time.time() - _boot_)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    up = f"{get_readable_time(bot_uptime)}"
    cpu = f"{cpu}%"
    ram = f"{mem}%"
    disk = f"{disk}%"
    return up, cpu, ram, disk
