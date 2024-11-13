# nr-epd-ventilation-index

This application sources ventillation index data from Environment Canada and
produces a text file similar to the bulletin produced by Environment Canada
prior to 2025. This file powers many of BC's services related to ventilation
index.

## Development Requirements

- uv (https://docs.astral.sh/uv/) for python version and dependency management.
- ruff (comes bundled with uv), run `uvx ruff check`, or better yet, install the
  editor extension and let it do all the work.