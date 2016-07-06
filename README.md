# IQFeed/DTN Downloader
This project provides command line tool and Python library to access DTN / IQFeed's historical data for equities. The provided command line tool ('iqfeed') is capable downloading 1 minute historical data from IQFeed client and store it in '.csv.gz' format.

## Prerequisites
 * Python 2.7 ([pypy](http://pypy.org) is recommended), DocOpt, PyTZ, backports.functools_lru_cache
 * IQFeed account
 * IQFeed client (e.g. [bratchenko's 'iqfeed-docker'](https://github.com/bratchenko/docker-iqfeed))

## Installation
`$ pip install iqfeed`

## Usage from command line
The provided `iqfeed` utility can be used to download CSV files from DTN / IQFeed.

Help screen:
```
iqfeed: Data downloader for Iqfeed/DTN
     Tibor Kiss <tibor.kiss@gmail.com> - Copyright (c) 2012-2016 All rights reserved

Usage:
  iqfeed process-file <filename> <start_year> <end_year> [-d DIR] [-i CON] [-t TZ] [-D]
  iqfeed download <instrument> <start_year> <end_year> [-d DIR] [-i CON] [-t TZ] [-D]
  iqfeed -h | --help

Commands:
  download            Download the specified instrument
  get-from-file       Download instruments listed in the specified file

Options:
  -d DIR --download-dir DIR   Directory where the files will be downloaded [default: .]
  -i CON --iqfeed CON         IQFeed host & port [default: localhost:9100]
  -t TZ --tz TZ               Time zone [default: US/Eastern]
  -D                          Debug mode
  -h                          Help screen

Note:
Date format for end_date and start_date: YYYYMMDD
```

### Start IQFeed client
`$ docker run -e LOGIN='<username>' -e PASSWORD='<password>' -p 5009:5010 -p 9100:9101 bratchenko/iqfeed`

### Download single instrument (SPY) for the time period 2010-2016
`$ iqfeed download SPY 2010 2016`

### Download multiple instruments listed in a text file
`$ iqfeed process-file russell-3000.lst 2016 2016`


## Usage from Python
Use the following snippet to obtain list of Bar objects.
```python
import pytz
from iqfeed import get_bars

instrument = 'GLD'
start_date = '20150101'
end_date = '20151231'
tz = pytz.timezone('US/Eastern')
seconds_per_bar = 60  # For 1M data
iqfeed_host = 'localhost'
iqfeed_port = 9100

bars = get_bars(instrument, start_date, end_date, tz, seconds_per_bar, iqfeed_host, iqfeed_port)
```

The Bar object is a named tuple which holds the Open, High, Low, Close and Volume values for the given time:
```python
IQFeedBar(datetime=datetime.datetime(2015, 1, 2, 9, 30, tzinfo=<DstTzInfo 'US/Eastern' EST-1 day, 19:00:00 STD>), open=112.46, high=112.46, low=112.45, close=112.46, volume=192104)
```

## License
[Apache License Version 2.0](http://www.apache.org/licenses/)