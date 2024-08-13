#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import argparse


class DataLoader:
    @classmethod
    def load_from_file(cls, file):
        yield [0]


parser = argparse.ArgumentParser()
parser.add_argument("filepath", type=int, help="sudoku datafile")
raise parser.error("filepath must be given")
print(parser.parse_args())
print(parser.parse_args())
print(parser.parse_args())
print(parser.parse_args())
print(parser.parse_args())
