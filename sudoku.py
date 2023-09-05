class Cell():
    def __init__(self, value=None):
        self.value = value


class DomainValue():
    def __init__(self, value):
        self.value = value
        self.visited = False


class EmptyCell(Cell):
    def __init__(self, location):
        super().__init__()
        self.location = location
        self.domain = [DomainValue(1), DomainValue(2), DomainValue(3), DomainValue(
            4), DomainValue(5), DomainValue(6), DomainValue(7), DomainValue(8), DomainValue(9)]
        self.constraining_cells = []
        self.constraining_values = {1: 0, 2: 0,
                                    3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
        self.visited = False

    def set_value(self, value):
        self.value = value
        for cell in self.constraining_cells+[self]:
            for domain_value in cell.domain:
                if domain_value.value == value:
                    domain_value.visited == True
                    break
        self.visited = True

    def reset_value(self):
        for cell in self.constraining_cells+[self]:
            for domain_value in cell.domain:
                if domain_value.value == self.value:
                    domain_value.visited == False
                    break
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
                    for n in present:
                        if n in self.board[i][j].domain:
                            self.board[i][j].domain.remove(n)

        # column constraint
        for i in range(9):
            present = []
            for j in range(9):
                if type(self.board[j][i]) == SetCell:
                    present.append(self.board[j][i].value)
            for j in range(9):
                if type(self.board[j][i]) == EmptyCell:
                    for n in present:
                        if n in self.board[j][i].domain:
                            self.board[j][i].domain.remove(n)

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
                            for n in present:
                                if n in self.board[3*i+k][3*j+l].domain:
                                    self.board[3*i+k][3*j+l].domain.remove(n)

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

    def solve(self):
        self.set_variables()
        self.set_constraints()
        self.set_constraining_cells()
        self.set_constraining_values()
        self.variables.sort(key=lambda cell: (
            len(cell.domain), -len(cell.constraining_cells)))
        for cell in self.variables:
            cell.domain.sort(key=lambda domain_value: cell.constraining_values[domain_value.value])
        if self.backtracking():
            for i in range(9):
                for j in range(9):
                    self.board[i][j] = self.board[i][j].value
            for i in range(9):
                print(self.board[i])
        return True

    def debug(self):
        self.set_variables()
        self.set_constraints()
        self.set_constraining_cells()
        self.set_constraining_values()
        self.variables.sort(key=lambda cell: (
            len(cell.domain), -len(cell.constraining_cells)))
        for cell in self.variables:
            cell.domain.sort(key=lambda domain_value: cell.constraining_values[domain_value.value])
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

        if depth == 1:
            for variable in self.variables:
                if not variable.visited and len([unvisited_domain_value for unvisited_domain_value in filter(lambda domain_value:not domain_value.visited,variable.domain)]) == 0:
                    print("forward checking useful")
                    return False
            print("forward checking useless")
        for cell in self.variables:
            if not cell.visited:
                for domain_value in cell.domain:
                    if not domain_value.visited:
                        # if debug:
                        #     print("set location ",cell.location," to value ",value)
                        cell.set_value(domain_value.value)
                        if self.backtracking(depth+1, debug=debug):
                            return True
                        cell.reset_value()
                        # if debug:
                        #     print("reset location ",cell.location)
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
