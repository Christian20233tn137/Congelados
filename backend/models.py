from pydantic import BaseModel
from enum import Enum
from typing import Optional


class GameStatus(str, Enum):
    PLAYING = "playing"
    VICTORY = "victory"
    DEFEAT = "defeat"


class Option(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class Question(BaseModel):
    id: int
    level: int
    topic: str
    text: str
    code: Optional[str] = None
    options: dict[str, str]
    correct_option: str


class StartGameResponse(BaseModel):
    session_id: str
    lives: int
    score: int
    current_level: int
    status: GameStatus
    total_questions: int
    message: str


class QuestionResponse(BaseModel):
    session_id: str
    level: int
    topic: str
    text: str
    code: Optional[str] = None
    options: dict[str, str]
    lives: int
    score: int
    status: GameStatus


class AnswerRequest(BaseModel):
    option: Option


class AnswerResponse(BaseModel):
    correct: bool
    correct_option: str
    lives: int
    score: int
    current_level: int
    status: GameStatus
    message: str


class StatusResponse(BaseModel):
    session_id: str
    lives: int
    score: int
    current_level: int
    status: GameStatus
    total_questions: int
