"use client"

import Link from "next/link"
import { ArrowLeft, ArrowRight, Gauge } from "@phosphor-icons/react"
import { useCustomer } from "@/hooks/use-customers"
import { useProjects } from "@/hooks/use-projects"
import { useCurrentUser, isSuperAdmin } from "@/lib/auth"
import { CreateProjectDialog } from "@/components/projects/create-project-dialog"
import { EditProjectDialog } from "@/components/projects/edit-project-dialog"
import { Badge } from "@/components/ui/badge"

const STATUS_VARIANT = {
  active: "health-good",
  on_hold: "health-warn",
  completed: "neutral",
} as const

export function CustomerDetailContent({ customerId }: { customerId: string }) {
  const user = useCurrentUser()
  const { data: customer } = useCustomer(customerId)
  const { data: projects, isLoading, isError, error } = useProjects(customerId)

  return (
    <div className="space-y-8">
      <Link href="/customers" className="inline-flex items-center gap-2 text-sm text-medium-gray hover:text-charcoal">
        <ArrowLeft size={14} /> Customers
      </Link>

      <div className="flex items-end justify-between">
        <div>
          <p className="eyebrow">Customer</p>
          <h1 className="text-headline-lg text-charcoal mt-2">{customer?.name ?? "…"}</h1>
          <p className="text-medium-gray text-body-md mt-1">{customer?.industry ?? "—"}</p>
        </div>
        {isSuperAdmin(user?.role) && <CreateProjectDialog customerId={customerId} />}
      </div>

      {isLoading && <p className="text-medium-gray text-sm">Loading projects…</p>}
      {isError && <p className="text-primary text-sm">{(error as Error).message}</p>}

      {projects && projects.length === 0 && (
        <div className="premium-card rounded-xl p-12 text-center">
          <p className="text-charcoal">No projects yet</p>
          <p className="text-medium-gray text-sm mt-1">Create a project, then connect Jira to sync delivery data.</p>
        </div>
      )}

      {projects && projects.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {projects.map((p) => (
            <Link
              key={p.id}
              href={`/projects/${p.id}`}
              className="premium-card rounded-xl p-8 border-l-4 border-l-primary group hover:border-primary/60 transition-colors"
            >
              <div className="flex items-start justify-between">
                <div>
                  <p className="eyebrow">{p.key}</p>
                  <h3 className="text-headline-md text-charcoal mt-2">{p.name}</h3>
                </div>
                <div className="flex items-center gap-1">
                  <Badge variant={STATUS_VARIANT[p.status]}>{p.status.replace("_", " ")}</Badge>
                  {isSuperAdmin(user?.role) && <EditProjectDialog projectId={p.id} compact />}
                </div>
              </div>
              <p className="text-medium-gray text-sm mt-3 line-clamp-2">{p.description ?? "No description"}</p>
              <div className="flex items-center gap-2 text-primary text-sm mt-6">
                <Gauge size={16} /> Open dashboard <ArrowRight size={14} />
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
