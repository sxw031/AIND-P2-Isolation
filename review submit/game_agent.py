"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
import sys


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    return heuristic3(game, player)

def heuristic1(game, player):
    """
    This is heuristic one, it simply returns the difference in number of legal moves left between the players.
    If `player` and its opponent have the same number of moves, then the returned value is zero.
    If the returned value is positive (negative), then `player` is doing better(worse) than its opponent.
    If the returned value is "inf" ("-inf"), then `player` has won (lost) the game.
    """

    # have we won the game?
    if game.is_winner(player):
        return float("inf")
    # do we have moves to play?
    if game.is_loser(player):
        return float("-inf")

    # we have moves to play. How many more than our opponent?
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(own_moves - opp_moves)

def heuristic2(game, player):
    """Outputs a score equal to the difference in the number of moves
    available to the two players, while penalizing the moves for the
    maximizing player that are against the wall and rewarding the moves
    for the minimizing player that are against the wall. Not submitted.
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    own_v_wall = [move for move in own_moves if move[0] == 0
                                             or move[0] == (game.height - 1)
                                             or move[1] == 0
                                             or move[1] == (game.width - 1)]

    opp_moves = game.get_legal_moves(game.get_opponent(player))
    opp_v_wall = [move for move in opp_moves if move[0] == 0
                                             or move[0] == (game.height - 1)
                                             or move[1] == 0
                                             or move[1] == (game.width - 1)]
    
    # Penalize/reward move count if some moves are against the wall
    return float(len(own_moves) - len(own_v_wall)
                 - len(opp_moves) + len(opp_v_wall))

def heuristic3(game, player):
    """
    In this heuristic, the more moves `player` has available from the evaluated position, the better, but not all
    starting positions are equal. If a player's position is closer to the center of the board, it is more probable that
    this player can do better than a player whose remaining moves are near the edge of the board (where they will have
    less options to move down the line). If there is no clear positional advantage (i.e. both players are at the same
    distance from the center, then we measure the longest run of moves that can be performed inside the 3x3 squares
    defined by the starting position and each of its legal moves left. The longest run one can hope to reach is 7.
    If the returned value is positive (negative), then `player` is doing better (worse) than its opponent.
    If the returned value is "inf" ("-inf"), then `player` has won (lost) the game.
    """

    # Have we won the game?
    if game.is_winner(player):
        return float("inf")

    # Do we even have moves to play?
    if game.is_loser(player):
        return float("-inf")

    # We have moves to play. How many more than our opponent?
    player_moves_left = len(game.get_legal_moves(player))
    opponent_moves_left = len(game.get_legal_moves(game.get_opponent(player)))

    if player_moves_left != opponent_moves_left:
        return float(player_moves_left - opponent_moves_left)

    else:
        # If we have the same number of moves available, look for a positional advantage.
        # Use the Manhattan distance to the center of the board to assess positional advantage.
        center_y_pos, center_x_pos = int(game.height / 2), int(game.width / 2)
        player_y_pos, player_x_pos = game.get_player_location(player)
        opponent_y_pos, opponent_x_pos = game.get_player_location(game.get_opponent(player))
        player_distance = abs(player_y_pos - center_y_pos) + abs(player_x_pos - center_x_pos)
        opponent_distance = abs(opponent_y_pos - center_y_pos) + abs(opponent_x_pos - center_x_pos)

        return float(opponent_distance - player_distance) / 10.

class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)  This parameter should be ignored when iterative = True.

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).  When True, search_depth should
        be ignored and no limit to search depth.

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            DEPRECATED -- This argument will be removed in the next release

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        if not legal_moves:
            return (-1,-1)

        result = None

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if self.iterative:
                if self.method == "minimax":
                    for depth in range(sys.maxsize):
                        _, move = self.minimax(game, depth)
                        result = move
                if self.method == "alphabeta":
                    for depth in range(sys.maxsize):
                        _, move = self.alphabeta(game, depth)
                        result = move
            else:
                if self.method == "minimax":
                    _, result = self.minimax(game, self.search_depth)
                if self.method == "alphabeta":
                    _, result = self.alphabeta(game, self.search_depth)

        except Timeout:
            # Handle any actions required at timeout, if necessary
            pass

        # Return the best move from the last completed search iteration
        return result

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # Get legal moves for active player
        legal_moves = game.get_legal_moves()

        # Game over terminal test
        if not legal_moves:
            # -inf or +inf from point of view of maximizing player
            return game.utility(self), (-1, -1)

        # Search depth reached terminal test
        if depth == 0:
            # Heuristic score from point of view of maximizing player
            return self.score(game, self), (-1, -1)

        best_move = None
        if maximizing_player:
            # Best for maximizing player is highest score
            best_score = float("-inf")
            for move in legal_moves:
                # Forecast_move switches the active player
                next_state = game.forecast_move(move)
                score, _ = self.minimax(next_state, depth - 1, False)
                if score > best_score:
                    best_score, best_move = score, move
        
        # Else minimizing player
        else:
            # Best for minimizing player is lowest score
            best_score = float("inf")
            for move in legal_moves:
                next_state = game.forecast_move(move)
                score, _ = self.minimax(next_state, depth - 1, True)
                if score < best_score:
                    best_score, best_move = score, move
        return best_score, best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # Get legal moves for active player
        legal_moves = game.get_legal_moves()

        # Game over terminal test
        if not legal_moves:
            # -inf or +inf from point of view of maximizing player
            return game.utility(self), (-1, -1)

        # Search depth reached terminal test
        if depth == 0:
            # Heuristic score from point of view of maximizing player
            return self.score(game, self), (-1, -1)

        # Alpha is the maximum lower bound of possible solutions
        # Alpha is the highest score so far ("worst" highest score is -inf)
        
        # Beta is the minimum upper bound of possible solutions
        # Beta is the lowest score so far ("worst" lowest score is +inf)

        best_move = None
        if maximizing_player:
            # Best for maximizing player is highest score
            best_score = float("-inf")
            for move in legal_moves:
                # Forecast_move switches the active player
                next_state = game.forecast_move(move)
                score, _ = self.alphabeta(next_state, depth - 1, alpha, beta, False)
                if score > best_score:
                    best_score, best_move = score, move
                # Prune if possible
                if best_score >= beta:
                    return best_score, best_move
                # Update alpha, if necessary
                alpha = max(alpha, best_score)
        
        # Else minimizing player
        else:
            # Best for minimizing player is lowest score
            best_score = float("inf")
            for move in legal_moves:
                next_state = game.forecast_move(move)
                score, _ = self.alphabeta(next_state, depth - 1, alpha, beta, True)
                if score < best_score:
                    best_score, best_move = score, move
                # Prune if possible
                if best_score <= alpha:
                    return best_score, best_move
                # Update beta, if necessary
                beta = min(beta, best_score)
        return best_score, best_move
