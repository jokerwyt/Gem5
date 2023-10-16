#include "cpu/pred/perceptron.hh"

namespace gem5 {

namespace branch_prediction{

PerceptronBP::PerceptronBP(const PerceptronBPParams& params) 
  : BPredUnit(params),
    perceptronNumber(params.perceptronNumber),
    perceptronHistoryBits(params.perceptronHistoryBits),
    stopTrainingThreshold(params.stopTrainingThreshold),
    thrs(params.numThreads)
{
  assert(this->perceptronHistoryBits <= 64);

  for (auto &predictor : thrs) {
    predictor.perceptronWeights.resize(perceptronNumber);
    for (auto &perceptron : predictor.perceptronWeights) {
      // one for constant
      perceptron.resize(perceptronHistoryBits + 1);
    }
  }
}

void PerceptronBP::uncondBranch(ThreadID tid, Addr pc, void*& bp_history) {}

unsigned int PerceptronBP::hash(Addr branch_addr) {
  return branch_addr % perceptronNumber;
}

bool PerceptronBP::lookup(ThreadID tid, Addr branch_addr,
                                                void*& bp_history) {
  auto &predictor = thrs[tid];
  unsigned int perceptron_id = this->hash(branch_addr);
  auto &perceptron = predictor.perceptronWeights[perceptron_id];
  auto &global_history = predictor.global_history;
  int sum = perceptron[0];
  auto tmp = predictor.global_history;

  for (int i = 1; i < perceptron.size(); i++, tmp >>= 1) {
    sum += perceptron[i] * ((tmp & 1) ? 1 : -1);
  }

  BranchInfo *bi = new BranchInfo{perceptron, global_history, sum, sum >= 0};

  bp_history = static_cast<void*>(bi);

  return sum >= 0;
}

void PerceptronBP::btbUpdate(ThreadID tid,Addr branch_addr,void*& bp_history) {}

void PerceptronBP::update(ThreadID tid, Addr branch_addr,
                                                bool taken, void* bp_history,
                                                bool squashed,
                                                const StaticInstPtr& inst,
                                                Addr corrTarget) {
  assert(bp_history != nullptr);
  BranchInfo *bi = static_cast<BranchInfo*>(bp_history);

  if (squashed) {
    // do nothing for a squashed instruction.
    delete bi;
    bp_history = nullptr;
    return;
  }

  auto &perceptron = bi->perceptron;
  auto global_history = bi->used_global_history;
  thrs[tid].global_history = (global_history << 1) | taken;

  if ((bi->sum > 0 ? bi->sum : -bi->sum) < this->stopTrainingThreshold || bi->pred_taken != taken) {
    // train the preceptron
    perceptron[0] += taken ? 1 : -1;

    for (int i = 1; i < perceptron.size(); i++, global_history >>= 1) {
      perceptron[i] += (taken ? 1 : -1) * ((global_history & 1) ? 1 : -1);
    }
  }

  delete bi;
  bp_history = nullptr;
}

void PerceptronBP::squash(ThreadID tid, void* bp_history) {
}

}  // namespace branch_prediction
}  // namespace gem5
