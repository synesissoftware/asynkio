#! /usr/bin/env python3

# ######################################################################## #
# File:     examples/interval_skip.py
#
# Purpose:  `Interval` demonstration with `SKIP` missed-tick behaviour.
#
# Created:  3rd August 2025
# Updated:  12th July 2026
#
# Author:   Matthew Wilson
#
# Copyright (c) Matthew Wilson, Synesis Information Systems Pty Ltd
# All rights reserved
#
# ######################################################################## #


import asyncio
import time

import diagnosticism as d
import diagnosticism.severity as sev

from asynkio.time import (
    Duration,
    Instant,
    Interval,
    MissedTickBehaviour,
)


async def run_with_skips(
    skip_increment,
    skip_duration,
):

    d.trace()

    interval = Interval(
        Duration.from_secs(1),
        missed_tick_behaviour=MissedTickBehaviour.SKIP,
    )

    t0 = Instant.now()

    t1 = t0

    count = 0

    while True:

        if 0 != count and 0 == (count % skip_increment):

            d.log(sev.INFO, f"⌛  hard sleeping for {skip_duration} ...")

            time.sleep(int(skip_duration) / 1_000_000_000.0)

        await interval

        count += 1

        t2 = Instant.now()

        p = interval.period()

        delta_1 = t2 - t1
        delta_N = t2 - t0
        delta_M = p * count
        delta_I = Duration.from_nanos(delta_N.as_nanos() % p.as_nanos())
        skew = delta_N - delta_M

        d.log(
            sev.INFO,
            f"⚙️  #{count} : ∆={delta_N}, ∂={delta_1}, {(skew).as_nanos():,} ({skew}); ∂={delta_I}",
        )

        t1 = t2


async def main():

    d.trace()

    skip_increment = 12
    skip_duration = Duration.from_millis(4_700)

    t = asyncio.create_task(
        run_with_skips(
            skip_increment,
            skip_duration,
        )
    )

    await asyncio.gather(t)


if __name__ == "__main__":

    d.enable_logging('ENABLE_LOGGING', True)
    d.enable_tracing('ENABLE_TRACING', True)

    try:

        asyncio.run(main())
    except KeyboardInterrupt:

        pass

