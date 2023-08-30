import sys
from solver.board import Board

def run(import_string:str) -> None:
    board:Board = Board(import_string)
    print(board)
    max_iterations:int = 100
    for _ in range(max_iterations):
        board.sweep_for_naked_candidates()
        if board.is_solved():
            print("all done!")
            break
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
    