#!/bin/bash


# for predictor in ${branch_predictor[@]}; do
#     echo "Running benchmarks with branch predictor: $predictor"
#     ./build/ARM/gem5.opt --outdir=m5out-lab2.1-2MM_base-$predictor \
#         configs/proj2/two-level.py --workload='test_bench/2MM/2mm_base' $predictor &

#     ./build/ARM/gem5.opt --outdir=m5out-lab2.1-BFS-$predictor \
#         configs/proj2/two-level.py --workload='test_bench/BFS/bfs -f test_bench/BFS/USA-road-d.NY.gr' $predictor &
# done

# Run the 2MM and BFS workloads with the simple BP and at least two other BPs 
# provided by Gem5 (like tournament BP or local BP). 
# Compare the performance of these BPs using the statistics in stats.txt.

# use “--alwaystake", “--tournament”, “--bimode" for this two workload

# make a list
branch_predictor=(stdperceptron8k stdperceptron64k)

#foreach the list
for predictor in ${branch_predictor[@]}; do
    echo "Running benchmarks with branch predictor: $predictor"
    ./build/ARM/gem5.opt --outdir=m5out-lab2-part3-addtive-2MM_base-$predictor \
        configs/proj2/two-level.py --workload='test_bench/2MM/2mm_base' --$predictor &

    ./build/ARM/gem5.opt --outdir=m5out-lab2-part3-addtive-BFS-$predictor \
        configs/proj2/two-level.py --workload='test_bench/BFS/bfs -f test_bench/BFS/USA-road-d.NY.gr' --$predictor &
done

wait