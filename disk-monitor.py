#!/usr/bin/env python3

import argparse
import psutil

sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

def main():
    parser = argparse.ArgumentParser(description='Get disk usage for a given partition (or all partitions)')
    parser.add_argument('partition', nargs='?', default=None, 
                        help='Partition to check space on. All partitions will be checked if this option is not used.')
    parser.add_argument('-s', '--size', nargs=1, choices=sizes, 
                        help='Disk usage should be reported in this increment.')
    argv = parser.parse_args()

    partitions = argv.partition
    if partitions is None:
        partitions = [diskpart.device for diskpart in psutil.disk_partitions()]
    print(partitions)
    

if __name__ == '__main__':
    main()
