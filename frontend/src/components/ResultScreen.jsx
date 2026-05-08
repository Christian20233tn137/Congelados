const PTS_PER_Q = 10;

export default function ResultScreen({ status, score, totalQuestions, onRestart, error }) {
  const isVictory = status === 'victory';
  const maxScore  = totalQuestions * PTS_PER_Q;
  const pct       = maxScore > 0 ? Math.round((score / maxScore) * 100) : 0;

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <div className="w-full max-w-md animate-fade-in">
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-2xl">

          {/* Result icon */}
          <div className={`w-20 h-20 mx-auto mb-6 rounded-2xl flex items-center justify-center border ${
            isVictory
              ? 'bg-emerald-500/10 border-emerald-500/25'
              : 'bg-rose-500/10 border-rose-500/25'
          }`}>
            <span className={`text-4xl font-black leading-none select-none ${
              isVictory ? 'text-emerald-400' : 'text-rose-400'
            }`}>
              {isVictory ? '✓' : '✕'}
            </span>
          </div>

          {/* Title */}
          <h2 className={`text-3xl font-black text-center mb-2 ${
            isVictory ? 'text-emerald-400' : 'text-rose-400'
          }`}>
            {isVictory ? '¡Lo lograste!' : 'Fin del juego'}
          </h2>
          <p className="text-center text-slate-400 text-sm mb-8 leading-relaxed">
            {isVictory
              ? 'Completaste todos los niveles sin quedarte sin vidas.'
              : 'Te quedaste sin vidas. Practica y vuelve a intentarlo.'}
          </p>

          {/* Score card */}
          <div className="bg-slate-950 border border-slate-800 rounded-xl p-6 mb-6 text-center">
            <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-3">
              Puntuación final
            </p>
            <p className="text-6xl font-black text-blue-400 leading-none tabular-nums mb-1">
              {score}
            </p>
            <p className="text-sm text-slate-500">de {maxScore} puntos posibles</p>

            {/* Efficiency bar */}
            <div className="mt-5">
              <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-700 ${
                    isVictory ? 'bg-emerald-500' : 'bg-blue-500'
                  }`}
                  style={{ width: `${pct}%` }}
                />
              </div>
              <p className="text-xs text-slate-600 mt-1.5">{pct}% de eficiencia</p>
            </div>
          </div>

          {error && (
            <div className="bg-rose-500/10 border border-rose-500/25 text-rose-400 text-sm rounded-xl px-4 py-3 mb-5">
              {error}
            </div>
          )}

          <button
            onClick={onRestart}
            className="w-full py-3.5 bg-blue-500 hover:bg-blue-400 active:scale-[.98] text-slate-950 font-bold text-base rounded-xl transition-all duration-150 cursor-pointer"
          >
            Jugar de nuevo
          </button>

        </div>
      </div>
    </div>
  );
}
