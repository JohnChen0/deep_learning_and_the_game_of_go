import argparse
import datetime
from collections import namedtuple

import h5py

from dlgo import agent
from dlgo import scoring
from dlgo import rl
from dlgo.goboard_fast import GameState, Player, Point


COLS = 'ABCDEFGHJKLMNOPQRST'
STONE_TO_CHAR = {
    None: '.',
    Player.black: 'x',
    Player.white: 'o',
}


def print_board(board):
    for row in range(BOARD_SIZE, 0, -1):
        line = []
        for col in range(1, BOARD_SIZE + 1):
            stone = board.get(Point(row=row, col=col))
            line.append(STONE_TO_CHAR[stone])
        print('%2d %s' % (row, ''.join(line)))
    print('   ' + COLS[:BOARD_SIZE])


class GameRecord(namedtuple('GameRecord', 'moves winner margin')):
    pass


def name(player):
    if player == Player.black:
        return 'B'
    return 'W'


def simulate_game(black_player, white_player):
    moves = []
    game = GameState.new_game(BOARD_SIZE)
    agents = {
        Player.black: black_player,
        Player.white: white_player,
    }
    while not game.is_over():
        next_move = agents[game.next_player].select_move(game)
        moves.append(next_move)
        game = game.apply_move(next_move)

    print_board(game.board)
    game_result = scoring.compute_game_result(game)
    print(game_result)

    return GameRecord(
        moves=moves,
        winner=game_result.winner,
        margin=game_result.winning_margin,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--board-size', type=int, default=9)
    parser.add_argument('--agent1', required=True)
    parser.add_argument('--agent2', required=True)
    parser.add_argument('--num-games', '-n', type=int, default=10)

    args = parser.parse_args()
    agent1_filename = args.agent1
    agent2_filename = args.agent2
    num_games = args.num_games
    global BOARD_SIZE
    BOARD_SIZE = args.board_size

    agent1 = rl.load_ac_agent(h5py.File(agent1_filename, 'r'))
    agent2 = rl.load_ac_agent(h5py.File(agent2_filename, 'r'))

    agent1_win = 0
    for i in range(args.num_games):
        print('Simulating game %d/%d...' % (i + 1, args.num_games))
        game_record = simulate_game(agent1, agent2)
        if game_record.winner == Player.black:
            agent1_win += 1

    print('Agent 1 won %d/%d times' % (agent1_win, args.num_games))


if __name__ == '__main__':
    main()
