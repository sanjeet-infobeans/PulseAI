"use client"

import { Sparkle } from "@phosphor-icons/react"
import { Button } from "@/components/ui/button"
import type { ConfidenceData } from "@/types/api"

const BAND = {
  green: { color: "#2F674F", label: "On track" },
  amber: { color: "#B07A1E", label: "Watch" },
  red: { color: "#EA1B3D", label: "At risk" },
}

export function ConfidenceMeter({
  confidence,
  onCompute,
  computing,
}: {
  confidence: ConfidenceData | null
  onCompute: () => void
  computing: boolean
}) {
  if (!confidence) {
    return (
      <div className="flex flex-col items-start gap-3">
        <p className="eyebrow">PulseAI prediction</p>
        <p className="text-medium-gray text-sm">No confidence score yet.</p>
        <Button size="sm" onClick={onCompute} disabled={computing}>
          <Sparkle size={14} className={computing ? "animate-pulse" : ""} />
          {computing ? "Scoring…" : "Compute confidence"}
        </Button>
      </div>
    )
  }

  const b = BAND[confidence.band]
  return (
    <div>
      <div className="flex items-center justify-between">
        <p className="eyebrow">Delivery confidence</p>
        <button
          onClick={onCompute}
          disabled={computing}
          className="text-xs text-primary hover:underline disabled:opacity-50"
        >
          {computing ? "…" : "Recompute"}
        </button>
      </div>
      <div className="flex items-baseline gap-2 mt-2">
        <span className="text-headline-lg text-charcoal tabular-nums">{confidence.score}</span>
        <span className="text-sm font-medium" style={{ color: b.color }}>{b.label}</span>
      </div>
      <div className="h-2 w-full bg-light-gray rounded-full overflow-hidden mt-3">
        <div
          className="h-full rounded-full"
          style={{ width: `${confidence.score}%`, background: b.color, transition: "width 700ms cubic-bezier(0.16,1,0.3,1)" }}
        />
      </div>
      <p className="text-xs text-medium-gray mt-2 tabular-nums">
        Rules {confidence.rule_score} · Judge {confidence.judge_score}
      </p>
      {confidence.rationale && (
        <p className="text-xs text-medium-gray mt-2 line-clamp-3">{confidence.rationale}</p>
      )}
    </div>
  )
}
