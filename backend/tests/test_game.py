import pytest
from fastapi.testclient import TestClient

from game_logic import INITIAL_LIVES, POINTS_PER_CORRECT, GameEngine
from main import app
from models import GameStatus
from questions import QUESTIONS

client = TestClient(app)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _wrong_option(correct_option: str) -> str:
    return next(o for o in ["A", "B", "C", "D"] if o != correct_option)


def _lose_all_lives(session_id: str) -> None:
    wrong = _wrong_option(QUESTIONS[0].correct_option)
    for _ in range(INITIAL_LIVES):
        client.post(f"/game/{session_id}/answer", json={"option": wrong})


def _win_game(session_id: str) -> None:
    for q in QUESTIONS:
        client.post(f"/game/{session_id}/answer", json={"option": q.correct_option})


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def session_id() -> str:
    response = client.post("/game/start")
    assert response.status_code == 201
    return response.json()["session_id"]


@pytest.fixture
def engine() -> GameEngine:
    return GameEngine(QUESTIONS)


# ---------------------------------------------------------------------------
# Inicio de partida
# ---------------------------------------------------------------------------

class TestStartGame:
    def test_returns_201(self):
        assert client.post("/game/start").status_code == 201

    def test_initial_state(self):
        data = client.post("/game/start").json()
        assert data["lives"] == INITIAL_LIVES
        assert data["score"] == 0
        assert data["current_level"] == 1
        assert data["status"] == "playing"
        assert data["total_questions"] == len(QUESTIONS)
        assert "session_id" in data
        assert "message" in data

    def test_sessions_are_unique(self):
        id1 = client.post("/game/start").json()["session_id"]
        id2 = client.post("/game/start").json()["session_id"]
        assert id1 != id2


# ---------------------------------------------------------------------------
# Obtener pregunta
# ---------------------------------------------------------------------------

class TestGetQuestion:
    def test_returns_200(self, session_id):
        assert client.get(f"/game/{session_id}/question").status_code == 200

    def test_has_required_fields(self, session_id):
        data = client.get(f"/game/{session_id}/question").json()
        for field in ("text", "options", "level", "topic", "lives", "score", "status"):
            assert field in data

    def test_has_four_options(self, session_id):
        data = client.get(f"/game/{session_id}/question").json()
        assert len(data["options"]) == 4

    def test_first_question_is_level_1(self, session_id):
        data = client.get(f"/game/{session_id}/question").json()
        assert data["level"] == 1

    def test_unknown_session_returns_404(self):
        assert client.get("/game/nonexistent-xyz/question").status_code == 404

    def test_returns_409_when_game_over(self, session_id):
        _lose_all_lives(session_id)
        assert client.get(f"/game/{session_id}/question").status_code == 409


# ---------------------------------------------------------------------------
# Respuesta correcta
# ---------------------------------------------------------------------------

class TestCorrectAnswer:
    def test_adds_points(self, session_id):
        correct = QUESTIONS[0].correct_option
        data = client.post(f"/game/{session_id}/answer", json={"option": correct}).json()
        assert data["correct"] is True
        assert data["score"] == POINTS_PER_CORRECT

    def test_advances_level(self, session_id):
        correct = QUESTIONS[0].correct_option
        client.post(f"/game/{session_id}/answer", json={"option": correct})
        status = client.get(f"/game/{session_id}/status").json()
        assert status["current_level"] == 2

    def test_does_not_lose_lives(self, session_id):
        correct = QUESTIONS[0].correct_option
        data = client.post(f"/game/{session_id}/answer", json={"option": correct}).json()
        assert data["lives"] == INITIAL_LIVES

    def test_each_correct_adds_exactly_10_points(self, session_id):
        for i, q in enumerate(QUESTIONS[:3], start=1):
            data = client.post(f"/game/{session_id}/answer", json={"option": q.correct_option}).json()
            assert data["score"] == POINTS_PER_CORRECT * i


# ---------------------------------------------------------------------------
# Respuesta incorrecta
# ---------------------------------------------------------------------------

class TestWrongAnswer:
    def test_loses_one_life(self, session_id):
        wrong = _wrong_option(QUESTIONS[0].correct_option)
        data = client.post(f"/game/{session_id}/answer", json={"option": wrong}).json()
        assert data["correct"] is False
        assert data["lives"] == INITIAL_LIVES - 1

    def test_does_not_add_points(self, session_id):
        wrong = _wrong_option(QUESTIONS[0].correct_option)
        data = client.post(f"/game/{session_id}/answer", json={"option": wrong}).json()
        assert data["score"] == 0

    def test_does_not_advance_level(self, session_id):
        wrong = _wrong_option(QUESTIONS[0].correct_option)
        client.post(f"/game/{session_id}/answer", json={"option": wrong})
        status = client.get(f"/game/{session_id}/status").json()
        assert status["current_level"] == 1

    def test_response_includes_correct_option(self, session_id):
        wrong = _wrong_option(QUESTIONS[0].correct_option)
        data = client.post(f"/game/{session_id}/answer", json={"option": wrong}).json()
        assert data["correct_option"] == QUESTIONS[0].correct_option


# ---------------------------------------------------------------------------
# Derrota
# ---------------------------------------------------------------------------

class TestDefeat:
    def test_status_is_defeat_after_three_wrong(self, session_id):
        _lose_all_lives(session_id)
        status = client.get(f"/game/{session_id}/status").json()
        assert status["status"] == "defeat"

    def test_lives_is_zero_on_defeat(self, session_id):
        _lose_all_lives(session_id)
        status = client.get(f"/game/{session_id}/status").json()
        assert status["lives"] == 0

    def test_cannot_answer_after_defeat(self, session_id):
        _lose_all_lives(session_id)
        response = client.post(f"/game/{session_id}/answer", json={"option": "A"})
        assert response.status_code == 409

    def test_score_unchanged_on_defeat(self, session_id):
        # answer one correct, then lose all lives on next level
        client.post(f"/game/{session_id}/answer", json={"option": QUESTIONS[0].correct_option})
        wrong = _wrong_option(QUESTIONS[1].correct_option)
        for _ in range(INITIAL_LIVES):
            client.post(f"/game/{session_id}/answer", json={"option": wrong})
        status = client.get(f"/game/{session_id}/status").json()
        assert status["score"] == POINTS_PER_CORRECT


# ---------------------------------------------------------------------------
# Victoria
# ---------------------------------------------------------------------------

class TestVictory:
    def test_status_is_victory_after_all_correct(self):
        sid = client.post("/game/start").json()["session_id"]
        _win_game(sid)
        status = client.get(f"/game/{sid}/status").json()
        assert status["status"] == "victory"

    def test_maximum_score_after_winning(self):
        sid = client.post("/game/start").json()["session_id"]
        _win_game(sid)
        status = client.get(f"/game/{sid}/status").json()
        assert status["score"] == POINTS_PER_CORRECT * len(QUESTIONS)

    def test_lives_unchanged_after_perfect_game(self):
        sid = client.post("/game/start").json()["session_id"]
        _win_game(sid)
        status = client.get(f"/game/{sid}/status").json()
        assert status["lives"] == INITIAL_LIVES

    def test_cannot_answer_after_victory(self):
        sid = client.post("/game/start").json()["session_id"]
        _win_game(sid)
        response = client.post(f"/game/{sid}/answer", json={"option": "A"})
        assert response.status_code == 409


# ---------------------------------------------------------------------------
# Reinicio
# ---------------------------------------------------------------------------

class TestRestart:
    def test_resets_to_initial_state(self, session_id):
        client.post(f"/game/{session_id}/answer", json={"option": QUESTIONS[0].correct_option})
        data = client.post(f"/game/{session_id}/restart").json()
        assert data["lives"] == INITIAL_LIVES
        assert data["score"] == 0
        assert data["current_level"] == 1
        assert data["status"] == "playing"

    def test_restart_after_defeat(self, session_id):
        _lose_all_lives(session_id)
        data = client.post(f"/game/{session_id}/restart").json()
        assert data["status"] == "playing"
        assert data["lives"] == INITIAL_LIVES

    def test_restart_after_victory(self):
        sid = client.post("/game/start").json()["session_id"]
        _win_game(sid)
        data = client.post(f"/game/{sid}/restart").json()
        assert data["status"] == "playing"
        assert data["score"] == 0

    def test_unknown_session_returns_404(self):
        assert client.post("/game/nonexistent/restart").status_code == 404


# ---------------------------------------------------------------------------
# Estado de la sesión
# ---------------------------------------------------------------------------

class TestStatus:
    def test_returns_200(self, session_id):
        assert client.get(f"/game/{session_id}/status").status_code == 200

    def test_initial_status(self, session_id):
        data = client.get(f"/game/{session_id}/status").json()
        assert data["lives"] == INITIAL_LIVES
        assert data["score"] == 0
        assert data["current_level"] == 1
        assert data["status"] == "playing"
        assert data["total_questions"] == len(QUESTIONS)

    def test_unknown_session_returns_404(self):
        assert client.get("/game/nonexistent/status").status_code == 404


# ---------------------------------------------------------------------------
# Lógica de negocio — GameEngine (unit tests)
# ---------------------------------------------------------------------------

class TestGameEngine:
    def test_start_creates_session_with_initial_state(self, engine):
        session = engine.start_game()
        assert session.lives == INITIAL_LIVES
        assert session.score == 0
        assert session.current_level == 1
        assert session.status == GameStatus.PLAYING

    def test_get_session_returns_none_for_unknown_id(self, engine):
        assert engine.get_session("nonexistent") is None

    def test_correct_answer_updates_score_and_level(self, engine):
        session = engine.start_game()
        q = engine.get_current_question(session)
        correct, _ = engine.process_answer(session, q.correct_option)
        assert correct is True
        assert session.score == POINTS_PER_CORRECT
        assert session.current_level == 2

    def test_wrong_answer_reduces_lives(self, engine):
        session = engine.start_game()
        q = engine.get_current_question(session)
        wrong = _wrong_option(q.correct_option)
        correct, _ = engine.process_answer(session, wrong)
        assert correct is False
        assert session.lives == INITIAL_LIVES - 1
        assert session.score == 0

    def test_defeat_when_lives_reach_zero(self, engine):
        session = engine.start_game()
        q = engine.get_current_question(session)
        wrong = _wrong_option(q.correct_option)
        for _ in range(INITIAL_LIVES):
            engine.process_answer(session, wrong)
        assert session.status == GameStatus.DEFEAT
        assert session.lives == 0

    def test_victory_when_all_questions_answered(self, engine):
        session = engine.start_game()
        for q in QUESTIONS:
            engine.process_answer(session, q.correct_option)
        assert session.status == GameStatus.VICTORY
        assert session.score == POINTS_PER_CORRECT * len(QUESTIONS)

    def test_raises_when_answering_after_game_over(self, engine):
        session = engine.start_game()
        q = engine.get_current_question(session)
        wrong = _wrong_option(q.correct_option)
        for _ in range(INITIAL_LIVES):
            engine.process_answer(session, wrong)
        with pytest.raises(ValueError, match="La partida ya terminó"):
            engine.process_answer(session, "A")

    def test_get_current_question_returns_none_after_game_over(self, engine):
        session = engine.start_game()
        q = engine.get_current_question(session)
        wrong = _wrong_option(q.correct_option)
        for _ in range(INITIAL_LIVES):
            engine.process_answer(session, wrong)
        assert engine.get_current_question(session) is None

    def test_restart_resets_all_fields(self, engine):
        session = engine.start_game()
        engine.process_answer(session, QUESTIONS[0].correct_option)
        engine.restart_game(session)
        assert session.lives == INITIAL_LIVES
        assert session.score == 0
        assert session.current_level == 1
        assert session.status == GameStatus.PLAYING
