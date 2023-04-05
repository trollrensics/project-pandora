# Project Pandora

https://beeldengeluid.nl/kennis/projecten/pandora

The project team consists of Nederlands Instituut voor Beeld & Geluid (coordinator), Trollrensics, Maastricht University, and Pointer, the journalistic editorial team of KRO-NCRV.

PANDORA provides tools that enable black-box algorithm analyses to be performed by researchers. Additionally, research is being conducted on ways to make the public more resilient to the influence of disinformation. Results will be shared with the academic community and will inform policymakers about the 'auditing' of algorithms.

## This repository

This source code takes a number of TikTok GDPR export files and loads them into a MySQL database.
Subsequently, it will resolve the redirections and retrieve and store the movies using the Trollrensics platform. 
It will also retrieve the description and store it in the database.

The code also has functionality to export the data to a XLSX file.

The GDPR export files should be placed in a `data/` directory and have filenames `TikTok_Data_xxxxxxxxxx.json` where `xxxxxxxxxx` is a timestamp.

Usage: `python3 tiktokdata.py`

### Command line options:
* `--create-db`: create database structure only
* `--read-data`: read the data from the JSON files into the database
* `--download-videos`: resolve redirections and retrieve videos
* `--export`: export database to `xlsx` file.

If no command line options are given, all tasks are performed.

### Environment variables:
* `MYSQL_USER=`
* `MYSQL_PASSWORD=`
* `MYSQL_HOST=localhost`
* `MYSQL_PORT=3306`
* `MYSQL_DATABASE=`
* `TROLLRENSICS_API_KEY=`

### Credits

(c)2023 Trollrensics BV

License: MIT
