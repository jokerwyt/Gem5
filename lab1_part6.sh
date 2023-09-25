#!/bin/sh


# copy pthread_matrixmult/test-thread.rcS to lab1-part6/test-thread#.rcS, change the number of threads in test-thread#.rcS to #

# cp pthread_matrixmult/test.rcS lab1-part6/test-thread1.rcS
# cp pthread_matrixmult/test.rcS lab1-part6/test-thread2.rcS
# cp pthread_matrixmult/test.rcS lab1-part6/test-thread3.rcS
# cp pthread_matrixmult/test.rcS lab1-part6/test-thread4.rcS
# cp pthread_matrixmult/test.rcS lab1-part6/test-thread5.rcS
# cp pthread_matrixmult/test.rcS lab1-part6/test-thread6.rcS
# cp pthread_matrixmult/test.rcS lab1-part6/test-thread7.rcS
# cp pthread_matrixmult/test.rcS lab1-part6/test-thread8.rcS


# build/ARM/gem5.opt configs/example/fs.py --outdir=m5out-lab1-part6-thread1 \
#     --kernel=vmlinux.arm64 --disk-image=ubuntu-18.04-arm64-docker.img --num-cpu=8 --script=lab1-part6/test-thread1.rcS

# for thread 1 to thread 8, keep --num-cpu=8, but change test-thread1.rcS to test-thread#.rcS, and change the output dir to m5out-lab1-part6-thread#

for i in 1 2 3 4 5 6 7 8
do
    build/ARM/gem5.opt  --outdir=m5out-lab1-part6-thread$i configs/deprecated/example/fs.py \
    --kernel=vmlinux.arm64 --disk-image=ubuntu-18.04-arm64-docker.img --num-cpu=8 --script=lab1-part6/test-thread$i.rcS &
done

# wait all background processes to finish
wait
