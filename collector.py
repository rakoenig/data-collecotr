#!/usr/bin/env python3
import argparse
import os
import sys
import json
from statistics import mean
from datetime import datetime, timedelta
from inspect import getmembers, isfunction
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urlparse
import yaml
import re


api="https://progress.opensuse.org/projects/qe-yast/issues.json"

def retry_request(method, url, data, headers, attempts=7):
    retries = Retry(
        total=attempts, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504]
    )
    http = requests.Session()
    parsed_url = urlparse(url)
    http.mount("{}://".format(parsed_url.scheme), HTTPAdapter(max_retries=retries))
    return http.request(method, url, data=data, headers=headers)


def json_rest(method, url, rest=None):
    text = json.dumps(rest)
    try:
        key = os.environ["REDMINE_API_KEY"]
    except KeyError:
        exit("REDMINE_API_KEY is required to be set")
    headers = {
        "User-Agent": "backlogger ({})".format("https://progress.opensuse.org/projects/qe-yast/wiki"),
        "Content-Type": "application/json",
        "X-Redmine-API-Key": key,
    }
    r = retry_request(method, url, data=text, headers=headers)
    r.raise_for_status()
    return r.json() if r.text else None


def check_backlog(query):
    root = json_rest("GET", api + "?" + query)
    issue_count = int(root["total_count"])
    return (issue_count)


def _today_nanoseconds():
    dt = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    epoch = datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds() * 1000000000)



if __name__ == "__main__":
    filter_start="utf8=✓&set_filter=1&sort=id:desc&f[]=status_id&op[status_id]==&v[status_id][]=3&f[]=closed_on&op[closed_on]=><&v[closed_on][]="
    filter_mid="&v[closed_on][]="
    filter_end="&f[]=&c[]=subject&c[]=project&c[]=status&c[]=assigned_to&c[]=fixed_version&c[]=is_private&c[]=due_date&c[]=relations&group_by=&t[]="
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="2024-01-01")
    parser.add_argument("--end", default=datetime.today().strftime('%Y-%m-%d'))
    switches = parser.parse_args()
    startdate=datetime.strptime(switches.start, '%Y-%m-%d')
    enddate=datetime.strptime(switches.end, '%Y-%m-%d')
    currentdate=startdate
    while currentdate <= enddate:
        num=check_backlog(filter_start + switches.start + filter_mid + currentdate.strftime('%Y-%m-%d') + filter_end)
        numstr=str(num)
        print(currentdate.strftime('%Y-%m-%d') + ", " + numstr)
        
        currentdate=currentdate + timedelta(days=1)
    

    
