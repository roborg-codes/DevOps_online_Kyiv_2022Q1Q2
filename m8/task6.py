#!/bin/env python3

import os
import psutil
import math
from typing import Union

def status_bar(i: Union[int, float], width: int, sign: str) -> str:
    l: int = int(width * i // 100) - 2
    r: int = width - l - 2
    return "[" + (sign * l) + (" " * r) + "]\n"

def in_gigabytes(x: int) -> float:
    return x / math.pow(1024, 3)


def main() -> int:
    term_w, _ = os.get_terminal_size()
    output: str = "System info".center(term_w)

    '''
    CPU
    '''
    cpu_cnt = psutil.cpu_count(logical=True)
    cpu_load = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq()

    output += f"\nCPU ".ljust(term_w, '=')
    output += f"\nCount: {cpu_cnt}\n"
    output += f"Load: {cpu_load}%\n"
    output += f"Frequecny: {cpu_freq.current:.0f} MHz / {cpu_freq.max:.0f} MHz\n"
    with open("/proc/cpuinfo", "r") as cpuinfo:
        for line in cpuinfo.readlines():
            if line.startswith("model name"):
                output += line.replace("model name	: ", "Model: ")
                break


    '''
    RAM
    '''
    ram = psutil.virtual_memory()
    swap = psutil.swap_memory()

    output += f"\nRAM ".ljust(term_w, '=')
    output += f"\nTotal: {in_gigabytes(ram.total):.1f} GB\n"
    output += f"Available: {in_gigabytes(ram.available):.1f} GB\n"
    output += status_bar(ram.percent, int(term_w/2), "*")
    output += f"Usage: {ram.percent:.0f}%\n"
    if swap.total > 0:
        output += f"\nSWAP ".ljust(term_w, '=')
        output += f"\nTotal: {in_gigabytes(swap.total):.1f}\n"
        output += f"Free: {in_gigabytes(swap.free):.1f}\n"
        output += status_bar(swap.percent, term_w, '=')
        output += f"Usage: {swap.percent:.0f}%\n"

    '''
    Storage
    '''
    # psutil.disk_usage()

    output += f"\nStorage ".ljust(term_w, '=')
    for part in psutil.disk_partitions():
        stat = psutil.disk_usage(part.mountpoint)
        output += f"\nDevice: {part.device}"
        output += f" mounted -> '{part.mountpoint}'\n"
        output += f"\tFilesystem: {part.fstype}\n"
        output += f"\tSpace used: {stat.percent}%\n"
        output += f"\tFree space: {in_gigabytes(stat.total - stat.used):.1f} GB / {in_gigabytes(stat.total):.1f} GB\n"


    '''
    Battery
    '''
    bat = psutil.sensors_battery()
    if bat:
        bat_status = "Charging" if bat.power_plugged else "Discharging" if bat.power_plugged == False else "Unknown"
        output += "\nBattery ".ljust(term_w, '=')
        output += f"\nCharge: {bat.percent:.2f}%\n"
        output += status_bar(bat.percent, int(term_w/2), "⚡")
        output += f"Battery status: {bat_status}\n"
        if not bat.power_plugged and bat.secsleft > 0:
            output += f"Time left: {bat.secsleft}\n"

    print(output)
    return 0


if __name__ == "__main__":
    exit(main())
