const TOTAL_LIVES = 3;

const TOPIC_COLOR = {
  Variables:     'bg-blue-500/10   text-blue-400   border-blue-500/20',
  Condicionales: 'bg-violet-500/10 text-violet-400 border-violet-500/20',
  Ciclos:        'bg-amber-500/10  text-amber-400  border-amber-500/20',
  Funciones:     'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
};

export default function QuestionScreen({
  question,
  lives,
  score,
  totalQuestions,
  selectedOption,
  answerResult,
  onAnswer,
}) {
  if (!question) return null;

  const progress = Math.round(((question.level - 1) / totalQuestions) * 100);
  const isLocked  = !!selectedOption;
  const topicColor = TOPIC_COLOR[question.topic] ?? 'bg-slate-700/30 text-slate-400 border-slate-700';

  const optionCls = (key) => {
    const base =
      'flex items-start gap-3 w-full px-4 py-3.5 border-2 rounded-xl text-left text-sm font-medium transition-all duration-150 disabled:cursor-default';

    if (!answerResult) {
      return `${base} border-slate-700 bg-slate-800/40 text-slate-200 hover:border-blue-500/60 hover:bg-slate-800 cursor-pointer`;
    }
    if (key === answerResult.correct_option)
      return `${base} border-emerald-500 bg-emerald-500/10 text-emerald-200`;
    if (key === selectedOption)
      return `${base} border-rose-500 bg-rose-500/10 text-rose-200`;
    return `${base} border-slate-800 bg-transparent text-slate-600`;
  };

  const keyCls = (key) => {
    const base = 'font-black text-xs mt-0.5 min-w-[14px] shrink-0';
    if (!answerResult)                         return `${base} text-blue-400`;
    if (key === answerResult.correct_option)   return `${base} text-emerald-400`;
    if (key === selectedOption)                return `${base} text-rose-400`;
    return `${base} text-slate-600`;
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <div className="w-full max-w-lg animate-fade-in">
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl">

          {/* HUD */}
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2.5">
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Vidas</span>
              <div className="flex gap-1.5">
                {Array.from({ length: TOTAL_LIVES }).map((_, i) => (
                  <div
                    key={i}
                    className={`w-2.5 h-2.5 rounded-full transition-colors duration-300 ${
                      i < lives ? 'bg-rose-500' : 'bg-slate-700'
                    }`}
                  />
                ))}
              </div>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Puntaje</span>
              <span className="text-base font-black text-blue-400 tabular-nums">{score}</span>
            </div>
          </div>

          {/* Progress bar */}
          <div className="mb-5">
            <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-blue-500 rounded-full transition-all duration-500"
                style={{ width: `${progress}%` }}
              />
            </div>
            <p className="text-xs text-slate-600 mt-1.5 text-right">
              Nivel {question.level} de {totalQuestions}
            </p>
          </div>

          {/* Topic badge + question */}
          <span className={`inline-block text-xs font-bold uppercase tracking-wide px-2.5 py-1 rounded-full border mb-3 ${topicColor}`}>
            {question.topic}
          </span>

          <p className="text-base font-semibold text-slate-100 leading-snug mb-1">
            {question.text}
          </p>

          {/* Code block */}
          {question.code && (
            <div className="my-4 rounded-xl overflow-hidden border border-slate-800 border-l-4 border-l-blue-500">
              <pre className="bg-slate-950 px-5 py-4 text-sm font-mono text-slate-300 leading-relaxed overflow-x-auto whitespace-pre">
                {question.code}
              </pre>
            </div>
          )}

          {/* Feedback banner */}
          {answerResult && (
            <div
              className={`flex items-start gap-2 px-4 py-3 rounded-xl text-sm font-semibold mb-4 animate-fade-in border ${
                answerResult.correct
                  ? 'bg-emerald-500/10 border-emerald-500/25 text-emerald-300'
                  : 'bg-rose-500/10 border-rose-500/25 text-rose-300'
              }`}
            >
              <span className="font-black text-base leading-none mt-0.5 shrink-0">
                {answerResult.correct ? '✓' : '✕'}
              </span>
              <span className="leading-snug">{answerResult.message}</span>
            </div>
          )}

          {/* Options */}
          <div className="flex flex-col gap-2.5">
            {Object.entries(question.options).map(([key, value]) => (
              <button
                key={key}
                className={optionCls(key)}
                onClick={() => onAnswer(key)}
                disabled={isLocked}
              >
                <span className={keyCls(key)}>{key}</span>
                <span className="leading-snug">{value}</span>
              </button>
            ))}
          </div>

        </div>
      </div>
    </div>
  );
}
