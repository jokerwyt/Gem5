#ifndef __CPU_PRED_Perceptron_PRED_HH__
#define __CPU_PRED_Perceptron_PRED_HH__

#include "base/types.hh"
#include "cpu/pred/bpred_unit.hh"
#include "params/PerceptronBP.hh"

#include <vector>

namespace gem5{
namespace branch_prediction {

class PerceptronBP : public BPredUnit {

  unsigned int perceptronNumber;
  unsigned int perceptronHistoryBits;
  unsigned int stopTrainingThreshold;

  struct PerceptronOneCore {
    std::vector<std::vector<int>> perceptronWeights;
    uint64_t global_history;
  };
  std::vector<PerceptronOneCore> thrs;

  unsigned int hash(Addr branch_addr);

  struct BranchInfo {
    std::vector<int> &perceptron;
    uint64_t used_global_history;
    int sum;
    bool pred_taken;
  };


 public:
  PerceptronBP(const PerceptronBPParams &params);
  void uncondBranch(ThreadID tid, Addr pc, void * &bp_history);
  bool lookup(ThreadID tid, Addr branch_addr, void * &bp_history);
  void btbUpdate(ThreadID tid, Addr branch_addr, void * &bp_history);
  void update(ThreadID tid, Addr branch_addr, bool taken, void *bp_history,
                bool squashed, const StaticInstPtr & inst, Addr corrTarget);
  void squash(ThreadID tid, void *bp_history);
};

}
}

#endif