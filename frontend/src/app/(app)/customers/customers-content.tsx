"use client"

import Link from "next/link"
import { Buildings, ArrowRight } from "@phosphor-icons/react"
import { useCustomers } from "@/hooks/use-customers"
import { useCurrentUser, isSuperAdmin } from "@/lib/auth"
import { CreateCustomerDialog } from "@/components/customers/create-customer-dialog"
import { Badge } from "@/components/ui/badge"

export function CustomersContent() {
  const user = useCurrentUser()
  const { data: customers, isLoading, isError, error } = useCustomers()

  return (
    <div className="space-y-8">
      <div className="flex items-end justify-between">
        <div>
          <p className="eyebrow">Portfolio</p>
          <h1 className="text-headline-lg text-charcoal mt-2">Customers</h1>
          <p className="text-medium-gray text-body-md mt-1">
            Every engagement PulseAI is watching over.
          </p>
        </div>
        {isSuperAdmin(user?.role) && <CreateCustomerDialog />}
      </div>

      {isLoading && <p className="text-medium-gray text-sm">Loading customers…</p>}
      {isError && <p className="text-primary text-sm">{(error as Error).message}</p>}

      {customers && customers.length === 0 && (
        <div className="premium-card rounded-xl p-12 text-center">
          <Buildings size={40} weight="light" className="mx-auto text-medium-gray/50" />
          <p className="text-charcoal mt-4">No customers yet</p>
          <p className="text-medium-gray text-sm mt-1">Create your first customer to begin.</p>
        </div>
      )}

      {customers && customers.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {customers.map((c) => (
            <Link
              key={c.id}
              href={`/customers/${c.id}`}
              className="premium-card rounded-xl p-8 group hover:border-primary/40 transition-colors"
            >
              <div className="flex items-start justify-between">
                <div className="w-11 h-11 rounded-md bg-background flex items-center justify-center">
                  <Buildings size={22} weight="regular" className="text-primary" />
                </div>
                {c.is_active ? (
                  <Badge variant="health-good">Active</Badge>
                ) : (
                  <Badge variant="neutral">Inactive</Badge>
                )}
              </div>
              <h3 className="text-headline-md text-charcoal mt-6">{c.name}</h3>
              <p className="text-medium-gray text-sm mt-1">{c.industry ?? "—"}</p>
              <div className="flex items-center gap-2 text-primary text-sm mt-6 opacity-0 group-hover:opacity-100 transition-opacity">
                View projects <ArrowRight size={14} />
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
