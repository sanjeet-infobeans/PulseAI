"use client"

import { ArrowRight, Clock, WarningCircle } from "@phosphor-icons/react"
import { Badge } from "@/components/ui/badge"
import { useDecisions, useDependencies } from "@/hooks/use-dependencies"

const RELATION_LABEL: Record<string, string> = {
  blocks: "blocks",
  depends_on: "depends on",
  mentioned_in: "mentioned in",
  derived_from: "derived from",
  impacts: "impacts",
}

export function RisksContent({ projectId }: { projectId: string }) {
  const { data: edges, isLoading } = useDependencies(projectId)
  const { data: decisions } = useDecisions(projectId)

  return (
    <div className="space-y-8">
      <div>
        <p className="eyebrow">Risk management</p>
        <h1 className="text-headline-lg text-charcoal mt-2">Hidden dependencies</h1>
        <p className="text-medium-gray text-body-md mt-1">
          Delivery chains inferred across stories, documents, and team decisions — recomputed nightly.
        </p>
      </div>

      {isLoading && <p className="text-medium-gray text-sm">Loading…</p>}

      {!isLoading && (!edges || edges.length === 0) && (
        <div className="premium-card rounded-xl p-12 text-center">
          <p className="text-charcoal">No dependency chains detected yet</p>
          <p className="text-medium-gray text-sm mt-1">
            Runs automatically after Jira syncs and overnight — check back once delivery data and documents exist.
          </p>
        </div>
      )}

      {edges && edges.length > 0 && (
        <div className="space-y-3">
          {edges.map((e) => (
            <div key={e.id} className="premium-card rounded-xl p-5">
              <div className="flex items-center justify-between gap-4">
                <div className="flex items-center gap-2 text-sm min-w-0 flex-wrap">
                  <span className="text-charcoal font-medium truncate">{e.from_ref}</span>
                  <span className="text-xs text-medium-gray uppercase tracking-wide shrink-0">{e.from_type}</span>
                  <span className="flex items-center gap-1 text-primary shrink-0">
                    <ArrowRight size={14} /> {RELATION_LABEL[e.relation] ?? e.relation}
                  </span>
                  <span className="text-charcoal font-medium truncate">{e.to_ref}</span>
                  <span className="text-xs text-medium-gray uppercase tracking-wide shrink-0">{e.to_type}</span>
                </div>
                <Badge variant={e.confidence >= 0.7 ? "severity-high" : e.confidence >= 0.4 ? "severity-med" : "severity-low"}>
                  {Math.round(e.confidence * 100)}% confidence
                </Badge>
              </div>
              {e.rationale && (
                <p className="text-xs text-medium-gray mt-2 flex items-start gap-1.5">
                  <WarningCircle size={13} className="mt-0.5 shrink-0" /> {e.rationale}
                </p>
              )}
            </div>
          ))}
        </div>
      )}

      {decisions && (decisions.pending.length > 0 || decisions.decided_count > 0) && (
        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-headline-md text-charcoal flex items-center gap-2">
              <Clock size={20} className="text-primary" /> Customer decisions
            </h2>
            {decisions.avg_delay_days != null && (
              <span className="text-sm text-medium-gray">
                Avg approval delay: <span className="text-charcoal tabular-nums">{decisions.avg_delay_days}d</span>
              </span>
            )}
          </div>
          {decisions.pending.length === 0 ? (
            <p className="text-medium-gray text-sm">No decisions currently awaiting approval.</p>
          ) : (
            <div className="premium-card rounded-xl overflow-hidden">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-medium-gray border-b border-light-gray">
                    <th className="px-5 py-3 font-normal">Topic</th>
                    <th className="px-5 py-3 font-normal">Requested by</th>
                    <th className="px-5 py-3 font-normal">Awaiting</th>
                  </tr>
                </thead>
                <tbody>
                  {decisions.pending.map((p, i) => (
                    <tr key={i} className="border-b border-light-gray last:border-0">
                      <td className="px-5 py-3 text-charcoal">{p.topic}</td>
                      <td className="px-5 py-3 text-medium-gray">{p.requested_by ?? "—"}</td>
                      <td className="px-5 py-3 tabular-nums">
                        <Badge variant={(p.days_pending ?? 0) > 7 ? "severity-high" : "severity-med"}>
                          {p.days_pending != null ? `${p.days_pending}d` : "—"}
                        </Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      )}
    </div>
  )
}
