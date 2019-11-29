# -*- coding: utf-8 -*-
# @Time    : 2019/11/12 13:41
# @Author  : Liu Yalong
# @File    : __init__.py.py
import click
from .cerate_project import CommandProject
from .create_spider import CommandSpider


@click.command(name='CreateProject')
# @click.option("--project_name", prompt="请输入模块名")  # prompt直接弹出一行，让用户输入
@click.argument('project_name')
def create_project_(project_name):
    """
    Create Project
    """
    CommandProject().run(project_name)


@click.command(name='CreateSpider')
@click.argument('spider_name')
def create_spider_(spider_name):
    """
    Create Spider
    """
    CommandSpider().run(spider_name)


# 分组功能，将多个命令分组
@click.group()
def base_command():
    pass


# 添加到组
base_command.add_command(create_project_)
base_command.add_command(create_spider_)

if __name__ == '__main__':
    base_command()
