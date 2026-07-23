"use client"

import { WarningCircle } from "@phosphor-icons/react"
import { Badge } from "@/components/ui/badge"
import { useResourceRisk } from "@/hooks/use-resources"
import { fmtPct } from "@/lib/utils"

const BURNOUT_VARIANT = {
  low: "severity-low",
  medium: "severity-med",
  high: "severity-high",
} as const

export function ResourcesContent({ projectId }: { projectId: string }) {
  const { data, isLoading } = useResourceRisk(projectId)

  return (
    <div className="space-y-8">
      <div>
        <p className="eyebrow">Team capacity</p>
        <h1 className="text-headline-lg text-charcoal mt-2">Resource risk</h1>
        <p className="text-medium-gray text-body-md mt-1">
          Utilization, burnout risk, and knowledge concentration across the team.
        </p>
      </div>

      {isLoading && <p className="text-medium-gray text-sm">Loading…</p>}

      {data && (
        <>
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-gutter">
            <div className="lg:col-span-4 premium-card rounded-xl p-8">
              <p className="eyebrow">Team utilization</p>
              <p className="text-headline-lg text-charcoal tabular-nums mt-2">
                {data.team_utilization_pct != null ? fmtPct(data.team_utilization_pct) : "—"}
              </p>
              <p className="text-xs text-medium-gray mt-1">{data.team_size ?? "—"} team members</p>
            </div>
            <div className="lg:col-span-8 premium-card rounded-xl p-8">
              <div className="flex items-center justify-between">
                <p className="eyebrow">Burnout risk</p>
                <Badge variant={BURNOUT_VARIANT[data.burnout_risk]}>{data.burnout_risk}</Badge>
              </div>
              <p className="text-charcoal text-sm mt-3">{data.burnout_reason || "No signal yet."}</p>
            </div>
          </div>

          {data.developers.length > 0 && (
            <section className="premium-card rounded-xl p-8">
              <p className="eyebrow mb-4">Developer utilization</p>
              <div className="space-y-4">
                {data.developers.map((d) => (
                  <div key={d.name}>
                    <div className="flex justify-between text-sm">
                      <span className="text-charcoal">{d.name} <span className="text-medium-gray text-xs">· {d.skill}</span></span>
                      <span className="tabular-nums text-medium-gray">{fmtPct(d.utilization_pct)}</span>
                    </div>
                    <div className="h-1.5 w-full bg-light-gray rounded-full overflow-hidden mt-1.5">
                      <div
                        className="h-full rounded-full"
                        style={{
                          width: `${Math.min(d.utilization_pct, 100)}%`,
                          background: d.utilization_pct > 100 ? "#EA1B3D" : d.utilization_pct > 90 ? "#B07A1E" : "#2F674F",
                        }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}

          <section className="space-y-4">
            <h2 className="text-headline-md text-charcoal flex items-center gap-2">
              <WarningCircle size={20} className="text-primary" /> Knowledge concentration
            </h2>
            {data.sole_holder_modules.length === 0 ? (
              <p className="text-medium-gray text-sm">No single-point-of-knowledge modules detected.</p>
            ) : (
              <div className="premium-card rounded-xl overflow-hidden">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-left text-medium-gray border-b border-light-gray">
                      <th className="px-5 py-3 font-normal">Module</th>
                      <th className="px-5 py-3 font-normal">Sole holder</th>
                      <th className="px-5 py-3 font-normal">Stories</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.sole_holder_modules.map((m) => (
                      <tr key={`${m.module}-${m.developer}`} className="border-b border-light-gray last:border-0">
                        <td className="px-5 py-3 text-charcoal">{m.module}</td>
                        <td className="px-5 py-3 text-medium-gray">{m.developer}</td>
                        <td className="px-5 py-3 text-medium-gray tabular-nums">{m.story_count}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>

          {data.recommendations.length > 0 && (
            <section className="premium-card rounded-xl p-8 border-t-4 border-t-primary">
              <p className="eyebrow mb-4">Recommendations</p>
              <ul className="space-y-2">
                {data.recommendations.map((r, i) => (
                  <li key={i} className="text-sm text-charcoal flex gap-2">
                    <span className="text-primary">·</span> {r}
                  </li>
                ))}
              </ul>
            </section>
          )}
        </>
      )}
    </div>
  )
}
