"use client"

import { useEffect, useRef, useState } from "react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { PaperPlaneTilt, ChatCircleDots } from "@phosphor-icons/react"
import { streamSSE } from "@/lib/stream"
import type { Citation } from "@/types/api"

interface Msg {
  role: "user" | "assistant"
  content: string
  citations?: Citation[]
  streaming?: boolean
}

/** Shared message-list/streaming/input UI for both the per-project and
 * portfolio-wide (customer/industry-scoped) Ask PulseAI pages — the only
 * difference between them is how a session is created and which endpoint
 * streams the answer, both passed in as callbacks. */
export function ChatThread({
  ensureSession, askPath, placeholder = "Ask a question…", suggestions = [], emptyStateText,
}: {
  ensureSession: () => Promise<string>
  askPath: (sessionId: string) => string
  placeholder?: string
  suggestions?: string[]
  emptyStateText: string
}) {
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [messages, setMessages] = useState<Msg[]>([])
  const [input, setInput] = useState("")
  const [busy, setBusy] = useState(false)
  const threadRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    threadRef.current?.scrollTo({ top: threadRef.current.scrollHeight, behavior: "smooth" })
  }, [messages])

  async function send(question: string) {
    if (!question.trim() || busy) return
    setBusy(true)
    setInput("")
    setMessages((m) => [...m, { role: "user", content: question }, { role: "assistant", content: "", streaming: true }])

    try {
      const sid = sessionId ?? (await (async () => {
        const s = await ensureSession()
        setSessionId(s)
        return s
      })())
      await streamSSE(
        askPath(sid),
        { question },
        {
          onEvent: (e) => {
            if (e.type === "token") {
              setMessages((m) => {
                const copy = [...m]
                copy[copy.length - 1] = {
                  ...copy[copy.length - 1],
                  content: copy[copy.length - 1].content + e.value,
                }
                return copy
              })
            } else if (e.type === "citations") {
              setMessages((m) => {
                const copy = [...m]
                copy[copy.length - 1] = { ...copy[copy.length - 1], citations: e.value }
                return copy
              })
            } else if (e.type === "error") {
              setMessages((m) => {
                const copy = [...m]
                copy[copy.length - 1] = { ...copy[copy.length - 1], content: `⚠ ${e.value}` }
                return copy
              })
            }
          },
        }
      )
    } catch (err) {
      setMessages((m) => {
        const copy = [...m]
        copy[copy.length - 1] = { role: "assistant", content: `⚠ ${(err as Error).message}` }
        return copy
      })
    } finally {
      setMessages((m) => {
        const copy = [...m]
        const last = copy[copy.length - 1]
        if (last) copy[copy.length - 1] = { ...last, streaming: false }
        return copy
      })
      setBusy(false)
    }
  }

  return (
    <div className="flex flex-col h-[calc(100vh-13rem)]">
      <div ref={threadRef} className="flex-1 overflow-y-auto no-scrollbar py-6 space-y-5">
        {messages.length === 0 && (
          <div className="flex flex-col items-center text-center py-10">
            <div className="w-16 h-16 rounded-full bg-surface premium-card flex items-center justify-center">
              <ChatCircleDots size={30} className="text-primary" />
            </div>
            <p className="text-charcoal text-body-lg mt-5">{emptyStateText}</p>
            {suggestions.length > 0 && (
              <div className="flex flex-wrap justify-center gap-2 mt-6 max-w-lg">
                {suggestions.map((s) => (
                  <button
                    key={s}
                    onClick={() => send(s)}
                    className="text-sm px-3 py-2 rounded-sm bg-surface border border-light-gray text-medium-gray hover:text-charcoal hover:border-primary/40 transition-colors"
                  >
                    {s}
                  </button>
                ))}
              </div>
            )}
          </div>
        )}

        {messages.map((m, i) => (
          <div key={i} className={m.role === "user" ? "flex justify-end" : "flex justify-start"}>
            <div
              className={
                m.role === "user"
                  ? "max-w-[80%] bg-primary text-white rounded-lg px-4 py-3 text-sm"
                  : "max-w-[85%] premium-card rounded-lg px-5 py-4"
              }
            >
              {m.role === "assistant" ? (
                <>
                  <div className="prose-pulse text-sm">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {m.content || (m.streaming ? "…" : "")}
                    </ReactMarkdown>
                  </div>
                  {m.citations && m.citations.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-3 pt-3 border-t border-light-gray">
                      {m.citations.map((c) => (
                        <span
                          key={c.ref}
                          title={c.label}
                          className="text-xs px-2 py-1 rounded-sm bg-background text-primary border border-light-gray"
                        >
                          {c.ref}
                        </span>
                      ))}
                    </div>
                  )}
                </>
              ) : (
                m.content
              )}
            </div>
          </div>
        ))}
      </div>

      <form
        onSubmit={(e) => { e.preventDefault(); send(input) }}
        className="relative mt-2"
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={placeholder}
          disabled={busy}
          className="w-full bg-surface border border-light-gray rounded-sm px-4 py-4 text-sm focus:ring-1 focus:ring-primary/30 focus:outline-none pr-12 shadow-premium"
        />
        <button
          type="submit"
          disabled={busy || !input.trim()}
          className="absolute right-4 top-1/2 -translate-y-1/2 text-primary hover:scale-110 transition-transform disabled:opacity-40"
          aria-label="Send"
        >
          <PaperPlaneTilt size={20} />
        </button>
      </form>
    </div>
  )
}
