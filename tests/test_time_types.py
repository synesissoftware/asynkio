#! /usr/bin/env python3

# ######################################################################## #
# File:     tests/test_time_types.py
#
# Purpose:  Unit-test for `asynkio.time.Duration` and
#           `asynkio.time.Interval`.
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


# ######################################
# Duration

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

    assert "123.4ms" == str(duration)


def test_Duration_REPR():

    assert "<asynkio.time.types.Duration: _duration=0>" == repr(Duration.from_nanos(0))


def test_Duration_STRINGS():

    assert "9ns" == str(Duration.from_nanos(9))
    assert "89ns" == str(Duration.from_nanos(89))
    assert "789ns" == str(Duration.from_nanos(789))

    assert "6.789µs" == str(Duration.from_nanos(6_789))
    assert "56.78µs" == str(Duration.from_nanos(56_789))
    assert "456.7µs" == str(Duration.from_nanos(456_789))

    assert "3.456ms" == str(Duration.from_nanos(3_456_789))
    assert "23.45ms" == str(Duration.from_nanos(23_456_789))
    assert "123.4ms" == str(Duration.from_nanos(123_456_789))

    assert "9.123s" == str(Duration.from_nanos(9_123_456_789))
    assert "89.12s" == str(Duration.from_nanos(89_123_456_789))
    assert "789.1s" == str(Duration.from_nanos(789_123_456_789))


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
    assert "500000s" == str(Duration.from_nanos(500_000_000_000_000))
    assert "6000000s" == str(Duration.from_nanos(6_000_000_000_000_000))
    assert "70000000s" == str(Duration.from_nanos(70_000_000_000_000_000))

    assert "11.11s" == str(Duration.from_nanos(11_111_111_111))
    assert "222.2s" == str(Duration.from_nanos(222_222_222_222))
    assert "3333s" == str(Duration.from_nanos(3_333_333_333_333))
    assert "44444s" == str(Duration.from_nanos(44_444_444_444_444))
    assert "555555s" == str(Duration.from_nanos(555_555_555_555_555))
    assert "6666666s" == str(Duration.from_nanos(6_666_666_666_666_666))
    assert "77777777s" == str(Duration.from_nanos(77_777_777_777_777_777))

    assert "-11.11s" == str(Duration.from_nanos(-11_111_111_111))
    assert "-222.2s" == str(Duration.from_nanos(-222_222_222_222))
    assert "-3333s" == str(Duration.from_nanos(-3_333_333_333_333))
    assert "-44444s" == str(Duration.from_nanos(-44_444_444_444_444))
    assert "-555555s" == str(Duration.from_nanos(-555_555_555_555_555))
    assert "-6666666s" == str(Duration.from_nanos(-6_666_666_666_666_666))
    assert "-77777777s" == str(Duration.from_nanos(-77_777_777_777_777_777))


def test_Duration_NEGATIVE_VALUES_STRINGS():

    assert "-9ns" == str(Duration.from_nanos(-9))
    assert "-89ns" == str(Duration.from_nanos(-89))
    assert "-789ns" == str(Duration.from_nanos(-789))

    assert "-6.789µs" == str(Duration.from_nanos(-6_789))
    assert "-56.78µs" == str(Duration.from_nanos(-56_789))
    assert "-456.7µs" == str(Duration.from_nanos(-456_789))

    assert "-3.456ms" == str(Duration.from_nanos(-3_456_789))
    assert "-23.45ms" == str(Duration.from_nanos(-23_456_789))
    assert "-123.4ms" == str(Duration.from_nanos(-123_456_789))

    assert "-9.123s" == str(Duration.from_nanos(-9_123_456_789))


    assert "-9ns" == str(Duration.from_nanos(-9))
    assert "-80ns" == str(Duration.from_nanos(-80))
    assert "-700ns" == str(Duration.from_nanos(-700))

    assert "-6µs" == str(Duration.from_nanos(-6_000))
    assert "-50µs" == str(Duration.from_nanos(-50_000))
    assert "-400µs" == str(Duration.from_nanos(-400_000))

    assert "-3ms" == str(Duration.from_nanos(-3_000_000))
    assert "-20ms" == str(Duration.from_nanos(-20_000_000))
    assert "-100ms" == str(Duration.from_nanos(-100_000_000))

    assert "-9s" == str(Duration.from_nanos(-9_000_000_000))
    assert "-10s" == str(Duration.from_nanos(-10_000_000_000))
    assert "-200s" == str(Duration.from_nanos(-200_000_000_000))
    assert "-3000s" == str(Duration.from_nanos(-3_000_000_000_000))
    assert "-40000s" == str(Duration.from_nanos(-40_000_000_000_000))


def test_Duration_OBSERVED_EDGE_CASES():

    assert "999.7ms" == str(Duration.from_nanos(999_772_000))
    assert "999.8ms" == str(Duration.from_nanos(999_800_000))
    assert "999.9ms" == str(Duration.from_nanos(999_974_000))

    assert "-999.7ms" == str(Duration.from_nanos(-999_772_000))
    assert "-999.8ms" == str(Duration.from_nanos(-999_800_000))
    assert "-999.9ms" == str(Duration.from_nanos(-999_974_000))


def test_Duration_WITH_PLUS_SIGN():

    assert "999.7ms" == f"{Duration.from_nanos(999_772_000)}"
    assert "999.8ms" == f"{Duration.from_nanos(999_800_000)}"
    assert "999.9ms" == f"{Duration.from_nanos(999_974_000)}"

    assert "-999.7ms" == f"{Duration.from_nanos(-999_772_000)}"
    assert "-999.8ms" == f"{Duration.from_nanos(-999_800_000)}"
    assert "-999.9ms" == f"{Duration.from_nanos(-999_974_000)}"

    assert "999.7ms" == f"{Duration.from_nanos(999_772_000):}"
    assert "999.8ms" == f"{Duration.from_nanos(999_800_000):}"
    assert "999.9ms" == f"{Duration.from_nanos(999_974_000):}"

    assert "+999.7ms" == f"{Duration.from_nanos(999_772_000):+}"
    assert "+999.8ms" == f"{Duration.from_nanos(999_800_000):+}"
    assert "+999.9ms" == f"{Duration.from_nanos(999_974_000):+}"


def test_Duration_ADD():

    d_100 = Duration.from_nanos(100)

    assert Duration.from_nanos(100) == (d_100 + Duration.from_nanos(0))
    assert Duration.from_nanos(50) == (d_100 + Duration.from_nanos(-50))
    assert Duration.from_nanos(150) == (d_100 + Duration.from_nanos(50))


def test_Duration_SUB():

    d_100 = Duration.from_nanos(100)

    assert Duration.from_nanos(100) == (d_100 - Duration.from_nanos(0))
    assert Duration.from_nanos(50) == (d_100 - Duration.from_nanos(50))
    assert Duration.from_nanos(150) == (d_100 - Duration.from_nanos(-50))


def test_Duration_DIV():

    d_100 = Duration.from_nanos(100)

    assert Duration.from_nanos(100) == (d_100 / 1)
    assert Duration.from_nanos(50) == (d_100 / 2)
    assert Duration.from_nanos(50) == (d_100 / 2.0)
    assert 1 == d_100 / Duration.from_nanos(100)


def test_Duration_MUL():

    d_100 = Duration.from_nanos(100)

    assert Duration.from_nanos(100) == (d_100 * 1)
    assert Duration.from_nanos(50) == (d_100 * 0.5)
    assert Duration.from_nanos(200) == (d_100 * 2.0)


# ######################################
# Instant

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


def test_Intant_REPR():

    assert "<asynkio.time.types.Instant: _t=0>" == repr(Instant(0))
    assert "<asynkio.time.types.Instant: _t=123>" == repr(Instant(123))
    assert "<asynkio.time.types.Instant: _t=123456>" == repr(Instant(123_456))
    assert "<asynkio.time.types.Instant: _t=123456789>" == repr(Instant(123_456_789))
    assert "<asynkio.time.types.Instant: _t=980123456789>" == repr(Instant(980_123_456_789))


def test_Intant_STR():

    instant_0 = Instant(0)

    assert "1970-01-01T00:00:00.000000Z" == str(instant_0)

    instant_x = Instant(1_754_271_065_290_980_000)

    assert "2025-08-04T01:31:05.290980Z" == str(instant_x)


def test_Intant_FMT():

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


def test_Intant_INT():

    assert 0 == Instant(0).__int__()
    assert 123 == Instant(123).__int__()

