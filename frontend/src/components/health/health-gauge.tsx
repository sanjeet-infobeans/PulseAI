"use client"

const BAND_COLOR = { green: "#2F674F", amber: "#B07A1E", red: "#EA1B3D" }

function band(score: number): keyof typeof BAND_COLOR {
  if (score < 50) return "red"
  if (score < 75) return "amber"
  return "green"
}

/** Radial arc gauge, 0–100. Compositor-friendly SVG (no layout animation). */
export function HealthGauge({ score, label = "Health" }: { score: number; label?: string }) {
  const r = 80
  const circumference = 2 * Math.PI * r
  const clamped = Math.max(0, Math.min(100, score))
  const offset = circumference * (1 - clamped / 100)
  const color = BAND_COLOR[band(clamped)]

  return (
    <div className="relative w-44 h-44 flex items-center justify-center">
      <svg className="w-full h-full -rotate-90" viewBox="0 0 176 176">
        <circle cx="88" cy="88" r={r} fill="transparent" stroke="#E6E6ED" strokeWidth="8" />
        <circle
          cx="88" cy="88" r={r} fill="transparent" stroke={color} strokeWidth="8"
          strokeLinecap="round" strokeDasharray={circumference} strokeDashoffset={offset}
          style={{ transition: "stroke-dashoffset 700ms cubic-bezier(0.16,1,0.3,1)" }}
        />
      </svg>
      <div className="absolute flex flex-col items-center">
        <span className="text-display-lg text-charcoal leading-none tabular-nums">{clamped}</span>
        <span className="text-[10px] uppercase tracking-widest font-medium text-medium-gray mt-2">{label}</span>
      </div>
    </div>
  )
}
