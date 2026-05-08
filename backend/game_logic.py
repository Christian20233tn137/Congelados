import uuid
from dataclasses import dataclass

from models import GameStatus, Question

INITIAL_LIVES = 3
POINTS_PER_CORRECT = 10


@dataclass
class GameSession:
    session_id: str
    lives: int
    score: int
    current_level: int
    status: GameStatus
    total_questions: int


class GameEngine:
    def __init__(self, questions: list[Question]):
        self.questions = questions
        self._sessions: dict[str, GameSession] = {}

    def start_game(self) -> GameSession:
        session_id = str(uuid.uuid4())
        session = GameSession(
            session_id=session_id,
            lives=INITIAL_LIVES,
            score=0,
            current_level=1,
            status=GameStatus.PLAYING,
            total_questions=len(self.questions),
        )
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> GameSession | None:
        return self._sessions.get(session_id)

    def get_current_question(self, session: GameSession) -> Question | None:
        if session.status != GameStatus.PLAYING:
            return None
        idx = session.current_level - 1
        if idx >= len(self.questions):
            return None
        return self.questions[idx]

    def process_answer(self, session: GameSession, option: str) -> tuple[bool, str]:
        if session.status != GameStatus.PLAYING:
            raise ValueError("La partida ya terminó.")

        question = self.get_current_question(session)
        if question is None:
            raise ValueError("No hay pregunta activa.")

        correct = option == question.correct_option

        if correct:
            session.score += POINTS_PER_CORRECT
            session.current_level += 1
            if session.current_level > len(self.questions):
                session.status = GameStatus.VICTORY
                message = (
                    f"¡Correcto! Completaste todos los niveles. "
                    f"Puntuación final: {session.score} puntos."
                )
            else:
                message = (
                    f"¡Correcto! +{POINTS_PER_CORRECT} puntos. "
                    f"Avanzas al nivel {session.current_level}."
                )
        else:
            session.lives -= 1
            if session.lives <= 0:
                session.lives = 0
                session.status = GameStatus.DEFEAT
                message = (
                    f"Incorrecto. La respuesta correcta era '{question.correct_option}'. "
                    f"Te quedaste sin vidas. Puntuación: {session.score}."
                )
            else:
                message = (
                    f"Incorrecto. La respuesta correcta era '{question.correct_option}'. "
                    f"Te quedan {session.lives} vida(s)."
                )

        return correct, message

    def restart_game(self, session: GameSession) -> GameSession:
        session.lives = INITIAL_LIVES
        session.score = 0
        session.current_level = 1
        session.status = GameStatus.PLAYING
        return session
