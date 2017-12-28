#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from collections import Counter

def get_dependences(jsfilename):
    deps = []
    try:
        with open(jsfilename, 'r') as f:
            lines = f.readlines()
            for l in lines:
                if l.find('//') == 0:
                    l = l[2:].strip()
                    if l.find('BOND!') == 0:
                        filename = l[5:].strip()
                        deps.append(filename)
                        deps.extend(get_dependences(filename))
    except IOError:
        pass
    
    return deps


result = []
argvs = sys.argv
argc = len(argvs)
deps = []

for i in xrange(1, argc):
    deps.extend(get_dependences(argvs[i]))
    deps.append(argvs[i])

# print deps
# deps = list(set(deps))

counter = Counter(deps)
sorted_list = sorted(counter.items(), key=lambda x: x[1], reverse=True)
for l in sorted_list:
    result.append('<script src="%s"></script>' % l[0])
    

# for dep in deps[::-1]:
#     result.append('<script src="%s"></script>' % dep)


with open('bond.js', 'w') as f:
    for r in result:
        f.write('document.write(`%s`);\n' % r)
