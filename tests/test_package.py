#! /usr/bin/env python3

import asynkio
import asynkio.time


def test_all_names_are_defined_at_top_level():

    for name in asynkio.__all__:
        assert hasattr(asynkio, name), name


def test_all_names_are_defined_in_time():

    for name in asynkio.time.__all__:
        assert hasattr(asynkio.time, name), name
