#! /usr/bin/env python3

# ######################################################################## #
# File:     examples/interval_burst.py
#
# Purpose:  `Interval` demonstration with `BURST` missed-tick behaviour.
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


async def run_with_bursts(
    burst_increment,
    burst_duration,
):

    d.trace()

    interval = Interval(
        Duration.from_secs(1),
        missed_tick_behaviour=MissedTickBehaviour.BURST,
    )

    t0 = Instant.now()

    t1 = t0

    count = 0

    while True:

        if 0 != count and 0 == (count % burst_increment):

            d.log(sev.NOTICE, f"⌛  hard sleeping for {burst_duration} ...")

            time.sleep(int(burst_duration) / 1_000_000_000.0)

        await interval

        count += 1

        t2 = Instant.now()

        p = interval.period()

        delta_1 = t2 - t1
        delta_N = t2 - t0
        delta_M = p * count

        d.log(
            sev.INFO,
            f"⚙️  #{count} : ∆={delta_N}, ∂={delta_1}, {(delta_N - delta_M).as_nanos():,} ({delta_N - delta_M})",
        )

        t1 = t2


async def main():

    d.trace()

    burst_increment = 12
    burst_duration = Duration.from_millis(4_700)

    t = asyncio.create_task(
        run_with_bursts(
            burst_increment,
            burst_duration,
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

