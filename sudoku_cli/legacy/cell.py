#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import dataclasses
from typing import Any, Final


EMPTY_CELL_VALUE: Final[int] = 0


@dataclasses.dataclass
class Cell:
    value: int
    static: bool = False

    get_value_count: int = 0
    set_value_count: int = 0

    def __getattribute__(self, fieldname: str):
        if fieldname == "value":
            self.get_value_count += 1
        return super().__getattribute__(fieldname)

    def __setattr__(self, fieldname: str, value: Any):
        if fieldname == "value":
            self.set_value_count += 1
        return super().__setattr__(fieldname, value)

    def clear_value(self):
        self.value = 0

    def reset_value(self):
        self.value = 1


c = Cell(value=1, static=False)
_ = c.value
c.value = 3
print(c)
c.clear_value()
print(c)
c.reset_value()
print(c)

Cell(value=1, static=False).value = 1
