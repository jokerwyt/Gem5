import m5
from m5.objects import *
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from new_cache import *


from optparse import OptionParser
parser = OptionParser()
parser.add_option('--workload', type="string", default="")

(options, args) = parser.parse_args()


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


root.system.cpu.l1cache = L1Cache()
root.system.l2cache = L2Cache()

root.system.cpu.l1bus = L2XBar()

root.system.cpu.icache_port = root.system.cpu.l1bus.cpu_side_ports
root.system.cpu.dcache_port = root.system.cpu.l1bus.cpu_side_ports

root.system.cpu.l1cache.cpu_side = root.system.cpu.l1bus.mem_side_ports


root.system.cpu.l1cache.mem_side = root.system.l2cache.cpu_side
root.system.l2cache.mem_side = root.system.membus.cpu_side_ports

root.system.mem_ctrl.port = root.system.membus.mem_side_ports 
root.system.cpu.createInterruptController() 
root.system.system_port = root.system.membus.cpu_side_ports
# root.system.cpu.interrupts[0].pio = system.membus.mem_side_ports
# root.system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports 
# root.system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

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

root.system.cpu.max_insts_any_thread = 1e7

m5.instantiate()
exit_event = m5.simulate()
print('Exiting @ tick {} because {}'.format(m5.curTick(), exit_event.getCause()))