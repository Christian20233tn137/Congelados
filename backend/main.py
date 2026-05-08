from fastapi import FastAPI, HTTPException

from game_logic import GameEngine
from models import (
    AnswerRequest,
    AnswerResponse,
    GameStatus,
    QuestionResponse,
    StartGameResponse,
    StatusResponse,
)
from questions import QUESTIONS

app = FastAPI(
    title="Código Congelado API",
    description="Backend del mini juego educativo de programación básica.",
    version="1.0.0",
)

engine = GameEngine(QUESTIONS)


@app.post("/game/start", response_model=StartGameResponse, status_code=201, tags=["game"])
def start_game():
    session = engine.start_game()
    return StartGameResponse(
        session_id=session.session_id,
        lives=session.lives,
        score=session.score,
        current_level=session.current_level,
        status=session.status,
        total_questions=session.total_questions,
        message="¡Bienvenido a Código Congelado! Responde correctamente para avanzar.",
    )


@app.get("/game/{session_id}/question", response_model=QuestionResponse, tags=["game"])
def get_question(session_id: str):
    session = engine.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Sesión no encontrada.")

    if session.status != GameStatus.PLAYING:
        raise HTTPException(
            status_code=409,
            detail=f"La partida ha terminado con estado: {session.status}.",
        )

    question = engine.get_current_question(session)
    if question is None:
        raise HTTPException(status_code=404, detail="No hay pregunta disponible.")

    return QuestionResponse(
        session_id=session_id,
        level=question.level,
        topic=question.topic,
        text=question.text,
        code=question.code,
        options=question.options,
        lives=session.lives,
        score=session.score,
        status=session.status,
    )


@app.post("/game/{session_id}/answer", response_model=AnswerResponse, tags=["game"])
def submit_answer(session_id: str, body: AnswerRequest):
    session = engine.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Sesión no encontrada.")

    question = engine.get_current_question(session)
    if question is None:
        raise HTTPException(
            status_code=409,
            detail="La partida ya terminó o no hay pregunta activa.",
        )

    try:
        correct, message = engine.process_answer(session, body.option.value)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    return AnswerResponse(
        correct=correct,
        correct_option=question.correct_option,
        lives=session.lives,
        score=session.score,
        current_level=session.current_level,
        status=session.status,
        message=message,
    )


@app.get("/game/{session_id}/status", response_model=StatusResponse, tags=["game"])
def get_status(session_id: str):
    session = engine.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Sesión no encontrada.")

    return StatusResponse(
        session_id=session.session_id,
        lives=session.lives,
        score=session.score,
        current_level=session.current_level,
        status=session.status,
        total_questions=session.total_questions,
    )


@app.post("/game/{session_id}/restart", response_model=StartGameResponse, tags=["game"])
def restart_game(session_id: str):
    session = engine.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Sesión no encontrada.")

    session = engine.restart_game(session)
    return StartGameResponse(
        session_id=session.session_id,
        lives=session.lives,
        score=session.score,
        current_level=session.current_level,
        status=session.status,
        total_questions=session.total_questions,
        message="¡Juego reiniciado! Buena suerte.",
    )
