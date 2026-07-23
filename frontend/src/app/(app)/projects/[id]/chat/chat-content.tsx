"use client"

import { api } from "@/lib/api"
import { ChatThread } from "@/components/chat/chat-thread"

const SUGGESTIONS = [
  "Build a requirement traceability matrix for the current sprint.",
  "What % of the BRD is covered by the current sprint?",
  "Which current-sprint items are out of scope (not in any document)?",
  "Show current blockers.",
]

export function ChatContent({ projectId }: { projectId: string }) {
  return (
    <div className="flex flex-col h-full">
      <div>
        <p className="eyebrow">Ask PulseAI</p>
        <h1 className="text-headline-lg text-charcoal mt-2">Ask PulseAI</h1>
      </div>
      <ChatThread
        ensureSession={async () => (await api.chatScoped.createSession({ project_id: projectId, title: "Ask PulseAI" })).id}
        askPath={(sid) => `/chat/sessions/${sid}/messages`}
        placeholder="Ask about this project…"
        suggestions={SUGGESTIONS}
        emptyStateText="Instant answers on status, blockers, and delivery risk."
      />
    </div>
  )
}
