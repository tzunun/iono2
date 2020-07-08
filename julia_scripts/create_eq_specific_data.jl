#=
This will be used to create earthquake specific data, to go back in time in 
the weather, tec and OlR data.  The points will be the lat, lon from eq and it is 
identified by using its timestamp and possibly magnitude.

This program expects a text files with a list of earthquakes from which to extract
the name(timestamp), lat, lon and magnitude. and create a new dataset per earthquake.
this dataset will combine weather data, tec and olr in a time period of 3 months of
readeings from those datasets that span about 20 years.
=#
function closest_point(array, point)
    _, idx = findmin(abs.(array .- point))
    array[idx]
end

#read timestamp

#read lat, lon, magnitude

#read using juliadb table the information for 3 months for tec, olr and weather.
#there should be on big juliadb table created for each of those, that way when creating
# reading files form the disk is minimized and all the operations are in RAM

# From the earthquake79 data
#timestamp will provide the name for the csv with weather information
#timestamp for name, lat, lon, for tec measurements csv
#timestamp for name, lat, lon, for OlR measurements csv

#= for this data i only need to access the files on the datatime and hour of 
    the earthquake.
    =#
