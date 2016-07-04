#!/usr/bin/env python2.7
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""iqfeed: Data downloader for Iqfeed/DTN
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

"""


import os
import sys
import logging

import docopt
import pytz

from .download import get_bars
from .tools import get_instruments_from_file, write_bars_to_file


def main():
    args = docopt.docopt(__doc__, argv=sys.argv[1:], version=0.4)

    log = logging.getLogger()
    log_console = logging.StreamHandler(sys.stdout)
    log.setLevel(logging.DEBUG if args['-D'] else logging.INFO)
    log_console.setLevel(logging.DEBUG if args['-D'] else logging.INFO)
    log.addHandler(log_console)

    if args['download']:
        instruments = (args['<instrument>'], )
    elif args['process-file']:
        instruments = get_instruments_from_file(args['<filename>'])

    start_year = int(args['<start_year>'])
    end_year = int(args['<end_year>'])
    iqfeed_host, iqfeed_port = args['--iqfeed'].split(':')
    iqfeed_port = int(iqfeed_port)
    tz = pytz.timezone(args['--tz'])
    download_dir = args['--download-dir']
    seconds_per_bar = 60  # 1M data

    for (i, instrument) in enumerate(instruments):
        try:
            log.info("Processing %s (%d out of %d)", instrument, i+1, len(instruments))

            for year in range(start_year, end_year+1):
                filename = '%s/HC-%s-1M-%d-iqfeed.csv.gz' % (download_dir, instrument, year)
                start_date = '%s0101' % year
                end_date = '%s1231' % year

                if os.path.exists(filename):
                    log.info('File already exists: %s', filename)
                    continue
                else:
                    log.info('Downloading to %s', filename)

                bars = get_bars(instrument, start_date, end_date, tz, seconds_per_bar, iqfeed_host, iqfeed_port)
                if len(bars):
                    write_bars_to_file(bars, filename, tz)

        except Exception as e:
            log.error('Exception during download, continuing', exc_info=e)
