#! /usr/bin/env python3

import asyncio
from unittest.mock import patch

from asynkio.time import (
    Duration,
    Instant,
    Interval,
    MissedTickBehaviour,
)

REF = 10_000_000_000
PERIOD_NS = 1_000_000_000


async def _await_interval(interval):

    await interval


def _run_await(interval):

    asyncio.run(_await_interval(interval))


def _build_interval(now_values, build_interval):
    """
    Builds an interval under mocked time without awaiting it.
    """

    now_iter = iter(now_values)

    def next_now():

        return next(now_iter)

    with patch('asynkio.time.interval.Instant.now', side_effect=next_now):
        return build_interval()


def _run_interval(now_values, build_interval, await_count=1):
    """
    Builds an interval under mocked time, awaits it `await_count` times,
    and returns `(interval, sleep_durations)`.
    """

    sleeps = []
    now_iter = iter(now_values)

    async def fake_sleep(seconds):

        sleeps.append(seconds)

    def next_now():

        return next(now_iter)

    with patch('asynkio.time.interval.Instant.now', side_effect=next_now):
        with patch(
            'asynkio.time.interval.asyncio.sleep',
            side_effect=fake_sleep,
        ):
            interval = build_interval()

            for _ in range(await_count):
                _run_await(interval)

            return interval, sleeps


def test_Interval_init_period_from_duration():

    interval = _build_interval(
        [Instant(REF)],
        lambda: Interval(Duration.from_secs(1), negative_bias=0),
    )

    assert PERIOD_NS == interval.period().as_nanos()


def test_Interval_init_period_from_int():

    interval = _build_interval(
        [Instant(REF)],
        lambda: Interval(PERIOD_NS, negative_bias=0),
    )

    assert PERIOD_NS == interval.period().as_nanos()


def test_Interval_negative_bias_default_large_period():

    interval = _build_interval(
        [Instant(REF)],
        lambda: Interval(PERIOD_NS),
    )

    assert 400_000 == interval.negative_bias().as_nanos()


def test_Interval_negative_bias_default_small_period():

    interval = _build_interval(
        [Instant(REF)],
        lambda: Interval(50_000_000),
    )

    assert 0 == interval.negative_bias().as_nanos()


def test_Interval_accessors():

    interval = _build_interval(
        [Instant(REF)],
        lambda: Interval(
            PERIOD_NS,
            missed_tick_behaviour=MissedTickBehaviour.DELAY,
            name='tick',
            negative_bias=0,
        ),
    )

    assert 'tick' == interval.name()
    assert MissedTickBehaviour.DELAY == interval.missed_tick_behaviour()
    assert MissedTickBehaviour.DELAY == interval.missed_tick_behavior()
    assert interval.reference_instant() is not None
    assert interval.recent_instant() is None
    assert 0 == interval.event_count()


def test_Interval_DELAY_await_sleep():

    _, sleeps = _run_interval(
        [Instant(REF), Instant(REF + 123)],
        lambda: Interval(
            PERIOD_NS,
            missed_tick_behaviour=MissedTickBehaviour.DELAY,
            negative_bias=100_000_000,
        ),
    )

    assert [0.9] == sleeps


def test_Interval_SKIP_first_await():

    interval, sleeps = _run_interval(
        [Instant(REF), Instant(REF)],
        lambda: Interval(
            PERIOD_NS,
            missed_tick_behaviour=MissedTickBehaviour.SKIP,
            negative_bias=0,
        ),
    )

    assert [1.0] == sleeps
    assert 1 == interval.event_count()
    assert REF == int(interval.recent_instant())


def test_Interval_SKIP_second_await_at_period_boundary():

    _, sleeps = _run_interval(
        [
            Instant(REF),
            Instant(REF),
            Instant(REF + PERIOD_NS),
        ],
        lambda: Interval(
            PERIOD_NS,
            missed_tick_behaviour=MissedTickBehaviour.SKIP,
            negative_bias=0,
        ),
        await_count=2,
    )

    assert [1.0, 1.0] == sleeps


def test_Interval_SKIP_await_with_remainder():
    """
    First await always sleeps a full period; subsequent awaits target the
    next period boundary from the reference (period - remainder).
    """

    _, sleeps = _run_interval(
        [
            Instant(REF),
            Instant(REF),
            Instant(REF + 500_000_000),
        ],
        lambda: Interval(
            PERIOD_NS,
            missed_tick_behaviour=MissedTickBehaviour.SKIP,
            negative_bias=0,
        ),
        await_count=2,
    )

    assert [1.0, 0.5] == sleeps


def test_Interval_SKIP_applies_negative_bias():
    """
    First await sleeps a full period (no bias); later awaits subtract
    `negative_bias` from the sleep when far enough from the boundary.
    """

    _, sleeps = _run_interval(
        [
            Instant(REF),
            Instant(REF),
            Instant(REF),
        ],
        lambda: Interval(
            PERIOD_NS,
            missed_tick_behaviour=MissedTickBehaviour.SKIP,
            negative_bias=100_000_000,
        ),
        await_count=2,
    )

    assert [1.0, 0.9] == sleeps


def test_Interval_BURST_catch_up_then_wait():

    late = REF + 2_500_000_000

    interval, sleeps = _run_interval(
        [
            Instant(REF),
            Instant(late),
            Instant(late),
            Instant(late),
        ],
        lambda: Interval(
            PERIOD_NS,
            missed_tick_behaviour=MissedTickBehaviour.BURST,
            negative_bias=0,
        ),
        await_count=3,
    )

    assert [0, 0, 0.5] == sleeps
    assert 3 == interval.event_count()


def test_Interval_event_count_increments():

    interval, _ = _run_interval(
        [
            Instant(REF),
            Instant(REF),
            Instant(REF + PERIOD_NS),
            Instant(REF + 2 * PERIOD_NS),
        ],
        lambda: Interval(
            PERIOD_NS,
            missed_tick_behaviour=MissedTickBehaviour.SKIP,
            negative_bias=0,
        ),
        await_count=3,
    )

    assert 3 == interval.event_count()


def test_MissedTickBehaviour_try_parse():

    assert MissedTickBehaviour.BURST == MissedTickBehaviour.try_parse('burst')
    assert MissedTickBehaviour.SKIP == MissedTickBehaviour.try_parse('SKIP')
    assert MissedTickBehaviour.DELAY == MissedTickBehaviour.try_parse('Delay')
    assert None is MissedTickBehaviour.try_parse('unknown')

