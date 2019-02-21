import calendar
import datetime
import requests

# EQ date, city and days_range
def create_dates_list(earthquake_date, days_range=21, years_range=20):
    day = 1
    year = 365.24225
    dates_list = []  # This will become a 2d array in order to obtain the historic temperatures
    
    date = convert_to_epoch(earthquake_date)
    years = epoch_list(eq_date, years_range, year)
    
    for year in years:
        dates_list.append(epoch_list(year, days_range, day))

    return dates_list


# UTC to UTC_epoch time.
def convert_to_epoch(timestamp):
    time_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    epoch = int(calendar.timegm(time.strptime(timestamp,time_format)))
    return epoch


# time_frame is the days or years from the date up to the specific days prior to the date. i.e 21 days before the date
def epoch_list(date, time_frame, time_interval):  # time_interval expects a value of 1 for day, and 365.24225 for year
    
    epoch_list = []
    start_epoch = datetime.datetime.fromtimestamp(date)
    
    for i in range(time_frame + 1):
        stop_epoch = start_epoch - datetime.timedelta(days=i*time_interval)
        epoch_list.append(int(stop_epoch.timestamp()))
        
    return epoch_list    # The original date is also returned in the list


def get_historic_temperatures(date, city, dates_list):
    # Api endpoint
    url = 'https://api.darksky.net/forecast/api_key/latitude,longitude,time'
    
    # Api key
    
    time = dates_list[0][1]   # This is just an example
    
    latitude = city['latitude']
    longitude = city['longitude']
    
    # This funtion will return the historic temperatures in a list with dates and temps.<Paste>

