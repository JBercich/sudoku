#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging

__version__: str = "0.1.0"


logging.basicConfig(
    level=logging.DEBUG,
    datefmt="[%m-%d %H:%M:%S]",
    format="%(asctime)s %(name)-16s %(levelname)-9s %(message)s",
)
