class Cell():
    def __init__(self, value=None):
        self.value = value


class EmptyCell(Cell):
    def __init__(self, location):
        super().__init__()
        self.location = location
        self.domain = [1,2,3,4,5,6,7,8,9]
        self.visited_domain=[None,None,None,None,None,None,None,None,None]
        self.constraining_cells = []
        self.constraining_values = {1: 0, 2: 0,
                                    3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
        self.visited = False

    def set_value(self, value):
        self.value = value
        for cell in self.constraining_cells+[self]:
            cell.visited_domain[value-1] = True
        self.visited = True

    def reset_value(self):
        for cell in self.constraining_cells+[self]:
            cell.visited_domain[self.value-1] = False
        self.value = None
        self.visited = False


class SetCell(Cell):
    def __init__(self, value):
        super().__init__(value)


class Board():
    def __init__(self, board):
        self.board = board
        self.variables = []

    def set_variables(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == None:
                    self.board[i][j] = EmptyCell((i, j))
                    self.variables.append(self.board[i][j])
                else:
                    self.board[i][j] = SetCell(self.board[i][j])

    def set_constraints(self):
        # row constraint
        for i in range(9):
            present = []
            for j in range(9):
                if type(self.board[i][j]) == SetCell:
                    present.append(self.board[i][j].value)
            for j in range(9):
                if type(self.board[i][j]) == EmptyCell:
                    for value in [1,2,3,4,5,6,7,8,9]:
                        if value in present and value in self.board[i][j].domain:
                            self.board[i][j].domain.remove(value)

        # column constraint
        for i in range(9):
            present = []
            for j in range(9):
                if type(self.board[j][i]) == SetCell:
                    present.append(self.board[j][i].value)
            for j in range(9):
                if type(self.board[j][i]) == EmptyCell:
                    for value in [1,2,3,4,5,6,7,8,9]:
                        if value in present and value in self.board[j][i].domain:
                            self.board[j][i].domain.remove(value)

        # quadrant constraint
        for i in range(3):
            for j in range(3):
                present = []
                for k in range(3):
                    for l in range(3):
                        if type(self.board[3*i+k][3*j+l]) == SetCell:
                            present.append(self.board[3*i+k][3*j+l].value)
                for k in range(3):
                    for l in range(3):
                        if type(self.board[3*i+k][3*j+l]) == EmptyCell:
                            for value in [1,2,3,4,5,6,7,8,9]:
                                if value in present and value in self.board[3*i+k][3*j+l].domain:
                                    self.board[3*i+k][3*j+l].domain.remove(value)

    def set_constraining_cells(self):
        # rowwise
        for i in range(9):
            constraining_cells = []
            for j in range(9):
                if type(self.board[i][j]) == EmptyCell:
                    constraining_cells.append(self.board[i][j])
            for j in range(9):
                if type(self.board[i][j]) == EmptyCell:
                    for cell in constraining_cells:
                        if cell.location != self.board[i][j].location and cell not in self.board[i][j].constraining_cells:
                            self.board[i][j].constraining_cells.append(cell)
        # columnwise
        for i in range(9):
            constraining_cells = []
            for j in range(9):
                if type(self.board[j][i]) == EmptyCell:
                    constraining_cells.append(self.board[j][i])
            for j in range(9):
                if type(self.board[j][i]) == EmptyCell:
                    for cell in constraining_cells:
                        if cell.location != self.board[j][i].location and cell not in self.board[j][i].constraining_cells:
                            self.board[j][i].constraining_cells.append(cell)
        # quadrantwise
        for i in range(3):
            for j in range(3):
                constraining_cells = []
                for k in range(3):
                    for l in range(3):
                        if type(self.board[3*i+k][3*j+l]) == EmptyCell:
                            constraining_cells.append(self.board[3*i+k][3*j+l])
                for k in range(3):
                    for l in range(3):
                        if type(self.board[3*i+k][3*j+l]) == EmptyCell:
                            for cell in constraining_cells:
                                if cell.location != self.board[3*i+k][3*j+l].location and cell not in self.board[3*i+k][3*j+l].constraining_cells:
                                    self.board[3*i+k][3*j +
                                                      l].constraining_cells.append(cell)

    def set_constraining_values(self):
        for variable in self.variables:
            for value in variable.domain:
                for cell in variable.constraining_cells:
                    if value in cell.domain:
                        variable.constraining_values[value] += 1

    def validate_board(self):
        # validate rows
        for i in range(9):
            present = set()
            for j in range(9):
                present.add(self.board[i][j].value)
            if len(present) != 9:
                return False
        # validate columns
        for i in range(9):
            present = set()
            for j in range(9):
                present.add(self.board[j][i].value)
            if len(present) != 9:
                return False
        # validate quadrants
        for i in range(3):
            for j in range(3):
                present = set()
                for k in range(3):
                    for l in range(3):
                        present.add(self.board[3*i+k][3*j+l].value)
                if len(present) != 9:
                    return False
        print("board is validated")
    
    def preprocess(self):
        self.set_variables()
        self.set_constraining_cells()
        self.set_constraining_values()
        self.variables.sort(key=lambda cell: (
            len(cell.domain), -len(cell.constraining_cells)))
        for cell in self.variables:
            cell.domain.sort(key=lambda value: cell.constraining_values[value])
        self.set_constraints()
    
    def display(self):
        board=[]
        for i in range(9):
            board.append([])
            for j in range(9):
                if self.board[i][j].value:
                    board[i].append(self.board[i][j].value)
                else:
                    board[i].append(0)
        for i in range(9):
            print(board[i])
    
    def show_stuff(self):
        for variable in self.variables:
            print(variable.location)
            print(variable.domain)
            print(len(variable.constraining_cells))
            for cell in variable.constraining_cells:
                print(cell.location)
            print(variable.constraining_values)
            print(variable.visited_domain)

    def solve(self):
        self.preprocess()
        if self.backtracking():
            self.display()
        return True

    def debug(self):
        self.preprocess()
        self.backtracking(debug=1)

    def backtracking(self, depth=0, debug=0):
        if debug:
            input()
            print(depth)
        if len([cell for cell in filter(lambda cell:not cell.visited, self.variables)]) == 0:
            if self.validate_board():
                return True
            else:
                return False

        if depth in []:
            for variable in filter(lambda variable:not variable.visited,self.variables):
                if len([unvisited_value for unvisited_value in filter(lambda value:not variable.visited_domain[value-1] and variable.constraining_values[value],variable.domain)]) == 0:
                    print("forward checking useful")
                    return False
            print("forward checking useless")
        for cell in self.variables:
            if not cell.visited:
                for value in cell.domain:
                    if not cell.visited_domain[value-1]:
                        if debug:
                            self.show_stuff()
                            print("set location ",cell.location," to value ",value)
                        cell.set_value(value)
                        if debug:
                            self.display()
                        if self.backtracking(depth+1, debug=debug):
                            return True
                        cell.reset_value()
                        if debug:
                            print("reset location ",cell.location)
        return False


Board([[None, 7, 1, 4, None, None, None, 3, None],
       [None, None, None, None, 7, None, None, None, 8],
       [9, None, None, 2, None, None, 4, None, None],
       [3, None, None, 9, None, None, 8, None, None],
       [None, None, 5, None, None, None, 1, None, None],
       [None, None, 7, None, None, 3, None, None, 5],
       [None, None, 2, None, None, 6, None, None, 9],
       [6, None, None, None, 8, None, None, None, None],
       [None, 1, None, None, None, 2, 7, 8, None]]).debug()
