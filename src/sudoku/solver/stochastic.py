# #!/usr/bin/env python3
# # -*- coding:utf-8 -*-

# import numpy as np

# x = "500670084407000630068000701000000209050980460679042518105869047796400852003720096"
# y = "532671984417298635968534721384156279251987463679342518125869347796413852843725196"


# shape = (9, 9)

# grid = np.asarray(list(x), dtype=np.uint8).reshape(shape)
# frozen = grid != 0

# allocate = np.random.randint(1, 9, shape)
# allocate[frozen] = grid[frozen]
# print(allocate, grid)

# """

#     https://en.wikipedia.org/wiki/Simulated_annealing#Pseudocode


# """


# # class StochasticSolver(Solver):
# #     def solve(self) -> bool:
# #         return False
# #         # return self._backtrack(self.grid, 0, self.validator)


# # with open(file="examples.csv", mode="r") as fp:
# #     problems = fp.readlines()


# # grid = [Grid(x) for x in problems][0]

# # print(grid)
