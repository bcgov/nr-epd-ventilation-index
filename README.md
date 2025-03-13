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

## Operating Guide

Manual intervention should not be needed because the application will run every
60 minutes, and abort if there exists a report for the day. However, if
necessary, but application can be triggered by manually starting the
`run_application` github workflow.

### Updating Zone Definitions and Weights

The zone definitions used by this application are the same zones that are used
by the
([Ventilation Index Interactive Map](https://governmentofbc.maps.arcgis.com/apps/webappviewer/index.html?id=6d288bc667b24528a5c1e3b4c0373d07)).
The zone definitions used by the map application define multiple polygons for
each zone, which would increase the runtime of this application. I have created
a script that will take the union of all zones with the same name and output a
compressed file suitable for use by this application.

To update the definitions follow the procedure:

1. Install uv (https://docs.astral.sh/uv/) for your platform. This software
   manages Python virtual environments without making any modifications to your
   system and will ensure that you can run the script.

2. Open a terminal in the root of your local copy of this code, and use uv to
   install the python development environment:

   ```bash
   uv sync --all-extras --dev
   ```

3. Place the updated zone definitions KML file, a GRIB2 forecast file, and the
   ventilation index weights csv file in the source directory and run
   the `process_data.py` script.

   ```bash
   uv run ./scripts/process_data.py forecast.grib2 ventilation_index_weights.csv Venting_Index_HD.kml
   ```

4. This may take several minutes to run depending on your device. It should
   create the point_data.csv file. Commit this to source control.

### Adding new / renaming zones

If a zone name changes, or a zone is added to the system, there is a data
structure that maps the zone name used on the Government of British Columbia
interactive ventilation index map and the legacy ECCC report for ingestion. This
structure is located in `utils/output.py`.
   
## Development Requirements

- uv (https://docs.astral.sh/uv/) for python version and dependency management.
- ruff (comes bundled with uv), run `uvx ruff check`, or better yet, install the
  editor extension and let it do all the work.

To set your environment up for development run `uv sync --all-extras --dev` to
automatically deploy a python virtual environment. This includes the ruff
formatter. To run the application run `uv run main.py`.

Testing the pull request system