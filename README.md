# data-collector

## About

This is a "quick & dirty" script to create CSV data from progress.opensuse.org. It is used as a proof of concept for the QE Yam metrics project. 

The code is a rough fork of [backlogger](https://github.com/openSUSE/backlogger), stripped down to the functionality we need.

## Usage

Invoke the script like that:
``` 
$ REDMINE_API_KEY=<your_api_key> ./collector --start=<YYYY-MM-DD> --end=>YYYY-MMM-DD>
```

### Parameters
- **--start**: Start date in YYYY-MM-DD format (default 2024-01-01)
- **--end**: End date in YYYM-MM-DD format (default is the current date)

### Output
The output is a series of CSV data, first column is the date starting at "--start" until "--end", the second column is the number of resolved tickets since the start date.

## Recommendations

You can pipe the data to other programms or append it to an existing CSV file. It is recommended to create headers for the CSV file, so the first line should read something like `date,number`. 

Also note that this script iterates, so if you want to use it to add daily data you need to modify it a bit, e.g. remove the iteration loop, so that it does just one measurement for today. 