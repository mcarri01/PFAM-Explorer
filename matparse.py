#!/usr/bin/python3

import numpy as np
import re
import sys
import argparse
from scipy.sparse import csgraph


def processMatrix(matrix, threshold):
    threshold = threshold / 100
    size = len(matrix)
    for i in range(0, size):
        for j in range(i+1, size):
            if matrix[i, j] < threshold:
                matrix[i, j] = 0
                matrix[j, i] = 0
    n = csgraph.connected_components(matrix, directed=False)[0]
    return n


p = argparse.ArgumentParser()
p.add_argument('thresholds', metavar='N', type=float, nargs='*', help='''\
        Calculates number of connected components in results output with\
        values cut off to 0 at each of these threshold percentages.''')
args = p.parse_args()
if len(args.thresholds) == 0:
    args.thresholds = [0]
args.thresholds = sorted(args.thresholds)

matpat = '>(.+)\n([^>]+)'
content = sys.stdin.read()
i = 0

outputstr = '['
for m in re.findall(matpat, content):
    header = m[0].rstrip().split()
    matrix = m[1].split('\n')[0:-1]
    matrix = [[float(entry) for entry in row.strip().split(' ')] for row in matrix]
    matrix = np.array(matrix)
    output = '{"family" : "' +  header[0] + '", '
    size, pannot, minlen, maxlen, diff = header[1:]
    output += '"connected_components" : {'
    n = len(args.thresholds)
    for i in range(0, n):
        t = args.thresholds[i]
        output += '"{0}" : "{1}"'.format(t, processMatrix(matrix, t))
        if i + 1 != n:
            output += ", "
        else:
            output += "}, "
    output += '"familysize" : "{0}"'.format(size) + '},'
    outputstr += output    
outputstr = outputstr[:-1]
outputstr += ']'
print(outputstr)
