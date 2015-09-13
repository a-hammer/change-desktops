#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Set desktop pictures for all desktops on OS X 10.9+.
#
# Arthur Hammer
# https://github.com/a-hammer/change-desktops

import os
import sys
import argparse
import subprocess
import sqlite3
from contextlib import closing
from collections import OrderedDict


DB = os.path.expanduser('~/Library/Application Support/Dock/desktoppicture.db')
GET_QUERY = 'SELECT * FROM data ORDER BY ROWID DESC'
SET_QUERY = 'UPDATE data SET value = (?)'


def execute(query, params=[]):
    if not os.path.exists(DB):
        raise IOError('Desktop picture database does not exist: %s' % DB)

    with closing(sqlite3.connect(DB)) as conn:
        return conn.execute(query, params).fetchall()


# Raises IOError, sqlite3.Error
def get_desktops():
    pics = execute(GET_QUERY)
    pics = [pic[0] for pic in pics]
    pics = [pic for pic in pics if not os.path.isdir(pic)]
    return list(OrderedDict.fromkeys(pics))  # Trim duplicates


# Raises IOError, sqlite3.Error, CalledProcessError
def set_desktops(pic):
    pic = os.path.abspath(pic)
    if not os.path.isfile(pic):
        raise IOError('File does not exist: %s' % pic.encode('utf-8'))

    execute(SET_QUERY, params=[pic])
    subprocess.check_call(['killall', 'Dock'])


def main():
    # Just wanted to try argparse...
    info = 'Set desktop pictures on all desktops.'
    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('picture',
                        type=lambda s: unicode(s, sys.stdin.encoding),
                        nargs='?',
                        help='image file to be set as desktop picture on all '
                             'desktops. Dock will be restarted after setting. '
                             'If argument is missing, lists most recent'
                             'desktop pictures.')
    args = parser.parse_args()

    try:
        if args.picture is not None:
            set_desktops(args.picture)
        else:
            print '\n'.join(get_desktops())
    except IOError, e:
        sys.stderr.write(str(e))
        sys.exit(1)
    except sqlite3.Error, e:
        sys.stderr.write('An error occured while accessing the databse:\n  %s'
                         '\nError:\n  %s' % (DB, str(e)))
        sys.exit(1)
    except subprocess.CalledProcessError, e:
        sys.stderr.write('Could not restart Dock. Restart manually for changes'
                         ' to take effect.')
        sys.exit(1)

if __name__ == '__main__':
    main()
