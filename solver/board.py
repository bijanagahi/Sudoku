from .cell import Cell, Box
from .utils import color
from pyxtension.streams import stream


class Board:
    def __init__(self, import_str: str) -> None:
        # all the cells as a flat map
        self.all_cells: list[Cell] = [Cell(int(_)) for _ in import_str]
        # all the cells as a 2d grid
        self.grid: list[list[Cell]] = [self.all_cells[x:x+9]
                                       for x in range(0, 81, 9)]
        # a flat map of all 9 cells organized by box (1-9)
        self.boxes: list[list[Cell]] = self._init_boxes()

    def sweep_for_naked_candidates(self) -> None:
        row:list[Cell]
        i:int
        for row in self.grid:
            self._check(row)
        for i in range(9):
            self._check(self._getCol(i))
            self._check(self._getBox(i))
    
    def is_solved(self) -> bool:
        return len([cell for cell in self.all_cells if not cell.is_solved]) == 0
    
    def _check(self, row: list[Cell]) -> None:
        '''Checks the given list for fixed values and eliminates that value from all cells within.'''
        cell: Cell
        fixed_values: list[int] = [
            cell.value for cell in row if cell.is_solved]
        [cell.eliminate(fixed_values) for cell in row]
    
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
