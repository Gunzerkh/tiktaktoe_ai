import random
import numpy as np
import pickle

class TicTacToe:
    def __init__(self):
        self.board = [' ']*9
        self.winner = None

    def display_board(self):
        for i in range(0, 9, 3):
            print(f"{self.board[i]} | {self.board[i+1]} | {self.board[i+2]}")
            if i < 6:
                print("---------")

    def make_move(self, position, player):
        if self.board[position] == ' ':
            self.board[position] = player
            if self.check_win(player):
                self.winner = player
            return True
        return False
    
    def get_random_move(self):
        valid_moves = [i for i, spot in enumerate(self.board) if spot == ' ']
        return random.choice(valid_moves)

    def check_win(self, player, board=None):
        if board is None:
            board = self.board
        for combo in [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
                return True
        return False
    
    def get_winning_moves(self, player):
        winning_moves = []
        for i in range(9):
            if self.board[i] == ' ':
                new_board = self.board.copy()
                new_board[i] = player
                if self.check_win(player, new_board):
                    winning_moves.append(i)
        return winning_moves

    def is_draw(self):
        return ' ' not in self.board

class Node:
    def __init__(self, game, parent=None):
        self.game = game
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0

    def select_child(self):
        s = sorted(self.children, key=lambda c: c.wins/c.visits + np.sqrt(2*np.log(self.visits)/c.visits) if c.visits != 0 else -np.inf)[-1]
        return s

    def expand(self):
        for i in range(9):
            if self.game.board[i] == ' ':
                new_game = TicTacToe()
                new_game.board = self.game.board.copy()
                new_game.make_move(i, 'O')
                self.children.append(Node(new_game, self))

    def update(self, result):
        self.visits += 1
        self.wins += result

class TicTacToeAI:
    def __init__(self):
        self.record = {'win': 0, 'loss': 0, 'draw': 0}

    def get_move(self, game):
        # Block opponent's winning moves
        winning_moves = game.get_winning_moves('X')
        if winning_moves:
            return random.choice(winning_moves)
        root = Node(game)
        for _ in range(5000):  # Increase the number of simulations
            node = root
            while node.children:
                node = node.select_child()
            if node.game.winner is None and not node.game.is_draw():
                node.expand()
            while node:
                node.update(1 if node.game.winner == 'O' else 0)
                node = node.parent
        return [i for i, (new, old) in enumerate(zip(sorted(root.children, key=lambda c: c.visits)[-1].game.board, game.board)) if new != old][0]

    def update_record(self, game):
        if game.winner == 'O':
            self.record['win'] += 1
        elif game.winner == 'X':
            self.record['loss'] += 1
        else:
            self.record['draw'] += 1

class Simulation:
    def __init__(self, AI):
        self.AI = AI

    def play(self):
        game = TicTacToe()
        while game.winner is None and not game.is_draw():
            move = self.AI.get_move(game)
            game.make_move(move, 'O')
            if game.winner is not None or game.is_draw():
                break
            game.make_move(game.get_random_move(), 'X')
        self.AI.update_record(game)
        if game.winner == 'O':
            print("AI won the game!")
        elif game.winner == 'X':
            print("AI lost the game!")
        else:
            print("The game is a draw!")

def save_ai(ai, filename):
    with open(filename, 'wb') as f:
        pickle.dump(ai, f)

def load_ai(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def play_against_user(ai):
    game = TicTacToe()
    while game.winner is None and not game.is_draw():
        game.display_board()
        move = int(input("Enter your move (0-8): "))
        game.make_move(move, 'X')
        if game.winner is not None or game.is_draw():
            break
        move = ai.get_move(game)
        game.make_move(move, 'O')
    game.display_board()
    if game.winner == 'O':
        print("AI won the game!")
    elif game.winner == 'X':
        print("You won the game!")
    else:
        print("The game is a draw!")

if __name__ == "__main__":
#    AI = TicTacToeAI()
#    simulation = Simulation(AI)
#    total_games = 500
#    for i in range(total_games):
#        simulation.play()
#        if i != 0 and i % 10 == 0:  # Print accuracy every 10 games
#            current_win_rate = AI.record['win'] / (AI.record['win'] + AI.record['loss'])
#            print(f"After {i} games, current win rate (excluding draws): {current_win_rate}")
#    final_win_rate = AI.record['win'] / (AI.record['win'] + AI.record['loss'])
#    print("Final win rate (excluding draws): ", final_win_rate)
#    save_ai(AI, 'ai_data.pkl')
    loaded_ai = load_ai('ai_data.pkl')
    play_against_user(loaded_ai)