import calendar
import datetime
import requests
import time

# Create list of dates to check the historical temperatures
def create_dates_list(earthquake_date, days_range=20, years_range=20):
    '''create a list of years and days, with a range of 20 days prior to the earthquake and for the past
    20 years'''

    historical_dates_list = []  # This will become a 2d array in order to obtain the historic temperatures
    day = 1
    year = 365.24225
    
    earthquake_unix_time = convert_to_unix_time(earthquake_date)
    years = unix_time_list(earthquake_unix_time, years_range, year)  # Years becomes a list of years_range
    
    for year in years:
        historical_dates_list.append(unix_time_list(year, days_range, day))  # The historical dates (days) are generated

    return historical_dates_list


# UTC to UTC_unix_time time.
def convert_to_unix_time(timestamp):
    '''Convert the earthquake date usually provided in the format of 2018-12-20T17:01:55.150Z to unix time.
    This helps with dates calculations'''

    time_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    return int(calendar.timegm(time.strptime(timestamp,time_format)))


# time_frame is the days or years from the date up to the specific days prior to the date. i.e 21 days before the date
def unix_time_list(earthquake_date, time_frame, time_interval):  # time_interval expects a value of 1 for day, and 365.24225 for year
    '''Generate a list of a range of dates in unix time, calculated using the time_frame which is range of years or days
    based on the time_interval (day, for days and year for years)'''
    
    unix_time_list = []
    starting_unix_time = datetime.datetime.fromtimestamp(earthquake_date)
    
    for i in range(time_frame + 1):
        stopping_unix_time = starting_unix_time - datetime.timedelta(days=i*time_interval) 
        unix_time_list.append(int(stopping_unix_time.timestamp()))
        
    return unix_time_list    # The original date is also returned in the list


def get_historic_temperatures(date, city, dates_list):
    # Api endpoint
    url = 'https://api.darksky.net/forecast/api_key/latitude,longitude,time'
    
    # Api key
    
    time = dates_list[0][1]   # This is just an example
    
    latitude = city['latitude']
    longitude = city['longitude']
    
    # This funtion will return the historic temperatures in a list with dates and temps.<Paste>

### Todo list
# A file containing the calcualted unix time date range will be created
# from that file calls will be made to the api, the results will be stored in a files historical temperatures
# Temperature will have to be checked with nearest city to check if this could turn into a feature.
# Temperature has to be close to the terminator time, sunrise and sunset time.  This is provided from the API response
# The actual terminator temps can then be obtained by looking into the object and finding the closest time in the 
# response to the terminator time.  If the time falls between the hours provided pick the earliest time in the morning
# and later time in the afternoon.  Or just calculate and average of the two temperatures.
