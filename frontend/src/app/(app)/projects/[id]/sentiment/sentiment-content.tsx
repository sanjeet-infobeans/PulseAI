"use client"

import { Gauge } from "@phosphor-icons/react"
import { Badge } from "@/components/ui/badge"
import { useSentiment } from "@/hooks/use-sentiment"

const TREND_VARIANT = { improving: "severity-low", steady: "neutral", declining: "severity-high" } as const
const TREND_COLOR = { improving: "#2F674F", steady: "#6B6B6B", declining: "#EA1B3D" } as const

function Sparkline({ series, color }: { series: number[]; color: string }) {
  if (series.length < 2) return null
  const w = 320, h = 64, pad = 4
  const min = Math.min(...series), max = Math.max(...series)
  const range = max - min || 1
  const points = series.map((v, i) => {
    const x = pad + (i / (series.length - 1)) * (w - pad * 2)
    const y = h - pad - ((v - min) / range) * (h - pad * 2)
    return `${x},${y}`
  })
  return (
    <svg viewBox={`0 0 ${w} ${h}`} className="w-full h-16" role="img" aria-label="Sentiment score trend">
      <polyline points={points.join(" ")} fill="none" stroke={color} strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

export function SentimentContent({ projectId }: { projectId: string }) {
  const { data, isLoading } = useSentiment(projectId)

  return (
    <div className="space-y-8">
      <div>
        <p className="eyebrow">Stakeholder sentiment</p>
        <h1 className="text-headline-lg text-charcoal mt-2">Customer sentiment trend</h1>
        <p className="text-medium-gray text-body-md mt-1">
          Inferred from Teams/Slack signals and refreshed nightly.
        </p>
      </div>

      {isLoading && <p className="text-medium-gray text-sm">Loading…</p>}

      {data && (
        <div className="premium-card rounded-xl p-8">
          <div className="flex items-center justify-between">
            <p className="eyebrow flex items-center gap-2"><Gauge size={16} /> Current sentiment</p>
            <Badge variant={TREND_VARIANT[data.trend]}>{data.trend}</Badge>
          </div>
          <p className="text-headline-lg text-charcoal tabular-nums mt-3">
            {data.current_score != null ? `${Math.round(data.current_score)}%` : "—"}
          </p>
          <div className="mt-4">
            <Sparkline series={data.series} color={TREND_COLOR[data.trend]} />
          </div>
          {data.history_points < 2 && (
            <p className="text-xs text-medium-gray mt-2">
              Trend will sharpen after a few nightly refresh cycles.
            </p>
          )}
          {data.reasons.length > 0 && (
            <div className="mt-6 pt-6 border-t border-light-gray">
              <p className="eyebrow mb-2">Reasons</p>
              <ul className="space-y-1.5">
                {data.reasons.map((r, i) => (
                  <li key={i} className="text-sm text-charcoal"><span className="text-primary">·</span> {r}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
