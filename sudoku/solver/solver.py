#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Base solver abstract class."""

from abc import ABC, abstractclassmethod


class Solver(ABC):
    @classmethod
    def a(cls):
        pass


# g = Grid()
# g[0, 8] = 9
# print(g)
# print(g._get_count)
# for i in range(9):
#     for j in range(9):
#         print((i, j), g[i, j].value)

# #         if re.fullmatch(r"[0-9].{0,81}", grid) is None:
# #         "070000043040009610800634900094052000358460020000800530080070091902100005007040802"
