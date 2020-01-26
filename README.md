**Earthquake Project**
Closest City
				find the closest city to the epicenter of an earthquake.

Historical Weather Data
				Obtain historical ambient temperature from a location or city.  This is usually only 30 days prior to the
				date given.

**Install**
Anaconda 3.7
or
Miniconda 3.7

**Terminology**

	Terminator: The line that separates day and night, it is also referred to as the "grey line" and the "twilight zone".  For more information see
    https://sos.noaa.gov/datasets/daynight-terminator-daily/


**Important!**
	This code has been tested on Ubuntu 18.04LTS other Linux distributions might work.
	aria2 is used instead of wget to speed up downloading the data.  wget only downloads a file at a time.

	if using ubuntu
	sudo apt install aria2

**Python 3.6 is required for the iono environment**
YML file is provided (iono.yml) you will have to use conda or miniconda.
The conda-forge channel will be the source of the libraries on this
environment. 

conda env create -f iono.yml

**Downloading the data**
mkdir esag_ionex
sh shell_scripts/download_files.sh

**Extracting the Data**
Files are compressed; with a .Z ending
run the following command from directory containing the downloaded esag files.

uncompress esag*


**Transforming the Data**
Since this a project uses both Julia and Python3, Julia is used for the
computational intensive tasks and Python3 mostly for the DASH/Flask
application.  In the future Genie.jl might be used to replace the Api/App
functionallity (Dash/Flask)

run the julia.ipynb notebook using jupyter lab or notebook.
The notebook will basically create the CSV and Table files needed to create
the database.  The table files are needed by JuliaDB
