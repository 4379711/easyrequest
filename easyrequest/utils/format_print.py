# -*- coding: utf-8 -*-

colors = {
    'green': '32m',
    'blue': '34m',
    'red': '31m',
    'white': '37m'
}


def pprint(*args, color='red'):
    """
    Output different color fonts in the console.
    """
    tmp = colors.get(color, '31m')

    if len(args) == 1:
        print(f'''\033[{tmp}{args[0]}\033[0m''')
    else:
        for i in args:
            print(f'''\033[{tmp}{i}''', end=' ')
        print('\033[0m')
