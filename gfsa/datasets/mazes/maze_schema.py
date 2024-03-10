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

"""A graph schema for 2d gridworld mazes.

This schema assumes that the maze has no dead ends; in other words, every square
can be exited in at least two directions. This is consistent with the mazes
generated by labmaze.
"""

import itertools
from typing import List, Tuple

import numpy as np

from gfsa import graph_types


def build_maze_schema(min_neighbors):
  """Build a schema for a 2d gridworld maze.

  A node type like "cell_LxUD" corresponds to a cell that has neighbors in the
  left, up, and down directions. The in and out edges for this cell would be
  "L_out", "U_out", "D_out", "L_in", "U_in", "D_in".

  Args:
    min_neighbors: Minimum number of neighbors a grid cell will have. For
      instance, if min_neighbors=2 then the schema will only have types for
      cells that are connected to at least 2 other cells.

  Returns:
    Schema describing the maze.
  """
  maze_schema = {}
  for (has_l, has_r, has_u, has_d) in itertools.product([False, True],
                                                        repeat=4):
    if np.count_nonzero([has_l, has_r, has_u, has_d]) < min_neighbors:
      continue

    name = (f"cell_{'L' if has_l else 'x'}{'R' if has_r else 'x'}"
            f"{'U' if has_u else 'x'}{'D' if has_d else 'x'}")
    node_schema = graph_types.NodeSchema([], [])
    for direction, used in (
        ("L", has_l),
        ("R", has_r),
        ("U", has_u),
        ("D", has_d),
    ):
      if used:
        node_schema.in_edges.append(graph_types.InEdgeType(direction + "_in"))
        node_schema.out_edges.append(
            graph_types.OutEdgeType(direction + "_out"))

    maze_schema[graph_types.NodeType(name)] = node_schema
  return maze_schema


def encode_maze(
    maze):
  """Encode a boolean mask array as a graph.

  We assume a [row, col]-indexed coordinate system, oriented so that going right
  corresponds to changing indexes as (0, +1), and going down corresponds to
  changing indies as (+1, 0).

  Args:
    maze: Maze, as a boolean array <bool[width, height]>, where True corresponds
      to cells that should be nodes in the graph.

  Returns:
    Encoded graph, along with a list of the coordinate indices of each cell in
    the graph.
  """
  # (direction, reverse direction, (dr, dc))
  shifts = [
      ("L", "R", (0, -1)),
      ("R", "L", (0, 1)),
      ("U", "D", (-1, 0)),
      ("D", "U", (1, 0)),
  ]
  graph = {}
  idx_to_cell = []
  for i in range(maze.shape[0]):
    for j in range(maze.shape[1]):
      if maze[i, j]:
        typename = "cell_"
        out_edges = {}
        for name, in_name, (di, dj) in shifts:
          ni = i + di
          nj = j + dj
          if (0 <= ni < maze.shape[0] and 0 <= nj < maze.shape[1] and
              maze[ni, nj]):
            typename = typename + name
            out_edges[graph_types.OutEdgeType(f"{name}_out")] = [
                graph_types.InputTaggedNode(
                    graph_types.NodeId(f"cell_{ni}_{nj}"),
                    graph_types.InEdgeType(f"{in_name}_in"))
            ]
          else:
            typename = typename + "x"
        graph[graph_types.NodeId(f"cell_{i}_{j}")] = graph_types.GraphNode(
            graph_types.NodeType(typename), out_edges)
        idx_to_cell.append((i, j))

  return graph, idx_to_cell
