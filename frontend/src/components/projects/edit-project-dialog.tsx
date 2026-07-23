"use client"

import { useEffect, useState } from "react"
import { PencilSimple } from "@phosphor-icons/react"
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
import { useProject, useUpdateProject } from "@/hooks/use-projects"
import { PROJECT_INDUSTRY_LABELS, type ProjectIndustry } from "@/types/api"

export function EditProjectDialog({ projectId }: { projectId: string }) {
  const [open, setOpen] = useState(false)
  const { data: project } = useProject(projectId)
  const update = useUpdateProject(projectId)

  const [description, setDescription] = useState("")
  const [startDate, setStartDate] = useState("")
  const [endDate, setEndDate] = useState("")
  const [industry, setIndustry] = useState<ProjectIndustry | "">("")
  const [totalPersonHours, setTotalPersonHours] = useState("")

  useEffect(() => {
    if (!project) return
    setDescription(project.description ?? "")
    setStartDate(project.start_date ?? "")
    setEndDate(project.target_end_date ?? "")
    setIndustry(project.industry ?? "")
    setTotalPersonHours(project.total_person_hours != null ? String(project.total_person_hours) : "")
  }, [project])

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    await update.mutateAsync({
      description: description.trim() || null,
      start_date: startDate || null,
      target_end_date: endDate || null,
      industry: industry || null,
      total_person_hours: totalPersonHours ? Number(totalPersonHours) : null,
    })
    setOpen(false)
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline">
          <PencilSimple size={16} />
          Edit project
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Edit project</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="flex flex-col gap-4 px-8 py-6">
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="ep-desc">Description</Label>
              <Input id="ep-desc" value={description} onChange={(e) => setDescription(e.target.value)} />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="ep-industry">Industry</Label>
              <Select
                id="ep-industry"
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
              <Label htmlFor="ep-hours">Total person hours</Label>
              <Input
                id="ep-hours" type="number" min="0" step="1"
                value={totalPersonHours} onChange={(e) => setTotalPersonHours(e.target.value)}
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="ep-start">Start date</Label>
                <Input id="ep-start" type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
              </div>
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="ep-end">End date</Label>
                <Input id="ep-end" type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
              </div>
            </div>
            {update.isError && (
              <p className="text-xs text-primary">{(update.error as Error).message}</p>
            )}
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={update.isPending}>
              {update.isPending ? "Saving…" : "Save changes"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
