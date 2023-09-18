#!/bin/bash

# ./build/ARM/gem5.opt --outdir=m5out-2MM_base-default \
#     configs/proj1/two-level.py --cpu_clock=1.8GHz --ddr3_1600_8x8 \
#     --workload='test_bench/2MM/2mm_base' &

# ./build/ARM/gem5.opt --outdir=m5out-BFS-default \
#     configs/proj1/two-level.py --cpu_clock=1.8GHz --ddr3_1600_8x8 \
#     --workload='test_bench/BFS/bfs -f test_bench/BFS/USA-road-d.NY.gr' &

# ./build/ARM/gem5.opt --outdir=m5out-bzip2-default \
#     configs/proj1/two-level.py --cpu_clock=1.8GHz --ddr3_1600_8x8 \
#     --workload='test_bench/bzip2/bzip2_base.amd64-m64-gcc42-nn test_bench/bzip2/inp ut.source 280' & 

# ./build/ARM/gem5.opt --outdir=m5out-mcf-default \
#     configs/proj1/two-level.py --cpu_clock=1.8GHz --ddr3_1600_8x8 \
#     --workload='test_bench/mcf/mcf_base.amd64-m64-gcc42-nn test_bench/mcf/inp.in' &


# I have seven memory types, their names are 
# --ddr3_1600_8x8
# --ddr3_2133_8x8
# --ddr4_2400_8x8
# --ddr4_2400_16x4
# --lpddr2_s4_1066_1x32
# --wideio_200_1x128
# --lpddr3_1600_1x32

# construct a list with all the memory types
mem_types=(--ddr3_1600_8x8 --ddr3_2133_8x8 --ddr4_2400_8x8 --ddr4_2400_16x4 --lpddr2_s4_1066_1x32 --wideio_200_1x128 --lpddr3_1600_1x32)

# for each memory type, run all the benchmarks
for mem_type in ${mem_types[@]}; do
    echo "Running benchmarks with memory type: $mem_type"
    ./build/ARM/gem5.opt --outdir=m5out-2MM-$mem_type \
        configs/proj1/two-level.py --cpu_clock=1.8GHz $mem_type \
        --workload='test_bench/2MM/2mm_base' &

    ./build/ARM/gem5.opt --outdir=m5out-BFS-$mem_type \
        configs/proj1/two-level.py --cpu_clock=1.8GHz $mem_type \
        --workload='test_bench/BFS/bfs -f test_bench/BFS/USA-road-d.NY.gr' &

    ./build/ARM/gem5.opt --outdir=m5out-bzip2-$mem_type \
        configs/proj1/two-level.py --cpu_clock=1.8GHz $mem_type \
        --workload='test_bench/bzip2/bzip2_base.amd64-m64-gcc42-nn test_bench/bzip2/inp ut.source 280' & 

    ./build/ARM/gem5.opt --outdir=m5out-mcf-$mem_type \
        configs/proj1/two-level.py --cpu_clock=1.8GHz $mem_type \
        --workload='test_bench/mcf/mcf_base.amd64-m64-gcc42-nn test_bench/mcf/inp.in' &
done

