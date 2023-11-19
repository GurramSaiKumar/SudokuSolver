import re
import tkinter as tk


class SudokuGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku Solver")

        self.entries = [[tk.Entry(master, width=3, justify="center", font=("Helvetica", 12),
                                  validate="key", validatecommand=(master.register(self.validate_input), '%P'))
                         for _ in range(9)] for _ in range(9)]

        for i in range(9):
            for j in range(9):
                padx, pady = 2, 2

                # Add background color to highlight the 3x3 subgrids
                subgrid_color = "lightgray" if (i // 3 + j // 3) % 2 == 0 else "white"
                self.entries[i][j].configure(bg=subgrid_color, bd=1)

                self.entries[i][j].grid(row=i, column=j, padx=padx, pady=pady, ipadx=5, ipady=5, sticky="nsew")

        self.active_cell = (0, 0)
        self.highlight_active_cell()

        # Add labels for messages
        self.message_label = tk.Label(master, text="", font=("Helvetica", 12), fg="green")
        self.message_label.grid(row=10, columnspan=9, pady=5)

        # Add a Solve button
        solve_button = tk.Button(master, text="Solve", command=self.solve_sudoku)
        solve_button.grid(row=11, columnspan=9, pady=10)

        # Add Clear button
        clear_button = tk.Button(master, text="Clear", command=self.clear_entries)
        clear_button.grid(row=12, columnspan=9, pady=10)

        # Configure row and column weights
        for i in range(9):
            master.grid_rowconfigure(i, weight=1)
            master.grid_columnconfigure(i, weight=1)

    def validate_input(self, new_value):
        if re.match("^[1-9]?$", new_value):
            self.message_label.config(text="Valid input", fg="green")
            return True
        else:
            self.message_label.config(text="Invalid input (only digits 1-9 allowed)", fg="red")
            return False

    def highlight_active_cell(self):
        i, j = self.active_cell
        self.entries[i][j].configure(bd=3)

    def remove_highlight_from_active_cell(self):
        i, j = self.active_cell
        self.entries[i][j].configure(bd=1)

    def solve_sudoku(self):
        # Extract the current state of the puzzle from the entry widgets
        puzzle = [[int(self.entries[i][j].get()) if self.entries[i][j].get() else 0 for j in range(9)] for i in
                  range(9)]

        if self.solve_recursive(puzzle):
            # If a solution is found, update the entry widgets with the solution
            for i in range(9):
                for j in range(9):
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].insert(0, str(puzzle[i][j]))
            self.message_label.config(text="Sudoku solved successfully!", fg="green")
        else:
            self.message_label.config(text="No solution found", fg="red")

    def solve_recursive(self, puzzle):
        # Find an empty cell to fill
        empty_cell = self.find_empty_cell(puzzle)
        if not empty_cell:
            # If no empty cells are found, the puzzle is solved
            return True

        row, col = empty_cell

        # Try filling in digits from 1 to 9
        for digit in range(1, 10):
            if self.is_valid(puzzle, row, col, digit):
                # If the digit is valid, try filling it in
                puzzle[row][col] = digit

                # Recursively attempt to solve the rest of the puzzle
                if self.solve_recursive(puzzle):
                    return True

                # If the recursive call fails, backtrack (reset the cell)
                puzzle[row][col] = 0

        # If no valid digit is found, backtrack
        return False

    def find_empty_cell(self, puzzle):
        # Find the first empty cell (represented by 0)
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] == 0:
                    return i, j
        return None

    def is_valid(self, puzzle, row, col, digit):
        if digit in puzzle[row]:
            return False

        if digit in [puzzle[i][col] for i in range(9)]:
            return False

        row_start, col_start = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                _row = row_start + i
                _col = col_start + j
                if digit == puzzle[_row][_col]:
                    return False
        return True

    def clear_entries(self):
        # Clear all entry widgets
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)

        self.message_label.config(text="Entries cleared", fg="green")


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
