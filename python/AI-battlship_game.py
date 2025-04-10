import random

SIZE = 5

EMPTY = '.'
SHIP = 'X'
HIT = '*'
MISS = 'O'

class Board:
    def __init__(self):
        self.board = [[EMPTY] * SIZE for _ in range(SIZE)]
        self.ships = []

    def place_ship(self, ship_size, x, y, direction):
        """Размещаем корабль на поле."""
        if direction == 'H': 
            for i in range(ship_size):
                self.board[y][x + i] = SHIP
        elif direction == 'V': 
            for i in range(ship_size):
                self.board[y + i][x] = SHIP
        self.ships.append((ship_size, x, y, direction))

    def print_board(self, show_ships=False):
        """Выводим поле на экран."""
        print("  " + " ".join([str(i) for i in range(SIZE)]))
        for y in range(SIZE):
            row = str(y) + " "
            for x in range(SIZE):
                if show_ships and self.board[y][x] == SHIP:
                    row += SHIP + " "
                else:
                    row += self.board[y][x] + " "
            print(row)

    def is_game_over(self):
        """Проверяем, остались ли корабли на поле."""
        for row in self.board:
            if SHIP in row:
                return False
        return True

    def make_move(self, x, y):
        """Делаем ход, проверяя попадание в корабль."""
        if self.board[y][x] == SHIP:
            self.board[y][x] = HIT
            return True
        elif self.board[y][x] == EMPTY:
            self.board[y][x] = MISS
            return False
        return None

class Game:
    def __init__(self):
        self.player_board = Board()
        self.computer_board = Board()
        self.computer_visible_board = Board()

    def place_computer_ships(self):
        """Размещаем корабли компьютера случайным образом."""
        ships = [3, 2, 2, 1, 1]  
        for ship_size in ships:
            placed = False
            while not placed:
                direction = random.choice(['H', 'V'])
                x = random.randint(0, SIZE - 1)
                y = random.randint(0, SIZE - 1)
                if direction == 'H' and x + ship_size <= SIZE:
                    placed = True
                    for i in range(ship_size):
                        if self.computer_board.board[y][x + i] == SHIP:
                            placed = False
                            break
                    if placed:
                        self.computer_board.place_ship(ship_size, x, y, direction)
                elif direction == 'V' and y + ship_size <= SIZE:
                    placed = True
                    for i in range(ship_size):
                        if self.computer_board.board[y + i][x] == SHIP:
                            placed = False
                            break
                    if placed:
                        self.computer_board.place_ship(ship_size, x, y, direction)

    def place_player_ships(self):
        """Пользователь размещает свои корабли вручную."""
        ships = [3, 2, 2, 1, 1]
        for ship_size in ships:
            placed = False
            while not placed:
                print(f"Размещение корабля размером {ship_size}")
                self.player_board.print_board(show_ships=True)
                x, y, direction = self.get_player_input()
                if self.is_valid_move(x, y, direction, ship_size, self.player_board):
                    self.player_board.place_ship(ship_size, x, y, direction)
                    placed = True
                else:
                    print("Некорректный ход, попробуйте снова.")

    def get_player_input(self):
        """Получаем ввод от игрока."""
        x = int(input("Введите координату X: "))
        y = int(input("Введите координату Y: "))
        direction = input("Введите направление (H - горизонтально, V - вертикально): ").upper()
        return x, y, direction

    def is_valid_move(self, x, y, direction, ship_size, board):
        """Проверяем, можно ли разместить корабль на данном месте."""
        if direction == 'H':
            if x + ship_size > SIZE:
                return False
            for i in range(ship_size):
                if board.board[y][x + i] == SHIP:
                    return False
        elif direction == 'V':
            if y + ship_size > SIZE:
                return False
            for i in range(ship_size):
                if board.board[y + i][x] == SHIP:
                    return False
        return True

    def player_turn(self):
        """Ход игрока."""
        print("Ход игрока")
        self.computer_visible_board.print_board(show_ships=False)
        x, y = self.get_player_input_for_attack()
        hit = self.computer_board.make_move(x, y)
        if hit:
            print("Попадание!")
        else:
            print("Мимо!")

    def computer_turn(self):
        """Ход компьютера."""
        print("Ход компьютера")
        x = random.randint(0, SIZE - 1)
        y = random.randint(0, SIZE - 1)
        print(f"Компьютер атакует {x}, {y}")
        hit = self.player_board.make_move(x, y)
        if hit:
            print("Компьютер попал!")
        else:
            print("Компьютер промахнулся.")

    def get_player_input_for_attack(self):
        """Получаем координаты для атаки от игрока."""
        x = int(input("Введите координату X для атаки: "))
        y = int(input("Введите координату Y для атаки: "))
        return x, y

    def play(self):
        """Запуск игры."""
        self.place_computer_ships()
        self.place_player_ships()

        while True:
            self.player_turn()
            if self.computer_board.is_game_over():
                print("Вы выиграли!")
                break
            self.computer_turn()
            if self.player_board.is_game_over():
                print("Вы проиграли!")
                break

if __name__ == "__main__":
    game = Game()
    game.play()
