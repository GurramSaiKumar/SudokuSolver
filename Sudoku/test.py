puzzle = [[1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]


def solve_recursive(puzzle):
    # Find an empty cell to fill
    empty_cell = find_empty_cell(puzzle)
    if not empty_cell:
        # If no empty cells are found, the puzzle is solved
        return True

    row, col = empty_cell

    # Try filling in digits from 1 to 9
    for digit in range(1, 10):
        # digit_str = str(digit)
        if is_valid(puzzle, row, col, digit):
            # If the digit is valid, try filling it in
            puzzle[row][col] = digit

            # Recursively attempt to solve the rest of the puzzle
            if solve_recursive(puzzle):
                return True

            # If the recursive call fails, backtrack (reset the cell)
            puzzle[row][col] = 0

    # If no valid digit is found, backtrack
    return False


def find_empty_cell(puzzle):
    # Find the first empty cell (represented by 0)
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                return i, j
    return None


def is_valid(puzzle, row, col, digit):
    # Check if the digit is not present in the same row, column, or 3x3 subgrid
    for i in range(0, 9):
        if puzzle[row][i] == digit:
            return False
    for i in range(0, 9):
        if puzzle[i][col] == digit:
            return False

    row_start, col_start = 3 * (row // 3), 3 * (col // 3)
    for i in range(0, 3):
        for j in range(0, 3):
            _row = row_start + i
            _col = col_start + j
            if digit == puzzle[_row][_col]:
                return False
    return True

    # return (
    #         self.is_digit_valid_in_row(puzzle, row, digit) and
    #         self.is_digit_valid_in_col(puzzle, col, digit) and
    #         self.is_digit_valid_in_grid(puzzle, row, col, digit)
    # )

    # Update is_digit_valid_in_row, is_digit_valid_in_col, and is_digit_valid_in_grid


def is_digit_valid_in_row(puzzle, row, digit):
    return puzzle[row].count(digit) == 0


def is_digit_valid_in_col(puzzle, col, digit):
    return [puzzle[i][col] for i in range(9)].count(digit) == 0


def is_digit_valid_in_grid(puzzle, row, col, digit):
    row_start, col_start = 3 * (row // 3), 3 * (col // 3)
    return all(
        puzzle[row_start + i][col_start + j] != digit
        for i in range(3) for j in range(3)
    )


print(f'Before solving {puzzle}')
solve_recursive(puzzle)
print(f'After solving {puzzle}')
