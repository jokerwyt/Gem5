#!/bin/bash

# # ./build/ARM/gem5.opt --outdir=m5out-lab2.1-2MM_base \
# #     configs/proj2/two-level.py --workload='test_bench/2MM/2mm_base' &

# # ./build/ARM/gem5.opt --outdir=m5out-lab2.1-BFS \
# #     configs/proj2/two-level.py --workload='test_bench/BFS/bfs -f test_bench/BFS/USA-road-d.NY.gr' &


# # use “--local”, “--tournament”, “--bimode" for this two workload
# # construct a list with all possible branch predictor
branch_predictor=(--local --tournament --bimode)

# #foreach the list
# for predictor in ${branch_predictor[@]}; do
#     echo "Running benchmarks with branch predictor: $predictor"
#     ./build/ARM/gem5.opt --outdir=m5out-lab2.1-2MM_base-$predictor \
#         configs/proj2/two-level.py --workload='test_bench/2MM/2mm_base' $predictor &

#     ./build/ARM/gem5.opt --outdir=m5out-lab2.1-BFS-$predictor \
#         configs/proj2/two-level.py --workload='test_bench/BFS/bfs -f test_bench/BFS/USA-road-d.NY.gr' $predictor &
# done

### part 1.2

### use different btb size
# construct a list with all possible btb size
btb_size=(64 512 4096 32768 262144)

# for all branch predictor, use all btb size to run a benchmark
# for predictor in ${branch_predictor[@]}; do
#     for size in ${btb_size[@]}; do
#         echo "Running benchmarks with branch predictor: $predictor and btb size: $size"
#         ./build/ARM/gem5.opt --outdir=m5out-lab2.2-2MM_base-$predictor-btb-$size \
#             configs/proj2/two-level.py --workload='test_bench/2MM/2mm_base' $predictor --btbentry=$size &

#         ./build/ARM/gem5.opt --outdir=m5out-lab2.2-BFS-$predictor-btb-$size \
#             configs/proj2/two-level.py --workload='test_bench/BFS/bfs -f test_bench/BFS/USA-road-d.NY.gr' $predictor --btbentry=$size &
#     done
# done


### part 1.3
### use different ras size
# construct a list with all possible ras size
ras_size=(4 16 64 512 4096)

# for all branch predictor, use all ras size to run a benchmark
# for predictor in ${branch_predictor[@]}; do
#     for size in ${ras_size[@]}; do
#         echo "Running benchmarks with branch predictor: $predictor and ras size: $size"
#         ./build/ARM/gem5.opt --outdir=m5out-lab2.3-2MM_base-$predictor-ras-$size \
#             configs/proj2/two-level.py --workload='test_bench/2MM/2mm_base' $predictor --ras=$size &

#         ./build/ARM/gem5.opt --outdir=m5out-lab2.3-BFS-$predictor-ras-$size \
#             configs/proj2/two-level.py --workload='test_bench/BFS/bfs -f test_bench/BFS/USA-road-d.NY.gr' $predictor --ras=$size &
#     done
# done

### part 1.4
### use different localsize
# construct a list with all possible localsize
localsize=(32 256 2048 16384 131072)

# for only local branch predictor, use all localsize to run a benchmark
for size in ${localsize[@]}; do
    echo "Running benchmarks with branch predictor: --local and local size: $size"
    # ./build/ARM/gem5.opt --outdir=m5out-lab2.4-2MM_base-local-$size \
    #     configs/proj2/two-level.py --workload='test_bench/2MM/2mm_base' --local --localsize=$size &

    ./build/ARM/gem5.opt --outdir=m5out-lab2.4-BFS-local-$size \
        configs/proj2/two-level.py --workload='test_bench/BFS/bfs -f test_bench/BFS/USA-road-d.NY.gr' --local --localsize=$size &
done
wait
