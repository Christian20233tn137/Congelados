const BASE = '/game';

async function request(path, options = {}) {
  const res = await fetch(BASE + path, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail ?? `Error ${res.status}`);
  }
  return res.json();
}

export const startGame = () =>
  request('/start', { method: 'POST' });

export const getQuestion = (sessionId) =>
  request(`/${sessionId}/question`);

export const submitAnswer = (sessionId, option) =>
  request(`/${sessionId}/answer`, {
    method: 'POST',
    body: JSON.stringify({ option }),
  });

export const restartGame = (sessionId) =>
  request(`/${sessionId}/restart`, { method: 'POST' });
