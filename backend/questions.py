from models import Question

QUESTIONS: list[Question] = [
    # Variables
    Question(
        id=1, level=1, topic="Variables",
        text="¿Qué imprime este código?",
        code="let x = 5;\nlet y = 3;\nconsole.log(x + y);",
        options={"A": "8", "B": "53", "C": "x + y", "D": "Error"},
        correct_option="A",
    ),
    Question(
        id=2, level=2, topic="Variables",
        text="¿Cuál es el valor de 'resultado'?",
        code="let a = 10;\nlet resultado = a * 2 - 5;\nconsole.log(resultado);",
        options={"A": "25", "B": "15", "C": "20", "D": "5"},
        correct_option="B",
    ),
    # Condicionales
    Question(
        id=3, level=3, topic="Condicionales",
        text="¿Qué imprime este código?",
        code=(
            "let edad = 18;\n"
            "if (edad >= 18) {\n"
            "  console.log('Mayor de edad');\n"
            "} else {\n"
            "  console.log('Menor de edad');\n"
            "}"
        ),
        options={"A": "Menor de edad", "B": "Error", "C": "Mayor de edad", "D": "18"},
        correct_option="C",
    ),
    Question(
        id=4, level=4, topic="Condicionales",
        text="¿Qué imprime este código?",
        code=(
            "let x = 7;\n"
            "if (x % 2 === 0) {\n"
            "  console.log('Par');\n"
            "} else {\n"
            "  console.log('Impar');\n"
            "}"
        ),
        options={"A": "Par", "B": "Impar", "C": "0", "D": "Error"},
        correct_option="B",
    ),
    # Ciclos
    Question(
        id=5, level=5, topic="Ciclos",
        text="¿Cuántas veces se ejecuta el console.log?",
        code="for (let i = 0; i < 3; i++) {\n  console.log(i);\n}",
        options={"A": "2", "B": "4", "C": "3", "D": "1"},
        correct_option="C",
    ),
    Question(
        id=6, level=6, topic="Ciclos",
        text="¿Qué imprime este código?",
        code=(
            "let suma = 0;\n"
            "for (let i = 1; i <= 4; i++) {\n"
            "  suma += i;\n"
            "}\n"
            "console.log(suma);"
        ),
        options={"A": "4", "B": "6", "C": "10", "D": "16"},
        correct_option="C",
    ),
    # Funciones
    Question(
        id=7, level=7, topic="Funciones",
        text="¿Qué imprime este código?",
        code=(
            "function saludar(nombre) {\n"
            "  return 'Hola, ' + nombre;\n"
            "}\n"
            "console.log(saludar('Ana'));"
        ),
        options={"A": "saludar(Ana)", "B": "Hola, Ana", "C": "nombre", "D": "Error"},
        correct_option="B",
    ),
    Question(
        id=8, level=8, topic="Funciones",
        text="¿Qué valor retorna la función?",
        code=(
            "function doble(n) {\n"
            "  return n * 2;\n"
            "}\n"
            "console.log(doble(6));"
        ),
        options={"A": "6", "B": "3", "C": "62", "D": "12"},
        correct_option="D",
    ),
    # Variables (extra)
    Question(
        id=9, level=9, topic="Variables",
        text="¿Qué imprime este código?",
        code=(
            "let nombre = 'Juan';\n"
            "let saludo = 'Hola ' + nombre;\n"
            "console.log(saludo);"
        ),
        options={"A": "Hola Juan", "B": "nombre", "C": "Juan", "D": "Error"},
        correct_option="A",
    ),
    # Ciclos (extra)
    Question(
        id=10, level=10, topic="Ciclos",
        text="¿Qué imprime este código?",
        code=(
            "let i = 0;\n"
            "while (i < 3) {\n"
            "  i++;\n"
            "}\n"
            "console.log(i);"
        ),
        options={"A": "0", "B": "2", "C": "3", "D": "4"},
        correct_option="C",
    ),
]
