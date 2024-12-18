from csp import Constraint, Variable

class ShipBoardConstraint(Constraint):
    def __init__(self, name, scope, board):
        Constraint.__init__(self, name, scope)
        self._name = "Ship_" + name
        self._board = board

    def check(self):
        assignment = ''

        for v in self.scope():
            if v.isAssigned():
                assignment = v.getValue()
            else:
                return True
        return self._board.update_board(assignment, v.name())

class Board:
    def __init__(self, board_info):
        self._rCnstr = []
        self._cCnstr = []
        self._sCnstr = []
        self._size = int
        self._undokeys = []
        self._undoDict = dict()
        self._rowPoints = list
        self._colPoints = list
        self._sCnstr = list
        self._board = list
        self._ships = dict()
        self.initialize_board(board_info)

    def get_board(self):
        return self._board

    def get_size(self):
        return self._size

    def get_rowC(self):
        return self._rCnstr

    def get_colC(self):
        return self._cCnstr

    def get_shipC(self):
        return self._sCnstr

    def print_board(self):
        for r in range(self._size):
            print("".join(self._board[r * self._size:(r + 1) * self._size]))
        print('\n')

    def remove_last_points(self):
        key = self._undokeys.pop()
        for i in self._undoDict[key]:
            self._board[i] = '0'
        del self._undoDict[key]
        for point in self._ships.keys():
            if self._ships[point] == key:
                del self._ships[point]
                break


    def add_ship(self, points, key):
        if key != 'init' and key != 'zero':
            for ship in self._ships.keys():
                if ship == points:
                    return False
                elif set(self.get_points(ship)) & set(self.get_points(points)):
                    return False
            self._ships[points] = key
        return True

    def count_rows(self):
        self._rowPoints = [0] * self._size
        for r in range(self._size):
            for c in range(self._size):
                if self._board[r * self._size + c] != '0' and self._board[r * self._size + c] != '.':
                    self._rowPoints[r] += 1

    def count_cols(self):
        self._colPoints = [0] * self._size
        for r in range(self._size):
            for c in range(self._size):
                if self._board[r * self._size + c] != '0' and self._board[r * self._size + c] != '.':
                    self._colPoints[c] += 1

    def get_points(self, point):
        if point[0] == point[1]:
            return [point[0]]

        x = point[1] % self._size - point[0] % self._size
        y = point[1] // self._size - point[0] // self._size
        points = []

        if x <= y:
            for n in range(x + 1):
                points.extend(range(point[0] + n, point[0] + n + (y + 1) * self._size, self._size))
        else:
            for n in range(y + 1):
                points.extend(range(point[0] + n * self._size, point[0] + (x + 1) + n * self._size))
        return points

    def initialize_board(self, board_info):
        self._size = len(board_info[0])
        for i in range(self._size):
            self._rCnstr.append(int(board_info[0][i]))
            self._cCnstr.append(int(board_info[1][i]))
        self._sCnstr = [int(i) for i in board_info[2]]
        self._board = [coord for row in board_info[3:] for coord in row]
        self.solve_board((0,0),'zero')
        for point in range(len(self._board)):
            if self._board[point] != '0' and self._board[point] != '.':
                self.update_board((point, point), 'init')


    def update_board(self, points, key):
        if not key in self._undoDict:
            self._undokeys.append(key)
            self._undoDict[key] = []
        if not self.add_ship(points, key):
            return False
        if points[0] == points[1]:
            if self._board[points[0]] == '0' or  self._board[points[0]] == 'S':
                self._board[points[0]] = 'S'
                self._undoDict[key].append(points[0])
            else:
                return False
        else:
            if points[1] - points[0] < self._size:
                if self._board[points[0]] == '0':
                    self._board[points[0]] = '<'
                    self._undoDict[key].append(points[0])
                elif not(self._board[points[0]] == '<'):
                    return False
                if self._board[points[1]] == '0':
                    self._board[points[1]] = '>'
                    self._undoDict[key].append(points[1])
                elif not(self._board[points[1]] == '>'):
                    return False
                for i in range(points[1] - points[0] - 1):
                    if self._board[points[0] + i + 1] == '0':
                        self._board[points[0] + i + 1] = 'M'
                        self._undoDict[key].append(points[0] + i + 1)
                    elif not(self._board[points[0] + i + 1] == 'M'):
                        return False
            else:
                if self._board[points[0]] == '0':
                    self._board[points[0]] = '^'
                    self._undoDict[key].append(points[0])
                elif not(self._board[points[0]] == '^'):
                    return False
                if self._board[points[1]] == '0':
                    self._board[points[1]] = 'v'
                    self._undoDict[key].append(points[1])
                elif not(self._board[points[1]] == 'v'):
                    return False
                for i in range((points[1] - points[0]) // self._size - 1):
                    if self._board[points[0] + (i + 1) * self._size] == '0':
                        self._board[points[0] + (i + 1) * self._size] = 'M'
                        self._undoDict[key].append(points[0] + (i + 1) * self._size)
                    elif not(self._board[points[0] + (i + 1) * self._size] == 'M'):
                        return False

        return self.solve_board(points, key)


    def solve_board(self, points, key):
        self.count_rows()
        self.count_cols()
        for i in range(self._size):
            if self._rowPoints[i] > self._rCnstr[i] or self._colPoints[i] > self._cCnstr[i]:
                return False
            if self._rowPoints[i] == self._rCnstr[i]:
                if not key in self._undoDict:
                    self._undokeys.append(key)
                    self._undoDict[key] = []
                for j in range(i * self._size, (i + 1) * self._size):
                    if self._board[j] == '0':
                        self._board[j] = '.'
                        self._undoDict[key].append(j)
            if self._colPoints[i] == self._cCnstr[i]:
                if not key in self._undoDict:
                    self._undokeys.append(key)
                    self._undoDict[key] = []
                for j in range(i, self._size ** 2, self._size):
                    if self._board[j] == '0':
                        self._board[j] = '.'
                        self._undoDict[key].append(j)
        if key != 'zero':
            i, f = points[0], points[1]
            i = i if i - self._size < 0 else i - self._size
            i = i if i % self._size - 1 < 0 else i - 1
            f = f + 1 if f % self._size + 1 < self._size else f
            f = f + self._size if f + self._size < self._size ** 2 else f
            water = [p for p in self.get_points((i, f)) if p not in self.get_points(points)]
            for w in water:
                if self._board[w] == '.':
                    pass
                elif self._board[w] == '0':
                    self._board[w] = '.'
                    self._undoDict[key].append(w)
                else:
                    return False
        return True


