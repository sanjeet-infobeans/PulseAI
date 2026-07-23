"use client"

import { useState } from "react"
import { CalendarPlus } from "@phosphor-icons/react"
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
import { useAddLeave } from "@/hooks/use-resources"

function daysBetween(start: string, end: string): number {
  if (!start || !end) return 0
  const ms = new Date(end).getTime() - new Date(start).getTime()
  return Math.max(1, Math.round(ms / 86_400_000) + 1)
}

export function AddLeaveDialog({ projectId, resourceId, resourceName }: {
  projectId: string
  resourceId: string
  resourceName: string
}) {
  const [open, setOpen] = useState(false)
  const [leaveType, setLeaveType] = useState("")
  const [startDate, setStartDate] = useState("")
  const [endDate, setEndDate] = useState("")
  const [status, setStatus] = useState("Pending")
  const addLeave = useAddLeave(projectId)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    await addLeave.mutateAsync({
      resourceId,
      body: {
        leave_type: leaveType.trim(),
        start_date: startDate,
        end_date: endDate,
        total_days: daysBetween(startDate, endDate),
        status,
      },
    })
    setLeaveType("")
    setStartDate("")
    setEndDate("")
    setStatus("Pending")
    setOpen(false)
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <button
          type="button"
          className="text-xs text-primary hover:underline flex items-center gap-1"
        >
          <CalendarPlus size={13} /> Add leave
        </button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Add leave for {resourceName}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="flex flex-col gap-4 px-8 py-6">
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="lv-type">Leave type</Label>
              <Input id="lv-type" required value={leaveType} onChange={(e) => setLeaveType(e.target.value)} placeholder="Vacation" />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="lv-start">Start date</Label>
                <Input id="lv-start" type="date" required value={startDate} onChange={(e) => setStartDate(e.target.value)} />
              </div>
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="lv-end">End date</Label>
                <Input id="lv-end" type="date" required value={endDate} onChange={(e) => setEndDate(e.target.value)} />
              </div>
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="lv-status">Status</Label>
              <Select id="lv-status" value={status} onChange={(e) => setStatus(e.target.value)}>
                <option value="Pending">Pending</option>
                <option value="Approved">Approved</option>
                <option value="Rejected">Rejected</option>
              </Select>
            </div>
            {addLeave.isError && (
              <p className="text-xs text-primary">{(addLeave.error as Error).message}</p>
            )}
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={addLeave.isPending || !leaveType.trim() || !startDate || !endDate}>
              {addLeave.isPending ? "Adding…" : "Add leave"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
