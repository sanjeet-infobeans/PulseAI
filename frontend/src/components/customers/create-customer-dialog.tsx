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
import { useCreateCustomer } from "@/hooks/use-customers"

export function CreateCustomerDialog() {
  const [open, setOpen] = useState(false)
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [industry, setIndustry] = useState("")
  const create = useCreateCustomer()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    await create.mutateAsync({
      name: name.trim(),
      contact_email: email.trim() || null,
      industry: industry.trim() || null,
    })
    setName("")
    setEmail("")
    setIndustry("")
    setOpen(false)
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>
          <Plus size={16} weight="regular" />
          New customer
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create customer</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="flex flex-col gap-4 px-8 py-6">
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="c-name">Name</Label>
              <Input id="c-name" required value={name} onChange={(e) => setName(e.target.value)} placeholder="Acme Corporation" />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="c-email">Contact email</Label>
              <Input id="c-email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="delivery@acme.com" />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="c-industry">Industry</Label>
              <Input id="c-industry" value={industry} onChange={(e) => setIndustry(e.target.value)} placeholder="Retail" />
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
              {create.isPending ? "Creating…" : "Create customer"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
