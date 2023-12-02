/**
 * Copyright (c) 2018-2020 Inria
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

#include "mem/cache/replacement_policies/mymru_rp.hh"

#include <cassert>
#include <memory>

#include "params/MyMRURP.hh"
#include "sim/cur_tick.hh"

namespace gem5
{

namespace replacement_policy
{

MyMRU::MyMRU(const Params &p)
  : Base(p)
{
}

void
MyMRU::invalidate(const std::shared_ptr<ReplacementData>& replacement_data)
{
    // Reset last touch timestamp
    auto data = std::static_pointer_cast<MyMRUReplData>(replacement_data);
    data->lastTouchTick = Tick(0);
    data->tag = false;
}

void
MyMRU::touch(const std::shared_ptr<ReplacementData>& replacement_data) const
{
    // Update last touch timestamp
    auto data = std::static_pointer_cast<MyMRUReplData>(replacement_data);
    data->lastTouchTick = curTick();
    data->tag = true;
}

void
MyMRU::reset(const std::shared_ptr<ReplacementData>& replacement_data) const
{
    // Set last touch timestamp
    auto data = std::static_pointer_cast<MyMRUReplData>(replacement_data);
    data->lastTouchTick = curTick();
    data->tag = true;
}

ReplaceableEntry*
MyMRU::getVictim(const ReplacementCandidates& candidates) const
{
    // There must be at least one replacement candidate
    assert(candidates.size() > 0 && candidates.size() > this->hand);

    // Visit all candidates to find victim
    size_t hand = 0;
    // priority: invalid entry
    // and get last_touch entry in hand
    size_t idx = 0;
    for (const auto& candidate : candidates) {
        auto data = std::static_pointer_cast<MyMRUReplData>(
            candidates[hand]->replacementData);
        if (data->lastTouchTick == 0) {
            return candidate;
        }

        if (data->lastTouchTick >
                std::static_pointer_cast<MyMRUReplData>(
                    candidates[hand]->replacementData)->lastTouchTick) {
            hand = idx;
        }
        idx++;
    }


    ReplaceableEntry* victim = candidates[hand];
    while (true) {
        // use clock replacement policy
        auto data = std::static_pointer_cast<MyMRUReplData>(
            candidates[hand]->replacementData);
        
        if (data->tag == true) {
            data->tag = false;
            hand = (hand + 1) % candidates.size();
        } else {
            victim = candidates[hand];
            hand = (hand + 1) % candidates.size();
            break;
        }
    }

    return victim;
}

std::shared_ptr<ReplacementData>
MyMRU::instantiateEntry()
{
    return std::shared_ptr<ReplacementData>(new MyMRUReplData());
}

} // namespace replacement_policy
} // namespace gem5
