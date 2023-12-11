/**
 * Copyright (c) 2018 Metempsy Technology Consulting
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met: redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer;
 * redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution;
 * neither the name of the copyright holders nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

 /**
  * Implementation of the Signature Path Prefetcher (v2)
  *
  * References:
  *     Path confidence based lookahead prefetching
  *     Jinchun Kim, Seth H. Pugsley, Paul V. Gratz, A. L. Narasimha Reddy,
  *     Chris Wilkerson, and Zeshan Chishti. 2016.
  *     In The 49th Annual IEEE/ACM International Symposium on
  *     Microarchitecture (MICRO-49). IEEE Press, Piscataway, NJ, USA,
  *     Article 60, 12 pages.
  */

#ifndef __MEM_CACHE_PREFETCH_PPF_HH__
#define __MEM_CACHE_PREFETCH_PPF_HH__

#include "mem/cache/prefetch/associative_set.hh"
#include "mem/cache/prefetch/signature_path_v2.hh"
#include "mem/packet.hh"

namespace gem5
{

struct PPFParams;

namespace prefetch
{

class PPF : public SignaturePathV2
{
    // actually in the paper it's only 5-bit saturating counter.
    // each feature is mapped to [0,4095]

    const int feature_bits = 12;
    const int feature_cnt = 4;
    const int weight_bits = 5; // make sure SatCounter8 can hold it.
    static const int kRejectTableSize = 1024;
    static const int kAcceptTableSize = 1024;

    int sumup_permit_threshold = 0;
    int trained_steps = 0;
    int over_trainning_threshold_positive = 0;
    int over_trainning_threshold_negative = 0;

    std::vector<std::vector<SatCounter8>> feature_weights;

    typedef std::vector<uint64_t> Features; // All features should be only feature_bit long.

    struct InferResult {
        bool valid;
        uint64_t prefetch_addr;
        int weight;
        Features features;

        InferResult() : valid(false), prefetch_addr(0), weight(0) {}
    };
    InferResult reject_table[kRejectTableSize], accept_table[kAcceptTableSize];


    void notifyEviction(const PacketPtr &pkt) override;
    int computeWeight(const PPF::Features &features);
    int into_signed(SatCounter8 s);
    SatCounter8 into_unsigned(int s);

public:
    PPF(const PPFParams &p);
    ~PPF() = default;

    void calculatePrefetch(const PrefetchInfo &pfi,
                           std::vector<AddrPriority> &addresses) override;
};

} // namespace prefetch
} // namespace gem5

#endif//__MEM_CACHE_PREFETCH_PPF_HH__
