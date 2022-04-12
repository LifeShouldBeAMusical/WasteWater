# WasteWater

## Running

To run in a command line:

`python main.py`

Optional commands are as follows:

`-j <Jurisdiction>` to search for data in a specific jurisdiction.

Supported Jurisdictions:

* Chicago
* District of Columbia
* Houston
* LA County
* New York City

`-c <County>` to search for data in a specific county.

`-s <State>` to search for data in a specific state or territory.


## Data Filtration

Samples that ended prior to 2 weeks from run date is completely ignored.
Otherwise, we look at the most recent sample(s) from each wastewater treatement plant.