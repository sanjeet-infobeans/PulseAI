"use client"

import { useState } from "react"
import { Plus, TrashSimple } from "@phosphor-icons/react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select } from "@/components/ui/select"
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { useCreateProject } from "@/hooks/use-projects"
import { api } from "@/lib/api"
import { PROJECT_INDUSTRY_LABELS, type ProjectIndustry } from "@/types/api"

type DraftResource = {
  name: string
  designation: string
  email: string
  allocationPercentage: string
  billable: boolean
  skills: string
}

const EMPTY_RESOURCE: DraftResource = {
  name: "", designation: "", email: "", allocationPercentage: "100", billable: true, skills: "",
}

export function CreateProjectDialog({ customerId }: { customerId: string }) {
  const [open, setOpen] = useState(false)
  const [name, setName] = useState("")
  const [key, setKey] = useState("")
  const [description, setDescription] = useState("")
  const [startDate, setStartDate] = useState("")
  const [endDate, setEndDate] = useState("")
  const [industry, setIndustry] = useState<ProjectIndustry | "">("")
  const [totalPersonHours, setTotalPersonHours] = useState("")
  const [resources, setResources] = useState<DraftResource[]>([])
  const [resourceError, setResourceError] = useState<string | null>(null)
  const create = useCreateProject(customerId)

  function addResourceRow() {
    setResources((rs) => [...rs, { ...EMPTY_RESOURCE }])
  }
  function updateResourceRow(i: number, patch: Partial<DraftResource>) {
    setResources((rs) => rs.map((r, idx) => (idx === i ? { ...r, ...patch } : r)))
  }
  function removeResourceRow(i: number) {
    setResources((rs) => rs.filter((_, idx) => idx !== i))
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setResourceError(null)
    const project = await create.mutateAsync({
      name: name.trim(),
      key: key.trim().toUpperCase(),
      description: description.trim() || null,
      start_date: startDate || null,
      target_end_date: endDate || null,
      industry: industry || null,
      total_person_hours: totalPersonHours ? Number(totalPersonHours) : null,
    })

    const validResources = resources.filter((r) => r.name.trim())
    if (validResources.length > 0) {
      try {
        await Promise.all(validResources.map((r) => api.resources.create(project.id, {
          name: r.name.trim(),
          designation: r.designation.trim() || null,
          email: r.email.trim() || null,
          allocation_percentage: r.allocationPercentage ? Number(r.allocationPercentage) : 100,
          billable: r.billable,
          skills: r.skills.split(",").map((s) => s.trim()).filter(Boolean),
        })))
      } catch {
        // Project was created successfully even if a resource sub-call failed —
        // don't lose that; let the user retry adding resources from the Resources page.
        setResourceError("Project created, but some resources couldn't be added — add them from the project's Resources page.")
        return
      }
    }

    setName("")
    setKey("")
    setDescription("")
    setStartDate("")
    setEndDate("")
    setIndustry("")
    setTotalPersonHours("")
    setResources([])
    setOpen(false)
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>
          <Plus size={16} weight="regular" />
          New project
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create project</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="flex flex-col gap-4 px-8 py-6">
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="p-name">Name</Label>
              <Input id="p-name" required value={name} onChange={(e) => setName(e.target.value)} placeholder="Project Atlas" />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="p-key">Key</Label>
              <Input id="p-key" required value={key} onChange={(e) => setKey(e.target.value)} placeholder="ATLAS" />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="p-desc">Description</Label>
              <Input id="p-desc" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Platform migration" />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="p-industry">Industry</Label>
              <Select
                id="p-industry"
                value={industry}
                onChange={(e) => setIndustry(e.target.value as ProjectIndustry | "")}
              >
                <option value="">Select industry…</option>
                {Object.entries(PROJECT_INDUSTRY_LABELS).map(([value, label]) => (
                  <option key={value} value={value}>{label}</option>
                ))}
              </Select>
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="p-hours">Total person hours</Label>
              <Input
                id="p-hours" type="number" min="0" step="1"
                value={totalPersonHours} onChange={(e) => setTotalPersonHours(e.target.value)}
                placeholder="4000"
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="p-start">Start date</Label>
                <Input id="p-start" type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
              </div>
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="p-end">End date</Label>
                <Input id="p-end" type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
              </div>
            </div>
            <div className="flex flex-col gap-2 pt-2 border-t border-light-gray">
              <div className="flex items-center justify-between">
                <Label>Resources</Label>
                <button type="button" onClick={addResourceRow} className="text-xs text-primary hover:underline">
                  + Add resource
                </button>
              </div>
              {resources.map((r, i) => (
                <div key={i} className="flex flex-col gap-2 p-3 rounded-sm border border-light-gray">
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-medium-gray">Resource {i + 1}</span>
                    <button type="button" onClick={() => removeResourceRow(i)} className="text-medium-gray hover:text-primary">
                      <TrashSimple size={14} />
                    </button>
                  </div>
                  <Input
                    placeholder="Name" value={r.name}
                    onChange={(e) => updateResourceRow(i, { name: e.target.value })}
                  />
                  <div className="grid grid-cols-2 gap-2">
                    <Input
                      placeholder="Designation" value={r.designation}
                      onChange={(e) => updateResourceRow(i, { designation: e.target.value })}
                    />
                    <Input
                      placeholder="Allocation %" type="number" min="0" max="100" value={r.allocationPercentage}
                      onChange={(e) => updateResourceRow(i, { allocationPercentage: e.target.value })}
                    />
                  </div>
                  <Input
                    placeholder="Email" type="email" value={r.email}
                    onChange={(e) => updateResourceRow(i, { email: e.target.value })}
                  />
                  <Input
                    placeholder="Skills (comma-separated)" value={r.skills}
                    onChange={(e) => updateResourceRow(i, { skills: e.target.value })}
                  />
                </div>
              ))}
              <p className="text-xs text-medium-gray">
                Planned leaves can be added per resource from the project&apos;s Resources page after creation.
              </p>
            </div>
            {(create.isError || resourceError) && (
              <p className="text-xs text-primary">
                {resourceError ?? (create.error as Error).message}
              </p>
            )}
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={create.isPending || !name.trim() || !key.trim()}>
              {create.isPending ? "Creating…" : "Create project"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
