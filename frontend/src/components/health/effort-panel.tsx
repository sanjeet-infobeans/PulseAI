"use client"

import { Scales } from "@phosphor-icons/react"
import { Badge } from "@/components/ui/badge"
import { EditProjectDialog } from "@/components/projects/edit-project-dialog"
import type { DashboardData } from "@/types/api"

const RISK_VARIANT = { low: "severity-low", medium: "severity-med", high: "severity-high" } as const

export function EffortPanel({
  effort, projectId,
}: {
  effort: DashboardData["effort"] | null
  projectId: string
}) {
  if (!effort) return null

  if (effort.estimated_hours === null) {
    return (
      <div className="premium-card rounded-xl p-8 flex items-center justify-between gap-6">
        <div>
          <p className="eyebrow flex items-center gap-2"><Scales size={16} /> Effort vs estimate</p>
          <p className="text-medium-gray text-sm mt-2">No effort estimate set for this project.</p>
        </div>
        <EditProjectDialog projectId={projectId} />
      </div>
    )
  }

  const consumedPct = effort.estimated_hours > 0
    ? Math.round(100 * effort.consumed_hours / effort.estimated_hours)
    : 0
  const over = effort.overshoot_pct != null && effort.overshoot_pct > 0

  return (
    <div className="premium-card rounded-xl p-8">
      <div className="flex items-center justify-between">
        <p className="eyebrow flex items-center gap-2"><Scales size={16} /> Effort vs estimate</p>
        {effort.overshoot_risk && (
          <Badge variant={RISK_VARIANT[effort.overshoot_risk]}>{effort.overshoot_risk} risk</Badge>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mt-4">
        <div>
          <p className="text-xs text-medium-gray">Estimated hours</p>
          <p className="text-headline-md text-charcoal tabular-nums mt-1">{effort.estimated_hours}</p>
        </div>
        <div>
          <p className="text-xs text-medium-gray">Consumed hours</p>
          <p className="text-headline-md text-charcoal tabular-nums mt-1">{effort.consumed_hours}</p>
        </div>
        <div>
          <p className="text-xs text-medium-gray">Remaining hours</p>
          <p className="text-headline-md text-charcoal tabular-nums mt-1">{effort.remaining_hours}</p>
        </div>
        <div>
          <p className="text-xs text-medium-gray">Projected total</p>
          <p className={`text-headline-md tabular-nums mt-1 ${over ? "text-primary" : "text-charcoal"}`}>
            {effort.projected_total_hours}
          </p>
        </div>
      </div>

      <div className="mt-5">
        <div className="h-2 w-full bg-light-gray rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full ${consumedPct > 100 ? "bg-primary" : "bg-charcoal/70"}`}
            style={{ width: `${Math.min(consumedPct, 100)}%` }}
          />
        </div>
        {effort.overshoot_pct != null && (
          <p className="text-xs text-medium-gray mt-2">
            {effort.overshoot_pct > 0 ? "+" : ""}{effort.overshoot_pct}% vs estimate
          </p>
        )}
      </div>
    </div>
  )
}
