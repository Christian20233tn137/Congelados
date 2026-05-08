export default function StartScreen({ onStart, error }) {
  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <div className="w-full max-w-md animate-fade-in">
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-2xl">

          {/* Logo */}
          <div className="flex justify-center mb-6">
            <div className="w-16 h-16 bg-blue-500/10 border border-blue-500/20 rounded-2xl flex items-center justify-center">
              <span className="font-mono font-black text-blue-400 text-xl select-none">&lt;/&gt;</span>
            </div>
          </div>

          {/* Heading */}
          <div className="text-center mb-8">
            <h1 className="text-3xl font-black tracking-tight text-slate-100 mb-2">
              Código Congelado
            </h1>
            <p className="text-slate-400 text-sm leading-relaxed">
              Resuelve retos de programación para avanzar de nivel
            </p>
          </div>

          {/* Stats grid */}
          <div className="bg-slate-950 border border-slate-800 rounded-xl p-5 mb-6">
            <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">
              Detalles del juego
            </p>
            <div className="grid grid-cols-2 gap-x-8 gap-y-4">
              {[
                { label: 'Niveles',     value: '10 preguntas' },
                { label: 'Vidas',       value: '3 intentos'  },
                { label: 'Por acierto', value: '+10 puntos'  },
                { label: 'Temas',       value: '4 categorías'},
              ].map(({ label, value }) => (
                <div key={label}>
                  <p className="text-xs text-slate-500 mb-0.5">{label}</p>
                  <p className="text-sm font-bold text-slate-100">{value}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Topics */}
          <div className="flex flex-wrap gap-2 mb-6">
            {[
              { name: 'Variables',     color: 'bg-blue-500/10   text-blue-400   border-blue-500/20'   },
              { name: 'Condicionales', color: 'bg-violet-500/10 text-violet-400 border-violet-500/20' },
              { name: 'Ciclos',        color: 'bg-amber-500/10  text-amber-400  border-amber-500/20'  },
              { name: 'Funciones',     color: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' },
            ].map(({ name, color }) => (
              <span
                key={name}
                className={`text-xs font-semibold px-2.5 py-1 rounded-full border ${color}`}
              >
                {name}
              </span>
            ))}
          </div>

          {error && (
            <div className="bg-rose-500/10 border border-rose-500/25 text-rose-400 text-sm rounded-xl px-4 py-3 mb-5">
              {error}
            </div>
          )}

          <button
            onClick={onStart}
            className="w-full py-3.5 bg-blue-500 hover:bg-blue-400 active:scale-[.98] text-slate-950 font-bold text-base rounded-xl transition-all duration-150 cursor-pointer"
          >
            Iniciar juego
          </button>
        </div>
      </div>
    </div>
  );
}
