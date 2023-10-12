#!/bin/bash

# m5out-lab2.6-BFS-tournament-$localsize-$localhissize-$globalsize
#	localsize	localhissize	globalsize
# default-value	2048	2048	8192


# fix localhissize and globalsize, change localsize
# grep all files in subdirectories m5out-lab2.6-BFS-tournament-$localsize-$localhissize-$globalsize, for "system.cpu.ipc"

# print the local size list, separated by tab
# echo -e "localsize\t 32\t 256\t 2048\t 16384\t 131072"
# for localsize in 32 256 2048 16384 131072; do
#     for localhissize in 2048; do
#         for globalsize in 8192; do
#             # grep 
#             grep "system.cpu.ipc" m5out-lab2.6-BFS-tournament-$localsize-$localhissize-$globalsize/stats.txt
#         done
#     done
# done

# fix localsize,  and globalsize, change localhissize
# grep all files in subdirectories m5out-lab2.6-BFS-tournament-$localsize-$localhissize-$globalsize, for "system.cpu.ipc"

echo -e "localhissize\t 32\t 256\t 2048\t 16384\t 131072"
for localsize in 2048; do
    for localhissize in 256 2048 16384 131072; do
        for globalsize in 8192; do
            # grep 
            grep "system.cpu.ipc" m5out-lab2.6-BFS-tournament-$localsize-$localhissize-$globalsize/stats.txt
        done
    done
done


# fix localhissize and localsize, change globalsize
# grep all files in subdirectories m5out-lab2.6-BFS-tournament-$localsize-$localhissize-$globalsize, for "system.cpu.ipc"


echo -e "globalsize\t 512\t 2048\t 8192\t 32768\t 131072"
for localsize in 2048; do
    for localhissize in 2048; do
        for globalsize in 512 2048 8192 32768 131072; do
            # grep 
            grep "system.cpu.ipc" m5out-lab2.6-BFS-tournament-$localsize-$localhissize-$globalsize/stats.txt
        done
    done
done