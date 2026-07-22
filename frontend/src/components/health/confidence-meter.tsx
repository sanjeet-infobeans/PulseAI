"use client"

import { Sparkle } from "@phosphor-icons/react"
import { Button } from "@/components/ui/button"
import type { ConfidenceCategory, ConfidenceData } from "@/types/api"

const BAND = {
  green: { color: "#2F674F", label: "On track" },
  amber: { color: "#B07A1E", label: "Watch" },
  red: { color: "#EA1B3D", label: "At risk" },
}

function bandColor(pct: number): string {
  if (pct >= 75) return BAND.green.color
  if (pct >= 50) return BAND.amber.color
  return BAND.red.color
}

const CATEGORY_LABEL: Record<ConfidenceCategory, string> = {
  requirement: "Requirement",
  engineering: "Engineering",
  testing: "Testing",
  dependencies: "Dependencies",
  resource: "Resource",
  customer: "Customer",
}
const CATEGORY_ORDER: ConfidenceCategory[] = [
  "requirement", "engineering", "testing", "dependencies", "resource", "customer",
]

function SubScoreGrid({ subScores }: { subScores: ConfidenceData["sub_scores"] }) {
  if (!subScores) return null
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 gap-x-5 gap-y-3 mt-4">
      {CATEGORY_ORDER.map((cat) => {
        const pct = subScores[cat]
        return (
          <div key={cat}>
            <div className="flex justify-between items-baseline">
              <span className="text-xs text-medium-gray">{CATEGORY_LABEL[cat]}</span>
              <span className="text-xs text-charcoal tabular-nums">{pct == null ? "—" : Math.round(pct)}</span>
            </div>
            <div className="h-1 w-full bg-light-gray rounded-full overflow-hidden mt-1">
              {pct != null && (
                <div
                  className="h-full rounded-full"
                  style={{ width: `${Math.min(Math.max(pct, 0), 100)}%`, background: bandColor(pct) }}
                />
              )}
            </div>
          </div>
        )
      })}
    </div>
  )
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
      <SubScoreGrid subScores={confidence.sub_scores} />
    </div>
  )
}
