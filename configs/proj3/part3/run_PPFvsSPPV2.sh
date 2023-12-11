#!/bin/bash

# get root directory of the project
# my path is configs/proj3/part3/run_PPFvsSPPV2.sh
root_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/../../.. >/dev/null 2>&1 && pwd )"

# kill all the processes if control C is pressed
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

prefetcher=("SPPV2" "PPF")
threshold=1

for p in ${prefetcher[@]}; do
    echo "evaluating prefetcher $p"

    $root_dir/build/ARM/gem5.opt --outdir=$root_dir/configs/proj3/part3/m5out-2MM-$p \
        $root_dir/configs/proj3/part3/two-level.py --prefetch $p --ppf_threshold=$threshold \
        --workload="$root_dir/test_bench/2MM/2mm_base" &

    $root_dir/build/ARM/gem5.opt --outdir=$root_dir/configs/proj3/part3/m5out-BFS-$p \
        $root_dir/configs/proj3/part3/two-level.py --prefetch $p --ppf_threshold=$threshold \
        --workload="$root_dir/test_bench/BFS/bfs -f $root_dir/test_bench/BFS/USA-road-d.NY.gr" &

    $root_dir/build/ARM/gem5.opt --outdir=$root_dir/configs/proj3/part3/m5out-bzip2-$p \
        $root_dir/configs/proj3/part3/two-level.py --prefetch $p --ppf_threshold=$threshold \
        --workload="$root_dir/test_bench/bzip2/bzip2_base.amd64-m64-gcc42-nn $root_dir/test_bench/bzip2/input.source 280" & 

    $root_dir/build/ARM/gem5.opt --outdir=$root_dir/configs/proj3/part3/m5out-mcf-$p \
        $root_dir/configs/proj3/part3/two-level.py --prefetch $p --ppf_threshold=$threshold \
        --workload="$root_dir/test_bench/mcf/mcf_base.amd64-m64-gcc42-nn $root_dir/test_bench/mcf/inp.in" &
done

wait

