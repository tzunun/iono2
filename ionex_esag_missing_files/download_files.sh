#!/usr/bin/bash

#time aria2c -d ionex_files/ -i ionex_files_urls.txt -j 120 --c true

DIR=$(dirname $(dirname $(readlink -f "$0")))
ESAG_DOWNLOAD_DIR="${DIR}/ionex_esag_missing_files" 
URL_FILE="${ESAG_DOWNLOAD_DIR}/list.txt"
DOWNLOAD_LOCATION="${ESAG_DOWNLOAD_DIR}"

#Create directory to store the downloaded files if it does not exist.
if [  -d "$ESAG_DOWNLOAD_DIR" ]; then
				echo "$ESAG_DOWNLOAD_DIR exists. Starting download.."
else
				echo "Directory not present, creating directory $ESAG_DOWNLOAD_DIR"
				mkdir ${ESAG_DOWNLOAD_DIR}
fi

# Download and save the files listed in the ionex_urls_esag.txt which is in
# the parent directory to a new directory named ionex_esag.
aria2c --dir=$DOWNLOAD_LOCATION --input-file=$URL_FILE --max-concurrent-downloads=120 --continue=true


