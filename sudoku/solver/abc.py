#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from abc import ABC, abstractmethod


class Solver(ABC):
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def setup(self, *args, **kwargs) -> bool:
        raise NotImplementedError

    @abstractmethod
    def solve(self, *args, **kwargs) -> bool:
        raise NotImplementedError

    @abstractmethod
    def check(self, *args, **kwargs) -> bool:
        raise NotImplementedError
