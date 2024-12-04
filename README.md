# Natural Resources - Environment Protection Division - Ventilation Index Project

British Columbia's ventilation index alert system is used by citizens to know
whether or not they are allowed to perform controlled burns in various regions
of the province.  Previously this data was sourced from Environment Canada's
ECCC Datamart where they post daily bulletins with forecast values. Recently,
Environment Canada has started publishing this data in much higher resolution in
the World Meteorological Organization's standard General Regularly-distributed
Information in Binary form format (GRIB). This project is a first step towards
modernizing British Columbia's capabilities by reading the GRIB data and
reproducing the original bulletin so that our systems can continue to operate.
It will allow us to produce more, and more highly detailed data in the future.

## Development Requirements

- uv (https://docs.astral.sh/uv/) for python version and dependency management.
- ruff (comes bundled with uv), run `uvx ruff check`, or better yet, install the
  editor extension and let it do all the work.