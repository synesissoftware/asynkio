# **asynkio** Changes


## 0.0.9 - 14th July 2026

* changes to `SKIP` (and `BURST`) functionality to provide more even behaviour;


## 0.0.8 - 12th July 2026

* updated GitHub Actions to run **ruff** / **black** (with trailing-blank-line strip before checks);


## 0.0.7 - 12th July 2026

* split implementation and test files for `Duration` and `Instant`;


## 0.0.6 - 12th July 2026

* added **black** / **ruff** formatting and linting (CI + **pyproject.toml**);


## 0.0.4 - 11th July 2026

* updated dependencies;


## 0.0.3 - 27th June 2026

* corrected project dependencies:
  * removed spurious runtime dependencies (**asyncio**, **diagnosticism**, **pytest**);
  * moved test/development dependencies to `[project.optional-dependencies]` (`dev`, `test`);
  * added `[dependency-groups] dev` so `uv sync` installs tooling for local development and testing;
* defined public API via `__all__` and package exports;
* removed **tests** from installable package via `[tool.setuptools.packages.find]`;
* added **MANIFEST.in**;
* aligned README badges with Diagnosticism.Python 0.16 style;
* added **pyproject.toml** classifiers for Python 3.11+ (including 3.14);
* fixed misspelt unit test names;
* added `Interval` unit tests with mocked **asyncio**;
* fixed `Interval.negative_bias()` return value;
* extended GitHub Actions workflow for feature branches, and Python 3.14;
* completed README **Dependencies**, **Examples**, and **Related projects** sections;
* moved interval demonstration scripts from **tests/** to **examples/**;
* updated GitHub Actions to install the project from **pyproject.toml**;
* added **build_dist_uv.sh** (build + `twine check`);
* aligned **build_dist.sh** with **build_dist_uv.sh** (system Python);


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

