#!/bin/bash

# ./build/ARM/gem5.opt --outdir=m5out-lab2.1-2MM_base \
#     configs/proj2/two-level.py --workload='test_bench/2MM/2mm_base' &

# ./build/ARM/gem5.opt --outdir=m5out-lab2.1-BFS \
#     configs/proj2/two-level.py --workload='test_bench/BFS/bfs -f test_bench/BFS/USA-road-d.NY.gr' &


# use “--local”, “--tournament”, “--bimode" for this two workload
# construct a list with all possible branch predictor
branch_predictor=(--local --tournament --bimode)

#foreach the list
for predictor in ${branch_predictor[@]}; do
    echo "Running benchmarks with branch predictor: $predictor"
    ./build/ARM/gem5.opt --outdir=m5out-lab2.1-2MM_base-$predictor \
        configs/proj2/two-level.py --workload='test_bench/2MM/2mm_base' $predictor &

    ./build/ARM/gem5.opt --outdir=m5out-lab2.1-BFS-$predictor \
        configs/proj2/two-level.py --workload='test_bench/BFS/bfs -f test_bench/BFS/USA-road-d.NY.gr' $predictor &
done


wait
