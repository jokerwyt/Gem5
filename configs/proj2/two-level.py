
from optparse import OptionParser
parser = OptionParser()
parser.add_option('--o3', action="store_true") 
parser.add_option('--inorder', action="store_true") 
parser.add_option('--cpu_clock', type="string", default="2GHz") 
parser.add_option('--workload', type="string", default="")
parser.add_option('--ddr3_1600_8x8', action="store_true") 
parser.add_option('--ddr3_2133_8x8', action="store_true") 
parser.add_option('--ddr4_2400_16x4', action="store_true") 
parser.add_option('--ddr4_2400_8x8', action="store_true") 
parser.add_option('--lpddr2_s4_1066_1x32', action="store_true") 
parser.add_option('--wideio_200_1x128', action="store_true") 
parser.add_option('--lpddr3_1600_1x32', action="store_true") 

parser.add_option('--local', action="store_true")
parser.add_option("--tournament", action="store_true")
parser.add_option('--bimode', action="store_true")
parser.add_option('--btbentry', type="int", default=4096)
parser.add_option('--ras', type="int", default=16)
parser.add_option('--localsize', type="int", default=2048)
parser.add_option('--localhissize', type="int", default=2048)
parser.add_option('--globalsize', type="int", default=8192)
parser.add_option('--choicesize', type="int", default=8192)
(options, args) = parser.parse_args()



import m5
from m5.objects import *
from new_cache import *

root = Root(full_system = False, system = System())
root.system.clk_domain = SrcClockDomain()
root.system.clk_domain.clock = '2GHz'
root.system.clk_domain.voltage_domain = VoltageDomain()

root.system.mem_mode = 'timing'
root.system.mem_ranges = [AddrRange ('2048MB')]
root.system.mem_ctrl = MemCtrl()
############### modify memory controller ########################### 
# root.system.mem_ctrl.dram = DDR4_2400_16x4()
root.system.mem_ctrl.dram = DDR4_2400_16x4()
if options.ddr3_1600_8x8:
    root.system.mem_ctrl.dram = DDR3_1600_8x8() 
elif options.ddr3_2133_8x8:
    root.system.mem_ctrl.dram = DDR3_2133_8x8() 
elif options.ddr4_2400_16x4:
    root.system.mem_ctrl.dram = DDR4_2400_16x4() 
elif options.ddr4_2400_8x8:
    root.system.mem_ctrl.dram = DDR4_2400_8x8() 
elif options.lpddr2_s4_1066_1x32:
    root.system.mem_ctrl.dram = LPDDR2_S4_1066_1x32() 
elif options.wideio_200_1x128:
    root.system.mem_ctrl.dram = WideIO_200_1x128() 
elif options.lpddr3_1600_1x32:
    root.system.mem_ctrl.dram = LPDDR3_1600_1x32() 
else:
    root.system.mem_ctrl.dram = DDR4_2400_16x4() #default setting
############### modify memory controller ###########################

root.system.mem_ctrl.dram.range = root.system.mem_ranges[0]

if options.o3:
    root.system.cpu = DerivO3CPU()
elif options.inorder:
    root.system.cpu = MinorCPU()
else:
    root.system.cpu = DerivO3CPU()
    # root.system.cpu = TimingSimpleCPU()

root.system.cpu.icache = L1ICache()
root.system.cpu.dcache = L1DCache()
root.system.l2cache = L2Cache()

############### add cpu clock domain #############################
root.system.cpu_clk_domain = SrcClockDomain()
root.system.cpu_clk_domain.clock = options.cpu_clock
root.system.cpu_clk_domain.voltage_domain = VoltageDomain()
root.system.cpu.clk_domain = root.system.cpu_clk_domain 
############### add cpu clock domain ##############################


########################### add branch predictor ###########################
if options.local:
    root.system.cpu.branchPred = LocalBP()
elif options.tournament:
    root.system.cpu.branchPred = TournamentBP()
elif options.bimode:
    root.system.cpu.branchPred = BiModeBP()
else:
    root.system.cpu.branchPred = TournamentBP()

root.system.cpu.branchPred.BTBEntries = options.btbentry
root.system.cpu.branchPred.RASSize = options.ras

if options.local:
    root.system.cpu.branchPred.localPredictorSize = options.localsize
elif options.tournament:
    root.system.cpu.branchPred.localPredictorSize = options.localsize
    root.system.cpu.branchPred.localHistoryTableSize = options.localhissize
    root.system.cpu.branchPred.globalPredictorSize = options.globalsize
    root.system.cpu.branchPred.choicePredictorSize = options.choicesize
elif options.bimode:
    root.system.cpu.branchPred.globalPredictorSize = options.globalsize
    root.system.cpu.branchPred.choicePredictorSize = options.choicesize
########################### add branch predictor ###########################

root.system.membus = SystemXBar()

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

exe_path = options.workload.split(' ')[0]
root.system.workload = SEWorkload.init_compatible(exe_path)

process = Process()
# process.cmd = [exe_path]
# process.cmd = ['test_bench/2MM/2mm_base']
# process.cmd = ['test_bench/BFS/bfs','-f','test_bench/BFS/USA-road-d.NY.gr']
# process.cmd = ['test_bench/bzip2/bzip2_base.amd64-m64-gcc42-nn','test_bench/bzip2/inp ut.source','280']
# process.cmd = ['test_bench/mcf/mcf_base.amd64-m64-gcc42-nn','test_bench/mcf/inp.in']
process.cmd = options.workload.split(' ')

root.system.cpu.workload = process
root.system.cpu.createThreads()

root.system.cpu.max_insts_any_thread = 1e9

m5.instantiate()
exit_event = m5.simulate()
print('Exiting @ tick {} because {}'.format(m5.curTick(), exit_event.getCause()))
