"use client"

import { ArrowRight, WarningCircle } from "@phosphor-icons/react"
import { Badge } from "@/components/ui/badge"
import { useDependencies } from "@/hooks/use-dependencies"

const RELATION_LABEL: Record<string, string> = {
  blocks: "blocks",
  depends_on: "depends on",
  mentioned_in: "mentioned in",
  derived_from: "derived from",
  impacts: "impacts",
}

export function RisksContent({ projectId }: { projectId: string }) {
  const { data: edges, isLoading } = useDependencies(projectId)

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
    </div>
  )
}
