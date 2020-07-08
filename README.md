## Note
Anonymous ftp access will be discountinued at CDDIS on October 31st 2020, there will be other ways to obtain the data but the script I wrote to get the ionospheric data wil no longer work.

Dark Sky was acquired by Apple and it is no longer accepting new singups.

**Earthquake Project**

Information about the scripts.

Closest City
				find the closest city to the epicenter of an earthquake.

Historical Weather Data
				Obtain historical ambient temperature from a location or city.  This is usually only 30 days prior to the
				date given.

**Install**
Julia
Once you have Julia installed, you need to install IJulia

Anaconda 3.7
or
Miniconda 3.7

**Terminology**

	Terminator: The line that separates day and night, it is also referred to as the "grey line" and the "twilight zone".  For more information see
    https://sos.noaa.gov/datasets/daynight-terminator-daily/


**Important!**
	This code has been tested on Ubuntu 18.04LTS other Linux distributions might work.
	aria2 is used instead of wget to speed up downloading the ionospheric data.  previously I was using wget and was only downloading a file at a time.

if using ubuntu
```console
sudo apt install aria2
```

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
```console
conda env create -f iono.yml
````

**Downloading the data**
Run the following command
```console
bash shell_scripts/download_files.sh
```

**Finding files with missing data (or without data)**
In the ionex_esag directory run the following

This will create/overwrite a file name empty_files_list.txt in the ionex_esag_missing_files
```console
find -type f -empty > ionex_esag_missing_files/empty_files_list.txt
```

compare the empty_files_list.txt with the list.txt, if there is a file that is not on the list.txt then you must add it, because the script download_missing_files.sh uses it to download the missing files.

for example if the missing file is: esag2490.18i.Z
the format is the following .../ionex/year/day/agency{day}0.{year}i.Z

The complete file name on the list.txt file would be:
ftp://cddis.nasa.gov/gnss/products/ionex/2018/249/jplg2490.18i.Z  

This will remove the empty files 
```console
find -type f -empty -exec rm -f {} \;
```

**Replace the empty files**

JPL along with other organizations provide similar data in the same format.
The data from esag is more uniform and complete.  I replaced the empty esag
files with their counterparts from jpl. (Do not attempt to used JPL to
download all the files, because the dataset has missing/corrupt data.)

**Download the missing files only if necessary** since the missing files are included in the repo.

from the ionex_esag_missing_files directory run the following
```console
bash download_files.sh ./
```


**Copy the missing files to the ionex_esag directory**

from the iono2 folder run 
```console
cp ionex_esag_missing_files/esag*.Z ionex_esag/
```

**Rename the downloade files in the ionex_esag_missing_files directoroy**

By replacing the jplg with esag in the file name. For example:

jplg0310.12i.Z will become esag0310.12i.Z

Or you could run the following command form within the ionex_esag directory
```console
for file in *.Z; do mv "$file" "${file/jpl/esa}"; done
```

**Backup Files**
from the iono2 directory run the following
```console
mkdir ionex_esag_bk

cp ionex_esag/* ionex_esag_bk
```


**Extracting the Data**
Files are compressed; with a .Z ending
run the following command from directory ionex_esag.

```console
uncompress esag*
```
**Transforming the Data**
Since this a project uses both Julia and Python3, Julia is used for the
computational intensive tasks and Python3 mostly for the DASH/Flask
application.  In the future Genie.jl might be used to replace the Api/App
functionallity (Dash/Flask)

run the julia.ipynb notebook using jupyter lab or notebook.
The notebook will basically create the CSV and Table files needed to create
the database.  The table files are needed by JuliaDB

**Create Directories to store data**

```console
mkdir tec_csv_esag tec_tables_esag
```

**OLR Dataset**

https://www.ncei.noaa.gov/

https://www.ncei.noaa.gov/data/outgoing-longwave-radiation-daily/access/


**TEC Dataset**

Explanation of the term:
https://www.swpc.noaa.gov/phenomena/total-electron-content

NASA Crustal Dynamics Data Information System
https://cddis.nasa.gov/

https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/atmospheric_products.html#iono

**Weather Data**
https://darksky.net

https://darksky.net/dev

