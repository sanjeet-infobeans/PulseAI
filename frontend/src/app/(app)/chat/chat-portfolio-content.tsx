"use client"

import { useState } from "react"
import { api } from "@/lib/api"
import { ChatThread } from "@/components/chat/chat-thread"
import { ScopePicker } from "@/components/chat/scope-picker"
import { useCustomers } from "@/hooks/use-customers"
import { PROJECT_INDUSTRY_LABELS, type CreateScopedSessionRequest, type ProjectIndustry } from "@/types/api"

function scopeLabel(scope: CreateScopedSessionRequest, customerName?: string): string {
  if (scope.project_id) return customerName ? `this project (${customerName})` : "this project"
  const parts: string[] = []
  if (scope.customer_id) parts.push(customerName ?? "this customer")
  if (scope.industry) parts.push(PROJECT_INDUSTRY_LABELS[scope.industry as ProjectIndustry] ?? scope.industry)
  return parts.length > 0 ? parts.join(" · ") : "your portfolio"
}

export function ChatPortfolioContent() {
  const [scope, setScope] = useState<CreateScopedSessionRequest | null>(null)
  const { data: customers } = useCustomers()

  if (!scope) {
    return <ScopePicker onSelect={setScope} />
  }

  const customerName = customers?.find((c) => c.id === scope.customer_id)?.name
  const label = scopeLabel(scope, customerName)

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between">
        <div>
          <p className="eyebrow">Ask PulseAI</p>
          <h1 className="text-headline-lg text-charcoal mt-2">Ask PulseAI</h1>
        </div>
        <button
          onClick={() => setScope(null)}
          className="text-xs text-primary hover:underline"
        >
          Change scope
        </button>
      </div>
      <ChatThread
        ensureSession={async () => (await api.chatScoped.createSession({
          ...scope, title: "Ask PulseAI",
        })).id}
        askPath={(sid) => `/chat/sessions/${sid}/messages`}
        placeholder={`Ask about ${label}…`}
        emptyStateText={`Ask about delivery status, blockers, or risk for ${label}.`}
      />
    </div>
  )
}
