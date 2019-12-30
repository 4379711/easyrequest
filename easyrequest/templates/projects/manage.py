#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from easyrequest import (
    schedule,
    load_tasks,
    timer_task_by_str,
)

for task_str in load_tasks():
    # register timer tasks
    timer_task_by_str(task_str)

if __name__ == '__main__':

    while True:
        schedule.run_pending()
        time.sleep(1)
