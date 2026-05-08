# Código Congelado

> Mini juego web educativo donde el jugador resuelve retos de programación básica para avanzar de nivel.

[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-06B6D4?style=flat&logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![Pytest](https://img.shields.io/badge/pytest-41%20tests-brightgreen?style=flat&logo=pytest&logoColor=white)](https://pytest.org)

---

## Descripción

**Código Congelado** es un mini juego web pensado para que alumnos de primer cuatrimestre practiquen conceptos básicos de programación. El jugador responde preguntas de opción múltiple sobre código JavaScript; cada acierto suma puntos y cada error cuesta una vida.

El proyecto fue desarrollado siguiendo la **metodología Cascada**, pasando por las fases de requisitos, análisis, diseño, desarrollo, pruebas y entrega.

---

## Cómo funciona

```
Inicio → Pregunta 1 → Pregunta 2 → ... → Pregunta 10 → Resultado final
           ↓ correcta: +10 pts, siguiente nivel
           ↓ incorrecta: −1 vida  →  0 vidas: derrota
```

| Regla                          | Valor         |
|-------------------------------|---------------|
| Vidas iniciales               | 3             |
| Puntos por respuesta correcta | +10           |
| Puntos por respuesta incorrecta | 0           |
| Condición de victoria         | 10/10 aciertos antes de perder las vidas |
| Condición de derrota          | 3 errores     |

---

## Temas que cubre

| Tema           | Preguntas |
|----------------|-----------|
| Variables      | 3         |
| Condicionales  | 2         |
| Ciclos         | 3         |
| Funciones      | 2         |

---

## Stack tecnológico

| Capa      | Tecnología                          |
|-----------|-------------------------------------|
| Backend   | Python 3.13 + FastAPI + Uvicorn     |
| Frontend  | React 19 + Vite 6 + Tailwind CSS 3  |
| Pruebas   | pytest + httpx + TestClient         |

---

## Estructura del proyecto

```
Congelados/
├── backend/
│   ├── main.py          # Rutas FastAPI
│   ├── game_logic.py    # Motor del juego (GameEngine)
│   ├── models.py        # Modelos Pydantic
│   ├── questions.py     # Banco de 10 preguntas
│   ├── requirements.txt
│   └── tests/
│       ├── conftest.py
│       └── test_game.py # 41 pruebas automatizadas
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Estado global y navegación
│   │   ├── api.js               # Capa de comunicación con el backend
│   │   ├── index.css            # Directivas Tailwind
│   │   └── components/
│   │       ├── StartScreen.jsx  # Pantalla de inicio
│   │       ├── QuestionScreen.jsx # Pantalla de pregunta
│   │       └── ResultScreen.jsx   # Pantalla de resultado
│   ├── tailwind.config.js
│   ├── vite.config.js           # Proxy /game → localhost:8000
│   └── package.json
│
├── requisitos_codigo_congelado.md
├── .gitignore
└── README.md
```

---

## Instalación y ejecución

### Requisitos previos

- Python 3.11+
- Node.js 18+

### 1. Clonar el repositorio

```bash
git clone <url-del-repo>
cd Congelados
```

### 2. Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

El servidor queda disponible en `http://localhost:8000`.  
La documentación interactiva (Swagger UI) en `http://localhost:8000/docs`.

### 3. Frontend

Abre una segunda terminal:

```bash
cd frontend
npm install
npm run dev
```

El juego queda disponible en `http://localhost:5173`.

---

## API — Endpoints

| Método | Ruta                          | Descripción                              |
|--------|-------------------------------|------------------------------------------|
| `POST` | `/game/start`                 | Inicia una nueva partida                 |
| `GET`  | `/game/{session_id}/question` | Obtiene la pregunta del nivel actual     |
| `POST` | `/game/{session_id}/answer`   | Envía la respuesta seleccionada          |
| `GET`  | `/game/{session_id}/status`   | Consulta el estado de la sesión          |
| `POST` | `/game/{session_id}/restart`  | Reinicia la partida con la misma sesión  |

### Ejemplo — iniciar partida

```bash
curl -X POST http://localhost:8000/game/start
```

```json
{
  "session_id": "a1b2c3d4-...",
  "lives": 3,
  "score": 0,
  "current_level": 1,
  "status": "playing",
  "total_questions": 10,
  "message": "¡Bienvenido a Código Congelado!"
}
```

### Ejemplo — enviar respuesta

```bash
curl -X POST http://localhost:8000/game/{session_id}/answer \
  -H "Content-Type: application/json" \
  -d '{"option": "A"}'
```

```json
{
  "correct": true,
  "correct_option": "A",
  "lives": 3,
  "score": 10,
  "current_level": 2,
  "status": "playing",
  "message": "¡Correcto! +10 puntos. Avanzas al nivel 2."
}
```

---

## Pruebas

```bash
cd backend
python -m pytest tests/ -v
```

```
41 passed in 0.98s
```

Las pruebas cubren:

- Inicio de partida y unicidad de sesiones
- Respuestas correctas e incorrectas
- Condición de derrota (3 errores)
- Condición de victoria (10 aciertos)
- Reinicio de partida
- Estado de sesión
- Lógica de negocio del `GameEngine` de forma aislada

---

## Metodología

El proyecto sigue la **metodología Cascada** en 6 fases:

1. **Requisitos** — funcionales (RF-01 a RF-15) y no funcionales (RNF-01 a RNF-09)
2. **Análisis** — usuarios, reglas del juego y módulos del sistema
3. **Diseño** — pantallas, flujo de navegación y estructura de datos
4. **Desarrollo** — backend (FastAPI) y frontend (React + Tailwind)
5. **Pruebas** — 41 casos automatizados con pytest
6. **Entrega** — juego funcional, API documentada y pruebas verificadas

El documento completo de requisitos está en [`requisitos_codigo_congelado.md`](./requisitos_codigo_congelado.md).
