"use client"

import Link from "next/link"
import { WarningCircle } from "@phosphor-icons/react"
import { Badge } from "@/components/ui/badge"
import { usePortfolio } from "@/hooks/use-portfolio"

const BAND_VARIANT = { red: "severity-high", amber: "severity-med", green: "severity-low" } as const

export function PortfolioContent() {
  const { data, isLoading } = usePortfolio()

  return (
    <div className="space-y-8">
      <div>
        <p className="eyebrow">Portfolio</p>
        <h1 className="text-headline-lg text-charcoal mt-2">Cross-project rollup</h1>
        <p className="text-medium-gray text-body-md mt-1">
          Health, confidence, and risk across every engagement in your organization.
        </p>
      </div>

      {isLoading && <p className="text-medium-gray text-sm">Loading…</p>}

      {data && (
        <>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-gutter">
            <Kpi label="Projects" value={data.projects.length} />
            <Kpi label="Needing attention" value={data.needing_attention_count} accent />
            <Kpi label="Avg scope growth" value={data.avg_scope_growth_pct != null ? `${data.avg_scope_growth_pct}%` : "—"} />
            <Kpi label="Highest-risk customer" value={data.highest_risk_customer ?? "—"} />
          </div>

          {data.most_common_blocker && (
            <div className="premium-card rounded-xl p-6 border-l-4 border-l-primary flex items-center gap-3">
              <WarningCircle size={18} className="text-primary shrink-0" />
              <p className="text-sm text-charcoal">
                Most common blocker across the portfolio: <span className="text-primary">{data.most_common_blocker}</span>
              </p>
            </div>
          )}

          {data.projects.length === 0 ? (
            <p className="text-medium-gray text-sm">No projects yet.</p>
          ) : (
            <div className="premium-card rounded-xl overflow-hidden">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-medium-gray border-b border-light-gray">
                    <th className="px-5 py-3 font-normal">Project</th>
                    <th className="px-5 py-3 font-normal">Customer</th>
                    <th className="px-5 py-3 font-normal">Confidence</th>
                    <th className="px-5 py-3 font-normal">Scope growth</th>
                  </tr>
                </thead>
                <tbody>
                  {data.projects.map((p) => (
                    <tr key={p.project_id} className="border-b border-light-gray last:border-0">
                      <td className="px-5 py-3">
                        <Link href={`/projects/${p.project_id}`} className="text-primary hover:underline">{p.name}</Link>
                      </td>
                      <td className="px-5 py-3 text-medium-gray">{p.customer_name}</td>
                      <td className="px-5 py-3 tabular-nums">
                        {p.band ? (
                          <Badge variant={BAND_VARIANT[p.band]}>{p.confidence_score}%</Badge>
                        ) : "—"}
                      </td>
                      <td className="px-5 py-3 text-medium-gray tabular-nums">
                        {p.scope_growth_pct != null ? `${p.scope_growth_pct}%` : "—"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </div>
  )
}

function Kpi({ label, value, accent }: { label: string; value: number | string; accent?: boolean }) {
  const isPositive = typeof value === "number" && value > 0
  return (
    <div className="premium-card rounded-xl p-6 flex flex-col justify-between">
      <p className="eyebrow">{label}</p>
      <p className={`text-headline-lg tabular-nums mt-2 ${accent && isPositive ? "text-primary" : "text-charcoal"}`}>{value}</p>
    </div>
  )
}
