"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Select } from "@/components/ui/select"
import { useCurrentUser, isSuperAdmin } from "@/lib/auth"
import { useCustomers } from "@/hooks/use-customers"
import { useProjects } from "@/hooks/use-projects"
import { PROJECT_INDUSTRY_LABELS, type ProjectIndustry } from "@/types/api"
import type { CreateScopedSessionRequest } from "@/types/api"

/** Auto-detects role: an admin picks any combination of industry / customer /
 * project — each further narrows the scope, down to one specific project.
 * A customer is always locked to their own customer_id and never sees
 * industry-wide chat; they only choose "all my projects" vs one specific
 * project of theirs. */
export function ScopePicker({ onSelect }: { onSelect: (scope: CreateScopedSessionRequest) => void }) {
  const user = useCurrentUser()
  const admin = isSuperAdmin(user?.role)

  return admin ? <AdminPicker onSelect={onSelect} /> : <CustomerPicker onSelect={onSelect} />
}

function AdminPicker({ onSelect }: { onSelect: (scope: CreateScopedSessionRequest) => void }) {
  const [industry, setIndustry] = useState<ProjectIndustry | "">("")
  const [customerId, setCustomerId] = useState("")
  const [projectId, setProjectId] = useState("")
  const { data: customers } = useCustomers()
  const { data: projects } = useProjects(customerId)

  return (
    <div className="premium-card rounded-xl p-8 max-w-md mx-auto mt-16 space-y-5">
      <div>
        <p className="eyebrow">Ask PulseAI</p>
        <h1 className="text-headline-md text-charcoal mt-2">Choose a scope</h1>
        <p className="text-medium-gray text-sm mt-1">
          Pick an industry, a customer, and/or a specific project — each choice narrows the next.
        </p>
      </div>

      <div className="flex flex-col gap-1.5">
        <Label htmlFor="scope-industry">Industry</Label>
        <Select id="scope-industry" value={industry} onChange={(e) => setIndustry(e.target.value as ProjectIndustry | "")}>
          <option value="">Any industry</option>
          {Object.entries(PROJECT_INDUSTRY_LABELS).map(([value, label]) => (
            <option key={value} value={value}>{label}</option>
          ))}
        </Select>
      </div>

      <div className="flex flex-col gap-1.5">
        <Label htmlFor="scope-customer">Customer</Label>
        <Select
          id="scope-customer" value={customerId}
          onChange={(e) => { setCustomerId(e.target.value); setProjectId("") }}
        >
          <option value="">Any customer</option>
          {customers?.map((c) => (
            <option key={c.id} value={c.id}>{c.name}</option>
          ))}
        </Select>
      </div>

      <div className="flex flex-col gap-1.5">
        <Label htmlFor="scope-project">Project</Label>
        <Select
          id="scope-project" value={projectId} disabled={!customerId}
          onChange={(e) => setProjectId(e.target.value)}
        >
          <option value="">{customerId ? "Any project for this customer" : "Pick a customer first"}</option>
          {projects?.map((p) => (
            <option key={p.id} value={p.id}>{p.name}</option>
          ))}
        </Select>
      </div>

      <Button
        className="w-full"
        disabled={!industry && !customerId && !projectId}
        onClick={() => onSelect({
          project_id: projectId || null,
          customer_id: customerId || null,
          industry: industry || null,
        })}
      >
        Start chat
      </Button>
    </div>
  )
}

function CustomerPicker({ onSelect }: { onSelect: (scope: CreateScopedSessionRequest) => void }) {
  const user = useCurrentUser()
  const customerId = user?.customerId ?? ""
  const [mode, setMode] = useState<"all" | "project">("all")
  const [projectId, setProjectId] = useState("")
  const { data: projects } = useProjects(customerId)

  return (
    <div className="premium-card rounded-xl p-8 max-w-md mx-auto mt-16 space-y-5">
      <div>
        <p className="eyebrow">Ask PulseAI</p>
        <h1 className="text-headline-md text-charcoal mt-2">Choose a scope</h1>
        <p className="text-medium-gray text-sm mt-1">
          Chat about all of your projects at once, or one specific project.
        </p>
      </div>

      <div className="flex flex-col gap-1.5">
        <Label htmlFor="scope-mode">Scope</Label>
        <Select id="scope-mode" value={mode} onChange={(e) => setMode(e.target.value as "all" | "project")}>
          <option value="all">All my projects</option>
          <option value="project">A specific project</option>
        </Select>
      </div>

      {mode === "project" && (
        <div className="flex flex-col gap-1.5">
          <Label htmlFor="scope-project">Project</Label>
          <Select id="scope-project" value={projectId} onChange={(e) => setProjectId(e.target.value)}>
            <option value="">Select project…</option>
            {projects?.map((p) => (
              <option key={p.id} value={p.id}>{p.name}</option>
            ))}
          </Select>
        </div>
      )}

      <Button
        className="w-full"
        disabled={mode === "project" && !projectId}
        onClick={() => onSelect(
          mode === "project"
            ? { project_id: projectId, customer_id: null, industry: null }
            : { project_id: null, customer_id: customerId, industry: null }
        )}
      >
        Start chat
      </Button>
    </div>
  )
}
