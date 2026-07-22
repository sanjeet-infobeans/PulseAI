"use client"

import { UsersThree, CalendarBlank } from "@phosphor-icons/react"
import { useProject } from "@/hooks/use-projects"
import { useResources } from "@/hooks/use-resources"
import { Badge } from "@/components/ui/badge"
import { fmtDate } from "@/lib/utils"
import type { Resource, ResourceLeave } from "@/types/api"

export function ResourcesContent({ projectId }: { projectId: string }) {
  const { data: project } = useProject(projectId)
  const { data, isLoading } = useResources(projectId)

  const resources = data?.resources ?? []
  const summary = data?.summary

  const leaves = resources
    .flatMap((r) => r.planned_leaves.map((lv) => ({ resource: r, leave: lv })))
    .sort((a, b) => a.leave.start_date.localeCompare(b.leave.start_date))

  if (!isLoading && resources.length === 0) {
    return (
      <div className="space-y-8">
        <Header name={project?.name} />
        <div className="premium-card rounded-xl p-12 text-center">
          <p className="text-charcoal">No resource data yet</p>
          <p className="text-medium-gray text-sm mt-1">
            Assign a resource connector for this project to populate the team roster.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-gutter">
      <Header name={project?.name} />

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
        <h2 className="text-headline-md text-charcoal">Team roster</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-gutter">
          {resources.map((r) => (
            <ResourceCard key={r.resource_id} resource={r} />
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
    </div>
  )
}

function Header({ name }: { name?: string }) {
  return (
    <div>
      <p className="eyebrow">Resource planning</p>
      <h1 className="text-headline-lg text-charcoal mt-2">{name ?? "…"}</h1>
      <p className="text-medium-gray text-body-md mt-1">
        Team roster, allocation, and planned leaves behind this project&apos;s delivery capacity.
      </p>
    </div>
  )
}

function ResourceCard({ resource }: { resource: Resource }) {
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
        <Badge variant={resource.billable ? "health-good" : "neutral"}>
          {resource.billable ? "Billable" : "Non-billable"}
        </Badge>
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
