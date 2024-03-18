# data-collector

## About

This is a "quick & dirty" script to create CSV data from progress.opensuse.org. It is used as a proof of concept for the QE Yam metrics project. 

The code is a rough fork of [backlogger](https://github.com/openSUSE/backlogger), stripped down to the functionality we need.

## Usage

Invoke the script like that:
``` 
$ REDMINE_API_KEY=<your_api_key> ./collector --start=<YYYY-MM-DD> --end=<YYYY-MMM-DD>
```

### Parameters
- **--start**: Start date in YYYY-MM-DD format (default 2023-12-01)
- **--end**: End date in YYYM-MM-DD format (default is the current date)
- **--dump**: Initiates dump mode if set to "true" (default "false"). If enabled you will get a header line "Date,Resolved" plus one line with CSV data for each day from start to end. Otherwise you will just get one line, showing the count between start and end. 

### Output
The output is a series of CSV data, first column is the date starting at "--start" until "--end", the second column is the number of resolved tickets since the start date.

## Recommendations

You can pipe the data to other programms or append it to an existing CSV file. 

