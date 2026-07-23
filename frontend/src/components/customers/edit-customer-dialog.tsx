"use client"

import { useEffect, useState } from "react"
import { PencilSimple } from "@phosphor-icons/react"
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
import { useUpdateCustomer } from "@/hooks/use-customers"
import type { Customer } from "@/types/api"

export function EditCustomerDialog({ customer }: { customer: Customer }) {
  const [open, setOpen] = useState(false)
  const [name, setName] = useState(customer.name)
  const [email, setEmail] = useState(customer.contact_email ?? "")
  const [industry, setIndustry] = useState(customer.industry ?? "")
  const update = useUpdateCustomer(customer.id)

  useEffect(() => {
    setName(customer.name)
    setEmail(customer.contact_email ?? "")
    setIndustry(customer.industry ?? "")
  }, [customer])

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    await update.mutateAsync({
      name: name.trim(),
      contact_email: email.trim() || null,
      industry: industry.trim() || null,
    })
    setOpen(false)
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <button
          type="button"
          title="Edit customer"
          onClick={(e) => { e.preventDefault(); e.stopPropagation() }}
          className="w-8 h-8 rounded-md flex items-center justify-center text-medium-gray hover:text-primary hover:bg-background transition-colors"
        >
          <PencilSimple size={16} />
        </button>
      </DialogTrigger>
      <DialogContent onClick={(e) => e.stopPropagation()}>
        <DialogHeader>
          <DialogTitle>Edit customer</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="flex flex-col gap-4 px-8 py-6">
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="ec-name">Name</Label>
              <Input id="ec-name" required value={name} onChange={(e) => setName(e.target.value)} />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="ec-email">Contact email</Label>
              <Input id="ec-email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
              <p className="text-xs text-medium-gray">
                Changing this does not change their existing login credentials.
              </p>
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="ec-industry">Industry</Label>
              <Input id="ec-industry" value={industry} onChange={(e) => setIndustry(e.target.value)} />
            </div>
            {update.isError && (
              <p className="text-xs text-primary">{(update.error as Error).message}</p>
            )}
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={update.isPending || !name.trim()}>
              {update.isPending ? "Saving…" : "Save changes"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
