#!/usr/bin/env python3

import argparse
import sys
import re
import psutil
import pandas as pd

sizes = ['B', 'K', 'M', 'G', 'T', 'P', 'E']

def main():
    parser = argparse.ArgumentParser(description='Get disk usage for a given partition (or all partitions)')
    parser.add_argument('partition', nargs='?', default=None, 
                        help='Partition to check space on. All partitions will be checked if this option is not used.')
    parser.add_argument('-s', '--size', nargs=1, choices=sizes, default=None,
                        help='Disk usage should be reported in this increment.')
    parser.add_argument('-t', '--threshold-free', nargs=1, type=float, default=None,
                        help='Threshold to send emails at (eg. 20G free space left).')
    parser.add_argument('-p', '--percent-free', nargs=1, type=float, default=None,
                        help='Percentage threshold to send emails at (eg. 10 percent of total space left).')
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
    partstats['percent'] = 100. - partstats['percent']
    partstats[['total', 'used', 'free']] = partstats[['total', 'used', 'free']].applymap(lambda cell: humanize(cell, argv.size[0]))

    # print output
    print(partstats)


def humanize(num_bytes, size=None):
    '''
    Convert an arbitrary number of bytes to human-readable form.

    @param size: A scale factor (B, M, K, G, etc.)
    '''
    if size is not None:
        converted = round(num_bytes / 1024 ** sizes.index(size), 1)
        return re.sub(r'\.0', '', str(converted) + size)
    else:
        for factor in reversed(range(len(sizes))):
            converted = round(num_bytes / 1024 ** factor, 1)
            if converted >= 1:
                return re.sub(r'\.0', '', str(converted) + sizes[factor])


def dehumanize(byte_string):
    '''
    Convert a humanized bytestring (eg. 18.5T) to number of bytes
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
