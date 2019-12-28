#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from easyrequest import (
    schedule,
    load_tasks,
    timer_task_by_str,
    run_spider_name  # can not remove this package
)

for task_str in load_tasks():
    timer_task_by_str(task_str)

while True:
    schedule.run_pending()
    time.sleep(1)
