from .utils import color

class Cell:
    '''Defines a single cell within a Sudoku board'''

    def __init__(self, value: int = 0) -> None:
        self.value: int = value
        self.candidates: list[int] = [] if self.value > 0 else list(
            range(1, 9+1))  # add one because range is end exclusive
        self.is_solved: bool = value > 0
        # if the cell was given at the start, it can't be changed
        self.immutable: bool = value > 0

    def isSolved(self) -> bool:
        return self.is_solved

    # TODO - Optimize this....
    def eliminate(self, candidates: list[int]) -> None:
        '''Removes the given candidates from this cells possible candidates.

          If this operation results in only 1 candidate, solve this cell.
          If there are no remaining candidates after this operation, throw.
        '''
        # If we've already solved this one just skip
        if self.is_solved:
            return
        candidate: int
        for candidate in candidates:
            try:
                self.candidates.remove(candidate)
            except:
                pass
        if len(self.candidates) == 1:
            self.value = self.candidates[0]
            self.is_solved = True
            print("Solved cell!")
        if len(self.candidates) == 0:
            raise ValueError("Cell has no remaining possible candidates")

    def getColor(self) -> str:
        if self.immutable:
            return color.BOLD
        elif self.is_solved:
            return color.GREEN
        else:
            return color.RED
    
    def __str__(self) -> str:
        return str(self.value)


class Box:
    '''Defines a "Box" - a 3x3 grid of Cells'''

    def __init__(self,
                 row_1: tuple[Cell, Cell, Cell],
                 row_2: tuple[Cell, Cell, Cell],
                 row_3: tuple[Cell, Cell, Cell]) -> None:
        self.row_1: tuple[Cell, Cell, Cell] = row_1
        self.row_2: tuple[Cell, Cell, Cell] = row_2
        self.row_3: tuple[Cell, Cell, Cell] = row_3
