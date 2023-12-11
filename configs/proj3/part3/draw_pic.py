# 3. Show the performance of your prefetch filter on the workloads listed in Appendix B. Specifically, compare the performance (e.g., IPC) with and without your perfetch fileter. And compare the hit rate of L2-cache, the prefetcher accuracy (i.e., prefetcher.accuracy), and the prefetcher coverage (i.e., prefetcher.coverage). Additional statistics are acceptable if you feel they are useful.
# This script is draw_pic.py
# The filesystem structure 
# 
# pub25@Node5:~/gem5$ tree configs/proj3/part3/
# configs/proj3/part3/
# ├── draw_pic.py
# ├── m5out-2MM-PPF
# │   ├── config.ini
# │   ├── config.json
# │   └── stats.txt
# ├── m5out-2MM-SPPV2
# │   ├── config.ini
# │   ├── config.json
# │   └── stats.txt
# ├── m5out-BFS-PPF
# │   ├── config.ini
# │   ├── config.json
# │   └── stats.txt
# ├── m5out-BFS-SPPV2
# │   ├── config.ini
# │   ├── config.json
# │   └── stats.txt
# ├── m5out-bzip2-PPF
# │   ├── config.ini
# │   ├── config.json
# │   └── stats.txt
# ├── m5out-bzip2-SPPV2
# │   ├── config.ini
# │   ├── config.json
# │   └── stats.txt
# ├── m5out-mcf-PPF
# │   ├── config.ini
# │   ├── config.json
# │   └── stats.txt
# ├── m5out-mcf-SPPV2
# │   ├── config.ini
# │   ├── config.json
# │   └── stats.txt
# ├── new_cache.py
# ├── __pycache__
# │   └── new_cache.cpython-310.pyc
# ├── run_PPFvsSPPV2.sh
# └── two-level.py
#
#
#
# This script is used to collect
# 1. IPC
# 2. hit rate of L2-cache
# 3. prefetcher accuracy
# 4. prefetcher coverage
# and draw them into four picture.
#
# * IPC lies in the stats.txt file like this:
# system.cpu.ipc                               0.311506                       # IPC: instructions per cycle (core level) ((Count/Cycle))
#
# * hit rate needs to use hit count to divide access count (i.e. hit + miss)
# system.l2cache.overallHits::total              440912                       # number of overall hits (Count)
# system.l2cache.overallMisses::total             42222                       # number of overall misses (Count)
#
# * prefetcher accuracy lies in the stats.txt file like this:
# system.l2cache.prefetcher.accuracy           0.950467                       # accuracy of the prefetcher (Count)
#
# * prefetcher coverage lies in the stats.txt file like this:
# system.l2cache.prefetcher.coverage           0.578101                       # coverage brought by this prefetcher (Count)
# 
# from one stats.txt file, we can fetch a four-tuple (IPC, L2 hit rate, prefetcher accuracy, prefetcher coverage) 


import matplotlib.pyplot as plt
import numpy as np
import os
import re

# get the IPC of the two-level cache
def get_IPC(file_name):
    IPC = []
    with open(file_name, 'r') as f:
        for line in f.readlines():
            if 'system.cpu.commitStats0.ipc' in line:
                IPC.append(float(line.split()[1]))
    return IPC

# get the hit rate of the two-level cache
# * hit rate needs to use hit count to divide access count (i.e. hit + miss)
# system.l2cache.overallHits::total              440912                       # number of overall hits (Count)
# system.l2cache.overallMisses::total             42222                       # number of overall misses (Count)
def get_hit_rate(file_name):
    hit_rate = []
    hit = None
    miss = None
    with open(file_name, 'r') as f:
        for line in f.readlines():
            if 'system.l2cache.overallHits::total' in line:
                hit = int(line.split()[1])
            if 'system.l2cache.overallMisses::total' in line:
                miss = int(line.split()[1])
    assert hit != None and miss != None
    hit_rate.append(hit / (hit + miss))
    return hit_rate

# get the accuracy of the prefetcher
def get_accuracy(file_name):
    accuracy = []
    with open(file_name, 'r') as f:
        for line in f.readlines():
            if 'system.l2cache.prefetcher.accuracy' in line:
                accuracy.append(float(line.split()[1]))
    return accuracy

# get the coverage of the prefetcher
def get_coverage(file_name):
    coverage = []
    with open(file_name, 'r') as f:
        for line in f.readlines():
            if 'system.l2cache.prefetcher.coverage' in line:
                coverage.append(float(line.split()[1]))
    return coverage

# get root path of the project
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# get the IPC of the two-level cache
IPC_2MM_PPF = get_IPC(f'{root_path}/configs/proj3/part3/m5out-2MM-PPF/stats.txt')
IPC_2MM_SPPV2 = get_IPC(f'{root_path}/configs/proj3/part3/m5out-2MM-SPPV2/stats.txt')
IPC_BFS_PPF = get_IPC(f'{root_path}/configs/proj3/part3/m5out-BFS-PPF/stats.txt')
IPC_BFS_SPPV2 = get_IPC(f'{root_path}/configs/proj3/part3/m5out-BFS-SPPV2/stats.txt')
IPC_bzip2_PPF = get_IPC(f'{root_path}/configs/proj3/part3/m5out-bzip2-PPF/stats.txt')
IPC_bzip2_SPPV2 = get_IPC(f'{root_path}/configs/proj3/part3/m5out-bzip2-SPPV2/stats.txt')
IPC_mcf_PPF = get_IPC(f'{root_path}/configs/proj3/part3/m5out-mcf-PPF/stats.txt')
IPC_mcf_SPPV2 = get_IPC(f'{root_path}/configs/proj3/part3/m5out-mcf-SPPV2/stats.txt')

# get the hit rate of the two-level cache
hit_rate_2MM_PPF = get_hit_rate(f'{root_path}/configs/proj3/part3/m5out-2MM-PPF/stats.txt')
hit_rate_2MM_SPPV2 = get_hit_rate(f'{root_path}/configs/proj3/part3/m5out-2MM-SPPV2/stats.txt')
hit_rate_BFS_PPF = get_hit_rate(f'{root_path}/configs/proj3/part3/m5out-BFS-PPF/stats.txt')
hit_rate_BFS_SPPV2 = get_hit_rate(f'{root_path}/configs/proj3/part3/m5out-BFS-SPPV2/stats.txt')
hit_rate_bzip2_PPF = get_hit_rate(f'{root_path}/configs/proj3/part3/m5out-bzip2-PPF/stats.txt')
hit_rate_bzip2_SPPV2 = get_hit_rate(f'{root_path}/configs/proj3/part3/m5out-bzip2-SPPV2/stats.txt')
hit_rate_mcf_PPF = get_hit_rate(f'{root_path}/configs/proj3/part3/m5out-mcf-PPF/stats.txt')
hit_rate_mcf_SPPV2 = get_hit_rate(f'{root_path}/configs/proj3/part3/m5out-mcf-SPPV2/stats.txt')

# get the accuracy of the prefetcher
accuracy_2MM_PPF = get_accuracy(f'{root_path}/configs/proj3/part3/m5out-2MM-PPF/stats.txt')
accuracy_2MM_SPPV2 = get_accuracy(f'{root_path}/configs/proj3/part3/m5out-2MM-SPPV2/stats.txt')
accuracy_BFS_PPF = get_accuracy(f'{root_path}/configs/proj3/part3/m5out-BFS-PPF/stats.txt')
accuracy_BFS_SPPV2 = get_accuracy(f'{root_path}/configs/proj3/part3/m5out-BFS-SPPV2/stats.txt')
accuracy_bzip2_PPF = get_accuracy(f'{root_path}/configs/proj3/part3/m5out-bzip2-PPF/stats.txt')
accuracy_bzip2_SPPV2 = get_accuracy(f'{root_path}/configs/proj3/part3/m5out-bzip2-SPPV2/stats.txt')
accuracy_mcf_PPF = get_accuracy(f'{root_path}/configs/proj3/part3/m5out-mcf-PPF/stats.txt')
accuracy_mcf_SPPV2 = get_accuracy(f'{root_path}/configs/proj3/part3/m5out-mcf-SPPV2/stats.txt')

# get the coverage of the prefetcher
coverage_2MM_PPF = get_coverage(f'{root_path}/configs/proj3/part3/m5out-2MM-PPF/stats.txt')
coverage_2MM_SPPV2 = get_coverage(f'{root_path}/configs/proj3/part3/m5out-2MM-SPPV2/stats.txt')
coverage_BFS_PPF = get_coverage(f'{root_path}/configs/proj3/part3/m5out-BFS-PPF/stats.txt')
coverage_BFS_SPPV2 = get_coverage(f'{root_path}/configs/proj3/part3/m5out-BFS-SPPV2/stats.txt')
coverage_bzip2_PPF = get_coverage(f'{root_path}/configs/proj3/part3/m5out-bzip2-PPF/stats.txt')
coverage_bzip2_SPPV2 = get_coverage(f'{root_path}/configs/proj3/part3/m5out-bzip2-SPPV2/stats.txt')
coverage_mcf_PPF = get_coverage(f'{root_path}/configs/proj3/part3/m5out-mcf-PPF/stats.txt')
coverage_mcf_SPPV2 = get_coverage(f'{root_path}/configs/proj3/part3/m5out-mcf-SPPV2/stats.txt')

# draw the IPC bar chart, put four workloads and two prefetcher together
labels = ['2MM', 'BFS', 'bzip2', 'mcf']
PPF = [IPC_2MM_PPF[-1], IPC_BFS_PPF[-1], IPC_bzip2_PPF[-1], IPC_mcf_PPF[-1]]
SPPV2 = [IPC_2MM_SPPV2[-1], IPC_BFS_SPPV2[-1], IPC_bzip2_SPPV2[-1], IPC_mcf_SPPV2[-1]]
width = 0.35
x = np.arange(len(labels))
fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, PPF, width, label='PPF')
rects2 = ax.bar(x + width/2, SPPV2, width, label='SPPV2')
ax.set_ylabel('IPC')
ax.set_title('IPC of four workloads')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
plt.savefig('000IPC.png')


# good job! generate hit rate, accuracy and coverage bar chart
labels = ['2MM', 'BFS', 'bzip2', 'mcf']
PPF = [hit_rate_2MM_PPF[-1], hit_rate_BFS_PPF[-1], hit_rate_bzip2_PPF[-1], hit_rate_mcf_PPF[-1]]
SPPV2 = [hit_rate_2MM_SPPV2[-1], hit_rate_BFS_SPPV2[-1], hit_rate_bzip2_SPPV2[-1], hit_rate_mcf_SPPV2[-1]]
width = 0.35
x = np.arange(len(labels))
fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, PPF, width, label='PPF')
rects2 = ax.bar(x + width/2, SPPV2, width, label='SPPV2')
ax.set_ylabel('L2 Hit rate')
ax.set_title('L2 Hit rate of four workloads')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
plt.savefig('000Hit_rate.png')

labels = ['2MM', 'BFS', 'bzip2', 'mcf']
PPF = [accuracy_2MM_PPF[-1], accuracy_BFS_PPF[-1], accuracy_bzip2_PPF[-1], accuracy_mcf_PPF[-1]]
SPPV2 = [accuracy_2MM_SPPV2[-1], accuracy_BFS_SPPV2[-1], accuracy_bzip2_SPPV2[-1], accuracy_mcf_SPPV2[-1]]
width = 0.35
x = np.arange(len(labels))
fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, PPF, width, label='PPF')
rects2 = ax.bar(x + width/2, SPPV2, width, label='SPPV2')
ax.set_ylabel('Accuracy')
ax.set_title('Accuracy of four workloads')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
plt.savefig('000Accuracy.png')

labels = ['2MM', 'BFS', 'bzip2', 'mcf']
PPF = [coverage_2MM_PPF[-1], coverage_BFS_PPF[-1], coverage_bzip2_PPF[-1], coverage_mcf_PPF[-1]]
SPPV2 = [coverage_2MM_SPPV2[-1], coverage_BFS_SPPV2[-1], coverage_bzip2_SPPV2[-1], coverage_mcf_SPPV2[-1]]
width = 0.35
x = np.arange(len(labels))
fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, PPF, width, label='PPF')
rects2 = ax.bar(x + width/2, SPPV2, width, label='SPPV2')
ax.set_ylabel('Coverage')
ax.set_title('Coverage of four workloads')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
plt.savefig('000Coverage.png')