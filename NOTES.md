# asynkio - NOTES <!-- omit in toc -->


## Testing

`$ uv sync`

`$ uv run pytest`


## Building distributions

`$ ./build_dist_uv.sh`

Builds `sdist` and `wheel` under `dist/` and runs `twine check` (via
**uv** and `.venv`).

`$ ./build_dist.sh`

Same steps using system **`python3`** (requires `build` and `twine` to
be installed).


<!-- ########################### end of file ########################### -->

