'''
Name(s):
UW netid(s):
'''

from game_engine import genmoves
import math


class BackgammonPlayer:
    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()
        self.specialStaticEval = None
        self.prune = False
        self.maxPly = None
        self.setMaxPly()
        self.states = 0
        self.cutoffs = 0
        # feel free to create more instance variables as needed.

    # For students in partnership: UWNETID + " " + UWNETID
    def nickname(self):
        return "kg52 cyqpp"

    # If prune==True, then your Move method should use Alpha-Beta Pruning
    # otherwise Minimax
    def useAlphaBetaPruning(self, prune=False):
        self.prune = prune
        self.states = 0
        self.cutoffs = 0

    # Returns a tuple containing the number explored
    # states as well as the number of cutoffs.
    def statesAndCutoffsCounts(self):
        return self.states, self.cutoffs

    # Given a ply, it sets a maximum for how far an agent
    # should go down in the search tree. maxply=2 indicates that
    # our search level will go two level deep.
    def setMaxPly(self, maxply=2):
        self.maxPly = maxply

    # If not None, it update the internal static evaluation
    # function to be func
    def useSpecialStaticEval(self, func):
        self.specialStaticEval = func

    def initialize_move_gen_for_state(self, state, who, die1, die2):
        self.move_generator = self.GenMoveInstance.gen_moves(state, who, die1, die2)

    def get_all_possible_moves(self):
        """Uses the mover to generate all legal moves. Returns an array of move commands & new_states pair"""
        move_list = []
        done_finding_moves = False
        any_non_pass_moves = False
        while not done_finding_moves:
            try:
                m = next(self.move_generator)    # Gets a (move, state) pair.
                # print("next returns: ",m[0]) # Prints out the move.    For debugging.
                if m[0] != 'p':
                    any_non_pass_moves = True
                    move_list.append([m[0], m[1]])    # Add the move and the state to the list.
            except StopIteration as e:
                done_finding_moves = True
        if not any_non_pass_moves:
            move_list.append('p')
        return move_list

    # Given a state and a roll of dice, it returns the best move for
    # the state.whose_move.
    # Keep in mind: a player can only pass if the player cannot move any checker with that role
    def move(self, state, die1=1, die2=6):
        # TODO: return a move for the current state and for the current player.
        # Hint: you can get the current player with state.whose_move
        player = state.whose_move

        # result is a move, state pair
        if self.prune:
            result = self.alpha_beta(state, self.maxPly, player, -math.inf, math.inf, die1, die2)[0]
        else:
            result = self.minimax(state, self.maxPly, player, die1, die2)[0]

        if result is None:
            return "p"
        else:
            return result[0]

    # Minimax, return the best move and its static evaluation
    def minimax(self, state, ply_left, player, die1, die2):
        # if ply == 0: return None and static evaluation
        if ply_left == 0:
            if not self.specialStaticEval:
                return None, self.staticEval(state)
            else:
                return None, self.specialStaticEval(state)

        # generate all the moves possible for current state
        self.initialize_move_gen_for_state(state, player, die1, die2)
        moves = self.get_all_possible_moves()

        # keeps track of the static evaluation from each new state
        evals = []

        # if not pass, find the static evaluation for each move and add it to the list
        if moves[0] != 'p':
            for move in moves:
                new_state = move[1]
                evals.append(self.minimax(new_state, ply_left - 1, 1 - player, die1, die2)[1])
                self.states += 1
            # find the optimal move and return move, static evaluation pair
            if player == 0:
                return moves[evals.index(max(evals))], max(evals)
            else:
                return moves[evals.index(min(evals))], min(evals)
        # if pass, return the current state and static evaluation
        else:
            if not self.specialStaticEval:
                return None, self.staticEval(state)
            else:
                return None, self.specialStaticEval(state)

    def alpha_beta(self, state, ply_left, player, alpha, beta, die1, die2):
        # if ply == 0: return None and static evaluation
        if ply_left == 0:
            if not self.specialStaticEval:
                return None, self.staticEval(state)
            else:
                return None, self.specialStaticEval(state)

        # generate all the moves possible for current state
        self.initialize_move_gen_for_state(state, player, die1, die2)
        moves = self.get_all_possible_moves()

        # keeps track of the static evaluation from each new state
        evals = []
        # if not pass, find the static evaluation for each move and add it to the list
        if moves[0] != 'p':
            for move in moves:
                new_state = move[1]
                eval = self.alpha_beta(new_state, ply_left - 1, 1 - player, alpha, beta, die1, die2)[1]
                self.states += 1
                evals.append(eval)

                # update alpha/beta
                if player == 0:
                    alpha = max(alpha, eval)
                else:
                    beta = min(beta, eval)
                # check cutoff
                if beta <= alpha:
                    self.cutoffs += 1
                    break

            # find the optimal move and return move, static evaluation pair
            if player == 0:
                return moves[evals.index(max(evals))], max(evals)
            else:
                return moves[evals.index(min(evals))], min(evals)
        # if pass, return the current state and static evaluation
        else:
            if not self.specialStaticEval:
                return None, self.staticEval(state)
            else:
                return None, self.specialStaticEval(state)


    # Hint: Look at game_engine/boardState.py for a board state properties you can use.
    def staticEval(self, state):
        # Let position be i, number of checkers on the position be n
        pointLists = state.pointLists
        result = 0
        for i in range(len(pointLists)):
            increment = 0
            white = False
            n = len(pointLists[i])
            # if no checkers, continue loop
            if n == 0:
                continue
            if pointLists[i][0] == 0:
                white = True

            # If n = 1, result += n * i
            # If n = 2, result += n * i * 2
            # If n > 2, result += n * i * 0.9 (avoid high stacking)
            if n == 1:
                if white:
                    increment += n * i
                else:
                    increment -= n * (23 - i)
            elif n == 2:
                if white:
                    increment += n * i * 2
                else:
                    increment -= n * (23 - i) * 2
            else:
                if white:
                    increment += n * i * 0.8 ** (n-2)
                else:
                    increment -= n * (23 - i) * 0.8 ** (n-2)
            result += increment

        for b in state.bar:
            if b == 0:
                result -= 50
            else:
                result += 50

        # For each bare offed checker, plus or minus 100
        result += len(state.white_off) * 100
        result -= len(state.red_off) * 100

        return result