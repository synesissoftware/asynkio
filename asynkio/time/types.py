
import time
from typing import Self

class Duration:
    """
    Represents a span of time.
    """

    def __init__(
        self,
        from_ns,
        to_ns,
    ):
        """
        Creates a new instance from the number of nanoseconds represented by
        `to_ns - from_ns`.
        """

        assert from_ns <= to_ns

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

        return self._duration / 1_000_000_000

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

    def __format__(self, format_spec) -> str:

        v = self._duration

        if v == 0:

            return "0s"

        if v >= 1_000_000:

            if v >= 1_000_000_000:

                q, r = divmod(v, 1_000_000_000)

                if r > 1_000_000:

                    return f"{self._duration / 1_000_000_000.0:.4}s"
                else:

                    return f"{self._duration // 1_000_000_000}s"
            else:

                q, r = divmod(v, 1_000_000)

                if r > 1_000:

                    return f"{self._duration / 1_000_000.0:.4}ms"
                else:

                    return f"{self._duration // 1_000_000}ms"

        if v >= 1_000:

            q, r = divmod(v, 1_000)

            if r > 1:

                return f"{self._duration / 1_000.0:.4}µs"
            else:

                return f"{self._duration // 1_000}µs"

        return f"{self._duration}ns"

    def __str__(self):

        return self.__format__('')


class Instant:
    """
    Represents a moment in time.
    """

    def __init__(self, t_ns):
        """
        Initialises with the given time instant (specified in nanoseconds).
        """

        self._t = t_ns

    @staticmethod
    def now() -> Self:
        """
        Initialises with the current time instant.
        """

        t_now_ns = time.time_ns()

        return Instant(t_now_ns)

    def __lt__(self, other):
        """
        Determines whether the called instance is less-than the `other`
        instance of `Instant`.
        """

        if isinstance(other, Instant):

            return self._t < other._t

        raise NotImplemented

    def __le__(self, other):
        """
        Determines whether the called instance is less-than-or-equal-to the
        `other` instance of `Instant`.
        """

        if isinstance(other, Instant):

            return self._t <= other._t

        raise NotImplemented

    def __sub__(self, other):
        """
        Subtracts the `other` - which may be an instance of `Instant` or an
        instance of `Duration` - from the called instance.
        """

        if isinstance(other, Instant):

            return Duration(other._t, self._t)

        if isinstance(other, Duration):

            return Instant(self._t - other.as_nanos())

        return NotImplemented

    def __add__(self, other):
        """
        Adds the `other` instance of `Duration` to the called instance.
        """

        if isinstance(other, Duration):

            return Instant(self._t + other.as_nanos())

        return NotImplemented

