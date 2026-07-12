#! /usr/bin/env python3

# ######################################################################## #
# File:     tests/test_time_instant.py
#
# Purpose:  Unit-test for `asynkio.time.Instant`.
#
# Created:  25th July 2025
# Updated:  12th July 2026
#
# Copyright (c) Matthew Wilson, Synesis Information Systems Pty Ltd
# All rights reserved
#
# ######################################################################## #


from asynkio.time import (
    Duration,
    Instant,
)


def test_Instant_CREATE():

    instant_1 = Instant.now()
    instant_2 = Instant.now()

    assert not (instant_1 > instant_2)
    assert instant_1 <= instant_2

    assert not (instant_2 < instant_1)
    assert instant_2 >= instant_1

    duration_1_2 = instant_2 - instant_1

    max_duration_delta = 5

    assert duration_1_2.as_micros() < max_duration_delta, f"{duration_1_2.as_micros()} should be < {max_duration_delta}"

    instant_3 = instant_1 + Duration.from_micros(123)

    duration_1_3 = instant_3 - instant_1

    assert 123_000 == duration_1_3.as_nanos()


def test_Instant_REPR():

    assert "<asynkio.time.instant.Instant: _t=0>" == repr(Instant(0))
    assert "<asynkio.time.instant.Instant: _t=123>" == repr(Instant(123))
    assert "<asynkio.time.instant.Instant: _t=123456>" == repr(Instant(123_456))
    assert "<asynkio.time.instant.Instant: _t=123456789>" == repr(Instant(123_456_789))
    assert "<asynkio.time.instant.Instant: _t=980123456789>" == repr(Instant(980_123_456_789))


def test_Instant_STR():

    instant_0 = Instant(0)

    assert "1970-01-01T00:00:00.000000Z" == str(instant_0)

    instant_x = Instant(1_754_271_065_290_980_000)

    assert "2025-08-04T01:31:05.290980Z" == str(instant_x)


def test_Instant_FMT():

    instant_0 = Instant(0)

    assert "1970-01-01T00:00:00.000000Z" == format(instant_0, '')

    assert "0" == format(instant_0, 'd')

    instant_x = Instant(1_754_271_065_290_980_000)

    assert "2025-08-04T01:31:05.290980Z" == format(instant_x, '')

    assert "1754271065290980000" == format(instant_x, 'd')
    assert "141303303650632435240" == format(instant_x, 'o')
    assert "18586c3d466a3aa0" == format(instant_x, 'x')
    assert "18586C3D466A3AA0" == format(instant_x, 'X')

    assert "+1754271065290980000" == format(instant_x, '+d')
    assert "+141303303650632435240" == format(instant_x, '+o')
    assert "+18586c3d466a3aa0" == format(instant_x, '+x')
    assert "+18586C3D466A3AA0" == format(instant_x, '+X')

    assert "1754271065290980000" == format(instant_x, '#d')
    assert "0o141303303650632435240" == format(instant_x, '#o')
    assert "0x18586c3d466a3aa0" == format(instant_x, '#x')
    assert "0X18586C3D466A3AA0" == format(instant_x, '#X')


def test_Instant_INT():

    assert 0 == Instant(0).__int__()
    assert 123 == Instant(123).__int__()

