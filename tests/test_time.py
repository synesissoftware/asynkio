#! /usr/bin/env python3

# ######################################################################## #
# File:     tests/test_time.py
#
# Purpose:  Unit-test for `asynkio.time.Duration`.
#
# Created:  25th July 2025
# Updated:  24th August 2025
#
# Copyright (c) Matthew Wilson, Synesis Information Systems Pty Ltd
# All rights reserved
#
# ######################################################################## #


import math
from asynkio.time import (
    Duration,
    Instant,
)


def test_Duration_DURATION_0():

    duration = Duration(0, 0)

    assert 0 == duration.as_nanos()
    assert 0 == duration.as_micros()
    assert 0 == duration.as_millis()
    assert 0 == duration.as_secs()
    assert 0.0 == duration.as_secs_f()

    assert 0 == duration.subsec_nanos()
    assert 0 == duration.subsec_micros()
    assert 0 == duration.subsec_millis()

    assert "0s" == str(duration)


def test_Duration_DURATION_1_SECOND():

    duration = Duration.from_secs(1)

    assert 1_000_000_000 == duration.as_nanos()
    assert 1_000_000 == duration.as_micros()
    assert 1_000 == duration.as_millis()
    assert 1 == duration.as_secs()
    assert math.isclose(1.0, duration.as_secs_f())

    assert 0 == duration.subsec_nanos()
    assert 0 == duration.subsec_micros()
    assert 0 == duration.subsec_millis()

    assert "1s" == str(duration)


def test_Duration_DURATION_123_MILLISECONDS():

    duration = Duration.from_millis(123)

    assert 123_000_000 == duration.as_nanos()
    assert 123_000 == duration.as_micros()
    assert 123 == duration.as_millis()
    assert 0 == duration.as_secs()
    assert math.isclose(0.123, duration.as_secs_f())

    assert 123_000_000 == duration.subsec_nanos()
    assert 123_000 == duration.subsec_micros()
    assert 123 == duration.subsec_millis()

    assert "123ms" == str(duration)


def test_Duration_DURATION_123_456_789_NANOSECONDS():

    duration = Duration.from_nanos(123_456_789)

    assert 123_456_789 == duration.as_nanos()
    assert 123_456 == duration.as_micros()
    assert 123 == duration.as_millis()
    assert 0 == duration.as_secs()
    assert math.isclose(0.123_456_789, duration.as_secs_f())

    assert 123_456_789 == duration.subsec_nanos()
    assert 123_456 == duration.subsec_micros()
    assert 123 == duration.subsec_millis()

    assert "123.5ms" == str(duration)


def test_Duration_STRINGS():

    assert "9ns" == str(Duration.from_nanos(9))
    assert "89ns" == str(Duration.from_nanos(89))
    assert "789ns" == str(Duration.from_nanos(789))

    assert "6.789µs" == str(Duration.from_nanos(6_789))
    assert "56.79µs" == str(Duration.from_nanos(56_789))
    assert "456.8µs" == str(Duration.from_nanos(456_789))

    assert "3.457ms" == str(Duration.from_nanos(3_456_789))
    assert "23.46ms" == str(Duration.from_nanos(23_456_789))
    assert "123.5ms" == str(Duration.from_nanos(123_456_789))

    assert "9.123s" == str(Duration.from_nanos(9_123_456_789))


    assert "9ns" == str(Duration.from_nanos(9))
    assert "80ns" == str(Duration.from_nanos(80))
    assert "700ns" == str(Duration.from_nanos(700))

    assert "6µs" == str(Duration.from_nanos(6_000))
    assert "50µs" == str(Duration.from_nanos(50_000))
    assert "400µs" == str(Duration.from_nanos(400_000))

    assert "3ms" == str(Duration.from_nanos(3_000_000))
    assert "20ms" == str(Duration.from_nanos(20_000_000))
    assert "100ms" == str(Duration.from_nanos(100_000_000))

    assert "9s" == str(Duration.from_nanos(9_000_000_000))
    assert "10s" == str(Duration.from_nanos(10_000_000_000))
    assert "200s" == str(Duration.from_nanos(200_000_000_000))
    assert "3000s" == str(Duration.from_nanos(3_000_000_000_000))
    assert "40000s" == str(Duration.from_nanos(40_000_000_000_000))


def test_Instant_CREATE():

    instant_1 = Instant.now()
    instant_2 = Instant.now()

    assert instant_1 < instant_2
    assert instant_1 <= instant_2

    assert instant_2 > instant_1
    assert instant_2 >= instant_1

    duration_1_2 = instant_2 - instant_1

    max_duration_delta = 10

    assert duration_1_2.as_micros() < max_duration_delta, f"{duration_1_2.as_micros()} should be < {max_duration_delta}"


    instant_3 = instant_1 + Duration.from_micros(123)

    duration_1_3 = instant_3 - instant_1

    assert 123_000 == duration_1_3.as_nanos()
