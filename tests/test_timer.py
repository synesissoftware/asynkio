#! /usr/bin/env python3

# ######################################################################## #
# File:     tests/test_timer.py
#
# Created:  25th July 2025
# Updated:  25th July 2025
#
# Author:   Matthew Wilson
#
# Copyright (c) Matthew Wilson, Synesis Information Systems Pty Ltd
# All rights reserved
#
# ######################################################################## #


import asyncio
import pyclasp as clasp
import diagnosticism as d
import diagnosticism.severity as sev
import time


async def run_sleep():

    d.trace()

    t1 = time.time_ns()

    while True:

        await asyncio.sleep(1)

        t2 = time.time_ns()

        d.log(sev.NOTICE, f"{d.func()} slept for {t2 - t1}")

        t1 = t2


async def run_delay():

    d.trace()

    t0 = time.perf_counter_ns()

    count = 0

    t1 = time.time_ns()

    delta = 1

    while True:

        await asyncio.sleep(delta)

        t2 = time.time_ns()

        d.log(sev.NOTICE, f"{d.func()} slept for {t2 - t1}")

        t1 = t2

        delta = 0.8


async def main():

    d.trace()

    await asyncio.gather(run_sleep(), run_delay())


if __name__ == "__main__":

    d.enable_logging('ENABLE_LOGGING', True)
    d.enable_tracing('ENABLE_TRACING', True)

    asyncio.run(main())