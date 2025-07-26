
from .types import (
    Duration,
    Instant,
)

import asyncio
import enum


class MissedTickBehaviour(enum.IntEnum):
    """
    .
    """

    Burst = 1
    Delay = 2
    Skip = 3


MissedTickBehavior = MissedTickBehaviour


class Interval:
    """
    .
    """

    def __init__(
        self,
        duration,
        missed_tick_behaviour=MissedTickBehaviour.Skip,
    ):
        """
        .
        """

        assert missed_tick_behaviour == MissedTickBehaviour.Skip, "currently only support skip"

        self._duration = duration
        self._missed_tick_behaviour = missed_tick_behaviour
        self._reference_instant = Instant.now()

    def __await__(self):
        """
        .
        """

        now = Instant.now()

        duration : Duration = now - self._reference_instant

        rem = self._duration.as_nanos() - (duration.as_nanos() % self._duration.as_nanos())

        rem -= 200_000

        return asyncio.sleep(rem / 1_000_000_000).__await__()


def interval(
    duration,
):

    pass

