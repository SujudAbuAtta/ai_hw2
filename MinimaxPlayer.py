def get_other_player(player: int) -> int:
    assert player ==1 or player == 2
    return 1 if player == 2 else 2


class MinimaxPlayer:
    def __init__(self):
        self.loc = None
        self.board = None
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.opp_loc = None

    def set_game_params(self, board):
        self.board = board
        for i, row in enumerate(board):
            for j, val in enumerate(row):
                if val == 1:
                    self.loc = (i, j)
                if val == 2:
                    self.opp_loc = (i, j)

    def set_rival_move(self, loc):
        self.board[self.opp_loc] = -1
        self.opp_loc = loc
        self.board[loc] = 2

    def get_player_loc(self, player: int):
        return self.loc if player == 1 else self.opp_loc

    def calc_heuristic_val(self):
        return 0

    def get_legal_moves(self, player: int):  # returns the direction!
        loc = self.get_player_loc(player)
        for d in self.directions:
            i = loc[0] + d[0]
            j = loc[1] + d[1]
            if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and self.board[i][j] == 0:  # then move is legal
                yield d

    def apply_move(self, player: int, move: (int, int)):
        assert move in self.get_legal_moves(player)
        old_loc = self.get_player_loc(player)
        new_loc = old_loc[0] + move[0], old_loc[1] + move[1]
        self.board[new_loc] = player
        self.board[old_loc] = -1

    def undo_move(self, player: int, move: (int, int)):
        curr_loc = self.get_player_loc(player)
        prev_loc = curr_loc[0] - move[0], curr_loc[1] - move[1]
        self.board[curr_loc] = 0
        self.board[prev_loc] = [player]

    def 

    def minimax(self, player: int, depth: int) -> (float, (int, int)):
        if depth == 0 :
            return self.calc_heuristic_val()
        if player == 1:  # my turn
            cur_max = -float('inf')
            best_move = None
            for move in self.get_legal_moves(player):
                self.apply_move(player, move)
                res = self.minimax(2, depth-1)
                if res > cur_max:
                    cur_max = res
                    best_move = move
                self.undo_move(player, move)
            assert best_move is not None #other wise would not get to here
            return cur_max, best_move
        else:  #opponent's turn
            cur_min = float('inf')
            worst_move = None
            for move in self.get_legal_moves(player):
                self.apply_move(player, move)
                res = self.minimax(1, depth-1)
                if res<cur_min:
                    cur_min = res
                    worst_move = move
                self.undo_move(2, move)
            assert worst_move is not None #other wise would not get to here
            return cur_min, worst_move