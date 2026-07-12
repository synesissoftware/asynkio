# asynkio - README <!-- omit in toc -->

Tokio-like functionality for Python

![Language](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![PyPI](https://img.shields.io/pypi/v/asynkio.svg)](https://pypi.org/project/asynkio/)
[![GitHub release](https://img.shields.io/github/v/release/synesissoftware/asynkio.svg)](https://github.com/synesissoftware/asynkio/releases/latest)
![Python](https://img.shields.io/badge/Python-3.11+-lightgrey)
[![CI](https://github.com/synesissoftware/asynkio/actions/workflows/python-package.yml/badge.svg)](https://github.com/synesissoftware/asynkio/actions/workflows/python-package.yml)
[![PyPI project](https://img.shields.io/badge/documentation-PyPI-lightgrey)](https://pypi.org/project/asynkio/)


## Table of contents <!-- omit in toc -->

- [Introduction](#introduction)
- [Installation \& Usage](#installation--usage)
- [Components](#components)
- [Examples](#examples)
- [Project Information](#project-information)
  - [Where to get help](#where-to-get-help)
  - [Contribution guidelines](#contribution-guidelines)
  - [Dependencies](#dependencies)
    - [Efferent (fan-out)](#efferent-fan-out)
      - [Development Dependencies](#development-dependencies)
    - [Afferent (fan-in)](#afferent-fan-in)
  - [Related projects](#related-projects)
  - [License](#license)


## Introduction

**asynkio** - a portmanteau of **asyncio** and **Tokio**, pronounced "ay sink ee-oh" - is a small, simple **Python** library that provides some of the features of the **Rust** **Tokio** library's features, such as `Duration`, `Instant`, and `Interval`.


## Installation & Usage

Install via **pip** or **pip3**, as in:

```
$ pip3 install asynkio
```

Use via **import**:

```python
from asynkio import (
    Duration,
    Instant,
    Interval,
    MissedTickBehaviour,
)
```

or:

```python
from asynkio.time import (
    Duration,
    Instant,
    Interval,
    MissedTickBehaviour,
)
```

`MissedTickBehavior` (US spelling) is also exported as an alias for
`MissedTickBehaviour`.


## Components

| Symbol | Description |
| --- | --- |
| `Duration` | Elapsed time, in nanoseconds (Tokio-like) |
| `Instant` | Point in time, as nanoseconds since the epoch |
| `Interval` | Async periodic timer with missed-tick policy |
| `MissedTickBehaviour` | Missed-tick policy (`BURST`, `DELAY`, `SKIP`) |


## Examples

Examples are provided in the `examples/` directory. See
[EXAMPLES.md](./EXAMPLES.md) for a summary of each script.

Run a script with, for example:

```
$ uv sync
$ uv run python examples/interval_skip.py
```


## Project Information


### Where to get help

[GitHub Page](https://github.com/synesissoftware/asynkio "GitHub Page")


### Contribution guidelines

Defect reports, feature requests, and pull requests are welcome on https://github.com/synesissoftware/asynkio.


### Dependencies

**asynkio** has no runtime dependencies beyond the **Python** standard
library (`asyncio`).


#### Efferent (fan-out)

Libraries upon which **asynkio** depends:

None.


##### Development Dependencies

* [**aiofiles**](https://pypi.org/project/aiofiles/) — development and demonstration tooling;
* [**black**](https://pypi.org/project/black/) — code formatter;
* [**diagnosticism**](https://pypi.org/project/diagnosticism/) — example scripts under `examples/`;
* [**pyclasp**](https://pypi.org/project/pyclasp/) — development and demonstration tooling;
* [**pytest**](https://pypi.org/project/pytest/) — unit-test runner;


#### Afferent (fan-in)

Projects that depend on **asynkio**:

None (currently).


### Related projects

* [**Tokio**](https://github.com/tokio-rs/tokio) (**Rust**) — the library whose time types **asynkio** emulates;
* [**Diagnosticism.Python**](https://github.com/synesissoftware/Diagnosticism.Python/) — used in `examples/` scripts;


### License

**asynkio** is released under the 3-clause BSD license. See [LICENSE](./LICENSE) for details.


<!-- ########################### end of file ########################### -->

