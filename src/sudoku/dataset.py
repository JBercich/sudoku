#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from csv import DictReader
from datetime import datetime
from enum import Enum, unique
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, computed_field


@unique
class Level(Enum):
    EASY = (0, "Easy", 0, 15)
    MEDIUM = (1, "Medium", 15, 25)
    HARD = (2, "Hard", 25, 35)
    MASTER = (3, "Master", 35, 45)
    EXTREME = (4, "Extreme", 45, 55)
    IMPOSSIBLE = (5, "Impossible", 55, 80)

    def __new__(cls, level: int, title: str, lower_bound: int, upper_bound: int):
        instance: Level = object.__new__(cls)
        instance._value: tuple = instance
        instance.level: int = level
        instance.title: str = title
        instance.lower_bound: int = lower_bound
        instance.upper_bound: int = upper_bound
        return instance

    def contains(self, value: int) -> bool:
        return value > self.lower_bound and value <= self.upper_bound


class Problem(BaseModel):
    problem: str = Field(
        ...,
        pattern=r"[0-9]{81}",
        description="",
    )
    solution: str = Field(
        ...,
        pattern=r"[1-9]{81}",
        description="",
    )
    uuid: UUID = Field(
        ...,
        default_factory=uuid4,
        description="",
    )
    timestamp: datetime = Field(
        ...,
        default_factory=datetime.now,
        description="",
    )

    @computed_field(description="")
    @property
    def level(self) -> Level:
        return next(x for x in Level if x.contains(self.problem.count("0"))).level


class Dataset:
    _HEADERS: list[str] = ["problem", "solution"]

    def __init__(self, file: str, headers: list[str] = _HEADERS, records: int = 1e3):
        self.entries: list[Problem] = []
        with open(file, "r") as fp:
            reader: DictReader = DictReader(fp, fieldnames=headers)
            next(reader, None)
            for record in reader:
                self.entries.append(Problem(**record))
                if reader.line_num > records:
                    break
