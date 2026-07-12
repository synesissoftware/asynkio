# asynkio Examples

| Name | Source & Description | Summary |
| --- | --- | --- |
| interval | [examples/interval.py](./examples/interval.py) | General `Interval` demonstration |
| interval-burst | [examples/interval_burst.py](./examples/interval_burst.py) | `BURST` missed-tick behaviour |
| interval-delay | [examples/interval_delay.py](./examples/interval_delay.py) | `DELAY` missed-tick behaviour |
| interval-skip | [examples/interval_skip.py](./examples/interval_skip.py) | `SKIP` missed-tick behaviour |

Run a script with, for example:

```
$ uv sync
$ uv run python examples/interval_skip.py
```

Examples require the development dependencies (`diagnosticism`, and so
on). Install them with `uv sync` or `pip install asynkio[dev]`.


<!-- ########################### end of file ########################### -->

