"use client"

import { useState } from "react"
import { Plus } from "@phosphor-icons/react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { useCreateResource } from "@/hooks/use-resources"

export function AddResourceDialog({ projectId }: { projectId: string }) {
  const [open, setOpen] = useState(false)
  const [name, setName] = useState("")
  const [designation, setDesignation] = useState("")
  const [email, setEmail] = useState("")
  const [allocation, setAllocation] = useState("100")
  const [billable, setBillable] = useState(true)
  const [skills, setSkills] = useState("")
  const create = useCreateResource(projectId)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    await create.mutateAsync({
      name: name.trim(),
      designation: designation.trim() || null,
      email: email.trim() || null,
      allocation_percentage: allocation ? Number(allocation) : 100,
      billable,
      skills: skills.split(",").map((s) => s.trim()).filter(Boolean),
    })
    setName("")
    setDesignation("")
    setEmail("")
    setAllocation("100")
    setBillable(true)
    setSkills("")
    setOpen(false)
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button size="sm">
          <Plus size={16} />
          Add resource
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Add resource</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="flex flex-col gap-4 px-8 py-6">
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="r-name">Name</Label>
              <Input id="r-name" required value={name} onChange={(e) => setName(e.target.value)} placeholder="Jane Doe" />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="r-designation">Designation</Label>
              <Input id="r-designation" value={designation} onChange={(e) => setDesignation(e.target.value)} placeholder="Backend Developer" />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="r-email">Email</Label>
              <Input id="r-email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="jane.doe@company.com" />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="r-allocation">Allocation %</Label>
                <Input id="r-allocation" type="number" min="0" max="100" value={allocation} onChange={(e) => setAllocation(e.target.value)} />
              </div>
              <div className="flex items-end gap-2 pb-1.5">
                <input id="r-billable" type="checkbox" checked={billable} onChange={(e) => setBillable(e.target.checked)} />
                <Label htmlFor="r-billable">Billable</Label>
              </div>
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="r-skills">Skills (comma-separated)</Label>
              <Input id="r-skills" value={skills} onChange={(e) => setSkills(e.target.value)} placeholder="React, FastAPI" />
            </div>
            {create.isError && (
              <p className="text-xs text-primary">{(create.error as Error).message}</p>
            )}
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={create.isPending || !name.trim()}>
              {create.isPending ? "Adding…" : "Add resource"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
