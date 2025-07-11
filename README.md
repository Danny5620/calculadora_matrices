# 🧮 Calculadora de Matrices

Una calculadora de matrices avanzada con interfaz gráfica moderna desarrollada en Python con CustomTkinter. Diseñada para estudiantes, profesores y profesionales que necesitan realizar cálculos matriciales de forma rápida y eficiente.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Instalación](#instalación)
- [Uso](#uso)
- [Operaciones Soportadas](#operaciones-soportadas)
- [Sintaxis de Expresiones](#sintaxis-de-expresiones)
- [Ejemplos](#ejemplos)
- [Solución de Problemas](#solución-de-problemas)

## ✨ Características

- 🎨 **Interfaz moderna y amigable** - Diseño intuitivo con CustomTkinter
- 📐 **Soporte para matrices grandes** - Hasta 10x10 elementos
- 🔢 **Operaciones básicas** - Suma, resta, multiplicación de matrices
- 🔄 **Operaciones avanzadas** - Transposición, determinante, matriz inversa
- 📊 **Operaciones con escalares** - Multiplicación y división por números
- 🧮 **Evaluador de expresiones** - Expresiones matemáticas complejas
- 💾 **Sistema de almacenamiento** - Guarda múltiples matrices simultáneamente
- 📝 **Matriz "Ans"** - Acceso rápido a resultados previos
- 🎯 **Validación de entrada** - Verificación automática de datos
- 🔧 **Manejo de errores** - Mensajes claros y útiles


## 🚀 Instalación

### Método 1: Ejecutable (Recomendado)
1. Descarga el archivo `CalculadoraMatrices.exe` desde [Releases](../../releases)
2. Ejecuta el archivo directamente
3. ¡Listo! No requiere instalación de Python ni dependencias

### Método 2: Desde el Código Fuente
1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/calculadora_matrices.git
   cd calculadora_matrices
   ```

2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta la aplicación:**
   ```bash
   python main.py
   ```

## 📖 Uso

### Inicio Rápido
1. **Crear Matrices:** Selecciona las dimensiones deseadas y usa los tabs M1, M2, M3, M4
2. **Llenar Datos:** Introduce los valores en cada celda de la matriz
3. **Operaciones Básicas:** Selecciona dos matrices y usa los botones de operación
4. **Expresiones Avanzadas:** Usa la sección "Operaciones Combinadas" para cálculos complejos
5. **Ver Resultados:** Los resultados aparecen automáticamente y se guardan en "Ans"

### Flujo de Trabajo Típico
1. Define las dimensiones de tu matriz
2. Ingresa los valores numéricos
3. Selecciona la operación deseada
4. Revisa el resultado en la matriz "Ans"
5. Usa "Ans" en operaciones posteriores si es necesario

## 🔧 Operaciones Soportadas

### Operaciones Básicas
- ➕ **Suma de matrices** (A + B) - Matrices del mismo tamaño
- ➖ **Resta de matrices** (A - B) - Matrices del mismo tamaño
- ✖️ **Multiplicación de matrices** (A × B) - Dimensiones compatibles

### Operaciones Unarias
- 🔄 **Transposición** (A^T) - Intercambia filas y columnas
- 🔢 **Determinante** (det(A)) - Solo para matrices cuadradas
- ↩️ **Matriz inversa** (A^-1) - Solo para matrices invertibles

### Operaciones con Escalares
- 📊 **Multiplicación por escalar** (k × A) - Multiplica cada elemento
- ➗ **División por escalar** (A ÷ k) - Divide cada elemento

### Expresiones Combinadas
Evalúa expresiones matemáticas complejas combinando múltiples operaciones:
- Operaciones anidadas con paréntesis
- Combinación de operaciones matriciales y escalares
- Uso de resultados previos (Ans)

## 📝 Sintaxis de Expresiones

### Referencias a Matrices
- `M1`, `M2`, `M3`, `M4` - Matrices creadas por el usuario
- `Ans` - Resultado de la última operación

### Operadores Escalares
- `k * M` - Multiplicación por escalar
- `M / k` - División por escalar
- `k` - Cualquier número real

### Operadores Binarios
- `+` - Suma de matrices
- `-` - Resta de matrices
- `*` - Multiplicación de matrices

### Operadores Unarios
- `M^T` - Transposición
- `det(M)` - Determinante
- `M^-1` - Matriz inversa

### Agrupación
- `()` - Paréntesis para agrupar operaciones

## 💡 Ejemplos

### Operaciones Básicas
```
M1 + M2                    # Suma simple
M1 - M2                    # Resta simple
M1 * M2                    # Multiplicación
```

### Operaciones con Escalares
```
3 * M1                     # Multiplicar por 3
M1 / 2                     # Dividir por 2
```

### Operaciones Avanzadas
```
M1^T                       # Transposición
det(M1)                    # Determinante
M1^-1                      # Matriz inversa
```

### Expresiones Complejas
```
(M1 + M2) * 3              # Suma y multiplicación por escalar
M1^T * M2^-1               # Transposición y multiplicación por inversa
det(M1) * M2 + M3          # Determinante como escalar
(M1 - M2)^T + Ans          # Combinación con resultado previo
```

## 🔍 Solución de Problemas

### Errores Comunes

**Error: "Las matrices no son del mismo tamaño"**
- Verifica que ambas matrices tengan las mismas dimensiones para suma/resta

**Error: "Dimensiones incompatibles para multiplicación"**
- Para A × B, el número de columnas de A debe igual al número de filas de B

**Error: "La matriz no es cuadrada"**
- El determinante y la inversa requieren matrices cuadradas (n×n)

**Error: "La matriz no es invertible"**
- La matriz tiene determinante cero, no se puede calcular la inversa

### Consejos de Rendimiento
- Para matrices grandes (8×8 o más), los cálculos pueden tomar unos segundos
- Verifica que todos los campos estén llenos antes de calcular
- USA números decimales con punto (.), no coma (,)

### Áreas de Mejora
- Soporte para matrices de mayor tamaño
- Exportación a diferentes formatos
- Más operaciones matriciales especializadas
- Interfaz en múltiples idiomas

