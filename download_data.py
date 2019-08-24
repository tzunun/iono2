import os.path
import subprocess

# Download the data
''' The data is contained on various files at the following location
    ftp://cddis.nasa.gov/gnss/products/ionex/
    ftp://cddis.nasa.gov/gnss/products/ionex/<year>/<day>/jpl0010.88i.Z
    for January 1, 1999 the address is
    ftp://cddis.nasa.gov/gnss/products/ionex/1999/001/jplg0010.99i.Z

    <year> in this case will be a range of 1999-2018
    <day> is a range from 001-365 (366 if it is a leap year)
    2000 is a leap year so there is a day 366,
    '''

# Base Url (starting directory)
base_url = 'ftp://cddis.nasa.gov/gnss/products/ionex/'
    
# Create a list of years as strings 1999-2018
years = [str(year) for year in range(1999, 2019)]

# Create a list of 3 digit days as strings 001-366 
days = ['%03d' % day for day in range(1, 367)] 

# Generate URL list of files to download.
def generate_file_url(url, year, day):
    return  ''.join([url, year, '/', day, '/jplg', day, '0.', year[2:], 'i.Z'])


def create_urls_list_file():
    global days
    global years
    global base_url
    leap_year = days
    regular_year = days[:-1]

    with open('ionex_files_urls.txt', 'w') as file:
        for year in years:
            
            if int(year) % 4 == 0:
                days = leap_year
            else:
                days == regular_year
            
            for day in days:
                file.write((generate_file_url(base_url, year, day) + '\n'))
            
def save_files():
    subprocess.Popen(['bash', 'download_files.sh'])


    # Some infourls
    print('Finished downloading files')
    

def download_files():

    # Check if file exists, else create the file
    if os.path.isfile('ionex_files_urls.txt'):
        save_files()
    else:
        create_urls_list_file()
        download_files()


if __name__ == "__main__":
    download_files()