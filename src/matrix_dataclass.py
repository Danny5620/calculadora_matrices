## Define what a matrix is in the dataclass

from dataclasses import dataclass
from typing import List


MATRIX_ROWS_OPTIONS: List[str] = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
MATRIX_COLS_OPTIONS: List[str] = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]


@dataclass
class Matrix:
    """A class to represent a matrix."""

    rows: int
    cols: int
    data: List[List[float]]

    def __post_init__(self):
        if self.rows < 0:
            raise ValueError("Row cannot be negative.")

        if self.cols < 0:
            raise ValueError("Column cannot be negative.")

        if len(self.data) != self.rows or any(len(row) != self.cols for row in self.data):
            raise ValueError("Data does not match specified dimensions.")

    def __init__(self, rows: int, cols: int, data: List[List[float]]):
        """Initializes a matrix with the given number of rows, columns, and data."""
        self.rows = rows
        self.cols = cols
        self.data = data

    def __str__(self):
        return "\n".join(["\t".join(map(str, row)) for row in self.data])

    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Can only add another Matrix.")

        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for addition.")

        result_data = []
        for i in range(self.rows):
            result_row = []
            for j in range(self.cols):
                result_row.append(self.data[i][j] + other.data[i][j])
            result_data.append(result_row)

        return Matrix(self.rows, self.cols, data=result_data)

    def __sub__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Can only subtract another Matrix.")

        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for subtraction.")

        result_data = []
        for i in range(self.rows):
            result_row = []
            for j in range(self.cols):
                result_row.append(self.data[i][j] - other.data[i][j])
            result_data.append(result_row)

        return Matrix(self.rows, self.cols, data=result_data)

    def scalar_multiply(self, scalar: float):
        """Multiplies the matrix by a scalar."""
        result_data = []
        for i in range(self.rows):
            result_row = []
            for j in range(self.cols):
                result_row.append(scalar * self.data[i][j])
            result_data.append(result_row)

        return Matrix(self.rows, self.cols, data=result_data)

    def matrix_multiply(self, other):
        """Multiplies the matrix by another matrix."""
        if self.cols != other.rows:
            raise ValueError("Number of columns in the first matrix must equal number of rows in the second matrix.")

        result_data = []
        for i in range(self.rows):
            result_row = []
            for j in range(other.cols):
                sum_product = sum(
                    self.data[i][k] * other.data[k][j] for k in
                    range(self.cols))
                result_row.append(sum_product)
            result_data.append(result_row)

        return Matrix(self.rows, other.cols, data=result_data)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self.scalar_multiply(other)
        elif isinstance(other, Matrix):
            return self.matrix_multiply(other)
        else:
            raise TypeError("Unsupported type for multiplication. Use a scalar or another Matrix.")

    def __rmul__(self, scalar: float):
        """Allows scalar multiplication from the left."""
        return self.scalar_multiply(scalar)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise ValueError("Cannot divide by zero.")
            return self.scalar_multiply(1 / other)
        else:
            raise TypeError("Can only divide by a scalar.")

    def transpose(self):
        """Transposes the matrix."""
        result_data = []
        for j in range(self.cols):
            result_row = []
            for i in range(self.rows):
                result_row.append(self.data[i][j])
            result_data.append(result_row)

        return Matrix(self.cols, self.rows, data=result_data)

    def determinant(self):
        """Calculates the determinant of the matrix."""
        if self.rows != self.cols:
            raise ValueError("Determinant can only be calculated for square matrices.")

        if self.rows == 1:
            return self.data[0][0]
        if self.rows == 2:
            return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]

        determinant = 0
        for col in range(self.cols):
            sub_matrix = Matrix(
                self.rows - 1, self.cols - 1,
                data=[row[:col] + row[col + 1:] for i, row in enumerate(self.data) if i != 0]
            )
            sign = (-1) ** col
            determinant += sign * self.data[0][col] * sub_matrix.determinant()

        del sub_matrix

        return determinant

    def inverse(self):
        """Calculates the inverse of the matrix."""
        if self.rows != self.cols:
            raise ValueError("Inverse can only be calculated for square matrices.")

        determinant = self.determinant()
        if determinant == 0:
            raise ValueError("Matrix is singular and cannot be inverted.")

        cofactor_data = []
        for i in range(self.rows):
            cofactor_row = []
            for j in range(self.cols):
                sub_matrix = Matrix(
                    self.rows - 1, self.cols - 1,
                    data=[row[:j] + row[j + 1:] for k, row in enumerate(self.data) if k != i]
                )
                sign = (-1) ** (i + j)
                cofactor_row.append(sign * sub_matrix.determinant())
            cofactor_data.append(cofactor_row)
        cofactor_matrix = Matrix(self.rows, self.cols, data=cofactor_data)
        adjugate_matrix = cofactor_matrix.transpose()

        inverse_matrix = adjugate_matrix / determinant
        del cofactor_matrix
        del adjugate_matrix

        return inverse_matrix
