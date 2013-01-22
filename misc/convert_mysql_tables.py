#!/usr/bin/env python
from __future__ import print_function
from collections import namedtuple
import optparse
import os
import sys

import sh

MYSQL_MAX_TABLE_NAME_LENGTH = 64

if hasattr(sys, 'real_prefix'):
    # We are inside a virtual env
    BASE_DIR = os.path.join(os.environ['VIRTUAL_ENV'], 'mayan')
else:
    BASE_DIR = os.getcwd()

Table = namedtuple('Table', '''name, engine, version, row_format, rows,
                    avg_row_length, data_length, max_data_length,
                    index_length, data_free, auto_increment, create_time,
                    update_time, check_time, collation, checksum,
                    create_options, comment''')


class Convert(object):
    _mysql = sh.Command('mysql')

    TABLE_TYPES = ['MyISAM', 'InnoDB', 'IBMDB2I', 'MERGE', 'MEMORY', 'EXAMPLE', 'FEDERATED', 'ARCHIVE', 'CSV', 'BLACKHOLE']

    def __init__(self, database, username, password):
        self.database = database
        self.username = username
        self.password = password
        self.mysql = self._mysql.bake(database=self.database, user=self.username, password=self.password)

    def get_tables(self, engine=None):
        for table in self.mysql(_in='SHOW TABLE STATUS IN `%s`;' % self.database).stdout.splitlines()[1:]:  # Discard first line which is just a title
            table = Table._make(table.split('\t'))  # Split by tab, and make each string into a Table instance argument
            if table.engine == engine or not engine:
                yield table

    def execute(self, destination, source=None, dryrun=False, verbose=False):
        if dryrun:
            print('\t')
            print('-' * 21)
            print('Tables to be modified')
            print('-' * 21)
            for table in self.get_tables(source):
                print (table.name, ' ' * (MYSQL_MAX_TABLE_NAME_LENGTH - len(table.name)), table.engine)
        else:
            for table in self.get_tables(source):
                command = 'ALTER TABLE `%s` ENGINE = %s;' % (table.name, destination)

                if verbose:
                    print('Converting table %s to engine %s...' % (table.name, destination), end='')
                    sys.stdout.flush()
                    
                process = self.mysql(_in=command)

                if verbose:
                    print ('Done.')


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-n', '--dry-run', help='don\'t actually change anything', dest='dryrun', default=False, action='store_true')
    parser.add_option('-d', '--database', help='which database to convert', dest='db', action='store', metavar='database')
    parser.add_option('-u', '--username', help='username used to connect to the database', dest='user', action='store', metavar='username')
    parser.add_option('-p', '--password', help='password used to connect to the database', dest='passwd', action='store', metavar='password')
    parser.add_option('-s', '--source', help='engine type of tables to convert', dest='src', action='store', metavar='source')
    parser.add_option('-c', '--destination', help='engine type to convert the tables', dest='dest', action='store', metavar='destination')
    parser.add_option('-v', '--verbose', help='verbose output', dest='verbose', default=False, action='store_true')

    (opts, args) = parser.parse_args()

    if not opts.db or not opts.user or not opts.passwd or not opts.dest:
        parser.print_help()
    elif opts.src and opts.src not in Convert.TABLE_TYPES:
        sys.stderr.write('Unknown source table engine type.\n')
    elif opts.dest and opts.dest not in Convert.TABLE_TYPES:
        sys.stderr.write('Unknown destination table engine type.\n')
    else:
        convert = Convert(opts.db, opts.user, opts.passwd)
        convert.execute(opts.dest, opts.src, opts.dryrun, opts.verbose)
