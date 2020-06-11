import time

big_int = 1000000
class ContestPlayer:
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

    def get_other_player(self, player: int):
        return 1 if player == 2 else 2

    def calc_heuristic_val(self) -> float:
        legal_moves_num = self.legal_moves_num(1)
        return -legal_moves_num if legal_moves_num > 0 else -5

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
        new_loc = (old_loc[0] + move[0]), (old_loc[1] + move[1])
        self.board[new_loc] = player
        self.board[old_loc] = -1
        if player == 1:
            self.loc = new_loc
        else:
            self.opp_loc = new_loc

    def undo_move(self, player: int, move: (int, int)):
        curr_loc = self.get_player_loc(player)
        prev_loc = (curr_loc[0] - move[0]), (curr_loc[1] - move[1])
        self.board[curr_loc] = 0
        self.board[prev_loc] = player
        if player == 1:
            self.loc = prev_loc
        else:
            self.opp_loc = prev_loc

    """
    checks if game ended for player
    returns:
    true in case game ended else false
    the last 2 return values are relevant for game end case only
    game result: -1 is player lost, 0 if tie, 1 if winning
    move to make: if winning or tie then don't make a move, if winning then make a winning move
    """

    def game_ended(self, player: int) -> (bool, int, (int, int)):
        if not self.has_moves(player):
            if not self.has_moves(self.get_other_player(player)):  # tie
                return True, 0, (0, 0)
            return True, -1, (0, 0)  # player lost

        #  check winning
        assert self.has_moves(player)
        if not self.has_moves(self.get_other_player(player)):
            winning_move = self.get_final_winning_move(player)
            # print("looks like player " + str(player) + " winning, my winning move is " + str(self.get_player_loc(player)))
            if winning_move is None:  # all coming moves will bring a tie
                return True, 0, self.get_random_legal_move(player)
            # there is a way to win
            return True, 1, winning_move

        return False, -2, (-2, -2)

    def get_random_legal_move(self, player):
        assert self.has_moves(player)
        for m in self.get_legal_moves(player):
            return m

    def has_time(self, deadline_time):
        return time.time() < deadline_time

    def has_moves(self, player):
        for _ in self.get_legal_moves(player):
            return True
        return False

    def legal_moves_num(self, player):
        return sum(1 for _ in self.get_legal_moves(player))

    def get_final_winning_move(self, player: int) -> (int, int):
        assert self.has_moves(player)
        winning_move = None
        for move in self.get_legal_moves(player):
            self.apply_move(player, move)
            if self.has_moves(player):
                winning_move = move
            self.undo_move(player, move)
        return winning_move

    def AlphaBeta(self, player: int, depth: int, deadline_time, alpha, beta) -> (float, (int, int)):
        game_ended, utility, move = self.game_ended(player)

        if game_ended:
            # print("in this move game for player " + str(player) + " ends with utiity " + str(utility))
            if utility == 1:
                if player == 1:
                    return big_int, move
                return -big_int, move
            if utility == -1:
                if player == 1:
                    return -big_int, move
                return big_int, move
            return 0, move

        # assuming we have at least one sec, and function in never called when player has lost -> will always find another move
        if depth == 0 or not self.has_time(deadline_time):
            return self.calc_heuristic_val(), self.get_random_legal_move(player)

        if player == 1:  # my turn
            cur_max = -float('inf')
            best_move = None
            for move in self.get_legal_moves(player):
                self.apply_move(player, move)
                res = (self. AlphaBeta(2, depth - 1, deadline_time, alpha, beta))[0]
                if res > cur_max:
                    cur_max = res
                    best_move = move
                self.undo_move(player, move)
                alpha = max(alpha,cur_max)
                if(cur_max >= beta):
                    break
            assert best_move is not None  # other wise would not get to here
            return cur_max, best_move
        else:  # opponent's turn
            cur_min = float('inf')
            worst_move = None
            for move in self.get_legal_moves(player):
                self.apply_move(player, move)
                res = (self. AlphaBeta(1, depth - 1, deadline_time, alpha, beta))[0]
                if res < cur_min:
                    cur_min = res
                    worst_move = move
                self.undo_move(2, move)
                beta = min(beta,cur_min)
                if(cur_min <= alpha):
                    break
            assert worst_move is not None  # other wise would not get to here
            return cur_min, worst_move

    def make_move(self, player_time) -> (int, int):
        deadline_time = player_time + time.time() - 0.2
        depth = 0
        move = None
        alpha = -float('inf')
        beta = float('inf')
        while self.has_time(deadline_time) and depth < self.board.size:
            move = self. AlphaBeta(1, depth, deadline_time, alpha, beta)[1]
            depth += 1
        new_loc = self.loc[0] + move[0], self.loc[1] + move[1]
        self.board[self.loc] = -1
        self.board[new_loc] = 1
        self.loc = new_loc
        return move
