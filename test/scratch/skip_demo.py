#! /usr/bin/env python3

# ######################################################################## #
# File:     test/scratch/skip_demo.py
#
# Purpose:  Busy multi-task scratch demo for `Interval` SKIP heartbeats,
#           recording per-task timings with Diagnosticism DOOMGrams. It is
#           intended to stress the event loop in the spirit of the SKIP
#           triple-fire observation.
#
# Created:  12th July 2026
# Updated:  12th July 2026
#
# Author:   Matthew Wilson
#
# Copyright (c) Matthew Wilson, Synesis Information Systems Pty Ltd
# All rights reserved
#
# ######################################################################## #


"""
Run:

    ENABLE_LOGGING=1 uv run python test/scratch/skip_demo.py

Every 15s the SKIP heartbeat logs at INFORMATIONAL with a DOOMGram for the
heartbeat preparation itself (via DOOMScope) plus DOOMGrams for the busy
service tasks.
"""

from __future__ import annotations

import asyncio
import random
import time

import diagnosticism as d
from diagnosticism import nanoseconds_to_string
import diagnosticism.severity as sev

from asynkio.time import (
    Duration,
    Instant,
    Interval,
    MissedTickBehaviour,
)

HEARTBEAT_PERIOD_SECS = 10


async def busy_service(
    name: str,
    gram: d.DOOMGram,
    *,
    async_busy_lo_ms: float,
    async_busy_hi_ms: float,
    hard_sleep_lo_ms: float = 0.0,
    hard_sleep_hi_ms: float = 0.0,
    hard_sleep_every: int = 0,
) -> None:
    """
    Notionally real service work: mostly async-busy, occasionally hard-blocking
    the event loop so SKIP heartbeats can lag under load.
    """

    d.trace()

    task = asyncio.current_task()
    if task is not None:

        task.set_name(name)

    n = 0

    while True:

        n += 1

        async_ms = random.uniform(async_busy_lo_ms, async_busy_hi_ms)

        with d.DOOMScope(gram):

            # synthesised "busy" activity (yields to the loop)
            await asyncio.sleep(async_ms / 1_000)

            if hard_sleep_every and n % hard_sleep_every == 0:

                hard_ms = random.uniform(hard_sleep_lo_ms, hard_sleep_hi_ms)

                if hard_ms > 0:

                    # block the loop — mirrors websocket / sync work pressure
                    time.sleep(hard_ms / 1_000)

        # keep the scheduler saturated without monopolising one task forever
        await asyncio.sleep(0)


async def heartbeat(
    heartbeat_gram: d.DOOMGram,
    service_grams: dict[str, d.DOOMGram],
) -> None:
    """
    SKIP-mode Interval heartbeat every HEARTBEAT_PERIOD_SECS.
    """

    d.trace()

    interval = Interval(
        Duration.from_secs(HEARTBEAT_PERIOD_SECS),
        missed_tick_behaviour=MissedTickBehaviour.SKIP,
        name='skip-demo-heartbeat',
    )

    t0 = Instant.now()
    t_prev = t0
    count = 0

    while True:

        await interval

        count += 1

        now = Instant.now()

        # Floored whole seconds since heartbeat start — repeats on accidental
        # multi-fire within the same second (the SKIP defect signature).
        elapsed_s = (now - t0).as_secs()

        # Wall time since the previous heartbeat (near-zero on multi-fire).
        since_last = nanoseconds_to_string((now - t_prev).as_nanos())
        t_prev = now

        with d.DOOMScope(heartbeat_gram):

            service_parts = []

            for name, gram in service_grams.items():

                service_parts.append(
                    f"{name} {gram.to_strip()} ({gram.to_nmmm()})",
                )

            body = ' | '.join(service_parts)

        d.log(
            sev.INFORMATIONAL,
            f"❤️  #{count} +{elapsed_s}s ∂={since_last} hb={heartbeat_gram.to_nmmm()} | {body}",
        )


def _epsilon_thread_main() -> None:
    """
    Runs on a worker thread: emit a blank line once per second.
    """

    while True:

        print()
        time.sleep(1.0)


async def epsilon() -> None:
    """
    Offload blank-line ticking to the default thread-pool executor so it is
    independent of event-loop load.
    """

    d.trace()

    loop = asyncio.get_running_loop()

    await loop.run_in_executor(None, _epsilon_thread_main)


async def main() -> None:

    d.trace()

    heartbeat_gram = d.DOOMGram()

    service_grams = {
        'alpha': d.DOOMGram(),
        'bravo': d.DOOMGram(),
        'charlie': d.DOOMGram(),
        'delta': d.DOOMGram(),
    }

    await asyncio.gather(
        heartbeat(heartbeat_gram, service_grams),
        epsilon(),
        busy_service(
            'alpha',
            service_grams['alpha'],
            async_busy_lo_ms=0.5,
            async_busy_hi_ms=3.0,
        ),
        busy_service(
            'bravo',
            service_grams['bravo'],
            async_busy_lo_ms=2.0,
            async_busy_hi_ms=12.0,
        ),
        busy_service(
            'charlie',
            service_grams['charlie'],
            async_busy_lo_ms=5.0,
            async_busy_hi_ms=25.0,
            hard_sleep_lo_ms=1.0,
            hard_sleep_hi_ms=8.0,
            hard_sleep_every=40,
        ),
        busy_service(
            'delta',
            service_grams['delta'],
            async_busy_lo_ms=0.2,
            async_busy_hi_ms=1.5,
            hard_sleep_lo_ms=5.0,
            hard_sleep_hi_ms=40.0,
            hard_sleep_every=200,
        ),
    )


if __name__ == '__main__':

    d.enable_logging('ENABLE_LOGGING', True)
    d.enable_tracing('ENABLE_TRACING', True)

    try:

        asyncio.run(main())
    except KeyboardInterrupt:

        pass

