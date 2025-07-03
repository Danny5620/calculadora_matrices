import customtkinter as ctk
from matrix_dataclass import Matrix, MATRIX_ROWS_OPTIONS, MATRIX_COLS_OPTIONS
from expression_parser import MatrixExpressionParser


class CalculatorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora de Matrices")
        self.geometry("1200x700")

        # Store multiple matrices
        self.matrices = {}  # Dictionary to store matrices by name
        self.current_matrix_name = None
        self.max_matrices = 4
        self.ans_matrix = None  # Special Ans matrix for results

        self.initialize_widgets()
        self.start_screen()

    def get_next_matrix_name(self):
        """Generate the next available matrix name"""
        for i in range(1, self.max_matrices + 1):
            matrix_name = f"Matriz_{i}"
            if matrix_name not in self.matrices:
                return matrix_name
        return None

    def initialize_widgets(self):
        # Main container frames
        self.left_frame = ctk.CTkFrame(self)
        self.right_frame = ctk.CTkFrame(self)

        # Left frame widgets (matrix input)
        self.combo_frame = ctk.CTkFrame(self.left_frame)

        self.order_label = ctk.CTkLabel(self.left_frame,
                                        text="Selecciona el orden de la matriz:")

        self.row_combo = ctk.CTkComboBox(self.left_frame,
                                         values=MATRIX_ROWS_OPTIONS,
                                         width=100,
                                         command=self.on_dimension_change)

        self.col_combo = ctk.CTkComboBox(self.left_frame,
                                         values=MATRIX_COLS_OPTIONS,
                                         width=100,
                                         command=self.on_dimension_change)

        # Matrix tab selector frame
        self.tab_frame = ctk.CTkFrame(self.left_frame)

        self.matrix_tabs_label = ctk.CTkLabel(self.tab_frame,
                                              text="Matrices:")

        # Create tab buttons for matrices 1-4
        self.tab_buttons = {}
        self.tab_button_frame = ctk.CTkFrame(self.tab_frame)

        for i in range(1, self.max_matrices + 1):
            matrix_name = f"Matriz_{i}"
            button = ctk.CTkButton(self.tab_button_frame,
                                   text=f"M{i}",
                                   width=40,
                                   height=30,
                                   command=lambda
                                       name=matrix_name: self.select_matrix_tab(
                                       name))
            self.tab_buttons[matrix_name] = button

        # Add Ans button
        self.ans_button = ctk.CTkButton(self.tab_button_frame,
                                        text="Ans",
                                        width=50,
                                        height=30,
                                        fg_color="orange",
                                        hover_color="darkorange",
                                        command=lambda: self.select_matrix_tab(
                                            "Ans"))
        self.tab_buttons["Ans"] = self.ans_button

        # Add new matrix button
        self.add_matrix_button = ctk.CTkButton(self.tab_frame,
                                               text="+",
                                               width=30,
                                               height=30,
                                               command=self.create_new_matrix)

        # Right frame widgets (operations)
        self.operations_label = ctk.CTkLabel(self.right_frame,
                                             text="Operaciones de Matrices",
                                             font=("Arial", 16, "bold"))

        self.operations_frame = ctk.CTkFrame(self.right_frame)

        # Initialize operations widgets
        self.initialize_operations_widgets()

    def initialize_operations_widgets(self):
        """Initialize all operation-related widgets"""
        # Matrix selectors frame
        self.selectors_frame = ctk.CTkFrame(self.operations_frame)

        # First matrix selector
        self.matrix1_label = ctk.CTkLabel(self.selectors_frame,
                                          text="Matriz A:")
        self.matrix1_combo = ctk.CTkComboBox(self.selectors_frame,
                                             values=["Seleccionar..."],
                                             width=120,
                                             state="readonly")

        # Second matrix selector
        self.matrix2_label = ctk.CTkLabel(self.selectors_frame,
                                          text="Matriz B:")
        self.matrix2_combo = ctk.CTkComboBox(self.selectors_frame,
                                             values=["Seleccionar..."],
                                             width=120,
                                             state="readonly")

        # Scalar input frame
        self.scalar_frame = ctk.CTkFrame(self.operations_frame)
        self.scalar_label = ctk.CTkLabel(self.scalar_frame, text="Escalar:")
        self.scalar_entry = ctk.CTkEntry(self.scalar_frame, width=80,
                                         placeholder_text="1.0")

        # Binary operations (3 buttons)
        self.binary_frame = ctk.CTkFrame(self.operations_frame)
        self.add_button = ctk.CTkButton(self.binary_frame,
                                        text="A + B",
                                        command=self.add_matrices,
                                        width=100)
        self.subtract_button = ctk.CTkButton(self.binary_frame,
                                             text="A - B",
                                             command=self.subtract_matrices,
                                             width=100)
        self.multiply_button = ctk.CTkButton(self.binary_frame,
                                             text="A × B",
                                             command=self.multiply_matrices,
                                             width=100)

        # Unary operations (3 buttons)
        self.unary_frame = ctk.CTkFrame(self.operations_frame)
        self.transpose_button = ctk.CTkButton(self.unary_frame,
                                              text="Transponer A",
                                              command=self.transpose_matrix,
                                              width=120)
        self.determinant_button = ctk.CTkButton(self.unary_frame,
                                                text="Determinante A",
                                                command=self.calculate_determinant,
                                                width=120)
        self.inverse_button = ctk.CTkButton(self.unary_frame,
                                            text="Inversa A",
                                            command=self.inverse_matrix,
                                            width=120)

        # Scalar operations (2 buttons)
        self.scalar_ops_frame = ctk.CTkFrame(self.operations_frame)
        self.scalar_mult_button = ctk.CTkButton(self.scalar_ops_frame,
                                                text="Escalar × A",
                                                command=self.scalar_multiply_matrix,
                                                width=120)
        self.scalar_div_button = ctk.CTkButton(self.scalar_ops_frame,
                                               text="A ÷ Escalar",
                                               command=self.scalar_divide_matrix,
                                               width=120)

        # Initialize expression widgets
        self.initialize_expression_widgets()

        # Result display
        self.result_frame = ctk.CTkFrame(self.operations_frame)
        self.result_label = ctk.CTkLabel(self.result_frame, text="Resultado:")

        # Save result section with dropdown and button
        self.save_frame = ctk.CTkFrame(self.result_frame)
        self.save_combo = ctk.CTkComboBox(self.save_frame,
                                          values=["Nueva Matriz"],
                                          width=150,
                                          state="readonly")
        self.save_result_button = ctk.CTkButton(self.save_frame,
                                                text="Guardar",
                                                command=self.save_result_as_matrix,
                                                state="disabled",
                                                width=80)

    def initialize_expression_widgets(self):
        """Initialize expression input widgets"""
        self.expression_frame = ctk.CTkFrame(self.operations_frame)

        # Expression input section
        expression_input_frame = ctk.CTkFrame(self.expression_frame)
        expression_input_frame.pack(fill="x", padx=10, pady=10)

        self.expression_label = ctk.CTkLabel(expression_input_frame,
                                            text="Expresión:",
                                            font=("Arial", 12, "bold"))
        self.expression_label.pack(anchor="w", pady=(0, 5))

        self.expression_entry = ctk.CTkEntry(expression_input_frame,
                                            width=400,
                                            height=35,
                                            placeholder_text="Ej: (M1 + M2) * 3 - M3^T")
        self.expression_entry.pack(fill="x", pady=(0, 10))

        # Buttons frame
        buttons_frame = ctk.CTkFrame(expression_input_frame)
        buttons_frame.pack(fill="x")

        self.evaluate_button = ctk.CTkButton(buttons_frame,
                                            text="Evaluar",
                                            command=self.evaluate_expression,
                                            width=100)
        self.evaluate_button.pack(side="left", padx=(0, 10))

        self.clear_expression_button = ctk.CTkButton(buttons_frame,
                                                    text="Limpiar",
                                                    command=self.clear_expression,
                                                    width=80)
        self.clear_expression_button.pack(side="left")

        # Help section
        help_frame = ctk.CTkFrame(self.expression_frame)
        help_frame.pack(fill="x", padx=10, pady=(0, 10))

        help_label = ctk.CTkLabel(help_frame,
                                 text="Sintaxis: M1, M2, M3, M4 (matrices), Ans (resultado), +, -, *, /, ^T (transpuesta), ^-1 (inversa), det(), ( )",
                                 font=("Arial", 10),
                                 text_color="gray",
                                 wraplength=450)
        help_label.pack(pady=5)

    def evaluate_expression(self):
        """Evaluate a mathematical expression with matrices"""
        try:
            expression = self.expression_entry.get().strip()
            if not expression:
                self.show_error("Ingresa una expresión")
                return

            # Create parser with current matrices
            parser = MatrixExpressionParser(self.matrices, self.ans_matrix)
            result = parser.evaluate(expression)

            # Check if result is a Matrix or a scalar (float/int)
            if isinstance(result, Matrix):
                self.save_to_ans(result)
                self.display_result(result, f"Expresión: {expression}")
            elif isinstance(result, (int, float)):
                # Handle scalar results (like determinants)
                self.display_determinant_result(result,
                                                f"Expresión: {expression}")
            else:
                self.show_error(
                    f"Tipo de resultado no soportado: {type(result)}")

        except Exception as e:
            self.show_error(f"Error en expresión: {str(e)}")

    def clear_expression(self):
        """Clear the expression input field"""
        self.expression_entry.delete(0, "end")

    def start_screen(self):
        # Pack main frames
        self.left_frame.pack(side="left", fill="both", expand=True,
                             padx=(10, 5), pady=10)
        self.right_frame.pack(side="right", fill="both", expand=True,
                              padx=(5, 10), pady=10)

        # Left frame layout
        self.order_label.pack(pady=10)

        # Create frame for side-by-side combo boxes
        self.combo_frame.pack(pady=5)

        self.row_combo.pack(side="left", padx=15, in_=self.combo_frame)

        # Add "x" label between combo boxes
        x_label = ctk.CTkLabel(self.combo_frame, text="x",
                               font=("Arial", 16, "bold"))
        x_label.pack(side="left", padx=5)

        self.col_combo.pack(side="left", padx=15, in_=self.combo_frame)

        # Set default values for combo boxes
        self.row_combo.set("2")
        self.col_combo.set("2")

        # Pack matrix tab frame
        self.tab_frame.pack(pady=(20, 5))

        self.matrix_tabs_label.pack(pady=(0, 5))

        # Pack tab button frame
        self.tab_button_frame.pack(pady=(0, 10))

        # Pack tab buttons horizontally
        for i, (matrix_name, button) in enumerate(self.tab_buttons.items()):
            button.pack(side="left", padx=2)

        # Pack add button
        self.add_matrix_button.pack(pady=(0, 10))

        # Right frame layout
        self.operations_label.pack(pady=20)
        self.operations_frame.pack(fill="both", expand=True, padx=20,
                                   pady=(0, 20))

        # Pack operations widgets
        self.pack_operations_widgets()

        # Update button states
        self.update_tab_states()

        # Create initial matrix grid
        self.create_matrix_grid()

    def pack_operations_widgets(self):
        """Pack all operations widgets"""
        # Matrix selectors
        self.selectors_frame.pack(pady=10, fill="x")
        self.matrix1_label.pack(side="left", padx=(10, 5))
        self.matrix1_combo.pack(side="left", padx=5)
        self.matrix2_label.pack(side="left", padx=(20, 5))
        self.matrix2_combo.pack(side="left", padx=5)

        # Scalar input
        self.scalar_frame.pack(pady=10, fill="x")
        self.scalar_label.pack(side="left", padx=(10, 5))
        self.scalar_entry.pack(side="left", padx=5)

        # Binary operations - just buttons
        self.binary_frame.pack(pady=10)
        self.add_button.pack(side="left", padx=5)
        self.subtract_button.pack(side="left", padx=5)
        self.multiply_button.pack(side="left", padx=5)

        # Unary operations - just buttons
        self.unary_frame.pack(pady=10)
        self.transpose_button.pack(side="left", padx=5)
        self.determinant_button.pack(side="left", padx=5)
        self.inverse_button.pack(side="left", padx=5)

        # Scalar operations - just buttons
        self.scalar_ops_frame.pack(pady=10)
        self.scalar_mult_button.pack(side="left", padx=5)
        self.scalar_div_button.pack(side="left", padx=5)

        # Add combined operations section
        combined_label = ctk.CTkLabel(self.operations_frame,
                                     text="Operaciones Combinadas",
                                     font=("Arial", 14, "bold"))
        combined_label.pack(pady=(20, 10))

        # Pack expression widgets
        self.expression_frame.pack(pady=10, fill="x")

        # Result display
        self.result_frame.pack(pady=10, fill="both", expand=True)
        self.result_label.pack(pady=(5, 0))

        # Save section
        self.save_frame.pack(pady=5, fill="x")
        self.save_combo.pack(side="left", padx=(0, 5))
        self.save_result_button.pack(side="left")

    def update_matrix_selectors(self):
        """Update the matrix selector combo boxes with available matrices"""
        matrix_names = list(self.matrices.keys())
        if self.ans_matrix:
            matrix_names.append("Ans")

        values = matrix_names if matrix_names else ["No hay matrices"]

        self.matrix1_combo.configure(values=values)
        self.matrix2_combo.configure(values=values)

        # Reset selections if current selection is no longer valid
        if self.matrix1_combo.get() not in matrix_names:
            self.matrix1_combo.set("Seleccionar...")
        if self.matrix2_combo.get() not in matrix_names:
            self.matrix2_combo.set("Seleccionar...")

    def update_save_selector(self):
        """Update the save dropdown with available matrices"""
        available_options = []

        # Add existing matrices (can overwrite) with clean names
        for i in range(1, self.max_matrices + 1):
            matrix_name = f"Matriz_{i}"
            if matrix_name in self.matrices:
                available_options.append(f"Matriz {i}")
            else:
                available_options.append(f"Matriz {i}")

        # Add option to create new matrix if slots available
        if len(self.matrices) < self.max_matrices:
            available_options.append("Nueva Matriz")

        if not available_options:
            available_options = ["Sin espacio disponible"]

        self.save_combo.configure(values=available_options)

        # Set default to "Nueva Matriz" if available, otherwise first option
        if "Nueva Matriz" in available_options:
            self.save_combo.set("Nueva Matriz")
        else:
            self.save_combo.set(available_options[0])

    def select_matrix_tab(self, matrix_name):
        """Select a matrix tab"""
        if matrix_name == "Ans":
            if self.ans_matrix:
                self.current_matrix_name = "Ans"
                self.row_combo.set(str(self.ans_matrix.rows))
                self.col_combo.set(str(self.ans_matrix.cols))
                self.create_matrix_grid()
            else:
                return
        elif matrix_name in self.matrices:
            self.current_matrix_name = matrix_name
            matrix = self.matrices[matrix_name]

            # Update combo boxes to match matrix dimensions
            self.row_combo.set(str(matrix.rows))
            self.col_combo.set(str(matrix.cols))

            # Recreate grid with matrix data
            self.create_matrix_grid()
        else:
            # Create new matrix if it doesn't exist
            self.current_matrix_name = matrix_name
            self.create_matrix_grid()

        # Update tab states
        self.update_tab_states()

    def update_tab_states(self):
        """Update the visual state of tab buttons"""
        for matrix_name, button in self.tab_buttons.items():
            if matrix_name == "Ans":
                if self.ans_matrix:
                    button.configure(fg_color="orange",
                                     hover_color="darkorange")
                else:
                    button.configure(fg_color="gray", hover_color="darkgray")
            elif matrix_name in self.matrices:
                button.configure(fg_color=["#3B8ED0", "#1F6AA5"],
                                 hover_color=["#36719F", "#144870"])
            else:
                button.configure(fg_color="gray", hover_color="darkgray")

            # Highlight current selection
            if matrix_name == self.current_matrix_name:
                button.configure(text_color="yellow")
            else:
                button.configure(text_color="white")

        # Update control button visibility
        self.update_button_visibility()

    def create_new_matrix(self):
        """Create a new matrix with current combo box dimensions"""
        next_name = self.get_next_matrix_name()
        if next_name and len(self.matrices) < self.max_matrices:
            self.current_matrix_name = next_name
            self.create_matrix_grid()
            self.update_tab_states()

    def update_button_visibility(self):
        """Show/hide buttons based on matrix count and selection"""
        # Show/hide + button based on matrix count
        if len(self.matrices) >= self.max_matrices:
            self.add_matrix_button.pack_forget()
        else:
            self.add_matrix_button.pack(pady=(0, 10))

    def on_dimension_change(self):
        """Called when combo box values change"""
        # Don't allow dimension changes for Ans matrix
        if self.current_matrix_name == "Ans":
            return

        # Reset current matrix when dimensions change manually
        if self.current_matrix_name:
            # Check if current matrix matches new dimensions
            if self.current_matrix_name in self.matrices:
                matrix = self.matrices[self.current_matrix_name]
                new_rows = int(self.row_combo.get())
                new_cols = int(self.col_combo.get())
                if matrix.rows != new_rows or matrix.cols != new_cols:
                    self.current_matrix_name = None

        self.create_matrix_grid()

    def create_matrix_grid(self):
        """Create or update the matrix input grid"""
        # Get dimensions from combo boxes
        rows = int(self.row_combo.get())
        cols = int(self.col_combo.get())

        # Clear existing matrix display if any
        if hasattr(self, 'matrix_frame'):
            self.matrix_frame.destroy()

        # Create matrix frame
        self.matrix_frame = ctk.CTkFrame(self.left_frame)
        self.matrix_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Create header frame for title and delete button
        header_frame = ctk.CTkFrame(self.matrix_frame)
        header_frame.pack(fill="x", pady=(10, 0))

        # Create title for matrix input
        current_name = self.current_matrix_name or "Nueva Matriz"
        is_ans = self.current_matrix_name == "Ans"

        title_text = f"{current_name} - {rows}x{cols}"
        if is_ans:
            title_text += " (Solo lectura)"

        matrix_title = ctk.CTkLabel(header_frame,
                                    text=title_text,
                                    font=("Arial", 14, "bold"))
        matrix_title.pack(side="left", padx=(10, 0), pady=10)

        # Add delete button to header frame (not for Ans matrix)
        if (self.current_matrix_name and
                self.current_matrix_name in self.matrices and
                self.current_matrix_name != "Ans"):
            self.delete_matrix_button = ctk.CTkButton(header_frame,
                                                      text="Eliminar",
                                                      command=self.delete_current_matrix,
                                                      width=80,
                                                      fg_color="red",
                                                      hover_color="darkred")
            self.delete_matrix_button.pack(side="right", padx=(0, 10), pady=10)

        # Create grid frame for entries
        grid_frame = ctk.CTkFrame(self.matrix_frame)
        grid_frame.pack(pady=10)

        # Create entry widgets grid
        self.entry_widgets = []
        for i in range(rows):
            row_entries = []
            for j in range(cols):
                entry = ctk.CTkEntry(grid_frame, width=60, height=30,
                                     state="disabled" if is_ans else "normal")
                entry.grid(row=i, column=j, padx=2, pady=2)

                # Bind keyboard navigation events (only for non-Ans matrices)
                if not is_ans:
                    entry.bind("<KeyPress>", lambda event, r=i,
                                                    c=j: self.handle_key_navigation(
                        event, r, c))
                    entry.bind("<Return>",
                               lambda event, r=i, c=j: self.handle_enter_key(
                                   event, r, c))

                row_entries.append(entry)
            self.entry_widgets.append(row_entries)

        # If there's a current matrix, populate the grid with its values
        self.populate_grid_from_current_matrix()

        # Add button to create/update Matrix object from input (not for Ans matrix)
        if not is_ans:
            create_button = ctk.CTkButton(self.matrix_frame,
                                          text="Crear/Actualizar Matriz",
                                          command=self.create_matrix_object,
                                          width=200)
            create_button.pack(pady=10)

    def handle_key_navigation(self, event, row, col):
        """Handle arrow key navigation in matrix grid"""
        if not hasattr(self, 'entry_widgets') or not self.entry_widgets:
            return

        rows = len(self.entry_widgets)
        cols = len(self.entry_widgets[0])
        current_entry = self.entry_widgets[row][col]

        # Handle arrow keys for navigation
        if event.keysym == "Up" and row > 0:
            self.entry_widgets[row - 1][col].focus()
            return "break"
        elif event.keysym == "Down" and row < rows - 1:
            self.entry_widgets[row + 1][col].focus()
            return "break"
        elif event.keysym == "Left":
            # Only navigate to previous cell if cursor is at the beginning
            cursor_pos = current_entry.index("insert")
            if cursor_pos == 0 and col > 0:
                self.entry_widgets[row][col - 1].focus()
                self.entry_widgets[row][col - 1].icursor("end")
                return "break"
        elif event.keysym == "Right":
            # Only navigate to next cell if cursor is at the end
            cursor_pos = current_entry.index("insert")
            text_length = len(current_entry.get())
            if cursor_pos == text_length and col < cols - 1:
                self.entry_widgets[row][col + 1].focus()
                self.entry_widgets[row][col + 1].icursor(0)
                return "break"

    def handle_enter_key(self, event, row, col):
        """Handle Enter key navigation in matrix grid"""
        if not hasattr(self, 'entry_widgets') or not self.entry_widgets:
            return

        rows = len(self.entry_widgets)
        cols = len(self.entry_widgets[0])

        # Move to next element in row, or first element of next row
        if col < cols - 1:
            # Move to next column in same row
            self.entry_widgets[row][col + 1].focus()
            self.entry_widgets[row][col + 1].icursor(0)
        elif row < rows - 1:
            # Move to first column of next row
            self.entry_widgets[row + 1][0].focus()
            self.entry_widgets[row + 1][0].icursor(0)
        else:
            # If on last element, wrap to first element
            self.entry_widgets[0][0].focus()
            self.entry_widgets[0][0].icursor(0)

        return "break"

    def populate_grid_from_current_matrix(self):
        """Populate the grid with values from the currently selected matrix"""
        matrix = None

        if self.current_matrix_name == "Ans" and self.ans_matrix:
            matrix = self.ans_matrix
        elif (self.current_matrix_name and
              self.current_matrix_name in self.matrices):
            matrix = self.matrices[self.current_matrix_name]

        if matrix:
            grid_rows = len(self.entry_widgets)
            grid_cols = len(self.entry_widgets[0])

            # Clear all entries first
            for i in range(grid_rows):
                for j in range(grid_cols):
                    self.entry_widgets[i][j].delete(0, "end")

            # Populate with matrix data
            for i in range(min(matrix.rows, grid_rows)):
                for j in range(min(matrix.cols, grid_cols)):
                    self.entry_widgets[i][j].insert(0, str(matrix.data[i][j]))

    def create_matrix_object(self):
        """Creates or updates Matrix object from the input grid values"""
        try:
            rows = len(self.entry_widgets)
            cols = len(self.entry_widgets[0])

            # Extract data from entry widgets
            data = []
            for i in range(rows):
                row_data = []
                for j in range(cols):
                    value = self.entry_widgets[i][j].get().strip()
                    if not value:
                        value = "0"
                    row_data.append(float(value))
                data.append(row_data)

            # Create or update Matrix object
            if self.current_matrix_name is None:
                matrix_name = self.get_next_matrix_name()
                if matrix_name is None:
                    self.show_error("No hay espacio para más matrices")
                    return
                self.current_matrix_name = matrix_name
            else:
                matrix_name = self.current_matrix_name

            matrix = Matrix(rows, cols, data=data)
            self.matrices[matrix_name] = matrix

            # Update tab states and matrix selectors
            self.update_tab_states()
            self.update_matrix_selectors()

            # Update the title to show it's saved
            self.update_matrix_title("Matriz guardada!")

            # Recreate grid to show delete button if it's a new matrix
            if matrix_name not in self.matrices or not hasattr(self,
                                                               'delete_matrix_button'):
                self.create_matrix_grid()

        except ValueError as e:
            self.show_error("Error: Ingresa valores numéricos válidos")

    def delete_current_matrix(self):
        """Delete the currently selected matrix"""
        if self.current_matrix_name and self.current_matrix_name in self.matrices:
            # Remove matrix from dictionary
            del self.matrices[self.current_matrix_name]

            # Reset current selection
            self.current_matrix_name = None

            # Update tab states and matrix selectors
            self.update_tab_states()
            self.update_matrix_selectors()

            # Create new empty grid
            self.create_matrix_grid()

    def update_matrix_title(self, status_text=""):
        """Update the matrix title with current info"""
        rows = int(self.row_combo.get())
        cols = int(self.col_combo.get())
        current_name = self.current_matrix_name or "Nueva Matriz"

        title_text = f"{current_name} - {rows}x{cols}"
        if status_text:
            title_text += f" ({status_text})"

        # Find and update the title label
        for widget in self.matrix_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkLabel):
                        child.configure(text=title_text)
                        break

    # Matrix operation methods
    def get_selected_matrices(self):
        """Get the selected matrices from combo boxes"""
        matrix1_name = self.matrix1_combo.get()
        matrix2_name = self.matrix2_combo.get()

        matrix1 = None
        matrix2 = None

        if matrix1_name == "Ans":
            matrix1 = self.ans_matrix
        elif matrix1_name != "Seleccionar...":
            matrix1 = self.matrices.get(matrix1_name)

        if matrix2_name == "Ans":
            matrix2 = self.ans_matrix
        elif matrix2_name != "Seleccionar...":
            matrix2 = self.matrices.get(matrix2_name)

        return matrix1, matrix2

    def add_matrices(self):
        """Add two matrices"""
        matrix1, matrix2 = self.get_selected_matrices()

        if not matrix1 or not matrix2:
            self.show_error("Selecciona dos matrices para sumar")
            return

        try:
            result = matrix1 + matrix2
            self.save_to_ans(result)
            self.display_result(result,
                                f"Suma: {self.matrix1_combo.get()} + {self.matrix2_combo.get()}")
        except Exception as e:
            self.show_error(f"Error en suma: {str(e)}")

    def subtract_matrices(self):
        """Subtract two matrices"""
        matrix1, matrix2 = self.get_selected_matrices()

        if not matrix1 or not matrix2:
            self.show_error("Selecciona dos matrices para restar")
            return

        try:
            result = matrix1 - matrix2
            self.save_to_ans(result)
            self.display_result(result,
                                f"Resta: {self.matrix1_combo.get()} - {self.matrix2_combo.get()}")
        except Exception as e:
            self.show_error(f"Error en resta: {str(e)}")

    def multiply_matrices(self):
        """Multiply two matrices"""
        matrix1, matrix2 = self.get_selected_matrices()

        if not matrix1 or not matrix2:
            self.show_error("Selecciona dos matrices para multiplicar")
            return

        try:
            result = matrix1 * matrix2
            self.save_to_ans(result)
            self.display_result(result,
                                f"Multiplicación: {self.matrix1_combo.get()} × {self.matrix2_combo.get()}")
        except Exception as e:
            self.show_error(f"Error en multiplicación: {str(e)}")

    def transpose_matrix(self):
        """Transpose a matrix"""
        matrix1_name = self.matrix1_combo.get()
        matrix1 = None

        if matrix1_name == "Ans":
            matrix1 = self.ans_matrix
        elif matrix1_name != "Seleccionar...":
            matrix1 = self.matrices.get(matrix1_name)

        if not matrix1:
            self.show_error("Selecciona una matriz para transponer")
            return

        try:
            result = matrix1.transpose()
            self.save_to_ans(result)
            self.display_result(result, f"Transpuesta: {matrix1_name}ᵀ")
        except Exception as e:
            self.show_error(f"Error en transposición: {str(e)}")

    def calculate_determinant(self):
        """Calculate determinant of a matrix"""
        matrix1_name = self.matrix1_combo.get()
        matrix1 = None

        if matrix1_name == "Ans":
            matrix1 = self.ans_matrix
        elif matrix1_name != "Seleccionar...":
            matrix1 = self.matrices.get(matrix1_name)

        if not matrix1:
            self.show_error("Selecciona una matriz para calcular determinante")
            return

        try:
            det = matrix1.determinant()
            self.display_determinant_result(det, matrix1_name)
        except Exception as e:
            self.show_error(f"Error calculando determinante: {str(e)}")

    def inverse_matrix(self):
        """Calculate inverse of a matrix"""
        matrix1_name = self.matrix1_combo.get()
        matrix1 = None

        if matrix1_name == "Ans":
            matrix1 = self.ans_matrix
        elif matrix1_name != "Seleccionar...":
            matrix1 = self.matrices.get(matrix1_name)

        if not matrix1:
            self.show_error("Selecciona una matriz para calcular inversa")
            return

        try:
            result = matrix1.inverse()
            self.save_to_ans(result)
            self.display_result(result, f"Inversa: {matrix1_name}⁻¹")
        except Exception as e:
            self.show_error(f"Error calculando inversa: {str(e)}")

    def scalar_multiply_matrix(self):
        """Multiply matrix by scalar"""
        matrix1_name = self.matrix1_combo.get()
        matrix1 = None

        if matrix1_name == "Ans":
            matrix1 = self.ans_matrix
        elif matrix1_name != "Seleccionar...":
            matrix1 = self.matrices.get(matrix1_name)

        if not matrix1:
            self.show_error(
                "Selecciona una matriz para multiplicar por escalar")
            return

        try:
            scalar = float(self.scalar_entry.get() or "1.0")
            result = scalar * matrix1
            self.save_to_ans(result)
            self.display_result(result,
                                f"Multiplicación escalar: {scalar} × {matrix1_name}")
        except ValueError:
            self.show_error("Ingresa un valor escalar válido")
        except Exception as e:
            self.show_error(f"Error en multiplicación escalar: {str(e)}")

    def scalar_divide_matrix(self):
        """Divide matrix by scalar"""
        matrix1_name = self.matrix1_combo.get()
        matrix1 = None

        if matrix1_name == "Ans":
            matrix1 = self.ans_matrix
        elif matrix1_name != "Seleccionar...":
            matrix1 = self.matrices.get(matrix1_name)

        if not matrix1:
            self.show_error("Selecciona una matriz para dividir por escalar")
            return

        try:
            scalar = float(self.scalar_entry.get() or "1.0")
            result = matrix1 / scalar
            self.save_to_ans(result)
            self.display_result(result,
                                f"División escalar: {matrix1_name} ÷ {scalar}")
        except ValueError:
            self.show_error("Ingresa un valor escalar válido")
        except Exception as e:
            self.show_error(f"Error en división escalar: {str(e)}")

    def save_to_ans(self, result_matrix):
        """Save result to Ans matrix"""
        self.ans_matrix = result_matrix
        self.update_tab_states()
        self.update_matrix_selectors()

    def display_result(self, result_matrix, operation_text):
        """Display the result matrix in a grid"""
        # Clear existing result display
        if hasattr(self, 'result_grid_frame'):
            self.result_grid_frame.destroy()

        # Create result grid frame
        self.result_grid_frame = ctk.CTkFrame(self.result_frame)
        self.result_grid_frame.pack(pady=5, fill="both", expand=True)

        # Add operation title
        operation_label = ctk.CTkLabel(self.result_grid_frame,
                                       text=operation_text,
                                       font=("Arial", 12, "bold"))
        operation_label.pack(pady=(5, 10))

        # Create grid for result matrix
        grid_frame = ctk.CTkFrame(self.result_grid_frame)
        grid_frame.pack(pady=5)

        for i in range(result_matrix.rows):
            for j in range(result_matrix.cols):
                entry = ctk.CTkEntry(grid_frame,
                                     width=60,
                                     height=30,
                                     state="disabled")
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry.configure(state="normal")
                entry.insert(0, str(result_matrix.data[i][j]))
                entry.configure(state="disabled")

        # Add info label
        info_label = ctk.CTkLabel(self.result_grid_frame,
                                  text="Resultado guardado en Ans")
        info_label.pack(pady=5)

        # Store result for potential saving
        self.last_result = result_matrix
        self.save_result_button.configure(state="normal")

        # Update save selector options
        self.update_save_selector()

    def display_determinant_result(self, determinant_value, operation_text):
        """Display determinant result (special case - not a matrix)"""
        # Clear existing result display
        if hasattr(self, 'result_grid_frame'):
            self.result_grid_frame.destroy()

        # Create result display frame
        self.result_grid_frame = ctk.CTkFrame(self.result_frame)
        self.result_grid_frame.pack(pady=5, fill="both", expand=True)

        # Add operation title - handle both matrix names and expressions
        if operation_text.startswith("Expresión:"):
            title_text = "Resultado de expresión"
            expression_text = operation_text
        else:
            title_text = operation_text
            expression_text = ""

        operation_label = ctk.CTkLabel(self.result_grid_frame,
                                       text=title_text,
                                       font=("Arial", 12, "bold"))
        operation_label.pack(pady=(5, 10))

        # Show expression if it's an expression result
        if expression_text:
            expr_label = ctk.CTkLabel(self.result_grid_frame,
                                      text=expression_text,
                                      font=("Arial", 10),
                                      text_color="gray")
            expr_label.pack(pady=(0, 5))

        # Display determinant value
        det_label = ctk.CTkLabel(self.result_grid_frame,
                                 text=str(determinant_value),
                                 font=("Arial", 16))
        det_label.pack(pady=10)

        # Determinant is not a matrix, so disable save button
        self.last_result = None
        self.save_result_button.configure(state="disabled")

    def save_result_as_matrix(self):
        """Save the last result as a new matrix or overwrite existing one"""
        if not hasattr(self, 'last_result') or self.last_result is None:
            self.show_error("No hay resultado para guardar")
            return

        selected_option = self.save_combo.get()

        if selected_option == "Sin espacio disponible":
            self.show_error("No hay espacio disponible")
            return

        if selected_option.startswith("Matriz "):
            # Extract matrix number and convert to matrix name
            matrix_number = selected_option.split(" ")[1]
            matrix_name = f"Matriz_{matrix_number}"
            self.matrices[matrix_name] = self.last_result
            confirmation_text = f"Resultado guardado en Matriz {matrix_number}"
        else:
            # Create new matrix
            next_name = self.get_next_matrix_name()
            if next_name is None:
                self.show_error("No hay espacio para más matrices")
                return
            self.matrices[next_name] = self.last_result
            matrix_number = next_name.split("_")[1]
            confirmation_text = f"Resultado guardado en Matriz {matrix_number}"

        # Update UI
        self.update_tab_states()
        self.update_matrix_selectors()
        self.update_save_selector()

        # Show confirmation by updating info label
        for widget in self.result_grid_frame.winfo_children():
            if isinstance(widget,
                          ctk.CTkLabel) and "Resultado guardado" in widget.cget(
                    "text"):
                widget.configure(text=confirmation_text)
                break

    def show_error(self, message):
        """Display error message in result area"""
        # Clear existing result display
        if hasattr(self, 'result_grid_frame'):
            self.result_grid_frame.destroy()

        # Create error display frame
        self.result_grid_frame = ctk.CTkFrame(self.result_frame)
        self.result_grid_frame.pack(pady=5, fill="both", expand=True)

        # Display error message
        error_label = ctk.CTkLabel(self.result_grid_frame,
                                   text=f"ERROR: {message}", text_color="red",
                                   font=("Arial", 12))
        error_label.pack(pady=20)

        self.last_result = None
        self.save_result_button.configure(state="disabled")


if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    app = CalculatorGUI()
    app.mainloop()