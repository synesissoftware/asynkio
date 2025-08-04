
from datetime import (
    datetime,
    timezone,
)
import time
from typing import Self


class Duration:
    """
    Represents a span of time.
    """

    __slots__ = (
        "_duration",
    )

    def __init__(
        self,
        from_ns,
        to_ns,
    ):
        """
        Creates a new instance from the number of nanoseconds represented by
        `to_ns - from_ns`.
        """

        self._duration = to_ns - from_ns

    @staticmethod
    def from_nanos(t_ns : int) -> Self:
        """
        Creates a new instance from the specified number of nanoseconds.
        """

        return Duration(0, t_ns)

    @staticmethod
    def from_micros(t_us : int) -> Self:
        """
        Creates a new instance from the specified number of microseconds.
        """

        return Duration(0, t_us * 1_000)

    @staticmethod
    def from_millis(t_ms : int) -> Self:
        """
        Creates a new instance from the specified number of milliseconds.
        """

        return Duration(0, t_ms * 1_000_000)

    @staticmethod
    def from_secs(t_s : int) -> Self:
        """
        Creates a new instance from the specified number of seconds.
        """

        return Duration(0, t_s * 1_000_000_000)

    def as_nanos(self) -> int:
        """
        Total number of whole nanoseconds contained by this instance.
        """

        return self._duration

    def as_micros(self) -> int:
        """
        Total number of whole microseconds contained by this instance.
        """

        return self._duration // 1_000

    def as_millis(self) -> int:
        """
        Total number of whole milliseconds contained by this instance.
        """

        return self._duration // 1_000_000

    def as_secs(self) -> int:
        """
        Total number of whole seconds contained by this instance.
        """

        return self._duration // 1_000_000_000

    def as_secs_f(self) -> float:
        """
        The fractional number of seconds contained by this instance.
        """

        return self._duration / 1_000_000_000.0

    def subsec_nanos(self) -> int:
        """
        The fractional part of this instance, in nanoseconds.
        """

        return self._duration % 1_000_000_000

    def subsec_micros(self) -> int:
        """
        The fractional part of this instance, in microseconds.
        """

        return (self._duration % 1_000_000_000) // 1_000

    def subsec_millis(self) -> int:
        """
        The fractional part of this instance, in milliseconds.
        """

        return (self._duration % 1_000_000_000) // 1_000_000

    @staticmethod
    def _scale_index(n : int) -> tuple[int, int]:

        _SCALES = [
            1,
            10,
            100,
            1_000,
            10_000,
            100_000,
            1_000_000,
            10_000_000,
            100_000_000,
            1_000_000_000,
            10_000_000_000,
            100_000_000_000,
        ]

        assert n > 0
        assert len(_SCALES) == 12

        if n >= 100_000_000_000:

            return (11, _SCALES[11])

        l = 0
        h = 11

        count = 0

        while l <= h:

            count += 1

            assert count < 5, f"too many loops while trying to scale {n}"

            m = (h + l) // 2

            b = _SCALES[m]

            if n == b:

                return (m, b)

            if n < b:

                h = m

                continue
            else:
                assert n > b

                if n < b * 10:

                    return (m, b)
                else:

                    l = m

        return (11, _SCALES[11])

    @staticmethod
    def duration_to_string(
        duration : Self | int,
        format_spec : str = '',
    ) -> str:

        v = int(duration)

        if v < 0:

            v = -v
            sign = '-'
        else:

            if '+' in format_spec:

                sign = '+'
            else:

                sign = ''

        if v == 0:

            return "0s"

        oom, divisor = Duration._scale_index(v)

        suffixes = [
            'ns',
            'µs',
            'ms',
            's',
        ]
        suffix = suffixes[oom // 3]

        def fmt(sign, whole, frac, suffix):

            if frac == 0:

                return f"{sign}{whole}{suffix}"
            else:

                if whole > 999:

                    return f"{sign}{whole}{suffix}"

                if whole > 99:

                    return f"{sign}{whole}.{frac}{suffix}"

                if whole > 9:

                    return f"{sign}{whole}.{frac:02d}{suffix}"

                return f"{sign}{whole}.{frac}{suffix}"

        if oom < 3:

            return f"{sign}{v}{suffix}"
        else:

            divisor_0 = divisor // 1_000

            i = oom % 3

            if i == 0:

                divisor_1 = 1_000
            elif i == 1:

                divisor_1 = 100
            else:

                divisor_1 = 10


            v //= divisor_0

            whole = v // divisor_1
            frac = v - (whole * divisor_1)


            return fmt(sign, whole, frac, suffix)

    def __eq__(self, rhs : Self | float | int) -> bool:

        if isinstance(rhs, Duration):

            return self._duration == rhs._duration

        if isinstance(rhs, (float, int)):

            return self._duration == int(rhs)

        return NotImplemented

    def __format__(self, format_spec) -> str:

        return self.duration_to_string(
            self._duration,
            format_spec=format_spec,
        )

    def __str__(self) -> str:

        return self.duration_to_string(
            self._duration,
            format_spec='',
        )

    def __repr__(self) -> str:

        return f"<{self.__module__}.{self.__class__.__name__}: _duration={self._duration}>"

    def __int__(self) -> int:
        """
        Converts an instance into an integer, representing the number of
        nanoseconds in the duration.
        """

        return self._duration

    def __add__(self, rhs : Self) -> Self:

        if isinstance(rhs, Duration):

            return Duration.from_nanos(self._duration + rhs._duration)

        return NotImplemented

    def __sub__(self, rhs : Self) -> Self:

        if isinstance(rhs, Duration):

            return Duration.from_nanos(self._duration - rhs._duration)

        return NotImplemented

    def __mul__(self, rhs : float | int) -> Self:

        if isinstance(rhs, float):

            return Duration.from_nanos(int(self._duration * rhs))

        if isinstance(rhs, int):

            return Duration.from_nanos(self._duration * rhs)

        return NotImplemented

    def __truediv__(self, rhs : Self | float | int) -> Self:

        if isinstance(rhs, (Duration, int)):

            return Duration.from_nanos(self._duration / int(rhs))

        if isinstance(rhs, float):

            return Duration.from_nanos(int(self._duration / rhs))

        return NotImplemented


class Instant:
    """
    Represents a moment in time.
    """

    __slots__ = (
        "_t",
    )

    def __init__(self, t_ns):
        """
        Initialises with the given time instant (specified in nanoseconds).
        """

        self._t = t_ns

    @staticmethod
    def _t_ns_to_d_utc(t_ns : int) -> datetime:
        """
        Convert the number of nanoseconds since epoch into a datetime
        instance assuming UTC.
        """

        return datetime.fromtimestamp(t_ns / 1_000_000_000.0, tz=timezone.utc)

    @staticmethod
    def now() -> Self:
        """
        Initialises with the current time instant.
        """

        t_now_ns = time.time_ns()

        return Instant(t_now_ns)

    @staticmethod
    def instant_to_string(
        instant : Self | int,
        format_spec : str = '',
    ) -> str:

        typed = None

        def set_type_or_raise(typed, t, c, b):

            # local as_type

            if typed is not None:

                raise ValueError(f"cannot specify type `{t}` as type already specified as `{typed[0]}`")

            else:

                return (t, c, b)

        show_plus = False
        show_base = False

        for c in format_spec:

            print(f"c={c}")

            if c == 'd':

                typed = set_type_or_raise(typed, int, c, '')

            if c == 'o':

                typed = set_type_or_raise(typed, int, c, '0o')

            if c == 'x':

                typed = set_type_or_raise(typed, int, c, '0x')

            if c == 'X':

                typed = set_type_or_raise(typed, int, c, '0X')

            if c == '+':

                show_plus = True

            if c == '#':

                show_base = True

        if typed:

            if typed[0] == int:

                fmt = ''

                if show_plus:

                    fmt += '+'

                if show_base:

                    fmt += '#'

                fmt += typed[1]

                return format(instant, fmt)
            else:

                return NotImplemented
        else:

            d = Instant._t_ns_to_d_utc(instant)

            return d.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def __format__(self, format_spec) -> str:

        return Instant.instant_to_string(
            self._t,
            format_spec=format_spec,
        )

    def __str__(self) -> str:

        return Instant.instant_to_string(
            self._t,
            format_spec='',
        )

    def __repr__(self) -> str:

        return f"<{self.__module__}.{self.__class__.__name__}: _t={self._t}>"

    def __int__(self) -> int:
        """
        Converts an instance into an integer, representing the number of
        nanoseconds since the epoch.
        """

        return self._t

    def __lt__(self, rhs) -> bool:
        """
        Determines whether the called instance is less-than the `rhs`
        instance of `Instant`.
        """

        if isinstance(rhs, Instant):

            return self._t < rhs._t

        raise NotImplemented

    def __le__(self, rhs) -> bool:
        """
        Determines whether the called instance is less-than-or-equal-to the
        `rhs` instance of `Instant`.
        """

        if isinstance(rhs, Instant):

            return self._t <= rhs._t

        raise NotImplemented

    def __sub__(self, rhs) -> Duration | Self:
        """
        Subtracts the `rhs` - which may be an instance of `Instant` or an
        instance of `Duration` - from the called instance.
        """

        if isinstance(rhs, Instant):

            return Duration(rhs._t, self._t)

        if isinstance(rhs, Duration):

            return Instant(self._t - rhs.as_nanos())

        return NotImplemented

    def __add__(self, rhs) -> Self:
        """
        Adds the `rhs` instance of `Duration` to the called instance.
        """

        if isinstance(rhs, Duration):

            return Instant(self._t + rhs.as_nanos())

        return NotImplemented

