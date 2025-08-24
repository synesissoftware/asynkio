
from .types import (
    Duration,
    Instant,
)

import asyncio
import enum


class MissedTickBehaviour(enum.IntEnum):
    """
    Defines the behaviour of an `Interval` when it misses a tick.

    See
    ---
        https://docs.rs/tokio/latest/tokio/time/enum.MissedTickBehavior.html
    """

    """
    Ticks as fast as possible until caught up.
    """
    BURST = 1
    """
    Tick at multiples of period from when tick was called, rather than from
    start.
    """
    DELAY = 2
    """
    Skips missed ticks and tick on the next multiple of period from start.
    """
    SKIP = 3


    def _to_str(self):

        if MissedTickBehaviour.BURST == self:

            return "BURST"

        if MissedTickBehaviour.DELAY == self:

            return "DELAY"

        if MissedTickBehaviour.SKIP == self:

            return "SKIP"

        return NotImplemented

    @staticmethod
    def try_parse(s : str):
        """
        Attempts, in a case-insensitive manner, to interpret a string into
        a named member of the class, i.e. a recognised enumerator; returns
        `None` if not recogised.
        """

        try:

            return MissedTickBehaviour[str(s).upper()]
        except KeyError:

            return None

    def __repr__(self):

        return f"<{self.__module__}.{self.__class__.__name__}.{self._to_str()}>"

    def __str__(self):

        return enum.Enum.__str__(self)


MissedTickBehavior = MissedTickBehaviour


class Interval:
    """
    Supports wait operations with a certain periodicity and behaviour for
    late ticking.
    """

    __slots__ = (
        # invariant fields
        '_period_ns',
        '_missed_tick_behaviour',
        '_name',
        '_negative_bias',
        '_reference_instant',
        # variant fields
        '_recent_instant',
        '_event_count',
    )

    def __init__(
        self,
        period : Duration | int,
        missed_tick_behaviour : MissedTickBehaviour=MissedTickBehaviour.SKIP,
        name=None,
        negative_bias=None,
    ):
        """
        Creates an instance, based on the given parameters.
        """

        assert isinstance(period, (Duration, int)), "`period` must be instance of `Duration` or `int` (which specifies nanoseconds)"

        assert negative_bias is None or negative_bias < int(period), "invalid `negative_bias` ({negative_bias}) given the `period` ({period)}"

        self._period_ns = int(period)
        self._missed_tick_behaviour = missed_tick_behaviour
        self._name = str(name) if name else ''
        self._negative_bias = negative_bias if isinstance(negative_bias, int) else 400_000 if self._period_ns > 100_000_000 else 0
        self._reference_instant = Instant.now()

        self._recent_instant = None
        self._event_count = 0

    def __repr__(self):

        return "" \
            f"<{self.__module__}.{self.__class__.__name__}: " \
            f"_period_ns: {self._period_ns:,}; " \
            f"_missed_tick_behaviour: {self._missed_tick_behaviour:}; " \
            f"_name: {self._name}; " \
            f"_negative_bias: {self._negative_bias}; " \
            f"_reference_instant: {self._reference_instant:}; " \
            f"_recent_instant: {self._recent_instant:}; " \
            f"_event_count: {self._event_count:,}; " \
            ">"

    def __await__(self):
        """
        .
        """

        self._event_count += 1

        now = Instant.now()


        if self._missed_tick_behaviour == MissedTickBehaviour.DELAY:

            # simply wait for given duration

            self._recent_instant = now

            return asyncio.sleep((self._period_ns - self._negative_bias) / 1_000_000_000).__await__()


        duration : Duration = now - self._reference_instant
        duration_ns = duration.as_nanos()

        # calculate number of intervals (`q`) and remainder (`r`)

        q, r = divmod(duration_ns, self._period_ns)


        if self._missed_tick_behaviour == MissedTickBehavior.BURST:

            # either ...

            if self._event_count <= q:

                # ... respond immediately if more than a full interval, or ...

                self._recent_instant = now

                return asyncio.sleep(0).__await__()

            if self._event_count + 1 == q:

                # ... wait for the last bit of the interval.

                self._recent_instant = now

                return asyncio.sleep(r / 1_000_000_000).__await__()


        # `SKIP` behaviour:
        #
        # T.B.C.

        # get the time _now_ and then calculate how much time has
        # elapsed, ...

        # ... and from this calculate how long the next wait should be

        p_ns = self._period_ns - r
        if p_ns > self._negative_bias:

            p_ns -= self._negative_bias

        self._recent_instant = now

        return asyncio.sleep(p_ns / 1_000_000_000).__await__()

    def event_count(self) -> int:
        """
        The number of times that the interval has been awaited.
        """

        return self._event_count

    def missed_tick_behaviour(self) -> str:
        """
        The interval's missed-tick behaviour.
        """

        return self._missed_tick_behaviour

    def missed_tick_behavior(self) -> str:
        """
        The interval's missed-tick behaviour.
        """

        return self.missed_tick_behaviour()

    def name(self) -> str:
        """
        The interval's name.
        """

        return self._name

    def negative_bias(self) -> Duration:
        """
        The interval's negative bias.
        """

        return Duration(self._negative_bias)

    def period(self) -> Duration:
        """
        The interval's period.
        """

        return Duration.from_nanos(self._period_ns)

    def recent_instant(self) -> Instant:
        """
        The instance's most recent await instant.
        """

        return self._recent_instant

    def reference_instant(self) -> Instant:
        """
        The instance's reference instant.
        """

        return self._reference_instant
