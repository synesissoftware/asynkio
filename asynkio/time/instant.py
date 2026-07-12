# Definition of `Instant`.

from datetime import (
    UTC,
    datetime,
)
import time
from typing import Self

from .duration import Duration


class Instant:
    """
    Represents a moment in time.
    """

    __slots__ = (
        # invariant fields:
        '_t',
        # variant fields:
    )

    def __init__(self, t_ns):
        """
        Initialises with the given time instant (specified in nanoseconds).
        """

        self._t = t_ns

    @staticmethod
    def _t_ns_to_d_utc(t_ns: int) -> datetime:
        """
        Convert the number of nanoseconds since epoch into a datetime
        instance assuming UTC.
        """

        return datetime.fromtimestamp(t_ns / 1_000_000_000.0, tz=UTC)

    @staticmethod
    def now() -> Self:
        """
        Initialises with the current time instant.
        """

        t_now_ns = time.time_ns()

        return Instant(t_now_ns)

    @staticmethod
    def instant_to_string(
        instant: Self | int,
        format_spec: str = '',
    ) -> str:

        typed = None

        def set_type_or_raise(
            typed,
            t,
            c,
            b,
        ):

            # local as_type

            if typed is not None:

                raise ValueError(f"cannot specify type `{t}` as type already specified as `{typed[0]}`")

            else:

                return (t, c, b)

        show_plus = False
        show_base = False

        for c in format_spec:

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

            if typed[0] is int:

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

        return NotImplemented

    def __le__(self, rhs) -> bool:
        """
        Determines whether the called instance is less-than-or-equal-to the
        `rhs` instance of `Instant`.
        """

        if isinstance(rhs, Instant):

            return self._t <= rhs._t

        return NotImplemented

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

