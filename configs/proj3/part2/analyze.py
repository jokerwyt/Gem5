# configs/proj3/part2
# ├── analyze.py
# ├── m5out-2MM-CLOCK
# │   ├── config.ini
# │   ├── config.json
# │   └── stats.txt
# ├── m5out-2MM-LRU
# │   ├── config.ini
# │   ├── config.json
# │   └── stats.txt
# ├── m5out-2MM-MRU
# │   ├── config.ini
# │   ├── config.json
# │   └── stats.txt
# ├── m5out-2MM-RANDOM
# │   ├── config.ini
# │   ├── config.json
# │   └── stats.txt
# ├── m5out-BFS-CLOCK
# │   ├── config.ini
# │   ├── config.json
# │   └── stats.txt
# ├── m5out-BFS-LRU
# │   ├── config.ini
# │   ├── config.json
# │   └── stats.txt
# ├── m5out-BFS-MRU
# │   ├── config.ini
# │   ├── config.json
# │   └── stats.txt
# ├── m5out-BFS-RANDOM
# │   ├── config.ini
# │   ├── config.json
# │   └── stats.txt
# ├── m5out-bzip2-CLOCK
# │   ├── config.ini
# │   ├── config.json
# │   └── stats.txt
# ├── m5out-bzip2-LRU
# │   ├── config.ini
# │   ├── config.json
# │   └── stats.txt
# ├── m5out-bzip2-MRU
# │   ├── config.ini
# │   ├── config.json
# │   └── stats.txt
# ├── m5out-bzip2-RANDOM
# │   ├── config.ini
# │   ├── config.json
# │   └── stats.txt
# ├── m5out-mcf-CLOCK
# │   ├── config.ini
# │   ├── config.json
# │   └── stats.txt
# ├── m5out-mcf-LRU
# │   ├── config.ini
# │   ├── config.json
# │   └── stats.txt
# ├── m5out-mcf-MRU
# │   ├── config.ini
# │   ├── config.json
# │   └── stats.txt
# ├── m5out-mcf-RANDOM
# │   ├── config.ini
# │   ├── config.json
# │   └── stats.txt
# └── run.sh


# Here is analyze.py. Given the directory structure, collect the stats.txt files and print the IPCs and L1/L2 cache miss rate.
# and draw a bar chart to compare the IPCs and L1/L2 cache miss rate of different replacement policies.
#
# below show the format of stats.txt 
# for example, there are some lines in stats.txt like this:
# 
# system.cpu.ipc                               0.349378                       # IPC: instructions per cycle (core level) ((Count/Cycle))
# system.cpu.icache.overallHits::total       1000007966                       # number of overall hits (Count)
# system.cpu.icache.overallMisses::total            266                       # number of overall misses (Count)
# system.cpu.dcache.overallHits::total       1000007966                       # number of overall hits (Count)
# system.cpu.dcache.overallMisses::total            266                       # number of overall misses (Count)
#
#
# You need to:
# 1. extract the IPCs and L1/L2 cache miss rate (calculated by divide these two) from stats.txt
# draw a beautiful bar chart to compare the IPCs and L1/L2 cache miss rate of different replacement policies.

import os
import matplotlib.pyplot as plt
import numpy as np
import re

from collections import namedtuple


Statistic = namedtuple('Statistic', ['ipc', 'l1d_miss_rate', 'l1i_miss_rate', 'l2_miss_rate'])

def get_ipc_and_miss_rate(file_path) -> Statistic:
    with open(file_path, 'r') as f:
        content = f.read()
    ipc = re.findall(r'system.cpu.ipc\s+(\d+.\d+)', content)[0]
    l1i_miss_cnt = re.findall(r'system.cpu.icache.overallMisses::total\s+(\d+)', content)[0]
    l1d_miss_cnt = re.findall(r'system.cpu.dcache.overallMisses::total\s+(\d+)', content)[0]
    l1i_hit_cnt = re.findall(r'system.cpu.icache.overallHits::total\s+(\d+)', content)[0]
    l1d_hit_cnt = re.findall(r'system.cpu.dcache.overallHits::total\s+(\d+)', content)[0]

    l2_miss_cnt = re.findall(r'system.l2cache.overallMisses::total\s+(\d+)', content)[0]
    l2_hit_cnt = re.findall(r'system.l2cache.overallHits::total\s+(\d+)', content)[0]

    l1i_miss_rate = int(l1i_miss_cnt) / (int(l1i_miss_cnt) + int(l1i_hit_cnt))
    l1d_miss_rate = int(l1d_miss_cnt) / (int(l1d_miss_cnt) + int(l1d_hit_cnt))
    l2_miss_rate = int(l2_miss_cnt) / (int(l2_miss_cnt) + int(l2_hit_cnt))

    if 'bzip' in file_path or 'mcf' in file_path:
        print(file_path, 'l2_miss_cnt', l2_miss_cnt, 'l2_hit_cnt', l2_hit_cnt)
    return Statistic(ipc=float(ipc), l1d_miss_rate=l1d_miss_rate, l1i_miss_rate=l1i_miss_rate, l2_miss_rate=l2_miss_rate)


policy = ['CLOCK', 'LRU', 'MRU', 'RANDOM']
benchmarks = ['2MM', 'BFS', 'bzip2', 'mcf']

result = {}

for p in policy:
    for b in benchmarks:
        file_path = os.path.join('m5out-{}-{}'.format(b, p), 'stats.txt')
        result[(p, b)] = get_ipc_and_miss_rate(file_path)


# print(result)

# draw ipc bar chart
# put bars into pictures by iterating all (policy, benchmark) pairs
x = np.arange(len(benchmarks))
width = 0.2

fig, ax = plt.subplots()
rects = []
for i in range(len(policy)):
    rects.append(ax.bar(x + i * width, [result[(policy[i], b)].ipc for b in benchmarks], width, label=policy[i]))

ax.set_ylabel('IPC')
ax.set_title('IPC by benchmarks and replacement policy')
ax.set_xticks(x)
ax.set_xticklabels(benchmarks)
ax.legend()

fig.tight_layout()
# plt.show()

# save to file
fig.savefig('ipc.png')



# draw l1d miss rate bar chart

fig, ax = plt.subplots()
rects = []
for i in range(len(policy)):
    rects.append(ax.bar(x + i * width, [result[(policy[i], b)].l1d_miss_rate for b in benchmarks], width, label=policy[i]))

ax.set_ylabel('L1D Miss Rate')
ax.set_title('L1D Miss Rate by benchmarks and replacement policy')
ax.set_xticks(x)
ax.set_xticklabels(benchmarks)
ax.legend()

fig.tight_layout()
# plt.show()

fig.savefig('l1d_miss_rate.png')

# draw l1i miss rate bar chart

fig, ax = plt.subplots()
rects = []
for i in range(len(policy)):
    rects.append(ax.bar(x + i * width, [result[(policy[i], b)].l1i_miss_rate for b in benchmarks], width, label=policy[i]))

ax.set_ylabel('L1I Miss Rate')
ax.set_title('L1I Miss Rate by benchmarks and replacement policy')
ax.set_xticks(x)
ax.set_xticklabels(benchmarks)
ax.legend()

fig.tight_layout()
# plt.show()

fig.savefig('l1i_miss_rate.png')


# draw l2 miss rate bar chart

fig, ax = plt.subplots()
rects = []
for i in range(len(policy)):
    rects.append(ax.bar(x + i * width, [result[(policy[i], b)].l2_miss_rate for b in benchmarks], width, label=policy[i]))

ax.set_ylabel('L2 Miss Rate')
ax.set_title('L2 Miss Rate by benchmarks and replacement policy')
ax.set_xticks(x)
ax.set_xticklabels(benchmarks)
ax.legend()

fig.tight_layout()
# plt.show()

fig.savefig('l2_miss_rate.png')