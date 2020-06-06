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
environment. **problems:** if you encounter a problem when creating the
environment, open the iono.yml and modify the file as follows:
asssuming that the line specifying matplotlib is the issue. Delete the part of
the line from the second `=` sign (including the second `=` sign) until the
end of the line.

Line causing the issue:
				matplotlib-base=3.1.3=py36hc955a2_0

Fixed
				matplotlib-base=3.1.3

Create the environment using the file iono.yml
conda env create -f iono.yml

**Downloading the data**
##In order to work properly the script must be run within the shell_scripts folder ##
mkdir ionex_esag
sh shell_scripts/download_files.sh

**Finding files with missing data (or without data)**
In the ionex_esag directory run the following
find -type f -empty -exec rm -f {} \;

**Backup Files**
mkdir ionex_esag_bk
cp ionex_esag/* ionex_esag_bk

**Extracting the Data**
Files are compressed; with a .Z ending
run the following command from directory containing the downloaded esag files.

uncompress esag*

**Replace the empty files**
JPL along with other organizations provide similar data in the same format.
The data from esag is more uniform and complete.  I replaced the empty esag
files with their counterparts from jpl. (Do not attempt to used JPL to
download all the files, because the dataset has missing/corrupt data.

cp ionex_esag_emptyfiles/esag*.12i ionex_esag/


**Transforming the Data**
Since this a project uses both Julia and Python3, Julia is used for the
computational intensive tasks and Python3 mostly for the DASH/Flask
application.  In the future Genie.jl might be used to replace the Api/App
functionallity (Dash/Flask)

run the julia.ipynb notebook using jupyter lab or notebook.
The notebook will basically create the CSV and Table files needed to create
the database.  The table files are needed by JuliaDB
