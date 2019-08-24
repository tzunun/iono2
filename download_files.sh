#!/usr/bin/bash

#time aria2c -d ionex_files/ -i ionex_files_urls.txt -j 120 --c true

time aria2c --dir=ionex_files/ --input-file=ionex_files_urls.txt --max-concurrent-downloads=120 --continue=true