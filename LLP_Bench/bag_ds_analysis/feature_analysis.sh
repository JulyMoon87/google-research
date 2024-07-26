# Copyright 2024 The Google Research Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash
for c in $(seq 1 26)
do
  python3 bag_ds_analysis/feature_analysis.py --c1=$c --c2=0 --grp_key_size_one=True --which_dataset=criteo_ctr
done

for c1 in $(seq 1 26)
do
  for c2 in $(seq $(($c1+1)) 26)
  do
    python3 bag_ds_analysis/feature_analysis.py --c1=$c1 --c2=$c2 --grp_key_size_one=False --which_dataset=criteo_ctr
  done
done

declare -a c1_c2_list_sscl=(
    '2 5'
    '3 5'
    '3 8'
    '3 16'
    '5 6'
    '5 7'
    '5 8'
    '5 9'
    '5 16'
    '8 16'
)

for c1_c2 in "${c1_c2_list_sscl[@]}"; do
    read -a strarr <<< "$c1_c2"  # uses default whitespace IFS
    python3 bag_ds_analysis/feature_analysis.py --c1=${strarr[0]} --c2=${strarr[1]}  --grp_key_size_one=False --which_dataset=criteo_sscl
done