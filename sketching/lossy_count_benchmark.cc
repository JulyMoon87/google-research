// Copyright 2024 The Google Research Authors.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "benchmark/benchmark.h"
#include "benchmark_utils.h"
#include "lossy_count.h"
#include "sketch.h"
#include "utils.h"

static void BM_LossyCountAdd(benchmark::State& state) {
  sketch::LossyCount sketch(/*window_size=*/2000);
  Add(state, &sketch);
}

static void BM_LossyCountFallbackAdd(benchmark::State& state) {
  sketch::LossyCountFallback sketch(/*window_size=*/2000, /*hash_count=*/5,
                                    /*hash_size=*/2048);
  Add(state, &sketch);
}

BENCHMARK(BM_LossyCountAdd)->Range(1 << 12, 1 << 21);
BENCHMARK(BM_LossyCountFallbackAdd)->Range(1 << 12, 1 << 21);
BENCHMARK_MAIN();
