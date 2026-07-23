"use client"

import { CalendarCheck, Sparkle } from "@phosphor-icons/react"
import { Button } from "@/components/ui/button"
import type { PredictionData } from "@/types/api"

function fmtDate(iso: string | null): string {
  if (!iso) return "—"
  return new Date(iso).toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" })
}

export function PredictionCard({
  prediction, onCompute, computing,
}: {
  prediction: PredictionData | null
  onCompute: () => void
  computing: boolean
}) {
  if (!prediction) {
    return (
      <div className="premium-card rounded-xl p-8 flex flex-col items-start gap-3">
        <p className="eyebrow">Delivery completion prediction</p>
        <p className="text-medium-gray text-sm">No prediction yet.</p>
        <Button size="sm" onClick={onCompute} disabled={computing}>
          <Sparkle size={14} className={computing ? "animate-pulse" : ""} />
          {computing ? "Predicting…" : "Predict completion"}
        </Button>
      </div>
    )
  }

  const late = prediction.baseline_target_date && prediction.predicted_completion_date
    && prediction.predicted_completion_date > prediction.baseline_target_date

  return (
    <div className="premium-card rounded-xl p-8">
      <div className="flex items-center justify-between">
        <p className="eyebrow flex items-center gap-2"><CalendarCheck size={16} /> Delivery completion prediction</p>
        <button onClick={onCompute} disabled={computing} className="text-xs text-primary hover:underline disabled:opacity-50">
          {computing ? "…" : "Recompute"}
        </button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mt-4">
        <div>
          <p className="text-xs text-medium-gray">Expected completion</p>
          <p className="text-headline-md text-charcoal mt-1">{fmtDate(prediction.baseline_target_date)}</p>
        </div>
        <div>
          <p className="text-xs text-medium-gray">Predicted completion</p>
          <p className={`text-headline-md mt-1 ${late ? "text-primary" : "text-charcoal"}`}>
            {fmtDate(prediction.predicted_completion_date)}
          </p>
        </div>
        <div>
          <p className="text-xs text-medium-gray">Probability on-time</p>
          <p className="text-headline-md text-charcoal tabular-nums mt-1">{Math.round(prediction.probability_on_time)}%</p>
          {prediction.reasons.length > 0 && (
            <details className="mt-1.5 group">
              <summary className="text-xs text-primary hover:underline cursor-pointer list-none">
                Why this estimate?
              </summary>
              <ul className="space-y-1 mt-2">
                {prediction.reasons.map((r, i) => (
                  <li key={i} className="text-xs text-medium-gray"><span className="text-primary">·</span> {r}</li>
                ))}
              </ul>
            </details>
          )}
        </div>
        <div>
          <p className="text-xs text-medium-gray">Confidence</p>
          <p className="text-headline-md text-charcoal tabular-nums mt-1">{Math.round(prediction.confidence_pct)}%</p>
        </div>
      </div>
      {prediction.recommendations.length > 0 && (
        <div className="mt-4">
          <p className="eyebrow mb-2">Recommendations</p>
          <ul className="space-y-1.5">
            {prediction.recommendations.map((r, i) => (
              <li key={i} className="text-sm text-charcoal"><span className="text-primary">·</span> {r}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
