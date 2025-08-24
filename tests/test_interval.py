#! /usr/bin/env python3

# ######################################################################## #
# File:     tests/test_interval.py
#
# Created:  25th July 2025
# Updated:  4th August 2025
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
    MissedTickBehaviour,
)

import asyncio
import diagnosticism as d
import diagnosticism.severity as sev
import sys
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

    interval = Interval(Duration.from_millis(timeout_ms), name=label, missed_tick_behaviour=MissedTickBehaviour.SKIP)

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


async def heartbeat(
    missed_tick_behaviour : MissedTickBehaviour,
):

    d.trace()

    interval = Interval(
        Duration.from_secs(1),
        missed_tick_behaviour=missed_tick_behaviour,
        name="heartbeat",
        negative_bias=1_200_000,
    )

    t0 = Instant.now()

    t1 = t0

    count = 0

    while True:

        await interval

        count += 1

        t2 = Instant.now()

        d.log(sev.INFO, f"❤️  #{count} : {t2 - t0}, {t2 - t1}, {Duration.from_nanos((t2 - t0).as_nanos() % 1_000_000_000)}")

        t1 = t2


async def main(
    missed_tick_behaviour : MissedTickBehaviour,
):

    d.trace()

    await asyncio.gather(
        heartbeat(missed_tick_behaviour),
        run_asyncio_sleep(   "asyncio.sleep      ", 5_000, synchronous_sleep_ms=0),
        run_asynkio_interval("asynkio.interval a1", 2_500, synchronous_sleep_ms=0),

        # run_asyncio_sleep(   "asyncio.sleep      ", 5_000, synchronous_sleep_ms=0),
        # run_asynkio_interval("asynkio.interval a1", 2_500, synchronous_sleep_ms=0),
        # run_asynkio_interval("asynkio.interval a2", 5_000, synchronous_sleep_ms=0),
        # run_asynkio_interval("asynkio.interval a3", 5_000, synchronous_sleep_ms=0),
        # run_asynkio_interval("asynkio.interval a4", 5_000, synchronous_sleep_ms=0),
        # run_asynkio_interval("asynkio.interval a5", 5_000, synchronous_sleep_ms=0),
        # run_asyncio_sleep(   "asyncio.sleep    S", 5_000, synchronous_sleep_ms=1_000),
        # run_asynkio_interval("asynkio.interval S1", 2_500, synchronous_sleep_ms=2_000),
        # run_asynkio_interval("asynkio.interval S2", 5_000, synchronous_sleep_ms=5_500),
    )

def show_help(
    file
):

    d.abort(f"USAGE: {d.get_program_name()} {{ burst | delay | skip }}", file=file, show_program_name=False)

if __name__ == "__main__":

    d.enable_logging('ENABLE_LOGGING', True)
    d.enable_tracing('ENABLE_TRACING', True)

    if len(sys.argv) != 2:

        show_help(file=sys.stderr)
    else:

        if '--help' == sys.argv[1]:

            show_help(file=sys.stdout)

        missed_tick_behaviour = MissedTickBehaviour.try_parse(sys.argv[1])

        if not missed_tick_behaviour:

            d.abort(f"unrecognised missed-tick-behaviour '{sys.argv[1]}'", trailing_prompt=True)
        else:

            print(f"running with {missed_tick_behaviour}")

            try:

                asyncio.run(main(missed_tick_behaviour))
            except KeyboardInterrupt:

                pass