# **asynkio** Changes


## 0.0.3 - 27th June 2026

* corrected project dependencies:
  * removed spurious runtime dependencies (`asyncio`, `diagnosticism`, `pytest`);
  * moved test/development dependencies to `[project.optional-dependencies]` (`dev`, `test`);
  * added `[dependency-groups] dev` so `uv sync` installs tooling for local development and testing;
* defined public API via `__all__` and package exports;
* removed **tests** from installable package via `[tool.setuptools.packages.find]`;
* added **MANIFEST.in**;
* aligned README badges with Diagnosticism.Python 0.16 style;
* added **pyproject.toml** classifiers for Python 3.11+;
* fixed misspelt unit test names;
* added `Interval` unit tests with mocked `asyncio`;
* fixed `Interval.negative_bias()` return value;
* extended GitHub Actions workflow for feature branches, and Python 3.14;
* completed README **Dependencies**, **Examples**, and **Related projects** sections;
* moved interval demonstration scripts from **tests/** to **examples/**;


## 0.0.2 - 24th August 2025

* added `Interval`;
* added `MissedTickBehaviour`;


## 0.0.1 - 24th August 2025

* significant enhancements to time types `Duration` and `Instant`;


## 0.0.0.1 - 24th August 2025

* tidying;


## 0.0.0 - 24th August 2025

* boilerplate;
* GitHub Actions;


## previous versions

T.B.C.


<!-- ########################### end of file ########################### -->

