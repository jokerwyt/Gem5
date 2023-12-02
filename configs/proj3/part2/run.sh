#!/bin/bash
# You are required to implement ClockRP in Gem5. To verify your correct implementation, you need to compare the performance of your implementation with other replacement policies implemented in Gem5 such as random, LRU, and MRU. We provide four different workloads for this experiment in the project #1 package. Please do Gem5 simulation on each workload and report their IPC (instructions per cycle) value and L1/L2 cache miss rate. You can turn in your analysis of performance behaviors with bar graphs.


        # ./build/ARM/gem5.opt --outdir=m5out-2MM-$clock-$model \
        #     configs/proj1/two-level.py $model --cpu_clock=$clock \
        #     --workload='test_bench/2MM/2mm_base' &

        # ./build/ARM/gem5.opt --outdir=m5out-BFS-$clock-$model \
        #     configs/proj1/two-level.py $model --cpu_clock=$clock \
        #     --workload='test_bench/BFS/bfs -f test_bench/BFS/USA-road-d.NY.gr' &

        # ./build/ARM/gem5.opt --outdir=m5out-bzip2-$clock-$model \
        #     configs/proj1/two-level.py $model --cpu_clock=$clock \
        #     --workload='test_bench/bzip2/bzip2_base.amd64-m64-gcc42-nn test_bench/bzip2/input.source 280' & 

        # ./build/ARM/gem5.opt --outdir=m5out-mcf-$clock-$model \
        #     configs/proj1/two-level.py $model --cpu_clock=$clock \
        #     --workload='test_bench/mcf/mcf_base.amd64-m64-gcc42-nn test_bench/mcf/inp.in' &

policy=("CLOCK" "RANDOM" "LRU" "MRU")

# iterate over all the policies

for p in ${policy[@]}; do

    echo "evaluating policy $p"

    ./build/ARM/gem5.opt --outdir=configs/proj3/part2/m5out-2MM-$p \
        configs/proj3/two-level.py --replace_policy=$p \
        --workload='test_bench/2MM/2mm_base' &

    ./build/ARM/gem5.opt --outdir=configs/proj3/part2/m5out-BFS-$p \
        configs/proj3/two-level.py --replace_policy=$p \
        --workload='test_bench/BFS/bfs -f test_bench/BFS/USA-road-d.NY.gr' &

    ./build/ARM/gem5.opt --outdir=configs/proj3/part2/m5out-bzip2-$p \
        configs/proj3/two-level.py --replace_policy=$p \
        --workload='test_bench/bzip2/bzip2_base.amd64-m64-gcc42-nn test_bench/bzip2/input.source 280' & 

    ./build/ARM/gem5.opt --outdir=configs/proj3/part2/m5out-mcf-$p \
        configs/proj3/two-level.py --replace_policy=$p \
        --workload='test_bench/mcf/mcf_base.amd64-m64-gcc42-nn test_bench/mcf/inp.in' &
done

wait