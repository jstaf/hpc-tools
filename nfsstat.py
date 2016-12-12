#!/usr/bin/env python
# use python2 for this one!!!! (solaris... sigh...)

import os
import sys
import re
import argparse
import subprocess
import numpy as np

def main():
    parser = argparse.ArgumentParser(description="Get disk usage on all nodes and sum it up by user")
    parser.add_argument('--nodelist', default='nodes.txt', type=str, help='List of nodes to check')
    parser.add_argument('--device', default=None, type=str, help='Check only usage on a specific device')
    argv = parser.parse_args()
    if not os.path.exists(argv.nodelist):
        sys.exit('Requires a list of nodes to check!')

    nodes = []
    with open(argv.nodelist) as nodelist:
        for line in nodelist:
            nodes.append(line.strip())

    all_stats = []
    for node in nodes:
        all_stats.extend(get_node_nfs(node))



def get_node_nfs(node):
    """
    Get and parse a node's NFS traffic.
    """
    ssh = subprocess.Popen(['ssh', node, '"/usr/sbin/nfsiostat"'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    nfsiostat = ssh.stdout.read().split('\n')    
    
    # list of dictionaries with nfs stats
    entries = []
    entry = {}
    for line in nfsiostat:
        if line == '':
            pass
        elif 'mounted on' in line:
            if not entry: # returns true if not empty
                entries.append(entry)
            entry = {}
            entry['device'] = line.split(':')[0]
            entry['user'] = line.split

    return entries
