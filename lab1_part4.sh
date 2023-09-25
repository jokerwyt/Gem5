#!/bin/bash

# ./build/ARM/gem5.opt --outdir=m5out-2MM_base-default \
#     configs/proj1/two-level.py --cpu_clock=1.8GHz --ddr3_1600_8x8 \
#     --workload='test_bench/2MM/2mm_base' &

# ./build/ARM/gem5.opt --outdir=m5out-BFS-default \
#     configs/proj1/two-level.py --cpu_clock=1.8GHz --ddr3_1600_8x8 \
#     --workload='test_bench/BFS/bfs -f test_bench/BFS/USA-road-d.NY.gr' &

# ./build/ARM/gem5.opt --outdir=m5out-bzip2-default \
#     configs/proj1/two-level.py --cpu_clock=1.8GHz --ddr3_1600_8x8 \
#     --workload='test_bench/bzip2/bzip2_base.amd64-m64-gcc42-nn test_bench/bzip2/input.source 280' & 

# # ./build/ARM/gem5.opt --outdir=m5out-mcf-default \
# #     configs/proj1/two-level.py --cpu_clock=1.8GHz --ddr3_1600_8x8 \
# #     --workload='test_bench/mcf/mcf_base.amd64-m64-gcc42-nn test_bench/mcf/inp.in' &


# # I have seven memory types, their names are 
# # --ddr3_1600_8x8
# # --ddr3_2133_8x8
# # --ddr4_2400_8x8
# # --ddr4_2400_16x4
# # --lpddr2_s4_1066_1x32
# # --wideio_200_1x128
# # --lpddr3_1600_1x32

# # construct a list with all the memory types
# mem_types=(--ddr3_1600_8x8 --ddr3_2133_8x8 --ddr4_2400_8x8 --ddr4_2400_16x4 --lpddr2_s4_1066_1x32 --wideio_200_1x128 --lpddr3_1600_1x32)

# # for each memory type, run all the benchmarks
# for mem_type in ${mem_types[@]}; do
#     echo "Running benchmarks with memory type: $mem_type"
#     # ./build/ARM/gem5.opt --outdir=m5out-2MM-$mem_type \
#     #     configs/proj1/two-level.py --cpu_clock=1.8GHz $mem_type \
#     #     --workload='test_bench/2MM/2mm_base' &

#     # ./build/ARM/gem5.opt --outdir=m5out-BFS-$mem_type \
#     #     configs/proj1/two-level.py --cpu_clock=1.8GHz $mem_type \
#     #     --workload='test_bench/BFS/bfs -f test_bench/BFS/USA-road-d.NY.gr' &

#     ./build/ARM/gem5.opt --outdir=m5out-bzip2-$mem_type \
#         configs/proj1/two-level.py --cpu_clock=1.8GHz $mem_type \
#         --workload='test_bench/bzip2/bzip2_base.amd64-m64-gcc42-nn test_bench/bzip2/input.source 280' & 

#     # ./build/ARM/gem5.opt --outdir=m5out-mcf-$mem_type \
#     #     configs/proj1/two-level.py --cpu_clock=1.8GHz $mem_type \
#     #     --workload='test_bench/mcf/mcf_base.amd64-m64-gcc42-nn test_bench/mcf/inp.in' &
# done

# use DDR4_2400_16x4(), but try --o3 and --inorder for different CPU models
# and iterate over cpu clock frequency [2.4, 2.8, 3.2, 3.6, 4.0]

# construct a list with all the cpu clock fre
cpu_clocks=(2.4GHz 2.8GHz 3.2GHz 3.6GHz 4.0GHz)
cpu_model=(--o3 --inorder)

# forloop both cpu clock frequency and cpu model
for clock in ${cpu_clocks[@]}; do
    for model in ${cpu_model[@]}; do
        echo "Running benchmarks with cpu clock: $clock and cpu model: $model"
        ./build/ARM/gem5.opt --outdir=m5out-2MM-$clock-$model \
            configs/proj1/two-level.py $model --cpu_clock=$clock \
            --workload='test_bench/2MM/2mm_base' &

        ./build/ARM/gem5.opt --outdir=m5out-BFS-$clock-$model \
            configs/proj1/two-level.py $model --cpu_clock=$clock \
            --workload='test_bench/BFS/bfs -f test_bench/BFS/USA-road-d.NY.gr' &

        ./build/ARM/gem5.opt --outdir=m5out-bzip2-$clock-$model \
            configs/proj1/two-level.py $model --cpu_clock=$clock \
            --workload='test_bench/bzip2/bzip2_base.amd64-m64-gcc42-nn test_bench/bzip2/input.source 280' & 

        ./build/ARM/gem5.opt --outdir=m5out-mcf-$clock-$model \
            configs/proj1/two-level.py $model --cpu_clock=$clock \
            --workload='test_bench/mcf/mcf_base.amd64-m64-gcc42-nn test_bench/mcf/inp.in' &
    done
done