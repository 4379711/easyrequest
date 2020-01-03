# -*- coding: utf-8 -*-
# @Time    : 2019/11/12 13:41
# @Author  : Liu Yalong
# @File    : __init__.py.py
from os.path import exists
from subprocess import Popen, PIPE
import click
import psutil

from .cerate_project import CommandProject
from .create_spider import CommandSpider
from .start_spider import CommandStartSpider
import os


@click.command(name='CreateProject')
# @click.option("--project_name", prompt="请输入模块名")  # prompt直接弹出一行，让用户输入
@click.argument('project_name')
def create_project_(project_name):
    """
    Create a spider project
    """
    CommandProject().run(project_name)


@click.command(name='CreateSpider')
@click.argument('spider_name')
def create_spider_(spider_name):
    """
    Create a Spider for project ,must create project before
    """
    CommandSpider().run(spider_name)


@click.command(name='RunSpider')
@click.argument('spider_name')
def run_spider_(spider_name):
    """
    Run Spider to get data
    """
    pid = os.getpid()
    to_write_file = str(spider_name) + '.pid'
    with open(to_write_file, 'w', encoding='utf-8') as f:
        f.write(str(pid))
        f.flush()
    CommandStartSpider().run(spider_name)


@click.command(name='StopSpider')
@click.argument('spider_name')
def stop_spider_(spider_name):
    """
    Stop a Spider
    """
    to_read_file = str(spider_name) + '.pid'
    if not exists(to_read_file):
        print('spider maybe not running')
        return
    with open(to_read_file, 'r', encoding='utf-8') as f:
        pid = int(f.readline())
        pid_list = psutil.pids()
        if pid not in pid_list:
            print('spider maybe not running')

    os.remove(to_read_file)
    command = f'taskkill /pid {pid} -f'

    pp = Popen(command,
               shell=True,
               universal_newlines=True,
               stdin=PIPE,
               stderr=PIPE,
               stdout=PIPE)
    pp.communicate()

    pid_list = psutil.pids()
    if int(pid) not in pid_list:
        print('stop spider successful')
    else:
        print('stop spider failed')


# 分组功能，将多个命令分组
@click.group()
def base_command():
    pass


# 添加到组
base_command.add_command(create_project_)
base_command.add_command(create_spider_)
base_command.add_command(run_spider_)
base_command.add_command(stop_spider_)

if __name__ == '__main__':
    base_command()
