from sys import argv
from getkey import getkey

def parse_game(game_file_path: str) -> dict:
    game = {}
    height = -1
    coord_cars = {}
    cars = []
    car_name = []
    max_moves = ""
    with open(game_file_path) as file:

        game['width'] = len(file.readline().strip()) - 2
        for line in file:
            height += 1
            width = -2
            for char in line.strip():
                width += 1
                if char.isalpha():
                    if char not in coord_cars:
                        coord_cars[char] = [(width, height)]
                    else:
                        coord_cars[char].append((width, height))
                elif char.isnumeric():
                    max_moves += char
        max_moves = int(max_moves)
        """game['max_moves'] = max_moves"""
        #sort the cars by alphabetical order
        for car in coord_cars:
            car_name.append(car)
        car_name.sort()
        for car in car_name:
            x,y = coord_cars[car][0]
            x2,y2 = coord_cars[car][1]
            if x != x2:
                sens = "h"
            elif y != y2:
                sens = "v"
            cars.append([coord_cars[car][0],sens, len(coord_cars[car])])
        """game['cars'] = cars"""
        #ni +1 ni -1 car ligne déja lue s'égalise avec ligne max_move
        game['height'] = height - 1
        game['cars'] = cars
        game['max_moves'] = max_moves
    return game

def valid_direction(game,car_index,direction):
    direction_dic = {"h": ["LEFT","RIGHT"],"v": ["UP","DOWN"]}
    car_direction = game["cars"][car_index][1]
    if direction in direction_dic[car_direction]:
        return True
    return False

def valid_move(car_index,coordinates,direction,game):
    front_position = {"UP":0,"DOWN":-1,"LEFT":0,"RIGHT":-1}
    car_front = coordinates[car_index][front_position[direction]]
    x,y = car_front
    if direction == "UP":
        for cars in coordinates:
            if (x, y - 1) in cars or y - 1 < 0:
                return False
    elif direction == "DOWN":
        for cars in coordinates:
            if (x, y + 1) in cars or y + 1 >= game["height"]:
                return False
    elif direction == "LEFT":
        for cars in coordinates:
            if (x - 1, y) in cars or x - 1 < 0:
                return False
    elif direction == "RIGHT":
        for cars in coordinates:
            if (x + 1, y) in cars or x + 1 >= game["width"]:
                return False
    return True

def car_attribute(game):
    cars_list = []
    car_index = 0
    for car in game["cars"]:
        car_name = chr(ord("A") + car_index)
        x,y = car[0]
        if car_index == 0:
            color = "\u001b[47m"
        else:
            for i in range(6,0,-1):
                if (car_index % 6) % i == 0:
                    color = f"\u001b[4{i}m"
                    break

        cars_coord = [car_name,color, car[0]]

        if car[1] == "h":
            for i in range(car[2] - 1):
                x = x + 1
                cars_coord.append((x,y))
        elif car[1] == "v":
            for i in range(car[2] - 1):
                y = y + 1
                cars_coord.append((x,y))
        car_index += 1
        cars_list.append(cars_coord)
    return cars_list

def car_coordinates(game):
    attributes = car_attribute(game)
    for cars in attributes:
        for i in range(2):
            cars.remove(cars[0])
    return attributes

def move_car(game: dict, car_index: int, direction: str) -> bool:
    coordinates = car_coordinates(game)
    move_dico = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}
    if car_index >= len(coordinates):
        print("ERROR: Selected car does not exist")
        return False
    if valid_direction(game,car_index,direction):
        if valid_move(car_index,coordinates,direction,game):
            x, y = game['cars'][car_index][0]
            x_move, y_move = move_dico[direction]
            game['cars'][car_index][0] = (x + x_move, y + y_move)
            return True
        else:
            print("ERROR: Invalid move")
            return False
    print("ERROR: Invalid direction")
    return False

def get_game_str(game: dict, current_move_number: int) -> str:
    corner = "+"
    walls = "-"
    map = ""
    borders = corner + (game["width"] * walls) + corner
    map += borders + "\n"
    black_text = "\033[30m"
    no_color = "\u001b[0m"
    cars_list = car_attribute(game)
    for i in range(game["height"]):
        map += "|"
        is_white = False
        for j in range(game["width"]):
            is_car = False
            for car in cars_list:
                if (j,i) in car:
                    if car[0] == 'A':
                        is_white = True
                        is_car = True
                        map += black_text + car[1] + car[0] + no_color
                    else:
                        map += car[1] + car[0] + no_color
                        is_car = True
            if is_car == False:
                map += "."
        if is_white is False:
            map += "|"
        map += "\n"
    map += borders + "\n"
    map += f"Move {current_move_number}/{game['max_moves']}\n"
    map += f"{game['max_moves'] - current_move_number} moves left."
    return map

def car_select(game,car=None):
    mvmnt = ["UP","DOWN","LEFT","RIGHT"]
    key = str(getkey())
    if len(key) == 1 and key.isalpha():
        print(f"car {key.upper()} selected")
        return car_select(game,key)
    elif key in mvmnt and car is not None:
        return car, key
    elif key in mvmnt and car is None:
        print("ERROR: No car selected")
        return car_select(game,None)
    elif key == "ESCAPE":
        return None, key
    else:
        print("ERROR: Invalid key")
        return car_select(game,None)

def is_win(game: dict) -> bool:
    x, y = main_car = game["cars"][0][0]
    main_car_length = game["cars"][0][2]
    victory_position = (game["width"] - main_car_length, y)
    if main_car != victory_position:
        return False
    else:
        return True

def play_game(game: dict) -> int:
    car = None
    i = 0
    while i < game["max_moves"] and is_win(game) is False:
        car,direction = car_select(game,car)
        if direction == "ESCAPE":
            end_code = 2
            break
        car_index = ord(car.upper()) - ord('A')
        if move_car(game,car_index,direction):
            i += 1
            is_win(game)
        current_move_number = i
        print(get_game_str(game, current_move_number))
    if i == game["max_moves"] :
        end_code = 1
    if is_win(game):
        end_code = 0
    return end_code

if __name__ == "__main__":
    game = parse_game(argv[1])
    current_move_number = 0
    print(get_game_str(game, current_move_number))
    ending = play_game(game)
    if ending == 0:
        print("You Won!! \nCongrats!!")
    elif ending == 1:
        print("GAME OVER: You lost! (no moves left).")
    elif ending == 2:
        print("GAME OVER: Game Forfeited!")
