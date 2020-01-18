# -*- coding: utf-8 -*-

import time
from easyrequest import (
    schedule,
    load_tasks,
    timer_task_by_str,
    run_spider_name
)


def run_task_by_timer():
    for task_str in load_tasks():
        # register timer tasks
        timer_task_by_str(task_str)
    while True:
        schedule.run_pending()
        time.sleep(1)


def run_once(spider_name):
    run_spider_name(spider_name)


if __name__ == '__main__':
    run_once()
