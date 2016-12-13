#!/usr/bin/env python
# use python2 for this one!!!! (solaris... sigh...)

import os
import sys
import re
import argparse
import subprocess
import csv

def main():
    parser = argparse.ArgumentParser(description="Get disk usage on all nodes and sum it up by user")
    parser.add_argument('--nodelist', default='nodes.txt', type=str, help='List of nodes to check')
    argv = parser.parse_args()
    if not os.path.exists(argv.nodelist):
        sys.exit('Requires a list of nodes to check!')

    # get node names
    nodes = []
    with open(argv.nodelist) as nodelist:
        for line in nodelist:
            nodes.append(line.strip())

    # get stats for nfs traffic
    all_stats = []
    for node in nodes:
        traffic = get_node_nfs(node)
        all_stats.append(concat_nfs_entry(node, traffic))

    # write to csv
    with open('nfs.csv', 'w') as out:
        csvwrite = csv.writer(out)
        csvwrite.writerow(['node', 'device', 'user', 
            'rOps_s', 'rkB_s', 'rkB_op', 'rretrans', 'ravgRTT_ms', 'ravgexe_ms',
            'wOps_s', 'wkB_s', 'wkB_op', 'wretrans', 'wavgRTT_ms', 'wavgexe_ms'])
        csvwrite.writerows(all_stats)


def get_node_nfs(node):
    """
    Get and parse a node's NFS traffic.
    """
    ssh = subprocess.Popen(['ssh', node, '-o ConnectTimeout=3 "/usr/sbin/nfsiostat"'], 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    nfsiostat = ssh.stdout.read().split('\n')

    # list of dictionaries with nfs stats
    entries = []
    entry = {}
    nextline = ''
    for line in nfsiostat:
        if 'mounted on' in line:
            if entry: # returns true if not empty
                # add last entry
                entries.append(entry)
            entry = {}
            entry['device'] = line.split(':')[0]
            entry['user'] = re.findall('/(\w+):', line)[0]
        elif 'read:' in line:
            nextline = 'read'
        elif 'write:' in line:
            nextline = 'write'
        elif nextline != '':
            # ops/s, kB/s, kB/op, retrans, avg RTT (ms), avg exe (ms)
            entry[nextline] = re.findall('[0-9]+\.*[0-9]*', line)
            nextline = ''
    return entries


def concat_nfs_entry(node, entries):
    """
    Parse apart NFS entries into something interpretable 
    """
    outlist = []
    for entry in entries:
        outlist.append([node, entry['device'], entry['user']] + entry['read'] + entry['write'])
    return outlist

if __name__ == '__main__':
    main()
