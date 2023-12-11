from m5.objects import *

class L1Cache(Cache):
    size = '64kB'
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20

    def __init__(self):
        super(L1Cache, self).__init__()


class L1DCache(Cache):
    size = '32kB' 
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20

    def __init__(self):
        super(L1DCache, self).__init__()

class L1ICache(Cache):
    size = '32kB'
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20

    def __init__(self):
        super(L1ICache, self).__init__()



class L2Cache(Cache):
    size = '256kB'
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12

    def __init__(self):
        super(L2Cache, self).__init__()


# class L2CacheWithPPF(Cache):
#     size = '256kB'
#     assoc = 8
#     tag_latency = 20
#     data_latency = 20
#     response_latency = 20
#     mshrs = 20
#     tgts_per_mshr = 12

    
#     def __init__(self):
#         super(L2CacheWithPPF, self).__init__()

# class L2CacheWithSPPV2(Cache):
#     size = '256kB'
#     assoc = 8
#     tag_latency = 20
#     data_latency = 20
#     response_latency = 20
#     mshrs = 20
#     tgts_per_mshr = 12

#     prefetcher = SignaturePathPrefetcherV2()
    
#     def __init__(self):
#         super(L2CacheWithSPPV2, self).__init__()

class L3Cache(Cache):
    size = '16MB'
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12

    def __init__(self):
        super(L3Cache, self).__init__()

