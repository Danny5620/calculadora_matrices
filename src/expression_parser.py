import re
from typing import List, Tuple, Dict, Any, Union
from matrix_dataclass import Matrix


class MatrixExpressionParser:
    """Parser for matrix mathematical expressions"""

    def __init__(self, matrices_dict: Dict[str, Matrix],
                 ans_matrix: Matrix = None):
        self.matrices = matrices_dict
        self.ans_matrix = ans_matrix

    def evaluate(self, expression: str) -> Matrix:
        """Main method to evaluate a matrix expression"""
        tokens = self.tokenize(expression)
        result = self.parse_expression(tokens)
        return result

    def tokenize(self, expression: str) -> List[Tuple[str, str]]:
        """Convert expression string into tokens"""
        # Remove spaces
        expression = expression.replace(" ", "")

        # Define patterns for different token types
        patterns = [
            (r'Matriz_\d+', 'MATRIX'),  # Matriz_1, Matriz_2, etc.
            (r'M\d+', 'MATRIX'),  # M1, M2, etc. (shorthand)
            (r'Ans', 'MATRIX'),  # Ans matrix
            (r'\d+\.?\d*', 'NUMBER'),  # Numbers (including decimals)
            (r'\+', 'PLUS'),
            (r'-', 'MINUS'),
            (r'\*', 'MULTIPLY'),
            (r'/', 'DIVIDE'),
            (r'\^T', 'TRANSPOSE'),
            (r'\^-1', 'INVERSE'),
            (r'det\(', 'DETERMINANT'),
            (r'\(', 'LPAREN'),
            (r'\)', 'RPAREN'),
        ]

        tokens = []
        i = 0

        while i < len(expression):
            matched = False

            for pattern, token_type in patterns:
                regex = re.compile(pattern)
                match = regex.match(expression, i)

                if match:
                    value = match.group(0)
                    tokens.append((token_type, value))
                    i = match.end()
                    matched = True
                    break

            if not matched:
                raise ValueError(
                    f"Invalid character at position {i}: '{expression[i]}'")

        return tokens

    def parse_expression(self, tokens: List[Tuple[str, str]]) -> Matrix:
        """Parse tokens into a matrix result using recursive descent parsing"""
        self.tokens = tokens
        self.position = 0
        return self.parse_addition()

    def current_token(self) -> Tuple[str, str]:
        """Get current token"""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return ('EOF', '')

    def consume_token(self, expected_type: str = None) -> Tuple[str, str]:
        """Consume and return current token"""
        token = self.current_token()
        if expected_type and token[0] != expected_type:
            raise ValueError(f"Expected {expected_type}, got {token[0]}")
        self.position += 1
        return token

    def parse_addition(self) -> Matrix:
        """Parse addition and subtraction (lowest precedence)"""
        result = self.parse_multiplication()

        while self.current_token()[0] in ['PLUS', 'MINUS']:
            op_token = self.consume_token()
            right = self.parse_multiplication()

            if op_token[0] == 'PLUS':
                result = result + right
            else:  # MINUS
                result = result - right

        return result

    def parse_multiplication(self) -> Matrix:
        """Parse multiplication and division (higher precedence)"""
        result = self.parse_unary()

        while self.current_token()[0] in ['MULTIPLY', 'DIVIDE']:
            op_token = self.consume_token()
            right = self.parse_unary()

            if op_token[0] == 'MULTIPLY':
                if isinstance(right, (int, float)):
                    result = result * right
                else:
                    result = result * right
            else:  # DIVIDE
                if isinstance(right, (int, float)):
                    result = result / right
                else:
                    raise ValueError("Cannot divide by a matrix")

        return result

    def parse_unary(self) -> Matrix:
        """Parse unary operations (transpose, inverse)"""
        result = self.parse_primary()

        # Handle postfix operators
        while self.current_token()[0] in ['TRANSPOSE', 'INVERSE']:
            op_token = self.consume_token()

            if op_token[0] == 'TRANSPOSE':
                result = result.transpose()
            elif op_token[0] == 'INVERSE':
                result = result.inverse()

        return result

    def parse_primary(self) -> Union[Matrix, float]:
        """Parse primary expressions (matrices, numbers, parentheses)"""
        token = self.current_token()

        if token[0] == 'MATRIX':
            return self.parse_matrix()
        elif token[0] == 'NUMBER':
            return self.parse_number()
        elif token[0] == 'LPAREN':
            return self.parse_parentheses()
        elif token[0] == 'DETERMINANT':
            return self.parse_determinant()
        else:
            raise ValueError(f"Unexpected token: {token}")

    def parse_matrix(self) -> Matrix:
        """Parse matrix reference"""
        token = self.consume_token('MATRIX')
        matrix_name = token[1]

        # Handle different matrix naming conventions
        if matrix_name == 'Ans':
            if self.ans_matrix is None:
                raise ValueError("Ans matrix is not available")
            return self.ans_matrix
        elif matrix_name.startswith('M'):
            # Convert M1, M2, etc. to Matriz_1, Matriz_2, etc.
            number = matrix_name[1:]
            full_name = f"Matriz_{number}"
            if full_name not in self.matrices:
                raise ValueError(f"Matrix {matrix_name} not found")
            return self.matrices[full_name]
        elif matrix_name in self.matrices:
            return self.matrices[matrix_name]
        else:
            raise ValueError(f"Matrix {matrix_name} not found")

    def parse_number(self) -> float:
        """Parse numeric value"""
        token = self.consume_token('NUMBER')
        return float(token[1])

    def parse_parentheses(self) -> Matrix:
        """Parse parenthesized expression"""
        self.consume_token('LPAREN')
        result = self.parse_addition()
        self.consume_token('RPAREN')
        return result

    def parse_determinant(self) -> float:
        """Parse determinant function"""
        self.consume_token('DETERMINANT')
        matrix = self.parse_addition()
        self.consume_token('RPAREN')
        return matrix.determinant()
