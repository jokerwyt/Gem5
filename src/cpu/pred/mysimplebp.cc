#include "cpu/pred/mysimplebp.hh"
#include "mysimplebp.hh"

namespace gem5 {

namespace branch_prediction{

gem5::branch_predictor::MySimpleBP::MySimpleBP(const MySimpleBPParams& params) {}

void gem5::branch_predictor::MySimpleBP::unconditionalBranch(
    ThreadID tid, Addr pc, void*& bp_history) {}
bool gem5::branch_predictor::MySimpleBP::lookup(ThreadID tid, Addr branch_addr,
                                                void*& bp_history) {
  return true;
}
void gem5::branch_predictor::MySimpleBP::btbUpdate(ThreadID tid,
                                                   Addr branch_addr,
                                                   void*& bp_history) {}
void gem5::branch_predictor::MySimpleBP::update(ThreadID tid, Addr branch_addr,
                                                bool taken, void* bp_history,
                                                bool squashed,
                                                const StaticInstPtr& inst,
                                                Addr corrTarget) {}
void gem5::branch_predictor::MySimpleBP::squash(ThreadID tid,
                                                void* bp_history) {}
}  // namespace branch_prediction
}  // namespace gem5
