
from copy import deepcopy
import unittest
from unittest.mock import patch

from ulbloque import *


TEST_GAME_GAME = {
    'width': 6,
    'height': 6,
    'max_moves': 40,
    'cars': (
        [(0, 2), 'h', 2],  # Voiture A
        [(2, 0), 'v', 3],  # Voiture B
        [(3, 0), 'h', 3],  # Voiture C
        [(0, 3), 'v', 2],  # Voiture D
        [(3, 3), 'h', 2],  # Voiture E
        [(5, 3), 'v', 3],  # Voiture F
        [(4, 4), 'v', 2],  # Voiture G
        [(1, 5), 'h', 3]   # Voiture H
    )
}

TEST_GAME_SOLUTION_1_SEQUENCE = ('D', 'DOWN', 'E', 'LEFT', 'E', 'LEFT', 'E', 'LEFT', 'B', 'DOWN', 'B', 'DOWN', 'F', 'UP', 'F', 'UP', 'G', 'UP', 'G', 'UP', 'G', 'UP', 'C', 'LEFT', 'C', 'LEFT', 'G', 'UP', 'H', 'RIGHT', 'H', 'RIGHT', 'B', 'DOWN', 'A', 'RIGHT', 'A', 'RIGHT', 'A', 'RIGHT', 'B', 'UP', 'H', 'LEFT', 'F', 'DOWN', 'F', 'DOWN', 'A', 'RIGHT')
"""Always pick car first then direction"""
TEST_GAME_SOLUTION_2_SEQUENCE = ('D', 'DOWN', 'E', 'LEFT', 'LEFT', 'LEFT', 'B', 'DOWN', 'DOWN', 'F', 'UP', 'UP', 'G', 'UP', 'UP', 'UP', 'C', 'LEFT', 'LEFT', 'G', 'UP', 'H', 'RIGHT', 'RIGHT', 'B', 'DOWN', 'A', 'RIGHT', 'RIGHT', 'RIGHT', 'B', 'UP', 'H', 'LEFT', 'F', 'DOWN', 'DOWN', 'A', 'RIGHT')
"""Continous move (using previous car)"""
TEST_GAME_SOLUTION_3_SEQUENCE = ('B', 'B', 'DOWN', 'B', 'DOWN', 'D', 'DOWN', 'B', 'UP', 'B', 'UP', 'E', 'LEFT', 'E', 'LEFT', 'E', 'LEFT', 'E', 'G', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'DOWN', 'C', 'LEFT', 'F', 'UP', 'F', 'UP', 'F', 'UP', 'G', 'UP', 'G', 'UP', 'G', 'UP', 'H', 'RIGHT', 'H', 'RIGHT', 'B', 'DOWN', 'DOWN', 'A', 'RIGHT', 'RIGHT', 'G', 'DOWN', 'DOWN', 'F', 'DOWN', 'DOWN', 'A', 'RIGHT', 'B', 'UP', 'H', 'LEFT', 'F', 'UP', 'F', 'UP', 'F', 'F', 'DOWN', 'F', 'DOWN', 'F', 'DOWN', 'A', 'RIGHT')
"""Realistic play with car collisions, backtracking and OOB moves"""

TEST_GAME_SOLUTION_1_CAR_POSITIONS = (
 ((0, 2), (2, 0), (3, 0), (0, 3), (3, 3), (5, 3), (4, 4), (1, 5)),
 ((0, 2), (2, 0), (3, 0), (0, 4), (3, 3), (5, 3), (4, 4), (1, 5)),
 ((0, 2), (2, 0), (3, 0), (0, 4), (2, 3), (5, 3), (4, 4), (1, 5)),
 ((0, 2), (2, 0), (3, 0), (0, 4), (1, 3), (5, 3), (4, 4), (1, 5)),
 ((0, 2), (2, 0), (3, 0), (0, 4), (0, 3), (5, 3), (4, 4), (1, 5)),
 ((0, 2), (2, 1), (3, 0), (0, 4), (0, 3), (5, 3), (4, 4), (1, 5)),
 ((0, 2), (2, 2), (3, 0), (0, 4), (0, 3), (5, 3), (4, 4), (1, 5)),
 ((0, 2), (2, 2), (3, 0), (0, 4), (0, 3), (5, 2), (4, 4), (1, 5)),
 ((0, 2), (2, 2), (3, 0), (0, 4), (0, 3), (5, 1), (4, 4), (1, 5)),
 ((0, 2), (2, 2), (3, 0), (0, 4), (0, 3), (5, 1), (4, 3), (1, 5)),
 ((0, 2), (2, 2), (3, 0), (0, 4), (0, 3), (5, 1), (4, 2), (1, 5)),
 ((0, 2), (2, 2), (3, 0), (0, 4), (0, 3), (5, 1), (4, 1), (1, 5)),
 ((0, 2), (2, 2), (2, 0), (0, 4), (0, 3), (5, 1), (4, 1), (1, 5)),
 ((0, 2), (2, 2), (1, 0), (0, 4), (0, 3), (5, 1), (4, 1), (1, 5)),
 ((0, 2), (2, 2), (1, 0), (0, 4), (0, 3), (5, 1), (4, 0), (1, 5)),
 ((0, 2), (2, 2), (1, 0), (0, 4), (0, 3), (5, 1), (4, 0), (2, 5)),
 ((0, 2), (2, 2), (1, 0), (0, 4), (0, 3), (5, 1), (4, 0), (3, 5)),
 ((0, 2), (2, 3), (1, 0), (0, 4), (0, 3), (5, 1), (4, 0), (3, 5)),
 ((1, 2), (2, 3), (1, 0), (0, 4), (0, 3), (5, 1), (4, 0), (3, 5)),
 ((2, 2), (2, 3), (1, 0), (0, 4), (0, 3), (5, 1), (4, 0), (3, 5)),
 ((3, 2), (2, 3), (1, 0), (0, 4), (0, 3), (5, 1), (4, 0), (3, 5)),
 ((3, 2), (2, 2), (1, 0), (0, 4), (0, 3), (5, 1), (4, 0), (3, 5)),
 ((3, 2), (2, 2), (1, 0), (0, 4), (0, 3), (5, 1), (4, 0), (2, 5)),
 ((3, 2), (2, 2), (1, 0), (0, 4), (0, 3), (5, 2), (4, 0), (2, 5)),
 ((3, 2), (2, 2), (1, 0), (0, 4), (0, 3), (5, 3), (4, 0), (2, 5)),
 ((4, 2), (2, 2), (1, 0), (0, 4), (0, 3), (5, 3), (4, 0), (2, 5))
)
"""Expected car positions at each move of the game (index of the tuple = number of moves)"""

TEST_GAME_SOLUTION_3_CAR_POSITIONS = (
 ((0, 2), (2, 0), (3, 0), (0, 3), (3, 3), (5, 3), (4, 4), (1, 5)),
 ((0, 2), (2, 1), (3, 0), (0, 3), (3, 3), (5, 3), (4, 4), (1, 5)),
 ((0, 2), (2, 2), (3, 0), (0, 3), (3, 3), (5, 3), (4, 4), (1, 5)),
 ((0, 2), (2, 2), (3, 0), (0, 4), (3, 3), (5, 3), (4, 4), (1, 5)),
 ((0, 2), (2, 1), (3, 0), (0, 4), (3, 3), (5, 3), (4, 4), (1, 5)),
 ((0, 2), (2, 0), (3, 0), (0, 4), (3, 3), (5, 3), (4, 4), (1, 5)),
 ((0, 2), (2, 0), (3, 0), (0, 4), (2, 3), (5, 3), (4, 4), (1, 5)),
 ((0, 2), (2, 0), (3, 0), (0, 4), (1, 3), (5, 3), (4, 4), (1, 5)),
 ((0, 2), (2, 0), (3, 0), (0, 4), (0, 3), (5, 3), (4, 4), (1, 5)),
 ((0, 2), (2, 1), (3, 0), (0, 4), (0, 3), (5, 3), (4, 4), (1, 5)),
 ((0, 2), (2, 1), (2, 0), (0, 4), (0, 3), (5, 3), (4, 4), (1, 5)),
 ((0, 2), (2, 1), (2, 0), (0, 4), (0, 3), (5, 2), (4, 4), (1, 5)),
 ((0, 2), (2, 1), (2, 0), (0, 4), (0, 3), (5, 1), (4, 4), (1, 5)),
 ((0, 2), (2, 1), (2, 0), (0, 4), (0, 3), (5, 0), (4, 4), (1, 5)),
 ((0, 2), (2, 1), (2, 0), (0, 4), (0, 3), (5, 0), (4, 3), (1, 5)),
 ((0, 2), (2, 1), (2, 0), (0, 4), (0, 3), (5, 0), (4, 2), (1, 5)),
 ((0, 2), (2, 1), (2, 0), (0, 4), (0, 3), (5, 0), (4, 1), (1, 5)),
 ((0, 2), (2, 1), (2, 0), (0, 4), (0, 3), (5, 0), (4, 1), (2, 5)),
 ((0, 2), (2, 1), (2, 0), (0, 4), (0, 3), (5, 0), (4, 1), (3, 5)),
 ((0, 2), (2, 2), (2, 0), (0, 4), (0, 3), (5, 0), (4, 1), (3, 5)),
 ((0, 2), (2, 3), (2, 0), (0, 4), (0, 3), (5, 0), (4, 1), (3, 5)),
 ((1, 2), (2, 3), (2, 0), (0, 4), (0, 3), (5, 0), (4, 1), (3, 5)),
 ((2, 2), (2, 3), (2, 0), (0, 4), (0, 3), (5, 0), (4, 1), (3, 5)),
 ((2, 2), (2, 3), (2, 0), (0, 4), (0, 3), (5, 0), (4, 2), (3, 5)),
 ((2, 2), (2, 3), (2, 0), (0, 4), (0, 3), (5, 0), (4, 3), (3, 5)),
 ((2, 2), (2, 3), (2, 0), (0, 4), (0, 3), (5, 1), (4, 3), (3, 5)),
 ((2, 2), (2, 3), (2, 0), (0, 4), (0, 3), (5, 2), (4, 3), (3, 5)),
 ((3, 2), (2, 3), (2, 0), (0, 4), (0, 3), (5, 2), (4, 3), (3, 5)),
 ((3, 2), (2, 2), (2, 0), (0, 4), (0, 3), (5, 2), (4, 3), (3, 5)),
 ((3, 2), (2, 2), (2, 0), (0, 4), (0, 3), (5, 2), (4, 3), (2, 5)),
 ((3, 2), (2, 2), (2, 0), (0, 4), (0, 3), (5, 1), (4, 3), (2, 5)),
 ((3, 2), (2, 2), (2, 0), (0, 4), (0, 3), (5, 0), (4, 3), (2, 5)),
 ((3, 2), (2, 2), (2, 0), (0, 4), (0, 3), (5, 1), (4, 3), (2, 5)),
 ((3, 2), (2, 2), (2, 0), (0, 4), (0, 3), (5, 2), (4, 3), (2, 5)),
 ((3, 2), (2, 2), (2, 0), (0, 4), (0, 3), (5, 3), (4, 3), (2, 5)),
 ((4, 2), (2, 2), (2, 0), (0, 4), (0, 3), (5, 3), (4, 3), (2, 5))
)

class TestULBloqueComplex(unittest.TestCase):
    def assertGameCarPositionEqual(self, game_car_computed:tuple, expected_cars_positions:tuple, message:str=None):
        self.assertEqual(len(game_car_computed), len(expected_cars_positions), "nombre de voitures incorrect")
        for i, car_pos_expected in enumerate(expected_cars_positions):
            car_computed = game_car_computed[i]
            self.assertTupleEqual(car_computed[0], car_pos_expected, f"{message}: position de la voiture d'index {i} incorrect")

    def assertPlayGameEqual(self, sequence:tuple, expected_cars_positions:tuple=None, expected_return:int=0, game:dict=None):
        """Compare the result of play_game with a sequence"""
        def mock_get_game_str(game, moves):
            res = original_get_game_str(game, moves)

            # Check if the cars are in the expected position at each step of the game
            if expected_cars_positions is not None:
                self.assertGameCarPositionEqual(game['cars'], expected_cars_positions[moves], f'problème de position des voitures au mouvement {moves}')

            return res

        if game is None:
            game = deepcopy(TEST_GAME_GAME)

        try:
            # Keep the original get_game_str function as we will patch it but wand to keep default behavior
            original_get_game_str = get_game_str
            with patch('ulbloque.getkey', side_effect=sequence) as mock_getkey, patch('ulbloque.get_game_str', mock_get_game_str):
                self.assertEqual(play_game(game), expected_return, f"La partie s'est terminée mais le jeu n'a pas retourné le bon code de fin ({expected_return})")
                
                # Check if the game was not prematurly ended
                try:
                    get_key_counter = 0
                    while mock_getkey() and get_key_counter < len(sequence):
                        get_key_counter += 1
                except StopIteration:
                    if get_key_counter > 0:
                        played, left = sequence[:-get_key_counter], sequence[-get_key_counter:]
                        self.fail(f"La partie s'est terminée prématurément!\nSéquence déjà jouée: {played}\nSéquence qui aurait dû être encore jouée pour finir la partie: {left}")

                # Check if the cars are in the expected position at the end of the game
                if expected_cars_positions is not None:
                    self.assertGameCarPositionEqual(game['cars'], expected_cars_positions[-1])

        except StopIteration:
            self.fail(f"Le jeu à demandé une direction/voiture alors que la partie devrait être terminée. Séquence de touches: {sequence}")
        except AssertionError:
            raise
        except Exception as e:
            self.fail(f"Une erreur innatendue est survenue lors de la simulation de la partie: {e}")
            raise

    def test_play_game_car_then_move(self):
        self.assertPlayGameEqual(TEST_GAME_SOLUTION_1_SEQUENCE, TEST_GAME_SOLUTION_1_CAR_POSITIONS)

    def test_play_game_continous_move(self):
        self.assertPlayGameEqual(TEST_GAME_SOLUTION_2_SEQUENCE, TEST_GAME_SOLUTION_1_CAR_POSITIONS)

    def test_play_game_realistic_gameplay(self):
        self.assertPlayGameEqual(TEST_GAME_SOLUTION_3_SEQUENCE, TEST_GAME_SOLUTION_3_CAR_POSITIONS)

    def test_play_game_basic_collision(self):
        self.assertPlayGameEqual(tuple(['A'] + ['RIGHT']*6) + TEST_GAME_SOLUTION_1_SEQUENCE, TEST_GAME_SOLUTION_1_CAR_POSITIONS)

    def test_play_game_exceed_move_numbers(self):
        self.assertPlayGameEqual(tuple(['F'] + ['UP', 'DOWN']*20), expected_return=1)


if __name__ == '__main__':
    unittest.main()
