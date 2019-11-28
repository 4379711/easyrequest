# -*- coding: utf-8 -*-
# @Time    : 2019/11/12 13:41
# @Author  : Liu Yalong
# @File    : __init__.py.py
import click
from .cerate_project import Command


@click.command(name='CreateProject')
@click.option("--project_name", prompt="请输入模块名")  # prompt直接弹出一行，让用户输入
def create_project_(project_name):
    """
    创建项目
    """
    click.echo(f'{project_name}即将创建')
    Command().run(project_name)

    click.echo(f'{project_name}创建完成')


# 分组功能，将多个命令分组
@click.group()
def base_command():
    pass


# 添加到组
base_command.add_command(create_project_)
# base_command.add_command(list_module)

if __name__ == '__main__':
    base_command()
