import sys
from solver.board import Board

'''
An example sample string for a very easy Sudoku:
000105000140000670080002400063070010900000003010090520007200080026000035000409000
'''

def run(import_string:str) -> None:
    board:Board = Board(import_string)
    print(board)
    board.solve() # go!
    print(board)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Invocation requires a valid 81 character Sudoku puzzle to begin.")
        exit(1)
    import_string: str = sys.argv[1]
    if len(import_string) != 81:
        print("Import string invalid")
        exit(1)
    run(import_string)
    