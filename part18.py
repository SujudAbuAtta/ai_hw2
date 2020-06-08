from MapsGenerator import ai_board
import numpy as np
from HeavyAlphaBetaPlayer import HeavyAlphaBetaPlayer
from LiteAlphaBetaPlayer import LiteAlphaBetaPlayer
import matplotlib.pyplot as plt

min_seconds = 1
max_seconds = 15
num_samples = 15


fig = plt.figure()
ax1 = fig.add_subplot(111)
times = []
depths = []

for t in np.linspace(min_seconds, max_seconds, num_samples):
    player = HeavyAlphaBetaPlayer()
    player.set_game_params(ai_board.copy())
    d = player.make_move(t)
    times.append(t)
    depths.append(d)
ax1.plot(times, depths, c='r', label="HeavyAlphaBetaPlayer")
plt.xlabel('Time')
plt.ylabel('Depth')
plt.legend(loc='upper left')
plt.show()

#
# fig2 = plt.figure()
# times = []
# depths = []
#
# for t in np.linspace(min_seconds, max_seconds, num_samples):
#     player = HeavyAlphaBetaPlayer()
#     player.set_game_params(ai_board.copy())
#     d = player.make_move(t)
#     times.append(t)
#     depths.append(d)
# ax1.plot(times, depths, c='g', label="HeavyAlphaBetaPlayer")
# plt.xlabel('Time')
# plt.ylabel('Depth')
# plt.legend(loc='upper left')
# plt.show()