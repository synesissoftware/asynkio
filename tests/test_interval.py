#! /usr/bin/env python3

# ######################################################################## #
# File:     tests/test_interval.py
#
# Created:  25th July 2025
# Updated:  26th July 2025
#
# Author:   Matthew Wilson
#
# Copyright (c) Matthew Wilson, Synesis Information Systems Pty Ltd
# All rights reserved
#
# ######################################################################## #


from asynkio.time import (
    Duration,
    Instant,
    Interval,
    # interval,
)

import asyncio
import pyclasp as clasp
import diagnosticism as d
import diagnosticism.severity as sev
import time


def _delta_as_ns(
    f: Instant,
    t: Instant,
) -> int:

    delta = int(t) - int(f)

    return delta

def _clipped_delta_as_ns(
    f: Instant,
    t: Instant,
    quantum_ns : int
) -> str:

    delta = int(t) - int(f)
    q, r = divmod(delta, quantum_ns)

    # d.dbgfl(f, t, delta, q, r)

    return Duration.from_nanos(r)


async def run_asyncio_sleep(
    label : str,
    timeout_ms : int,
    synchronous_sleep_ms : int,
):

    d.trace()

    t0 = Instant.now()

    t1 = t0

    while True:

        if synchronous_sleep_ms:

            time.sleep(synchronous_sleep_ms / 1_000)

        await asyncio.sleep(timeout_ms / 1_000)

        t2 = Instant.now()

        d.log(sev.NOTICE, f"{label} slept for {_delta_as_ns(t1, t2):,}; ∆={_clipped_delta_as_ns(t0, t2, timeout_ms * 1_000_000)}")

        t1 = t2


async def run_asynkio_interval(
    label : str,
    timeout_ms : int,
    synchronous_sleep_ms : int,
):

    d.trace()

    interval = Interval(Duration.from_millis(timeout_ms))

    t0 = Instant.now()

    t1 = t0

    count = 0

    delta = 1

    while True:

        if synchronous_sleep_ms:

            time.sleep(synchronous_sleep_ms / 1_000)

        await interval

        t2 = Instant.now()

        d.log(sev.NOTICE, f"{label} slept for {_delta_as_ns(t1, t2):,}; ∆={_clipped_delta_as_ns(t0, t2, timeout_ms * 1_000_000)}")

        t1 = t2


async def main():

    d.trace()

    await asyncio.gather(
        run_asyncio_sleep(   "asyncio.sleep     ", 5_000, synchronous_sleep_ms=0),
        run_asynkio_interval("asynkio.interval  ", 5_000, synchronous_sleep_ms=0),
        run_asyncio_sleep(   "asyncio.sleep    S", 5_000, synchronous_sleep_ms=1_000),
        run_asynkio_interval("asynkio.interval S", 5_000, synchronous_sleep_ms=1_000),
    )


if __name__ == "__main__":

    d.enable_logging('ENABLE_LOGGING', True)
    d.enable_tracing('ENABLE_TRACING', True)

    asyncio.run(main())