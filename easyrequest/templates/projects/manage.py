#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from easyrequest import schedule, run_spider_name, load_tasks
import time

load_tasks()

if __name__ == '__main__':

    while True:
        schedule.run_pending()
        time.sleep(1)
