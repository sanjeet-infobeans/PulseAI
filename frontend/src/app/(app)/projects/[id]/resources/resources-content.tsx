"use client"

import { CalendarBlank, TrashSimple, UsersThree, WarningCircle } from "@phosphor-icons/react"
import { Badge } from "@/components/ui/badge"
import { useDeleteResource, useResourceRisk, useResources } from "@/hooks/use-resources"
import { AddResourceDialog } from "@/components/projects/add-resource-dialog"
import { AddLeaveDialog } from "@/components/projects/add-leave-dialog"
import { fmtDate, fmtPct } from "@/lib/utils"
import type { Resource, ResourceLeave } from "@/types/api"

const BURNOUT_VARIANT = {
  low: "severity-low",
  medium: "severity-med",
  high: "severity-high",
} as const

export function ResourcesContent({ projectId }: { projectId: string }) {
  const { data: risk, isLoading: riskLoading } = useResourceRisk(projectId)
  const { data: roster, isLoading: rosterLoading } = useResources(projectId)

  const resources = roster?.resources ?? []
  const summary = roster?.summary

  const leaves = resources
    .flatMap((r) => r.planned_leaves.map((lv) => ({ resource: r, leave: lv })))
    .sort((a, b) => a.leave.start_date.localeCompare(b.leave.start_date))

  return (
    <div className="space-y-8">
      <div>
        <p className="eyebrow">Team capacity</p>
        <h1 className="text-headline-lg text-charcoal mt-2">Resources</h1>
        <p className="text-medium-gray text-body-md mt-1">
          Utilization, burnout risk, and knowledge concentration, plus the team roster,
          allocation, and planned leaves behind this project&apos;s delivery capacity.
        </p>
      </div>

      {riskLoading && rosterLoading && <p className="text-medium-gray text-sm">Loading…</p>}

      {risk && (
        <>
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-gutter">
            <div className="lg:col-span-4 premium-card rounded-xl p-8">
              <p className="eyebrow">Team utilization</p>
              <p className="text-headline-lg text-charcoal tabular-nums mt-2">
                {risk.team_utilization_pct != null ? fmtPct(risk.team_utilization_pct) : "—"}
              </p>
              <p className="text-xs text-medium-gray mt-1">{risk.team_size ?? "—"} team members</p>
            </div>
            <div className="lg:col-span-8 premium-card rounded-xl p-8">
              <div className="flex items-center justify-between">
                <p className="eyebrow">Burnout risk</p>
                <Badge variant={BURNOUT_VARIANT[risk.burnout_risk]}>{risk.burnout_risk}</Badge>
              </div>
              <p className="text-charcoal text-sm mt-3">{risk.burnout_reason || "No signal yet."}</p>
            </div>
          </div>

          {risk.developers.length > 0 && (
            <section className="premium-card rounded-xl p-8">
              <p className="eyebrow mb-4">Developer utilization</p>
              <div className="space-y-4">
                {risk.developers.map((d) => (
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
            {risk.sole_holder_modules.length === 0 ? (
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
                    {risk.sole_holder_modules.map((m) => (
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

          {risk.recommendations.length > 0 && (
            <section className="premium-card rounded-xl p-8 border-t-4 border-t-primary">
              <p className="eyebrow mb-4">Recommendations</p>
              <ul className="space-y-2">
                {risk.recommendations.map((r, i) => (
                  <li key={i} className="text-sm text-charcoal flex gap-2">
                    <span className="text-primary">·</span> {r}
                  </li>
                ))}
              </ul>
            </section>
          )}
        </>
      )}

      {!rosterLoading && resources.length === 0 ? (
        <div className="premium-card rounded-xl p-12 text-center space-y-4">
          <p className="text-charcoal">No resource roster yet</p>
          <p className="text-medium-gray text-sm mt-1">
            Add resources to track allocation and planned leave, or assign a resource connector
            to populate the team roster.
          </p>
          <div className="flex justify-center">
            <AddResourceDialog projectId={projectId} />
          </div>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-gutter">
            <Kpi label="Total resources" value={summary?.total_resources ?? 0} />
            <Kpi label="Active resources" value={summary?.active_resources ?? 0} />
            <Kpi
              label="On leave today"
              value={summary?.resources_on_leave_today ?? 0}
              accent={(summary?.resources_on_leave_today ?? 0) > 0}
            />
            <Kpi label="Planned leaves (next 30 days)" value={summary?.planned_leaves_next_30_days ?? 0} />
          </div>

          <section className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-headline-md text-charcoal">Team roster</h2>
              <AddResourceDialog projectId={projectId} />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-gutter">
              {resources.map((r) => (
                <ResourceCard key={r.resource_id} projectId={projectId} resource={r} />
              ))}
            </div>
          </section>

          {leaves.length > 0 && (
            <section className="space-y-4">
              <h2 className="text-headline-md text-charcoal flex items-center gap-2">
                <CalendarBlank size={20} className="text-primary" /> Upcoming leaves
              </h2>
              <div className="premium-card rounded-xl overflow-hidden">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-left text-medium-gray border-b border-light-gray">
                      <th className="px-5 py-3 font-normal">Resource</th>
                      <th className="px-5 py-3 font-normal">Leave type</th>
                      <th className="px-5 py-3 font-normal">Dates</th>
                      <th className="px-5 py-3 font-normal">Days</th>
                      <th className="px-5 py-3 font-normal">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {leaves.map(({ resource, leave }) => (
                      <LeaveRow key={leave.leave_id} resource={resource} leave={leave} />
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          )}
        </>
      )}
    </div>
  )
}

function ResourceCard({ projectId, resource }: { projectId: string; resource: Resource }) {
  const deleteResource = useDeleteResource(projectId)

  return (
    <div className="premium-card rounded-xl p-6 space-y-4">
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-center gap-3 min-w-0">
          <div className="w-10 h-10 shrink-0 flex items-center justify-center bg-background text-primary rounded-xl">
            <UsersThree size={20} weight="regular" />
          </div>
          <div className="min-w-0">
            <p className="text-charcoal truncate">{resource.name}</p>
            <p className="text-xs text-medium-gray truncate">{resource.designation}</p>
          </div>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <Badge variant={resource.billable ? "health-good" : "neutral"}>
            {resource.billable ? "Billable" : "Non-billable"}
          </Badge>
          <button
            type="button"
            title="Remove resource"
            className="text-medium-gray hover:text-primary"
            onClick={() => deleteResource.mutate(resource.resource_id)}
          >
            <TrashSimple size={15} />
          </button>
        </div>
      </div>

      <p className="text-xs text-medium-gray truncate">{resource.email}</p>

      <div>
        <div className="flex justify-between items-end">
          <span className="text-xs text-medium-gray">Allocation</span>
          <span className="text-sm text-primary tabular-nums">{resource.allocation_percentage}%</span>
        </div>
        <div className="h-1.5 w-full bg-light-gray rounded-full overflow-hidden mt-1">
          <div
            className="h-full bg-primary rounded-full"
            style={{ width: `${Math.min(resource.allocation_percentage, 100)}%` }}
          />
        </div>
      </div>

      <div className="flex flex-wrap gap-1.5">
        {resource.skills.map((skill) => (
          <Badge key={skill} variant="neutral">{skill}</Badge>
        ))}
      </div>

      <AddLeaveDialog projectId={projectId} resourceId={resource.resource_id} resourceName={resource.name} />
    </div>
  )
}

function LeaveRow({ resource, leave }: { resource: Resource; leave: ResourceLeave }) {
  return (
    <tr className="border-b border-light-gray last:border-0">
      <td className="px-5 py-3 text-charcoal">{resource.name}</td>
      <td className="px-5 py-3 text-medium-gray">{leave.leave_type}</td>
      <td className="px-5 py-3 text-medium-gray tabular-nums">
        {fmtDate(leave.start_date)} – {fmtDate(leave.end_date)}
      </td>
      <td className="px-5 py-3 text-medium-gray tabular-nums">{leave.total_days}</td>
      <td className="px-5 py-3">
        <Badge variant={leave.status === "Approved" ? "health-good" : "neutral"}>{leave.status}</Badge>
      </td>
    </tr>
  )
}

function Kpi({ label, value, accent }: { label: string; value: number; accent?: boolean }) {
  return (
    <div className="premium-card rounded-xl p-6 flex flex-col justify-between">
      <p className="eyebrow">{label}</p>
      <p className={`text-headline-lg tabular-nums mt-2 ${accent ? "text-primary" : "text-charcoal"}`}>{value}</p>
    </div>
  )
}
