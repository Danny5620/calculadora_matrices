# Calculadora de Matrices

Una calculadora de matrices con interfaz gráfica moderna desarrollada en Python con CustomTkinter.

## Características

- ✨ Interfaz moderna y amigable
- 🔢 Soporte para matrices hasta 10x10
- ➕ Operaciones básicas: suma, resta, multiplicación
- 🔄 Operaciones avanzadas: transposición, determinante, inversa
- 📊 Operaciones con escalares
- 🧮 Evaluación de expresiones matemáticas complejas
- 💾 Sistema de almacenamiento de múltiples matrices
- 📝 Matriz "Ans" para resultados previos

## Operaciones Soportadas

### Operaciones Básicas
- Suma de matrices (A + B)
- Resta de matrices (A - B)
- Multiplicación de matrices (A × B)

### Operaciones Unarias
- Transposición (A^T)
- Determinante (det(A))
- Matriz inversa (A^-1)

### Operaciones con Escalares
- Multiplicación por escalar (k × A)
- División por escalar (A ÷ k)

### Expresiones Combinadas
Evalúa expresiones matemáticas complejas como:
- `(M1 + M2) * 3`
- `M1^T * M2^-1`
- `det(M1) * M2 + M3`
- `(M1 - M2)^T + Ans`

## Instalación

### Método 1: Ejecutable (Recomendado)
1. Descarga el archivo `CalculadoraMatrices.exe` desde [Releases](../../releases)
2. Ejecuta el archivo directamente (no requiere instalación de Python)

### Método 2: Desde el código fuente
1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu-usuario/calculadora_matrices.git
   cd calculadora_matrices
    ```
2. Instala las dependencias:
    ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta la aplicación:
   ```bash
    python main.py
    ```

## Uso

1. Crear Matrices: Selecciona las dimensiones y usa los tabs M1, M2, M3, M4 para crear matrices
2. Operaciones Básicas: Selecciona dos matrices y usa los botones de operación
3. Expresiones: Usa la sección de "Operaciones Combinadas" para expresiones complejas
4. Resultados: Los resultados se guardan automáticamente en "Ans"

## Sintaxis de Expresiones

- M1, M2, M3, M4: Referencias a las matrices creadas
- Ans: Resultado de la última operación
- Operadores escalares:
  - `k * M` para multiplicación por escalar
  - `M / k` para división por escalar
- Operadores binarios:
  - `+` para suma
  - `-` para resta
  - `*` para multiplicación
- Operadores unarios:
  - `M^T` para transposición
  - `det(M)` para determinante
  - `M^-1` para inversa
