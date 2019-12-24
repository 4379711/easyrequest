# -*- coding: utf-8 -*-
# @Time    : 2019/04/22 13:53
# @Author  : Liu Yalong
# @File    : mydata.py


class MyDict:

    def __getattr__(self, item):
        return None

    def __getitem__(self, item):
        return getattr(self, item)

    def __iter__(self):
        for k, v in self.__dict__.items():
            yield k, v

    def __len__(self):
        return len(self.__dict__)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __str__(self):
        return f'''< {__name__}.MyDict object at {hex(id(MyDict))}>'''

    def __repr__(self):
        return '''MyDict object ,just like :
                {'a': 5,
                 'b': [1, 2],
                 'c': {1, 2, 3}
                 }
                '''

    @staticmethod
    def _type_check_(key, expect_type):
        if not isinstance(key, expect_type):
            raise TypeError(f"The type of the value <{key}> was wrong, expected type: <{expect_type}>")

    def append_key(self, key, value):
        if key not in self.__dict__:
            self.__dict__[key] = []

        else:
            self._type_check_(self.__dict__[key], list)

        self.__dict__[key].append(value)

    def add_key(self, key, value):
        if key not in self.__dict__:
            self.__dict__[key] = set()

        else:
            self._type_check_(self.__dict__[key], set)

        self.__dict__[key].add(value)

    def keys(self):
        return self.__dict__.keys()
