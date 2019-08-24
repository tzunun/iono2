**Earthquake Project**
Closest City
				find the closest city to the epicenter of an earthquake.

Historical Weather Data
				Obtain historical ambient temperature from a location or city.  This is usually only 30 days prior to the
				date given.

**Install**
Anaconda 3.7

**Terminology**

	Terminator: The line that separates day and night, it is also referred to as the "grey line" and the "twilight zone".  For more information see
    https://sos.noaa.gov/datasets/daynight-terminator-daily/


**Important!**
	This code has been tested on Ubuntu 18.04LTS other Linux distributions might work.
	aria2 is used instead of wget to speed up downloading the data.  wget only downloads a file at a time.

	if using ubuntu
	sudo apt install aria2