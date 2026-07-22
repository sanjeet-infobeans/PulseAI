"use client"

import { useState } from "react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { CheckCircle, Sparkle, WarningCircle } from "@phosphor-icons/react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { useLatestAnalysis, useLatestJudgeReview, useRunAnalysis, useRunJudge } from "@/hooks/use-analysis"
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
    </div>
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
        {(structured.risks as Array<Record<string, string>>).map((r, i) => (
          <div key={i} className="rounded-lg border-l-4 border-l-primary bg-background p-5">
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
