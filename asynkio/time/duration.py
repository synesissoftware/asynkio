# Definition of `Duration`.

from typing import Self

from diagnosticism import nanoseconds_to_string


class Duration:
    """
    Represents a span of time.
    """

    __slots__ = (
        # invariant fields:
        '_duration',
        # variant fields:
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
    def from_nanos(t_ns: int) -> Self:
        """
        Creates a new instance from the specified number of nanoseconds.
        """

        return Duration(0, t_ns)

    @staticmethod
    def from_micros(t_us: int) -> Self:
        """
        Creates a new instance from the specified number of microseconds.
        """

        return Duration(0, t_us * 1_000)

    @staticmethod
    def from_millis(t_ms: int) -> Self:
        """
        Creates a new instance from the specified number of milliseconds.
        """

        return Duration(0, t_ms * 1_000_000)

    @staticmethod
    def from_secs(t_s: int) -> Self:
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
    def duration_to_string(
        duration: Self | int,
        format_spec: str = '',
    ) -> str:
        """
        Formats a duration as a compact human-readable string.

        Delegates to
        `diagnosticism.nanoseconds_to_string()`.
        """

        return nanoseconds_to_string(
            int(duration),
            format_spec,
        )

    def __eq__(self, rhs: Self | float | int) -> bool:

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

    def __add__(self, rhs: Self) -> Self:

        if isinstance(rhs, Duration):

            return Duration.from_nanos(self._duration + rhs._duration)

        return NotImplemented

    def __sub__(self, rhs: Self) -> Self:

        if isinstance(rhs, Duration):

            return Duration.from_nanos(self._duration - rhs._duration)

        return NotImplemented

    def __mul__(self, rhs: float | int) -> Self:

        if isinstance(rhs, float):

            return Duration.from_nanos(int(self._duration * rhs))

        if isinstance(rhs, int):

            return Duration.from_nanos(self._duration * rhs)

        return NotImplemented

    def __truediv__(self, rhs: Self | float | int) -> Self:

        if isinstance(rhs, (Duration, int)):

            return Duration.from_nanos(self._duration / int(rhs))

        if isinstance(rhs, float):

            return Duration.from_nanos(int(self._duration / rhs))

        return NotImplemented

