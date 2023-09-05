import math
# raw board is given as 2d array of types of cells. the cells can be of type Empty, Black, Both, Row, or Col.
# Empty indicates an empty cell that can be filled with a number.
# Black indicates a black cell on the border that cannot be manipulated in any way.
# Both indicates a cell that has both a row total indicator and a column total indicator.
# Row indicates a cell that has only a row total indicator.
# Col indicates a cell that has only a column total indicator.


class Empty():
    def __init__(self):
        pass


class Black():
    def __init__(self):
        pass


class Row():
    def __init__(self, row):
        self.row = row


class Col():
    def __init__(self, col):
        self.col = col


class Both(Row, Col):
    def __init__(self, row, col):
        Row.__init__(self, row)
        Col.__init__(self, col)

# Empty cells will be replaced with Cells


class Total():
    def __init__(self, total):
        self.total = total


class Cell():
    def __init__(self):
        self.value = 0
        self.row_indicator = None
        self.row_total = None
        self.col_indicator = None
        self.col_total = None
        self.constraint_score = 0
        self.row_constraint_score = 0
        self.col_constraint_score = 0

    def set_value(self, value):
        self.row_total.total += value-self.value
        self.col_total.total += value-self.value
        self.value = value


class InitiateRowFirst(Cell):
    def __init__(self, indicator, total):
        super().__init__()
        self.row_indicator = indicator
        self.row_total = total


class InitiateColFirst(Cell):
    def __init__(self, indicator, total):
        super().__init__()
        self.col_indicator = indicator
        self.col_total = total


class Board():
    def __init__(self, board):
        self.board = board
        self.most_constrained = []

        # preprocessing associates each Empty cell and each row/column with its current value,
        # the indicator(s) it is associated with,
        # and the total(s) that its row and/or column have achieved so far.

        # preprocessing also assigns constraints to order cells for filling efficiently via backtracking heuristics.

        for i in range(len(board.board)):
            indicator = None
            total = None
            count = 0
            for j in range(len(board[0])):
                if type(board[i][j]) in [Row, Both]:
                    indicator = board[i][j].row
                    total = Total(0)
                    count = 0
                elif indicator != None and type(board[i][j]) == Empty:
                    board[i][j] = InitiateRowFirst(indicator, total)
                    self.most_constrained.append(board[i][j])
                    count += 1
                elif type(board[i][j]) == Black:
                    indicator = None
                    total = None
                    for k in range(len(self.most_constrained)-count, len(self.most_constrained)):
                        self.most_constrained[k].row_constraint_score = math.comb(
                            indicator+count-1, count-1)
                        self.most_constrained[k].constraint_score = math.comb(
                            indicator+count-1, count-1)

        for j in range(len(board[0])):
            indicator = None
            total = None
            count = 0
            for i in range(len(board)):
                if type(board[i][j]) in [Col, Both]:
                    indicator = board[i][j].col
                    total = Total(0)
                    count = 0
                elif indicator != None:
                    if type(board[i][j]) == Empty:
                        board[i][j] = InitiateColFirst(indicator, total)
                        self.most_constrained.append(board[i][j])
                    elif type(board[i][j]) == InitiateRowFirst:
                        board[i][j].col_indicator = indicator
                        board[i][j].col_total = total
                    count += 1
                elif type(board[i][j]) == Black:
                    indicator = None
                    total = None
                    for k in range(len(self.most_constrained)-count, len(self.most_constrained)):
                        self.most_constrained[k].col_constraint_score = math.comb(
                            indicator+count-1, count-1)
                        self.most_constrained[k].constraint_score += math.comb(
                            indicator+count-1, count-1)
        self.most_constrained.sort(key=lambda cell: cell.constraint_score)


board = Board([[Black(), Black(), Col(30), Col(4), Col(24), Black(), Col(4), Col(16)],
               [Black(), Both(19, 16), Empty(), Empty(),
                Empty(), Both(10, 9), Empty(), Empty()],
               [Row(39), Empty(), Empty(), Empty(),
                Empty(), Empty(), Empty(), Empty()],
               [Row(15), Empty(), Empty(), Both(10, 23),
                Empty(), Empty(), Col(10), Black()],
               [Black(), Row(16), Empty(), Empty(), Both(
                   4, 6), Empty(), Empty(), Col(16)],
               [Black(), Col(14), Both(9, 16), Empty(),
                Empty(), Both(12, 4), Empty(), Empty()],
               [Row(35), Empty(), Empty(), Empty(),
                Empty(), Empty(), Empty(), Empty()],
               [Row(16), Empty(), Empty(), Row(7), Empty(), Empty(), Empty(), Black()]])
