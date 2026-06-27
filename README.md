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

Examples are provided in the ```examples``` directory, along with a markdown description for each. A detailed list TOC of them is provided in [EXAMPLES.md](./EXAMPLES.md).


## Project Information


### Where to get help

[GitHub Page](https://github.com/synesissoftware/asynkio "GitHub Page")


### Contribution guidelines

Defect reports, feature requests, and pull requests are welcome on https://github.com/synesissoftware/asynkio.


### Dependencies

T.B.C.


### Related projects

T.B.C.


### License

**asynkio** is released under the 3-clause BSD license. See [LICENSE](./LICENSE) for details.


<!-- ########################### end of file ########################### -->

