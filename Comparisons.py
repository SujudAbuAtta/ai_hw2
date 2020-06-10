from MapsGenerator import ai_board
import numpy as np
from MinimaxPlayer import MinimaxPlayer
from AlphaBetaPlayer import AlphaBetaPlayer
from OrderedAlphaBetaPlayer import OrderedAlphaBetaPlayer
import matplotlib.pyplot as plt

# Configurations
names = ['AlphaBeta', 'OrderedAlphaBeta']
colors = ['g', 'b']
player_classes = [AlphaBetaPlayer, OrderedAlphaBetaPlayer]
min_seconds = 1
max_seconds = 25
num_samples = 25


fig = plt.figure()
ax1 = fig.add_subplot(111)
for name, color, player_class in zip(names, colors, player_classes):
    times = []
    depths = []
    for t in np.linspace(min_seconds, max_seconds, num_samples):
        player = player_class()
        player.set_game_params(ai_board.copy())
        d = player.make_move(t)
        times.append(t)
        depths.append(d)
    ax1.plot(times, depths, c=color, label=name)
plt.xlabel('Time')
plt.ylabel('Depth')
plt.legend(loc='upper left')
plt.show()
