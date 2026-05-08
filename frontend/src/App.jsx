import { useState } from 'react';
import StartScreen from './components/StartScreen';
import QuestionScreen from './components/QuestionScreen';
import ResultScreen from './components/ResultScreen';
import * as api from './api';

export default function App() {
  const [view, setView] = useState('start');
  const [sessionId, setSessionId] = useState(null);
  const [question, setQuestion] = useState(null);
  const [lives, setLives] = useState(3);
  const [score, setScore] = useState(0);
  const [totalQuestions, setTotalQuestions] = useState(10);
  const [gameStatus, setGameStatus] = useState('playing');
  const [selectedOption, setSelectedOption] = useState(null);
  const [answerResult, setAnswerResult] = useState(null);
  const [error, setError] = useState(null);

  const handleStart = async () => {
    setError(null);
    try {
      const session = await api.startGame();
      const q = await api.getQuestion(session.session_id);
      setSessionId(session.session_id);
      setQuestion(q);
      setLives(session.lives);
      setScore(session.score);
      setTotalQuestions(session.total_questions);
      setGameStatus('playing');
      setSelectedOption(null);
      setAnswerResult(null);
      setView('playing');
    } catch {
      setError('No se pudo conectar al servidor. Asegúrate de que el backend esté corriendo en el puerto 8000.');
    }
  };

  const handleAnswer = async (option) => {
    if (selectedOption) return;
    setSelectedOption(option);
    try {
      const result = await api.submitAnswer(sessionId, option);
      setAnswerResult(result);
      setLives(result.lives);
      setScore(result.score);
      setGameStatus(result.status);

      setTimeout(async () => {
        if (result.status === 'playing') {
          const q = await api.getQuestion(sessionId);
          setQuestion(q);
          setSelectedOption(null);
          setAnswerResult(null);
        } else {
          setView('result');
        }
      }, 1600);
    } catch {
      setSelectedOption(null);
      setError('Error al enviar la respuesta. Intenta de nuevo.');
    }
  };

  const handleRestart = async () => {
    setError(null);
    try {
      const session = await api.restartGame(sessionId);
      const q = await api.getQuestion(sessionId);
      setQuestion(q);
      setLives(session.lives);
      setScore(session.score);
      setTotalQuestions(session.total_questions);
      setGameStatus('playing');
      setSelectedOption(null);
      setAnswerResult(null);
      setView('playing');
    } catch {
      setError('Error al reiniciar. Intenta de nuevo.');
    }
  };

  if (view === 'start') {
    return <StartScreen onStart={handleStart} error={error} />;
  }

  if (view === 'playing') {
    return (
      <QuestionScreen
        question={question}
        lives={lives}
        score={score}
        totalQuestions={totalQuestions}
        selectedOption={selectedOption}
        answerResult={answerResult}
        onAnswer={handleAnswer}
      />
    );
  }

  return (
    <ResultScreen
      status={gameStatus}
      score={score}
      totalQuestions={totalQuestions}
      onRestart={handleRestart}
      error={error}
    />
  );
}
