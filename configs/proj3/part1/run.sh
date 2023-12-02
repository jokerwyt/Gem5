#!/bin/bash

./build/ARM/gem5.opt --outdir='configs/proj3/part1/m5-out-three-level' configs/proj3/part1/three-level.py --workload='tests/test-progs/hello/bin/arm/linux/hello' 
./build/ARM/gem5.opt --outdir='configs/proj3/part1/m5-out-two-level-unified-L1' configs/proj3/part1/two-level-unified-L1.py --workload='tests/test-progs/hello/bin/arm/linux/hello' 
./build/ARM/gem5.opt --outdir='configs/proj3/part1/m5-out-two-level-seperate-L2' configs/proj3/part1/two-level-seperate-L2.py --workload='tests/test-progs/hello/bin/arm/linux/hello' 
