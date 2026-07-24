"use client"

import { useState } from "react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { CheckCircle, ListChecks, MagicWand, ShieldWarning, Sparkle, WarningCircle } from "@phosphor-icons/react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { useLatestAnalysis, useLatestJudgeReview, useRunAnalysis, useRunJudge } from "@/hooks/use-analysis"
import { useRunSimulation } from "@/hooks/use-simulation"
import { useRisks, useScanRisks, useSetRiskStatus } from "@/hooks/use-risks"
import { useActionItems, useSetActionItemStatus } from "@/hooks/use-action-items"
import { severityBorder, sortBySeverity } from "@/lib/severity"
import { fmtRelative } from "@/lib/utils"
import type { AnalysisKind } from "@/types/api"

const KINDS: { key: AnalysisKind; label: string }[] = [
  { key: "executive", label: "Executive summary" },
  { key: "sprint", label: "Sprint analysis" },
  { key: "risk", label: "Risk summary" },
  { key: "recommendations", label: "Recommendations" },
]

export function AnalysisContent({ projectId }: { projectId: string }) {
  const [kind, setKind] = useState<AnalysisKind>("executive")

  return (
    <div className="space-y-8">
      <div>
        <p className="eyebrow">Project intelligence</p>
        <h1 className="text-headline-lg text-charcoal mt-2">AI analysis</h1>
        <p className="text-medium-gray text-body-md mt-1">
          Generated on demand from live delivery data.
        </p>
      </div>

      <Tabs value={kind} onValueChange={(v) => setKind(v as AnalysisKind)}>
        <TabsList>
          {KINDS.map((k) => (
            <TabsTrigger key={k.key} value={k.key}>{k.label}</TabsTrigger>
          ))}
        </TabsList>
        {KINDS.map((k) => (
          <TabsContent key={k.key} value={k.key}>
            <AnalysisPanel projectId={projectId} kind={k.key} label={k.label} />
          </TabsContent>
        ))}
      </Tabs>

      <WhatIfPanel projectId={projectId} />
      <ActiveRisksPanel projectId={projectId} />
      <ActionItemsPanel projectId={projectId} />
    </div>
  )
}

function ActiveRisksPanel({ projectId }: { projectId: string }) {
  const { data: risks, isLoading } = useRisks(projectId)
  const scan = useScanRisks(projectId)
  const setStatus = useSetRiskStatus(projectId)

  return (
    <section className="premium-card rounded-xl p-8 border-t-4 border-t-primary space-y-4">
      <div className="flex items-center justify-between">
        <p className="eyebrow flex items-center gap-2"><ShieldWarning size={16} /> Active risks</p>
        <Button variant="outline" size="sm" onClick={() => scan.mutate()} disabled={scan.isPending}>
          <Sparkle size={14} className={scan.isPending ? "animate-pulse" : ""} />
          {scan.isPending ? "Scanning…" : "Rescan risks"}
        </Button>
      </div>

      {isLoading && <p className="text-medium-gray text-sm">Loading…</p>}

      {!isLoading && (!risks || risks.length === 0) && (
        <p className="text-medium-gray text-sm">
          No active risks detected. Upload documents or run a scan to have the Risk Identifier
          agent scan delivery data and transcripts for risk.
        </p>
      )}

      {risks && risks.length > 0 && (
        <div className="space-y-3">
          {sortBySeverity(risks).map((r) => (
            <div key={r.id} className={`rounded-lg border-l-4 ${severityBorder(r.severity)} bg-background p-5`}>
              <div className="flex items-center justify-between gap-4">
                <h4 className="text-charcoal font-normal">{r.title}</h4>
                <div className="flex items-center gap-2 shrink-0">
                  <Badge variant={r.severity === "high" ? "severity-high" : r.severity === "medium" ? "severity-med" : "severity-low"}>
                    {r.severity}
                  </Badge>
                  <button
                    type="button"
                    className="text-xs text-primary hover:underline disabled:opacity-50"
                    disabled={setStatus.isPending}
                    onClick={() => setStatus.mutate({ riskId: r.id, status: "mitigated" })}
                  >
                    Mark mitigated
                  </button>
                </div>
              </div>
              {r.description && <p className="text-medium-gray text-sm mt-2">{r.description}</p>}
              <p className="text-xs text-medium-gray mt-2">Last seen {fmtRelative(r.last_seen_at)}</p>
            </div>
          ))}
        </div>
      )}
    </section>
  )
}

function ActionItemsPanel({ projectId }: { projectId: string }) {
  const { data: summary, isLoading } = useActionItems(projectId)
  const setStatus = useSetActionItemStatus(projectId)

  return (
    <section className="premium-card rounded-xl p-8 space-y-4">
      <p className="eyebrow flex items-center gap-2"><ListChecks size={16} /> Action items</p>

      {isLoading && <p className="text-medium-gray text-sm">Loading…</p>}

      {!isLoading && summary && (summary.open_count + summary.done_count) === 0 && (
        <p className="text-medium-gray text-sm">
          No action items yet. These are compiled automatically from uploaded meeting transcripts.
        </p>
      )}

      {summary && (summary.open_count + summary.done_count) > 0 && (
        <>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-xs text-medium-gray">Open</p>
              <p className="text-headline-md text-charcoal tabular-nums mt-1">{summary.open_count}</p>
            </div>
            <div>
              <p className="text-xs text-medium-gray">Done</p>
              <p className="text-headline-md text-charcoal tabular-nums mt-1">{summary.done_count}</p>
            </div>
          </div>
          <div className="space-y-5 pt-2">
            {Object.entries(summary.by_owner).map(([owner, items]) => (
              <div key={owner}>
                <p className="text-xs text-medium-gray mb-2">{owner}</p>
                <ul className="space-y-1.5">
                  {items.map((item) => (
                    <li key={item.id} className="flex items-center gap-2 text-sm">
                      <input
                        type="checkbox"
                        checked={item.status === "done"}
                        onChange={(e) => setStatus.mutate({ itemId: item.id, status: e.target.checked ? "done" : "open" })}
                      />
                      <span className={item.status === "done" ? "text-medium-gray line-through" : "text-charcoal"}>
                        {item.item}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </>
      )}
    </section>
  )
}

function WhatIfPanel({ projectId }: { projectId: string }) {
  const [scenario, setScenario] = useState("")
  const simulate = useRunSimulation(projectId)

  return (
    <section className="premium-card rounded-xl p-8 border-t-4 border-t-primary space-y-4">
      <p className="eyebrow flex items-center gap-2"><MagicWand size={16} /> What-if simulation</p>
      <div className="flex gap-3">
        <input
          value={scenario}
          onChange={(e) => setScenario(e.target.value)}
          placeholder="e.g. What if we add a Payment Gateway integration?"
          className="flex-1 rounded-sm border border-light-gray px-3 py-2 text-sm bg-background focus:outline-none focus:border-primary"
        />
        <Button
          onClick={() => simulate.mutate(scenario)}
          disabled={simulate.isPending || !scenario.trim()}
        >
          <Sparkle size={16} className={simulate.isPending ? "animate-pulse" : ""} />
          {simulate.isPending ? "Simulating…" : "Simulate"}
        </Button>
      </div>

      {simulate.data && (
        <div className="pt-4 border-t border-light-gray space-y-4">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div>
              <p className="text-xs text-medium-gray">Estimated time</p>
              <p className="text-headline-md text-charcoal tabular-nums mt-1">
                {simulate.data.estimated_weeks != null ? `${simulate.data.estimated_weeks}w` : "—"}
              </p>
            </div>
            <div>
              <p className="text-xs text-medium-gray">Risk</p>
              <Badge variant={simulate.data.risk === "high" ? "severity-high" : simulate.data.risk === "medium" ? "severity-med" : "severity-low"}>
                {simulate.data.risk}
              </Badge>
            </div>
            <div>
              <p className="text-xs text-medium-gray">Confidence impact</p>
              <p className={`text-headline-md tabular-nums mt-1 ${simulate.data.confidence_delta < 0 ? "text-primary" : "text-charcoal"}`}>
                {simulate.data.confidence_delta > 0 ? "+" : ""}{simulate.data.confidence_delta}
              </p>
            </div>
            <div>
              <p className="text-xs text-medium-gray">Resources needed</p>
              <p className="text-sm text-charcoal mt-1">
                {simulate.data.resources_needed.length > 0 ? simulate.data.resources_needed.join(", ") : "—"}
              </p>
            </div>
          </div>
          {simulate.data.summary && <p className="text-sm text-medium-gray">{simulate.data.summary}</p>}
        </div>
      )}
    </section>
  )
}

function AnalysisPanel({ projectId, kind, label }: { projectId: string; kind: AnalysisKind; label: string }) {
  const { data: latest, isLoading } = useLatestAnalysis(projectId, kind)
  const run = useRunAnalysis(projectId)
  const analysis = run.data?.kind === kind ? run.data : latest
  const judge = useRunJudge(projectId)
  const { data: latestReview } = useLatestJudgeReview(projectId, analysis?.id)
  const review = judge.data?.analysis_id === analysis?.id ? judge.data : latestReview

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <h2 className="text-headline-md text-charcoal">{label}</h2>
        <div className="flex items-center gap-3">
          {analysis && (
            <Button variant="outline" onClick={() => judge.mutate(analysis.id)} disabled={judge.isPending}>
              <CheckCircle size={16} className={judge.isPending ? "animate-pulse" : ""} />
              {judge.isPending ? "Verifying…" : "Verify with AI Judge"}
            </Button>
          )}
          <Button onClick={() => run.mutate({ kind })} disabled={run.isPending}>
            <Sparkle size={16} className={run.isPending ? "animate-pulse" : ""} />
            {run.isPending ? "Analyzing…" : analysis ? "Regenerate" : "Generate"}
          </Button>
        </div>
      </div>

      {run.isError && (
        <div className="flex items-center gap-2 text-sm text-primary">
          <WarningCircle size={16} /> {(run.error as Error).message}
        </div>
      )}

      {isLoading && <p className="text-medium-gray text-sm">Loading…</p>}

      {!analysis && !run.isPending && !isLoading && (
        <div className="premium-card rounded-xl p-12 text-center">
          <p className="text-medium-gray">No {label.toLowerCase()} yet. Generate one from current delivery data.</p>
        </div>
      )}

      {analysis && (
        <div className="premium-card rounded-xl p-8 border-t-4 border-t-primary">
          {kind === "executive" && (
            <div className="flex items-center gap-3 mb-4">
              <p className="text-xs text-medium-gray">
                {analysis.generated_by ? "Generated manually" : "Auto-generated overnight"} · {fmtRelative(analysis.created_at)}
              </p>
              {analysis.structured?.intervention_needed === true && (
                <Badge variant="severity-high">Intervention recommended</Badge>
              )}
              {analysis.structured?.intervention_needed === false && (
                <Badge variant="severity-low">No intervention required</Badge>
              )}
            </div>
          )}
          <article className="prose-pulse">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{analysis.content}</ReactMarkdown>
          </article>
          <StructuredView kind={kind} structured={analysis.structured} />
        </div>
      )}

      {review && <JudgeReviewPanel review={review} />}
    </div>
  )
}

function JudgeReviewPanel({ review }: { review: import("@/types/api").JudgeReview }) {
  return (
    <div className="premium-card rounded-xl p-6 border-l-4 border-l-medium-gray">
      <div className="flex items-center gap-2">
        <CheckCircle size={16} className="text-medium-gray" />
        <p className="eyebrow">AI Judge review</p>
      </div>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-4">
        <JudgeStat label="Coverage" value={`${Math.round(review.coverage_pct)}%`} />
        <JudgeStat label="Missing risks" value={String(review.missing_risks_count)} />
        <JudgeStat label="Missing stories" value={String(review.missing_stories_count)} />
        <JudgeStat label="Confidence" value={`${Math.round(review.confidence_pct)}%`} />
      </div>
      {review.notes && <p className="text-medium-gray text-sm mt-4">{review.notes}</p>}
    </div>
  )
}

function JudgeStat({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs text-medium-gray">{label}</p>
      <p className="text-headline-md text-charcoal tabular-nums mt-1">{value}</p>
    </div>
  )
}

function StructuredView({ kind, structured }: { kind: AnalysisKind; structured: Record<string, unknown> }) {
  if (kind === "risk" && Array.isArray(structured.risks)) {
    return (
      <div className="mt-8 space-y-4">
        {sortBySeverity(
          structured.risks as unknown as Array<{ severity: string; title: string; impact?: string; evidence?: string }>
        ).map((r, i) => (
          <div key={i} className={`rounded-lg border-l-4 ${severityBorder(r.severity)} bg-background p-5`}>
            <div className="flex items-center justify-between">
              <h4 className="text-charcoal font-normal">{r.title}</h4>
              <Badge variant={r.severity === "high" ? "severity-high" : r.severity === "medium" ? "severity-med" : "severity-low"}>
                {r.severity}
              </Badge>
            </div>
            <p className="text-medium-gray text-sm mt-2">{r.impact}</p>
            {r.evidence && <p className="text-xs text-medium-gray mt-2">Evidence: {r.evidence}</p>}
          </div>
        ))}
      </div>
    )
  }
  if (kind === "recommendations" && Array.isArray(structured.recommendations)) {
    return (
      <ol className="mt-8 space-y-3">
        {(structured.recommendations as Array<Record<string, string>>).map((r, i) => (
          <li key={i} className="flex gap-4">
            <span className="text-primary font-medium tabular-nums">{String(i + 1).padStart(2, "0")}</span>
            <div>
              <p className="text-charcoal">{r.title}</p>
              <p className="text-medium-gray text-sm">{r.detail}</p>
            </div>
          </li>
        ))}
      </ol>
    )
  }
  return null
}
