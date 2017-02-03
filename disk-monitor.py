#!/usr/bin/env python3

import argparse
import sys
import re
import psutil
import pandas as pd

sizes = ['B', 'K', 'M', 'G', 'T', 'P']

def main():
    parser = argparse.ArgumentParser(description='Get disk usage for a given partition (or all partitions)')
    parser.add_argument('partition', nargs='?', default=None, 
                        help='Partition to check space on. All partitions will be checked if this option is not used.')
    parser.add_argument('-s', '--size', nargs=1, choices=sizes, 
                        help='Disk usage should be reported in this increment.')
    argv = parser.parse_args()

    partitions = argv.partition
    all_partitions = [diskpart.mountpoint for diskpart in psutil.disk_partitions()]
    if partitions is None:
        partitions = all_partitions
    elif partitions not in all_partitions:
        sys.exit('Partition "' + partitions + '" not a valid partition. Must be one of: "' + '", "'.join(all_partitions) + '"')
    
    partstats = []
    for partition in partitions:
        partstats.append(psutil.disk_usage(partition))
    partstats = pd.DataFrame(partstats, index=partitions)
    print(partstats)
    print(partstats.applymap(humanize))


def humanize(num_bytes):
    '''
    Convert an arbitrary number of bytes to human-readable form.
    '''
    for factor in reversed(range(len(sizes))):
        converted = round(num_bytes / 1024 ** factor, 1)
        if converted >= 1:
            return re.sub(r'\.0', '', str(converted) + sizes[factor])


def dehumanize(byte_string):
    '''
    Convert a humanized bytestring (eg. 18.5TB) to number of bytes
    '''
    byte_string = str(byte_string)  # just in case
    factor = 0
    for scale in reversed(range(len(sizes))):
        if sizes[scale] in byte_string:
            factor = scale
            break       
    number = float(re.findall(r'[0-9]+\.?[0-9]*', byte_string)[0])
    return int(number * 1024 ** factor)


if __name__ == '__main__':
    main()
