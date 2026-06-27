# asynkio Examples

| Name | Source & Description | Summary |
| --- | --- | --- |
| interval | [tests/test_interval.py](./tests/test_interval.py) | General `Interval` demonstration |
| interval-burst | [tests/test_interval_burst.py](./tests/test_interval_burst.py) | `BURST` missed-tick behaviour |
| interval-delay | [tests/test_interval_delay.py](./tests/test_interval_delay.py) | `DELAY` missed-tick behaviour |
| interval-skip | [tests/test_interval_skip.py](./tests/test_interval_skip.py) | `SKIP` missed-tick behaviour |

Run a script with, for example:

```
$ uv sync
$ uv run python tests/test_interval_skip.py
```

Manual scripts require the development dependencies (`diagnosticism`, and
so on). An `examples/` directory may be added in a future release.


<!-- ########################### end of file ########################### -->
