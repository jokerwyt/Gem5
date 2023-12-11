import m5
from m5.objects import *
from new_cache import *


from optparse import OptionParser
parser = OptionParser()
parser.add_option('--workload', type="string", default="")
parser.add_option('--replace_policy', type="string", default="LRU") # random, LRU, MRU, and CLOCK
parser.add_option('--prefetch', type="string") # PPF or None
parser.add_option('--ppf_threshold', type="int", default=20)
parser.add_option('--train_step', type="int", default=1)
parser.add_option('--ot_thresh_pos', type="int", default=50)
parser.add_option('--ot_thresh_neg', type="int", default=-10)

# check prefetch is PPF or None



(options, args) = parser.parse_args()


if options.prefetch not in ["PPF", "SPPV2"]:
    print("Unknown prefetcher!")
    exit(1)


root = Root(full_system = False, system = System())

root.system.clk_domain = SrcClockDomain()
root.system.clk_domain.clock = '2GHz'
root.system.clk_domain.voltage_domain = VoltageDomain()


root.system.mem_mode = 'timing'
root.system.mem_ranges = [AddrRange ('2GB')] 
root.system.mem_ctrl = MemCtrl()
root.system.mem_ctrl.dram = DDR4_2400_16x4() 
root.system.mem_ctrl.dram.range = root.system.mem_ranges[0]



root.system.cpu = TimingSimpleCPU()
root.system.membus = SystemXBar()


root.system.cpu.icache = L1ICache()
root.system.cpu.dcache = L1DCache()

root.system.l2cache = L2Cache()

if options.prefetch == "PPF":
    root.system.l2cache.prefetcher = PPF(
        permitted_threshold = options.ppf_threshold,
        train_step = options.train_step,
        overtrainning_threshold_positive = options.ot_thresh_pos,
        overtrainning_threshold_negative = options.ot_thresh_neg,
    )
elif options.prefetch == "SPPV2":
    root.system.l2cache.prefetcher = SignaturePathPrefetcherV2()
else:
    print("Unknown prefetcher!")
    exit(1)

# root.system.cpu.icache_port = root.system.membus.cpu_side_ports 
# root.system.cpu.dcache_port = root.system.membus.cpu_side_ports 

root.system.cpu.icache.cpu_side = root.system.cpu.icache_port
root.system.cpu.dcache.cpu_side = root.system.cpu.dcache_port
root.system.l2bus = L2XBar()
root.system.cpu.icache.mem_side = root.system.l2bus.cpu_side_ports
root.system.cpu.dcache.mem_side = root.system.l2bus.cpu_side_ports
root.system.l2cache.cpu_side = root.system.l2bus.mem_side_ports
root.system.l2cache.mem_side = root.system.membus.cpu_side_ports

root.system.mem_ctrl.port = root.system.membus.mem_side_ports 
root.system.cpu.createInterruptController() 
root.system.system_port = root.system.membus.cpu_side_ports
# root.system.cpu.interrupts[0].pio = system.membus.mem_side_ports
# root.system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports 
# root.system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports



if options.replace_policy == "LRU":
    root.system.cpu.icache.replacement_policy = LRURP()
    root.system.cpu.dcache.replacement_policy = LRURP()
    root.system.l2cache.replacement_policy = LRURP()
# elif options.replace_policy == "MRU":
#     root.system.cpu.icache.replacement_policy = MRURP()
#     root.system.cpu.dcache.replacement_policy = MRURP()
#     root.system.l2cache.replacement_policy = MRURP()
# elif options.replace_policy == "RANDOM":
#     root.system.cpu.icache.replacement_policy = RandomRP()
#     root.system.cpu.dcache.replacement_policy = RandomRP()
#     root.system.l2cache.replacement_policy = RandomRP()
# elif options.replace_policy == "CLOCK":
#     root.system.cpu.icache.replacement_policy = MyMRURP()
#     root.system.cpu.dcache.replacement_policy = MyMRURP()
#     root.system.l2cache.replacement_policy = MyMRURP()
else:
    print("Unknown replacement policy!")
    exit(1)

# exe_path = 'tests/test-progs/hello/bin/arm/linux/hello' 
# root.system.workload = SEWorkload.init_compatible(exe_path) 

exe_path = options.workload.split(' ')[0]
root.system.workload = SEWorkload.init_compatible(exe_path)
process = Process()

# process.cmd = [exe_path]
# process.cmd = ['test_bench/2MM/2mm_base']
# process.cmd = ['test_bench/BFS/bfs','-f','test_bench/BFS/USA-road-d.NY.gr']
# process.cmd = ['test_bench/bzip2/bzip2_base.amd64-m64-gcc42-nn','test_bench/bzip2/inp ut.source','280']
# process.cmd = ['test_bench/mcf/mcf_base.amd64-m64-gcc42-nn','test_bench/mcf/inp.in']
# process.cmd = [exe_path]
process.cmd = options.workload.split(' ')


root.system.cpu.workload = process
root.system.cpu.createThreads()

root.system.cpu.max_insts_any_thread = 1e9

m5.instantiate()
exit_event = m5.simulate()
print('Exiting @ tick {} because {}'.format(m5.curTick(), exit_event.getCause()))