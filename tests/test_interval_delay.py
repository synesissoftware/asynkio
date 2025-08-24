#! /usr/bin/env python3

# ######################################################################## #
# File:     tests/test_interval_delay.py
#
# Created:  3rd August 2025
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
import time


async def run_with_delays(
    delay_increment,
    delay_duration,
):

    d.trace()

    interval = Interval(
        Duration.from_secs(1),
        missed_tick_behaviour=MissedTickBehaviour.DELAY,
    )

    t0 = Instant.now()

    t1 = t0

    count = 0

    while True:

        if 0 != count and 0 == (count % delay_increment):

            d.log(sev.INFO, f"⌛  hard sleeping for {delay_duration} ...")

            time.sleep(int(delay_duration) / 1_000_000_000.0)

        await interval

        count += 1

        t2 = Instant.now()

        p = interval.period()

        delta_1 = t2 - t1
        delta_N = t2 - t0
        delta_M = p * count

        d.log(sev.INFO, f"⚙️  #{count} : ∆={delta_N}, ∂={delta_1}, {(delta_N - delta_M).as_nanos():,} ({delta_N - delta_M})") # x̄∆={Duration.from_nanos((t2 - t0).as_nanos() % 1_000_000_000)}")
        # d.log(sev.INFO, f"⚙️  #{count} : {t2 - t0}, {t2 - t1} ({(t2 - t1).as_nanos()}), {Duration.from_nanos((t2 - t0).as_nanos() % 1_000_000_000)}")

        t1 = t2



async def main():

    d.trace()

    delay_increment = 12
    delay_duration = Duration.from_millis(4_700)

    t = asyncio.create_task(run_with_delays(
        delay_increment,
        delay_duration,
    ))

    await asyncio.gather(t)


if __name__ == "__main__":

    d.enable_logging('ENABLE_LOGGING', True)
    d.enable_tracing('ENABLE_TRACING', True)

    try:

        asyncio.run(main())
    except KeyboardInterrupt:

        pass
