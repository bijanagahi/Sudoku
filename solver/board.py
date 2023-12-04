from .cell import Cell, Box
from .utils import color
# from pyxtension.streams import stream


class Board:
    def __init__(self, import_str: str) -> None:
        # prevent infinite loops/recursion stack overflow
        self.max_iterations:int = 100
        # all the cells as a flat map
        self.all_cells: list[Cell] = [Cell(int(_)) for _ in import_str]
        # all the cells as a 2d grid
        self.grid: list[list[Cell]] = [self.all_cells[x:x+9]
                                       for x in range(0, 81, 9)]
        # a flat map of all 9 cells organized by box (1-9)
        self.boxes: list[list[Cell]] = self._init_boxes()
        # strategies is a list of functions in order of increasing complexity for solving the puzzle
        # we start with the lowest index (easiest) strategy, and run it until it no longer returns progress.
        # then we move to a more complicated strategy. As soon as any strategy returns progress, we reset back
        # to the initial strategy and start again.
        self.strategies: list[callable[[], bool]] = [ # type: ignore
            self.sweep_for_naked_singles,
            self.sweep_for_naked_doubles]

    def solve(self) -> None:
        current_strategy:int = 0
        did_update:bool = False
        for _ in range(self.max_iterations):
            did_update = self.strategies[current_strategy]()
            if not did_update: # nothing happened, let's move to a more complicated strategy
                if current_strategy == len(self.strategies) -1:
                    print("I'm stuck.")
                    print(self)
                    exit(1)
                current_strategy = min(current_strategy+1, len(self.strategies)-1) # prevent OOB
                print(f"Changing strategy: {self.strategies[current_strategy-1].__name__} -> {self.strategies[current_strategy].__name__}")
                print(self)
                continue # skip checking if the board is solved. we know it's not since state hasn't changed
            if self.is_solved():
                print("all done!")
                break
            if current_strategy > 0:
                print("Falling back to original strategy")
            current_strategy = 0 # since we updated something, reset back to base strategy.

    
    def sweep_for_naked_singles(self) -> bool:
        '''
        Simplest strategy.
        Iterate over the board and eliminate candidates in cells when that value appears anywhere in that row/col/box.
        '''
        row:list[Cell]
        i:int
        did_update:bool = False
        # By OR-ing this value with the results each time, we can 'sticky' it to True if it occurs at least once
        for row in self.grid:
            did_update |= self._check(row)
        for i in range(9):
            did_update |= self._check(self._getCol(i))
            did_update |= self._check(self._getBox(i))
        return did_update

    def sweep_for_naked_doubles(self) -> bool:
        '''
        Check all cells that only have two candidates against their row/col/box for sister cells.
        Eleminate those two value from all other cells in the row/col/box
        '''
        did_update:bool = False
        for row in self.grid:
            did_update |= self._check_doubles(row)
        for i in range(9):
            did_update |= self._check_doubles(self._getCol(i))
            did_update |= self._check_doubles(self._getBox(i))
        return did_update
    
    # TODO: if this is slow, consider actively keeping track of solved cells as we go
    def is_solved(self) -> bool:
        return len([cell for cell in self.all_cells if not cell.is_solved]) == 0
    
    def _check(self, row: list[Cell]) -> bool:
        '''Checks the given list for fixed values and eliminates that value from all cells within.'''
        cell: Cell
        fixed_values: list[int] = [
            cell.value for cell in row if cell.is_solved]
        results:list[bool] = [cell.eliminate(fixed_values) for cell in row]
        return results.count(True) > 0 # return True if any cells were updated during this operation
    
    def _check_doubles(self, row: list[Cell]) -> bool:
        '''Checks the given list for fixed pairs of doubles and eliminates that double from all other cells within.'''
        seen_doubles: set[tuple[int,int]] = set()
        cell:Cell
        did_update:bool = False
        all_doubles: list[tuple[int,int]] = [tuple(cell.candidates) for cell in row if len(cell.candidates) == 2]
        double: tuple[int,int]
        for double in all_doubles:
            if double in seen_doubles:
                did_update |= [cell.eliminate(list(double)) for cell in row if cell.candidates != list(double)].count(True) > 0
            else:
                seen_doubles.add(double)
        return did_update
    
    def _getRow(self, row: int) -> list[Cell]:
        '''Returns the given row of the grid'''
        return self.grid[row]

    def _getCol(self, col: int) -> list[Cell]:
        '''Return the given column of the grid'''
        return [self.grid[x][col] for x in range(9)]

    def _getBox(self, box: int) -> list[Cell]:
        '''Returns a flattened list cooresponding to the given Box in the grid'''
        return self.boxes[box]

    def _init_boxes(self) -> list[list[Cell]]:
        boxes: list[list[Cell]] = []
        row: list[Cell]
        idx: int
        box_a: list[Cell] = []
        box_b: list[Cell] = []
        box_c: list[Cell] = []
        for idx, row in enumerate(self.grid):
            box_a.extend(row[0:3])
            box_b.extend(row[3:6])
            box_c.extend(row[6:9])
            if (idx+1) % 3 == 0:
                boxes.append(box_a.copy())
                box_a = []
                boxes.append(box_b.copy())
                box_b = []
                boxes.append(box_c.copy())
                box_c = []
        return boxes

    def __str__(self) -> str:
        row_bar: str = "\n-------------------------\n"
        cell: Cell
        idx: int
        output: str = row_bar+"| "
        for idx, cell in enumerate(self.all_cells):
            cell_value: str = str(len(cell.candidates)
                                  ) if not cell.isSolved() else str(cell.value)
            cell_color:str = cell.getColor()
            
            output += f"{cell_color}{cell_value}{color.END} "
            if (idx+1) % 3 == 0:
                output += "| "
                if idx == 80:
                    continue
            if (idx+1) % 27 == 0:
                output += (row_bar + "| ")
                continue
            if (idx+1) % 9 == 0:
                output += "\n| "
        output += row_bar
        return output
