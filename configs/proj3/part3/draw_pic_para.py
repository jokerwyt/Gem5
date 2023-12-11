# 4. Try to modify the parameters of your PPF, like the threshold used in inferencing. Show the impact of these parameters on the performance, prefetcher accuracy, and prefetcher coverage. For simplicity, 3~5 values for each parameter are enough. The reasons for the changes in these statistics are required to be explained.
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
#
#.
# ├── para
# │   ├── m5out-2MM-PPF-threshold-16
# │   │   ├── config.ini
# │   │   ├── config.json
# │   │   └── stats.txt
# │   ├── m5out-2MM-PPF-threshold-24
# │   │   ├── config.ini
# │   │   ├── config.json
# │   │   └── stats.txt
# │   ├── m5out-2MM-PPF-threshold-32
# │   │   ├── config.ini
# │   │   ├── config.json
# │   │   └── stats.txt
# │   ├── m5out-2MM-PPF-threshold-40
# │   │   ├── config.ini
# │   │   ├── config.json
# │   │   └── stats.txt
# │   ├── m5out-2MM-PPF-threshold-8
# │   │   ├── config.ini
# │   │   ├── config.json
# │   │   └── stats.txt
# │   ├── m5out-BFS-PPF-threshold-16
# │   │   ├── config.ini
# │   │   ├── config.json
# │   │   └── stats.txt
# │   ├── m5out-BFS-PPF-threshold-24
# │   │   ├── config.ini
# │   │   ├── config.json
# │   │   └── stats.txt
# │   ├── m5out-BFS-PPF-threshold-32
# │   │   ├── config.ini
# │   │   ├── config.json
# │   │   └── stats.txt
# │   ├── m5out-BFS-PPF-threshold-40
# │   │   ├── config.ini
# │   │   ├── config.json
# │   │   └── stats.txt
# │   ├── m5out-BFS-PPF-threshold-8
# │   │   ├── config.ini
# │   │   ├── config.json
# │   │   └── stats.txt
# │   ├── m5out-bzip2-PPF-threshold-16
# │   │   ├── config.ini
# │   │   ├── config.json
# │   │   └── stats.txt
# │   ├── m5out-bzip2-PPF-threshold-24
# │   │   ├── config.ini
# │   │   ├── config.json
# │   │   └── stats.txt
# │   ├── m5out-bzip2-PPF-threshold-32
# │   │   ├── config.ini
# │   │   ├── config.json
# │   │   └── stats.txt
# │   ├── m5out-bzip2-PPF-threshold-40
# │   │   ├── config.ini
# │   │   ├── config.json
# │   │   └── stats.txt
# │   ├── m5out-bzip2-PPF-threshold-8
# │   │   ├── config.ini
# │   │   ├── config.json
# │   │   └── stats.txt
# │   ├── m5out-mcf-PPF-threshold-16
# │   │   ├── config.ini
# │   │   ├── config.json
# │   │   └── stats.txt
# │   ├── m5out-mcf-PPF-threshold-24
# │   │   ├── config.ini
# │   │   ├── config.json
# │   │   └── stats.txt
# │   ├── m5out-mcf-PPF-threshold-32
# │   │   ├── config.ini
# │   │   ├── config.json
# │   │   └── stats.txt
# │   ├── m5out-mcf-PPF-threshold-40
# │   │   ├── config.ini
# │   │   ├── config.json
# │   │   └── stats.txt
# │   └── m5out-mcf-PPF-threshold-8
# │       ├── config.ini
# │       ├── config.json
# │       └── stats.txt
# ├── run_diff_args.sh
# └── two-level.py
#
#
# This script focus on para/ directory. It should fecth those performance factors and draw 
# bar chart for each factor, demonstrating the impact of different thresholds.
# The location of this script is configs/proj3/part3/draw_pic_para.py

import os
import matplotlib.pyplot as plt
import numpy as np

def get_ipc(path):
    """ get IPC from one stats.txt file """
    with open(os.path.join(path, "stats.txt"), "r") as f:
        content = f.readlines()
        for line in content:
            if line.startswith("system.cpu.ipc"):
                return float(line.split()[1])


def get_hit_rate(path):
    """ get hit rate from one stats.txt file """
    with open(os.path.join(path, "stats.txt"), "r") as f:
        content = f.readlines()
        for line in content:
            if line.startswith("system.l2cache.overallHits::total"):
                hit = float(line.split()[1])
            elif line.startswith("system.l2cache.overallMisses::total"):
                miss = float(line.split()[1])
        return hit / (hit + miss)

def get_accuracy(path):
    """ get prefetcher accuracy from one stats.txt file """
    with open(os.path.join(path, "stats.txt"), "r") as f:
        content = f.readlines()
        for line in content:
            if line.startswith("system.l2cache.prefetcher.accuracy"):
                return float(line.split()[1])

def get_coverage(path):
    """ get prefetcher coverage from one stats.txt file """
    with open(os.path.join(path, "stats.txt"), "r") as f:
        content = f.readlines()
        for line in content:
            if line.startswith("system.l2cache.prefetcher.coverage"):
                return float(line.split()[1])
            
# parse the directory to get all listed threshold

threshold = []
for root, dirs, files in os.walk("para"):
    for dir in dirs:
        # if there is a "threshold" in the dir name
        if "threshold" in dir:
            threshold.append(dir.split("-")[-1])

# drop all duplicate elements and sort it as integer
threshold = sorted(list(set(threshold)), key=lambda x: int(x))

workload = ['2MM', 'BFS', 'bzip2', 'mcf']


# let focus on IPC first
# I want a bar chart with four groups (each for a workload),
# each group has five bars (each for a threshold)
# and save it to '000threshold_IPC.png'

fig, ax = plt.subplots()
index = np.arange(len(threshold))
bar_width = 0.15
opacity = 0.8

for i in range(len(workload)):
    ipc = []
    for j in range(len(threshold)):
        ipc.append(get_ipc(os.path.join("para", "m5out-" + workload[i] + "-PPF-threshold-" + threshold[j])))
    rects = ax.bar(index + i * bar_width, ipc, bar_width, alpha=opacity, label=workload[i])

ax.set_xlabel("Threshold")
ax.set_ylabel("IPC")
ax.set_title("IPC with different threshold")
ax.set_xticks(index + bar_width)
ax.set_xticklabels(threshold)
ax.legend()
plt.tight_layout()
plt.savefig("000threshold_IPC.png")
plt.close()

# then let focus on hit rate
# I want a bar chart with four groups (each for a workload),
# each group has five bars (each for a threshold)
# and save it to '001threshold_hit_rate.png'

fig, ax = plt.subplots()
index = np.arange(len(threshold))
bar_width = 0.15
opacity = 0.8

for i in range(len(workload)):
    hit_rate = []
    for j in range(len(threshold)):
        hit_rate.append(get_hit_rate(os.path.join("para", "m5out-" + workload[i] + "-PPF-threshold-" + threshold[j])))
    rects = ax.bar(index + i * bar_width, hit_rate, bar_width, alpha=opacity, label=workload[i])

ax.set_xlabel("Threshold")
ax.set_ylabel("Hit rate")
ax.set_title("Hit rate with different threshold")
ax.set_xticks(index + bar_width)
ax.set_xticklabels(threshold)
ax.legend()
plt.tight_layout()
plt.savefig("000threshold_hit_rate.png")
plt.close()

# then let focus on accuracy
# I want a bar chart with four groups (each for a workload),
# each group has five bars (each for a threshold)
# and save it to '002threshold_accuracy.png'

fig, ax = plt.subplots()
index = np.arange(len(threshold))
bar_width = 0.15
opacity = 0.8

for i in range(len(workload)):
    accuracy = []
    for j in range(len(threshold)):
        accuracy.append(get_accuracy(os.path.join("para", "m5out-" + workload[i] + "-PPF-threshold-" + threshold[j])))
    rects = ax.bar(index + i * bar_width, accuracy, bar_width, alpha=opacity, label=workload[i])

ax.set_xlabel("Threshold")
ax.set_ylabel("Accuracy")
ax.set_title("Accuracy with different threshold")
ax.set_xticks(index + bar_width)
ax.set_xticklabels(threshold)
ax.legend()
plt.tight_layout()
plt.savefig("000threshold_accuracy.png")
plt.close()

# then let focus on coverage
# I want a bar chart with four groups (each for a workload),
# each group has five bars (each for a threshold)
# and save it to '003threshold_coverage.png'

fig, ax = plt.subplots()
index = np.arange(len(threshold))
bar_width = 0.15
opacity = 0.8

for i in range(len(workload)):
    coverage = []
    for j in range(len(threshold)):
        coverage.append(get_coverage(os.path.join("para", "m5out-" + workload[i] + "-PPF-threshold-" + threshold[j])))
    rects = ax.bar(index + i * bar_width, coverage, bar_width, alpha=opacity, label=workload[i])

ax.set_xlabel("Threshold")
ax.set_ylabel("Coverage")
ax.set_title("Coverage with different threshold")
ax.set_xticks(index + bar_width)
ax.set_xticklabels(threshold)
ax.legend()
plt.tight_layout()
plt.savefig("000threshold_coverage.png")
plt.close()