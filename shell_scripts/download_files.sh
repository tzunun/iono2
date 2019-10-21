#!/usr/bin/bash

#time aria2c -d ionex_files/ -i ionex_files_urls.txt -j 120 --c true

START_TIME=$SECONDS

# Download and save the files listed in the ionex_files_urls.txt located in the parent directory to a new directory named ionex_files.
aria2c --dir=../ionex_files/ --input-file=../ionex_files_urls.txt --max-concurrent-downloads=120 --continue=true 

ELAPSED_TIME=$(($SECONDS - $START_TIME))

TOTAL_DOWNLOADED_FILES=$(wc -l ../ionex_files_urls.txt) 

echo "$TOTAL_DOWNLOADED_FILES were downloaded in $(($ELAPSED_TIME/60)) minutes $(($ELAPSED_TIME%60)) seconds."
