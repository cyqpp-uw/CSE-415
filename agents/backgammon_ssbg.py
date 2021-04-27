'''
Name(s): Kaijun Gao, Yunqian Cheng,
UW netid(s): kg52, cyqpp
'''

from game_engine import genmoves

class BackgammonPlayer:
    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()
        self.specialStaticEval = None
        self.maxPly = None
        self.setMaxPly()
        # feel free to create more instance variables as needed.

    # TODO: return a string containing your UW NETID(s)
    # For students in partnership: UWNETID + " " + UWNETID
    def nickname(self):
        return "kg52 cyqpp"

    # Given a ply, it sets a maximum for how far an agent
    # should go down in the search tree. Count the chance nodes
    # as a ply too!
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
    # the state.whose_move
    # Keep in mind: a player can only pass if the player cannot move any checker with that role
    def move(self, state, die1, die2):
        player = state.whose_move
        result = self.expectimax(state, self.maxPly, player, False, die1, die2)[0]
        if result is None:
            return "p"
        else:
            return result[0]


    def expectimax(self, state, ply_left, player, random, die1, die2):
        # if ply == 0: return None and static evaluation
        if ply_left == 0:
            if not self.specialStaticEval:
                return None, self.staticEval(state)
            else:
                return None, self.specialStaticEval(state)

        # If player is randomizer, find the expected evaluations based on possibilities.
        if random:
            expect_value = 0

            # for each dice combination, find the average evaluation of the moves, divide by 36 and add to total.
            for d1 in range(1, 7):
                for d2 in range(1, 7):
                    self.initialize_move_gen_for_state(state, player, d1, d2)
                    moves = self.get_all_possible_moves()
                    evals = []
                    if moves[0] != 'p':
                        for move in moves:
                            new_state = move[1]
                            eval = self.expectimax(new_state, ply_left - 1, 1 - player, True, d1, d2)[1]
                            evals.append(eval)
                        # average evaluation score for each dice combinations
                        expect_value += (sum(evals) / len(evals)) / 36

            return None, expect_value

        # If player is maximizer or minimizer, generate all the moves possible for current state
        else:
            self.initialize_move_gen_for_state(state, player, die1, die2)
            moves = self.get_all_possible_moves()

            # keeps track of the static evaluation from each new state
            evals = []

            # if not pass, find the static evaluation for each move and add it to the list
            if moves[0] != 'p':
                for move in moves:
                    new_state = move[1]
                    # player input here = -1 because every level should return exp-value except for the first one,
                    # where we pick the maximum or minimum
                    eval = self.expectimax(new_state, ply_left - 1, 1 - player, True, die1, die2)[1]
                    evals.append(eval)

                # find the optimal move and return move, static evaluation pair
                # if player == -1 -> return None, the average value of the evals
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
                    increment += n * i * 0.8 ** (n - 2)
                else:
                    increment -= n * (23 - i) * 0.8 ** (n - 2)
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

    '''Another static eval design, doesn't work as good as the one above'''
    ''' 
    def staticEval(self, state):
        score = 0
        white = 0
        red = 0

        for i in state.bar:
            if i == 0:
                score -= 20
            else:
                score += 20

        score += len(state.white_off) * 30
        score -= len(state.red_off) * 30

        for i in (0, 23, 1):
            for j in state.pointLists[i]:
                if j == 0:
                    if len(state.pointLists[i]) >= 2:
                        score += 10
                    white = 24 - i
                else:
                    if len(state.pointLists[i]) >= 2:
                        score -= 10
                    red = i + 1
        score = score - white + red
        return score

'''
