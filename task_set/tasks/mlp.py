# coding=utf-8
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

"""MLP on images task family."""

import collections
import numpy as np
import sonnet as snt

from task_set import registry
from task_set.tasks import base
from task_set.tasks import utils
import tensorflow.compat.v1 as tf


@registry.task_registry.register_sampler("mlp_family")
def sample_mlp_family_cfg(seed):
  """Sample a task config for a MLP model on image datasets.

  These configs are nested python structures that provide enough information
  to create an instance of the problem.

  Args:
    seed: int Random seed to generate task from.

  Returns:
    A nested dictionary containing a configuration.
  """
  # random offset seed to ensure different task families sample different
  # configs.
  rng = np.random.RandomState(seed + 99123491)
  cfg = collections.OrderedDict()
  n_layers = rng.choice([1, 2, 3, 4, 5, 6])
  cfg["layer_sizes"] = [
      utils.sample_log_int(rng, 16, 128) for _ in range(n_layers)
  ]
  cfg["activation"] = utils.sample_activation(rng)
  cfg["w_init"] = utils.sample_initializer(rng)
  cfg["dataset"] = utils.sample_image_dataset(rng)
  cfg["center_data"] = bool(rng.choice([True, False]))
  return cfg


@registry.task_registry.register_getter("mlp_family")
def get_mlp_family(cfg):
  """Get a task for the given cfg.

  Args:
    cfg: config specifying the model generated by `sample_mlp_family_cfg`.

  Returns:
    base.BaseTask for the given config.
  """
  act_fn = utils.get_activation(cfg["activation"])
  w_init = utils.get_initializer(cfg["w_init"])
  init = {"w": w_init}
  # cfg["dataset"] contains (dname, extra_info)

  dataset = utils.get_image_dataset(cfg["dataset"])

  def _fn(batch):
    image = utils.maybe_center(cfg["center_data"], batch["image"])
    hidden_units = cfg["layer_sizes"] + [batch["label_onehot"].shape[1]]
    net = snt.BatchFlatten()(image)
    mod = snt.nets.MLP(hidden_units, activation=act_fn, initializers=init)
    logits = mod(net)
    loss_vec = tf.nn.softmax_cross_entropy_with_logits_v2(
        labels=batch["label_onehot"], logits=logits)
    return tf.reduce_mean(loss_vec)

  return base.DatasetModelTask(lambda: snt.Module(_fn), dataset)
