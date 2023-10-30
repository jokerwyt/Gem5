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

# parser.add_option('--perceptron', action="store_true")
# parser.add_option('--globallen', type="int", default=30)
# parser.add_option('--threshold', type="int", default=63)
# parser.add_option('--perceptronnum', type="int", default=1024)

# change this three arguments for 5 different values

perceptronnum=(1024 2048 4096 8192 16384)
globallen=(1 5 10 30 60)
threshold=(5 20 63 100 200)

# foreach the three list, respectively
for i in ${perceptronnum[@]}; do
    echo "Running benchmarks with perceptronnum: $i, globallen: $j, threshold: $k"
    ./build/ARM/gem5.opt --outdir=m5out-lab2-part3-2MM_base-pernum-$i \
        configs/proj2/two-level.py --workload='test_bench/2MM/2mm_base' --perceptron --perceptronnum=$i &

    ./build/ARM/gem5.opt --outdir=m5out-lab2-part3-BFS-pernum-$i \
        configs/proj2/two-level.py --workload='test_bench/BFS/bfs -f test_bench/BFS/USA-road-d.NY.gr' --perceptron --perceptronnum=$i &
done

for j in ${globallen[@]}; do
    echo "Running benchmarks with perceptronnum: $i, globallen: $j, threshold: $k"
    ./build/ARM/gem5.opt --outdir=m5out-lab2-part3-2MM_base-globallen-$j \
        configs/proj2/two-level.py --workload='test_bench/2MM/2mm_base' --perceptron --globallen=$j &

    ./build/ARM/gem5.opt --outdir=m5out-lab2-part3-BFS-globallen-$j \
        configs/proj2/two-level.py --workload='test_bench/BFS/bfs -f test_bench/BFS/USA-road-d.NY.gr' --perceptron --globallen=$j &
done

for k in ${threshold[@]}; do
    echo "Running benchmarks with perceptronnum: $i, globallen: $j, threshold: $k"
    ./build/ARM/gem5.opt --outdir=m5out-lab2-part3-2MM_base-threshold-$k \
        configs/proj2/two-level.py --workload='test_bench/2MM/2mm_base' --perceptron --threshold=$k &

    ./build/ARM/gem5.opt --outdir=m5out-lab2-part3-BFS-threshold-$k \
        configs/proj2/two-level.py --workload='test_bench/BFS/bfs -f test_bench/BFS/USA-road-d.NY.gr' --perceptron --threshold=$k &
done


wait