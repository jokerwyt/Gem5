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

#include "mem/cache/prefetch/ppf.hh"

#include <cassert>

#include "debug/HWPrefetch.hh"
#include "debug/wyt.hh"
#include "mem/cache/prefetch/associative_set_impl.hh"
#include "params/PPF.hh"
#include "ppf.hh"

namespace gem5
{

namespace prefetch
{


int PPF::into_signed(SatCounter8 s) {
    return ((int)s) - (1 << (this->weight_bits - 1));
}

SatCounter8 PPF::into_unsigned(int s) {
    return SatCounter8(this->weight_bits, s + (1 << (this->weight_bits - 1)));
}

PPF::PPF(const PPFParams &p)
    : SignaturePathV2(p) {
    
    // we use four feature.
    // 0. conf^paddr
    // 1. cacheline (address >> 6)
    // 2. paddr (address >> 12)
    // 3. baddr (address itself)

    // we will only keep the low 12 bits of every feature.

    // now we are going to initialize feature_weights

    this->feature_weights.resize(this->feature_cnt, 
        std::vector<SatCounter8>(1<<this->feature_bits, SatCounter8(this->weight_bits,  into_unsigned(0) )));
    
    this->sumup_permit_threshold = p.permitted_threshold;
    this->trained_steps = p.train_step;
    this->over_trainning_threshold_positive = p.overtrainning_threshold_positive;
    this->over_trainning_threshold_negative = p.overtrainning_threshold_negative;

    // make sure those threshold and strained_steps within the range of (1<<weight_bits-1).
    assert(this->sumup_permit_threshold < feature_cnt * (1<<(this->weight_bits-1)));
    assert(this->trained_steps < (1<<(this->weight_bits-1)));
    assert(this->over_trainning_threshold_positive < feature_cnt * (1<<(this->weight_bits-1)));

    assert(this->over_trainning_threshold_negative < 0 && 
        this->over_trainning_threshold_negative > - feature_cnt * (1<<(this->weight_bits-1)));
}

int PPF::computeWeight(const PPF::Features &features) {
    int weight = 0;
    for (int i = 0; i < this->feature_cnt; i++) {
        weight += this->into_signed(this->feature_weights[i][features[i]]);
    }
    return weight;
}

void PPF::calculatePrefetch(const PrefetchInfo &pfi,
                            std::vector<AddrPriority> &addresses) {
    Addr request_addr = pfi.getAddr();

    // update feature_weights when demand access happens.
    {
        auto rej_entry = this->reject_table[request_addr % kRejectTableSize];
        if (rej_entry.valid) {
            if (rej_entry.prefetch_addr == request_addr) {
                DPRINTF(wyt, "reject table hit on demand access %lx\n", request_addr);
                // a demand access was wrongly rejected before.

                // update feature_weights
                Features features = rej_entry.features;

                int now_weight = this->computeWeight(features);

                if (now_weight <= this->over_trainning_threshold_positive) {
                    for (int i = 0; i < this->feature_cnt; i++) {
                        this->feature_weights[i][features[i]] += trained_steps;
                    }
                } else {
                    DPRINTF(wyt, "weight very large, need not to large it\n");
                }
            }
        }

        auto acc_entry = this->accept_table[request_addr % kAcceptTableSize];
        if (acc_entry.valid) {
            if (acc_entry.prefetch_addr == request_addr) {
                DPRINTF(wyt, "accept table hit on demand access %lx\n", request_addr);
                // a demand access was correctly accepted before.

                // update feature_weights
                Features features = acc_entry.features;

                int now_weight = this->computeWeight(features);

                if (now_weight <= this->over_trainning_threshold_positive) {
                    for (int i = 0; i < this->feature_cnt; i++) {
                        this->feature_weights[i][features[i]] += trained_steps;
                    }
                } else {
                    DPRINTF(wyt, "weight very large, need not to large it\n");
                }
            }
        }
    }



    Addr ppn = request_addr / pageBytes;
    stride_t current_block = (request_addr % pageBytes) / blkSize;
    stride_t stride;
    bool is_secure = pfi.isSecure();
    double initial_confidence = 1.0;

    // Get the SignatureEntry of this page to:
    // - compute the current stride
    // - obtain the current signature of accesses
    bool miss;
    SignatureEntry &signature_entry = getSignatureEntry(ppn, is_secure,
            current_block, miss, stride, initial_confidence);

    if (miss) {
        // No history for this page, can't continue
        return;
    }

    if (stride == 0) {
        // Can't continue with a stride 0
        return;
    }

    // Update the confidence of the current signature
    updatePatternTable(signature_entry.signature, stride);

    // Update the current SignatureEntry signature
    signature_entry.signature =
        updateSignature(signature_entry.signature, stride);

    signature_t current_signature = signature_entry.signature;
    double current_confidence = initial_confidence;
    stride_t current_stride = signature_entry.lastBlock;

    // Look for prefetch candidates while the current path confidence is
    // high enough

    bool first_prefetch = true;

    while (current_confidence > lookaheadConfidenceThreshold) {
        // With the updated signature, attempt to generate prefetches
        // - search the PatternTable and select all entries with enough
        //   confidence, these are prefetch candidates
        // - select the entry with the highest counter as the "lookahead"
        PatternEntry *current_pattern_entry =
            patternTable.findEntry(current_signature, false);
        PatternStrideEntry const *lookahead = nullptr;
        if (current_pattern_entry != nullptr) {
            unsigned long max_counter = 0;
            for (auto const &entry : current_pattern_entry->strideEntries) {
                //select the entry with the maximum counter value as lookahead
                if (max_counter < entry.counter) {
                    max_counter = entry.counter;
                    lookahead = &entry;
                }
                double prefetch_confidence =
                    calculatePrefetchConfidence(*current_pattern_entry, entry);

                if (prefetch_confidence >= prefetchConfidenceThreshold) {
                    assert(entry.stride != 0);
                    //prefetch candidate
                    
                    size_t pre_length = addresses.size();

                    addPrefetch(ppn, current_stride, entry.stride,
                                current_confidence, current_signature,
                                is_secure, addresses);

                    if (first_prefetch) {
                        // we can not prohibit the first prefetch.
                        first_prefetch = false;
                        continue;
                    }

                    bool is_prefetch = addresses.size() > pre_length;

                    if (is_prefetch) {
                        Features features(this->feature_cnt);
                        features[0] = (((size_t) (prefetch_confidence * 4096)) ^ ppn) & ((1<<this->feature_bits) - 1);
                        features[1] = (request_addr >> 6) & ((1<<this->feature_bits) - 1);
                        features[2] = (request_addr >> 12) & ((1<<this->feature_bits) - 1);
                        features[3] = request_addr & ((1<<this->feature_bits) - 1);

                        int weight = this->computeWeight(features);

                        Addr prefetch_addr = addresses.back().first;

                        if (weight < this->sumup_permit_threshold) {
                            DPRINTF(wyt, "reject prefetch %lx with weight %d", prefetch_addr, weight);
                            DPRINTF(wyt, "features: %lx %lx %lx %lx\n", features[0], features[1], features[2], features[3]);
                            DPRINTF(wyt, "features weight: %d %d %d %d\n", this->into_signed(this->feature_weights[0][features[0]]),
                                this->into_signed(this->feature_weights[1][features[1]]),
                                this->into_signed(this->feature_weights[2][features[2]]),
                                this->into_signed(this->feature_weights[3][features[3]]));

                            // reject
                            addresses.pop_back();
                            this->reject_table[prefetch_addr % kRejectTableSize].valid = true;
                            this->reject_table[prefetch_addr % kRejectTableSize].prefetch_addr = prefetch_addr;
                            this->reject_table[prefetch_addr % kRejectTableSize].weight = weight;
                            this->reject_table[prefetch_addr % kRejectTableSize].features = features;
                        } else {
                            DPRINTF(wyt, "accept prefetch %lx with weight %d", prefetch_addr, weight);
                            DPRINTF(wyt, "features: %lx %lx %lx %lx\n", features[0], features[1], features[2], features[3]);
                            DPRINTF(wyt, "features weight: %d %d %d %d\n", this->into_signed(this->feature_weights[0][features[0]]),
                                this->into_signed(this->feature_weights[1][features[1]]),
                                this->into_signed(this->feature_weights[2][features[2]]),
                                this->into_signed(this->feature_weights[3][features[3]]));

                            this->accept_table[prefetch_addr % kAcceptTableSize].valid = true;
                            this->accept_table[prefetch_addr % kAcceptTableSize].prefetch_addr = prefetch_addr;
                            this->accept_table[prefetch_addr % kAcceptTableSize].weight = weight;
                            this->accept_table[prefetch_addr % kAcceptTableSize].features = features;
                        }
                    }
                }
            }
        }

        if (lookahead != nullptr) {
            current_confidence *= calculateLookaheadConfidence(
                    *current_pattern_entry, *lookahead);
            current_signature =
                updateSignature(current_signature, lookahead->stride);
            current_stride += lookahead->stride;
        } else {
            current_confidence = 0.0;
        }
    }

    auxiliaryPrefetcher(ppn, current_block, is_secure, addresses);

}


void PPF::notifyEviction(const PacketPtr &pkt) {
    DPRINTF(wyt, "notifyEviction: %s\n", pkt->print());
    Addr addr = pkt->getAddr();
    
    // update feature_weights when eviction happens.

    // check accept_table first.
    auto acc_entry = this->accept_table[addr % kAcceptTableSize];
    DPRINTF(wyt, "evict %lx\n", addr);
    if (acc_entry.valid) {
        if (acc_entry.prefetch_addr == addr) {
            // a prefetch was wrongly accepted before.
            DPRINTF(wyt, "accept table hit on eviction %lx\n", addr);

            // update feature_weights
            Features features = acc_entry.features;
            if (this->computeWeight(features) >= this->over_trainning_threshold_negative) {
                for (int i = 0; i < this->feature_cnt; i++) {
                    this->feature_weights[i][features[i]] -= this->trained_steps;
                }
            } else {
                DPRINTF(wyt, "weight very small, need not to small it\n");
            }
        }
    }
}



} // namespace prefetch
} // namespace gem5
