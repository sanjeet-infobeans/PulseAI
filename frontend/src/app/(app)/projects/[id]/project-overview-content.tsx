"use client"

import { useState } from "react"
import Link from "next/link"
import { Gear, Sparkle, WarningCircle, ArrowRight } from "@phosphor-icons/react"
import { useProject } from "@/hooks/use-projects"
import { useConnectors, jiraConnector } from "@/hooks/use-connectors"
import { useDashboard, useComputeConfidence, useAlignment, useScopeCreep, usePrediction, useComputePrediction } from "@/hooks/use-dashboard"
import { useRunAnalysis } from "@/hooks/use-analysis"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { HealthGauge } from "@/components/health/health-gauge"
import { ConfidenceMeter } from "@/components/health/confidence-meter"
import { PredictionCard } from "@/components/health/prediction-card"
import { EffortPanel } from "@/components/health/effort-panel"
import { RiskCard } from "@/components/insights/risk-card"
import { EditProjectDialog } from "@/components/projects/edit-project-dialog"
import { fmtRelative, fmtPct } from "@/lib/utils"

export function ProjectOverviewContent({ projectId }: { projectId: string }) {
  const { data: project } = useProject(projectId)
  const { data: connectors } = useConnectors(projectId)
  const { data: dash, isLoading } = useDashboard(projectId)
  const compute = useComputeConfidence(projectId)
  const runAnalysis = useRunAnalysis(projectId)
  const alignment = useAlignment(projectId)
  const { data: scopeCreep } = useScopeCreep(projectId)
  const { data: prediction } = usePrediction(projectId)
  const computePrediction = useComputePrediction(projectId)
  const jira = jiraConnector(connectors)
  const [analyzing, setAnalyzing] = useState(false)

  const hasData = (dash?.totals?.stories ?? 0) > 0

  async function analyzeSprint() {
    setAnalyzing(true)
    try {
      await Promise.all([
        runAnalysis.mutateAsync({ kind: "executive" }),
        runAnalysis.mutateAsync({ kind: "risk" }),
        runAnalysis.mutateAsync({ kind: "recommendations" }),
        alignment.mutateAsync(),
      ])
      await compute.mutateAsync()
      await computePrediction.mutateAsync()
    } finally {
      setAnalyzing(false)
    }
  }

  if (!isLoading && !hasData) {
    return (
      <div className="space-y-8">
        <DashboardHeader projectId={projectId} name={project?.name} synced={jira?.last_synced_at ?? null} onAnalyze={analyzeSprint} analyzing={analyzing} disabled />
        <div className="premium-card rounded-xl p-12 text-center">
          <p className="text-charcoal">No delivery data yet</p>
          <p className="text-medium-gray text-sm mt-1">Connect Jira and run a sync to populate the dashboard.</p>
          <Button asChild className="mt-5"><Link href={`/projects/${projectId}/settings`}>Configure Jira</Link></Button>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-gutter">
      <DashboardHeader
        projectId={projectId} name={project?.name} synced={jira?.last_synced_at ?? null}
        onAnalyze={analyzeSprint} analyzing={analyzing}
      />

      {/* Hero row */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-gutter">
        <div className="lg:col-span-5 premium-card rounded-xl p-8 border-l-4 border-l-primary flex items-center justify-center">
          <HealthGauge score={dash?.health ?? 0} label="Overall health" />
        </div>
        <div className="lg:col-span-4 premium-card rounded-xl p-8 flex flex-col justify-between gap-6">
          <ConfidenceMeter
            confidence={dash?.confidence ?? null}
            onCompute={() => compute.mutate()}
            computing={compute.isPending}
          />
          {dash?.sprint_progress && (
            <div>
              <div className="flex justify-between items-end">
                <span className="text-sm text-medium-gray">{dash.sprint_progress.name}</span>
                <span className="text-headline-md text-primary tabular-nums">{fmtPct(dash.sprint_progress.completion_pct)}</span>
              </div>
              <div className="h-2 w-full bg-light-gray rounded-full overflow-hidden mt-2">
                <div className="h-full bg-primary rounded-full" style={{ width: `${Math.min(dash.sprint_progress.completion_pct, 100)}%` }} />
              </div>
            </div>
          )}
        </div>
        <div className="lg:col-span-3 grid grid-cols-1 gap-gutter">
          <Kpi label="Stories" value={dash?.totals?.stories ?? 0} />
          <Kpi label="Done" value={dash?.totals?.done ?? 0} />
          <Kpi label="Open issues" value={dash?.open_issues?.length ?? 0} accent />
        </div>
      </div>

      {/* Delivery completion prediction */}
      <PredictionCard
        prediction={prediction ?? null}
        onCompute={() => computePrediction.mutate()}
        computing={computePrediction.isPending}
      />

      {/* Effort vs estimate */}
      <EffortPanel effort={dash?.effort ?? null} projectId={projectId} />

      {/* Risk strip */}
      {dash?.risk_cards && dash.risk_cards.length > 0 && (
        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-headline-md text-charcoal">Priority risks</h2>
            <Link href={`/projects/${projectId}/analysis`} className="text-sm text-primary flex items-center gap-1 hover:underline">
              Full analysis <ArrowRight size={14} />
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-gutter">
            {dash.risk_cards.slice(0, 3).map((r, i) => <RiskCard key={i} risk={r} index={i} />)}
          </div>
        </section>
      )}

      {/* Requirements alignment vs the document knowledge base */}
      {alignment.data && <AlignmentPanel data={alignment.data} />}

      {/* Scope creep vs the earliest synced baseline */}
      {scopeCreep && scopeCreep.has_baseline && <ScopeCreepPanel data={scopeCreep} />}

      {/* Split: executive summary + timeline */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-gutter">
        <div className="lg:col-span-7 premium-card rounded-xl p-8 border-t-4 border-t-primary">
          <p className="eyebrow">AI executive summary</p>
          {dash?.executive_summary ? (
            <p className="text-charcoal text-sm leading-relaxed mt-3 whitespace-pre-line line-clamp-[12]">
              {dash.executive_summary}
            </p>
          ) : (
            <p className="text-medium-gray text-sm mt-3">
              Run <span className="text-primary">Analyze sprint</span> to generate an executive summary.
            </p>
          )}
        </div>
        <div className="lg:col-span-5 premium-card rounded-xl p-8">
          <div className="flex items-center justify-between">
            <p className="eyebrow">Sprint timeline</p>
            {dash?.sprint_panel.commitment_trend != null && (
              <span className="text-xs text-medium-gray">
                Avg {fmtPct(dash.sprint_panel.commitment_trend)} commitment
                <span className="text-medium-gray/70"> · last {dash.sprint_panel.commitment_trend_sprint_count} sprints</span>
              </span>
            )}
          </div>

          {dash?.sprint_panel.active ? (
            <div className="mt-4">
              <div className="flex justify-between text-xs text-medium-gray">
                <span>{dash.sprint_panel.active.name}</span>
                <span className="tabular-nums">{fmtPct(dash.sprint_panel.active.completion_pct)}</span>
              </div>
              <div className="h-1.5 w-full bg-light-gray rounded-full overflow-hidden mt-1">
                <div className="h-full rounded-full bg-primary" style={{ width: `${Math.min(dash.sprint_panel.active.completion_pct, 100)}%` }} />
              </div>
              <p className="text-xs text-medium-gray mt-1.5 tabular-nums">
                {dash.sprint_panel.active.completed_points} / {dash.sprint_panel.active.committed_points} pts committed
              </p>
            </div>
          ) : (
            <p className="text-medium-gray text-sm mt-4">No active sprint.</p>
          )}

          {dash?.sprint_panel.carried_forward && dash.sprint_panel.carried_forward.length > 0 && (
            <div className="mt-5 pt-4 border-t border-light-gray">
              <p className="text-xs text-medium-gray flex items-center gap-1.5 mb-2">
                <WarningCircle size={14} className="text-primary" />
                {dash.sprint_panel.carried_forward.length} carried forward
              </p>
              <ul className="space-y-1">
                {dash.sprint_panel.carried_forward.map((c) => (
                  <li key={c.key} className="text-xs text-charcoal">
                    <span className="text-primary">{c.key}</span> {c.title}
                    <span className="text-medium-gray"> · from {c.from_sprint_name}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>

      {/* Open issues */}
      {dash?.open_issues && dash.open_issues.length > 0 && (
        <section className="space-y-4">
          <h2 className="text-headline-md text-charcoal flex items-center gap-2">
            <WarningCircle size={20} className="text-primary" /> Blocked &amp; open issues
          </h2>
          <div className="premium-card rounded-xl overflow-hidden">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-medium-gray border-b border-light-gray">
                  <th className="px-5 py-3 font-normal">Key</th>
                  <th className="px-5 py-3 font-normal">Title</th>
                  <th className="px-5 py-3 font-normal">Assignee</th>
                  <th className="px-5 py-3 font-normal">Status</th>
                </tr>
              </thead>
              <tbody>
                {dash.open_issues.map((it) => (
                  <tr key={it.key} className="border-b border-light-gray last:border-0">
                    <td className="px-5 py-3 text-primary tabular-nums">{it.key}</td>
                    <td className="px-5 py-3 text-charcoal">{it.title}</td>
                    <td className="px-5 py-3 text-medium-gray">{it.assignee ?? "—"}</td>
                    <td className="px-5 py-3 text-medium-gray">{it.status ?? "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}
    </div>
  )
}

function DashboardHeader({
  projectId, name, synced, onAnalyze, analyzing, disabled,
}: {
  projectId: string
  name?: string
  synced: string | null
  onAnalyze: () => void
  analyzing: boolean
  disabled?: boolean
}) {
  return (
    <div className="flex items-end justify-between">
      <div>
        <p className="eyebrow">Delivery intelligence</p>
        <h1 className="text-headline-lg text-charcoal mt-2">{name ?? "…"}</h1>
        <p className="text-medium-gray text-body-md mt-1">
          {synced ? `Jira synced ${fmtRelative(synced)}` : "Connect Jira to populate delivery data"}
        </p>
      </div>
      <div className="flex items-center gap-3">
        <EditProjectDialog projectId={projectId} />
        <Button variant="outline" asChild>
          <Link href={`/projects/${projectId}/settings`}><Gear size={16} /> Jira</Link>
        </Button>
        <Button onClick={onAnalyze} disabled={analyzing || disabled}>
          <Sparkle size={16} className={analyzing ? "animate-pulse" : ""} />
          {analyzing ? "Analyzing…" : "Analyze sprint"}
        </Button>
      </div>
    </div>
  )
}

function AlignmentPanel({ data }: { data: import("@/types/api").AlignmentData }) {
  if (!data.has_knowledge_base) {
    return (
      <section className="premium-card rounded-xl p-8 border-l-4 border-l-medium-gray">
        <p className="eyebrow">Requirements alignment</p>
        <p className="text-medium-gray text-sm mt-2">{data.summary}</p>
      </section>
    )
  }
  const cov = data.requirement_coverage_pct ?? 0
  const sal = data.story_alignment_pct ?? 0
  return (
    <section className="premium-card rounded-xl p-8 border-t-4 border-t-primary space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="eyebrow">Requirements alignment</p>
          <h2 className="text-headline-md text-charcoal mt-1">Delivery vs. the knowledge base</h2>
        </div>
      </div>
      <p className="text-medium-gray text-sm">{data.summary}</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Meter label="BRD / requirement coverage" pct={cov} />
        <Meter label="Story alignment (traceable to a doc)" pct={sal} />
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <p className="eyebrow mb-2">Uncovered requirements</p>
          <ul className="space-y-1.5">
            {data.unmapped_requirements.length === 0 && <li className="text-sm text-good">All requirements covered</li>}
            {data.unmapped_requirements.map((r, i) => (
              <li key={i} className="text-sm text-charcoal"><span className="text-primary">·</span> {r}</li>
            ))}
          </ul>
        </div>
        <div>
          <p className="eyebrow mb-2">Out of scope (no document)</p>
          <ul className="space-y-1.5">
            {data.out_of_scope_stories.length === 0 && <li className="text-sm text-good">Every story traces to a requirement</li>}
            {data.out_of_scope_stories.map((s) => (
              <li key={s.key} className="text-sm text-charcoal">
                <span className="text-primary tabular-nums">{s.key}</span> — {s.title}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  )
}

function ScopeCreepPanel({ data }: { data: import("@/types/api").ScopeCreepData }) {
  const RISK_VARIANT = { low: "severity-low", medium: "severity-med", high: "severity-high" } as const
  return (
    <section className="premium-card rounded-xl p-8 border-t-4 border-t-primary space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="eyebrow">Scope creep</p>
          <h2 className="text-headline-md text-charcoal mt-1">Growth since first sync</h2>
        </div>
        <Badge variant={RISK_VARIANT[data.risk_level]}>{data.risk_level} risk</Badge>
      </div>
      {data.summary && <p className="text-medium-gray text-sm">{data.summary}</p>}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-gutter">
        <Kpi label="Scope growth" value={`${data.scope_growth_pct}%`} />
        <Kpi label="New stories" value={data.new_stories_added} />
        <Kpi label="Requirements tracked" value={data.requirements_tracked} />
        <Kpi label="Customer decisions" value={data.customer_decisions} />
      </div>
      {(data.estimated_schedule_impact_weeks > 0 || data.estimated_cost_impact_note) && (
        <p className="text-sm text-charcoal">
          Estimated impact: <span className="text-primary">{data.estimated_schedule_impact_weeks} weeks</span>
          {data.estimated_cost_impact_note && ` — ${data.estimated_cost_impact_note}`}
        </p>
      )}
    </section>
  )
}

function Meter({ label, pct }: { label: string; pct: number }) {
  return (
    <div>
      <div className="flex justify-between items-end">
        <span className="text-sm text-medium-gray">{label}</span>
        <span className="text-headline-md text-primary tabular-nums">{fmtPct(pct)}</span>
      </div>
      <div className="h-2 w-full bg-light-gray rounded-full overflow-hidden mt-2">
        <div className="h-full bg-primary rounded-full" style={{ width: `${Math.min(pct, 100)}%` }} />
      </div>
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
