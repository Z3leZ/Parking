
from copy import deepcopy
import unittest
from unittest.mock import patch, mock_open

from ulbloque import *

TEST_GAME_STR = """\
+------+
|..BCCC|
|..B...|
|AAB....
|D..EEF|
|D...GF|
|.HHHGF|
+------+
40
"""

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


class TestULBloque(unittest.TestCase):
    def assertGameEqual(self, game_computed:dict, game_expected:dict, msg:str=None):
        """Compare two games instance"""
        self.assertIn('width', game_computed, msg + "paramètre width manquant")
        self.assertIn('height', game_computed, msg + "paramètre height manquant")
        self.assertIn('max_moves', game_computed, msg + "paramètre max_moves manquant")
        self.assertEqual(game_computed['width'], game_expected['width'], msg + "width incorrect")
        self.assertEqual(game_computed['height'], game_expected['height'], msg + "height incorrect")
        self.assertEqual(game_computed['max_moves'], game_expected['max_moves'], msg + "max_moves incorrect")

        self.assertIn('cars', game_computed, msg + "paramètre cars manquant")
        game_car_computed, game_car_expected = game_computed['cars'], game_expected['cars']
        self.assertEqual(len(game_car_computed), len(game_car_expected), "nombre de voitures incorrect")
        for i, car_expected in enumerate(game_car_expected):
            car_computed = game_car_computed[i]
            self.assertListEqual(car_computed, car_expected, msg + f"voiture d'index {i} incorrecte")

    def test_parse_game(self):
        with patch("builtins.open", mock_open(read_data=TEST_GAME_STR)):
            print(f"Note: Pour le test `test_parse_game` le jeu n'est pas parsé depuis un fichier, mais depuis la string: \n\"\"\"{TEST_GAME_STR}\"\"\"")
            game = parse_game('dummy.txt')
        self.assertGameEqual(game, TEST_GAME_GAME, "Le jeu parsé n'est pas correct: ")

    def test_get_game_str(self):
        game = deepcopy(TEST_GAME_GAME)
        game_str = get_game_str(game, 36)
        for car_name in "ABCDEFGH":
            self.assertIn(car_name, game_str, f"La voiture {car_name} n'est pas affichée")
        self.assertIn("\u001b[47m", game_str, "Il n'y a pas de couleur de fond blanc (prévue pour la voiture A)")
        self.assertIn("\u001b[41m", game_str, "Il n'y a pas de couleur de fond rouge (prévue pour la voiture B et H)")
        self.assertIn("\u001b[46m", game_str, "Il n'y a pas de couleur de fond cyan (prévue pour la voiture G)")
        self.assertIn("36", game_str, "Le nombre de mouvements courrant n'est pas affiché")
        self.assertIn("40", game_str, "Le nombre de mouvements maximal n'est pas affiché")

    def test_move_car(self):
        game = deepcopy(TEST_GAME_GAME)
        move_car(game, 1, 'DOWN')
        self.assertTupleEqual(game['cars'][1][0], (2, 1), "Les coordonnées de la voiture B ne sont pas correctes. Elle aurait dû descendre en (2, 1)")
        move_car(game, 5, 'UP')
        self.assertTupleEqual(game['cars'][5][0], (5, 2), "Les coordonnées de la voiture F ne sont pas correctes. Elle aurait dû monter en (5, 2)")
        move_car(game, 2, 'LEFT')
        self.assertTupleEqual(game['cars'][2][0], (2, 0), "Les coordonnées de la voiture C ne sont pas correctes. Elle aurait dû aller à gauche en (2, 0)")
        move_car(game, 2, 'RIGHT')
        self.assertTupleEqual(game['cars'][2][0], (3, 0), "Les coordonnées de la voiture C ne sont pas correctes. Elle aurait dû aller à droite en (3, 0)")

    def test_move_car_advanced(self):
        game = deepcopy(TEST_GAME_GAME)
        car_A_ind = 0
        car_A_pos = game['cars'][car_A_ind][0]
        self.assertTupleEqual(car_A_pos, (0, 2), "Les coordonnées de la voiture A ne sont pas correctes. Elle aurait dû commencer en (0, 2)")
        for direction in ('UP', 'RIGHT', 'DOWN', 'LEFT'):
            # Toutes les directions ne devraient pas changer la position de la voiture A, car, soit elle est bloquée par une autre voiture, soit elle sort du plateau, soit elle est incohérente avec la direction de la voiture
            move_car(game, car_A_ind, direction)
            self.assertTupleEqual(car_A_pos, (0, 2), f"Les coordonnées de la voiture A ne sont pas correctes. Elle aurait dû rester en (0, 2) pour la direction '{direction}'")

    def test_is_win(self):
        game = deepcopy(TEST_GAME_GAME)
        self.assertFalse(is_win(game), "La partie est déjà gagnée en début de partie alors qu'elle ne devrait pas l'être")
        # On va "tricher" en téléportant la voiture A pour gagner plus facilement
        game['cars'][0][0] = (3, 2)
        self.assertFalse(is_win(game), "La partie ne devrait pas être gagnée avec A en (3, 2)")
        game['cars'][0][0] = (4, 2)
        self.assertTrue(is_win(game), "La partie n'est pas gagnée alors qu'elle devrait l'être (voiture A téléportée en (4, 2))")

    def test_play_game(self):
        try:
            play_game  # Vérifie si la fonction play_game existe
            print("Note: La fonction play_game est testée en profondeur dans le fichier test_ulbloque_extra.py")
        except NameError:
            self.fail("La fonction play_game n'existe pas")


if __name__ == '__main__':
    unittest.main()
