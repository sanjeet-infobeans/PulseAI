"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { ChatText } from "@phosphor-icons/react"

/** Floating Ask-PulseAI trigger (code.html). Links to the active project's chat. */
export function ChatFab() {
  const path = usePathname()
  const projectId = path.match(/\/projects\/([^/]+)/)?.[1] ?? null
  if (!projectId) return null

  const href = `/projects/${projectId}/chat`
  if (path === href) return null

  return (
    <Link
      href={href}
      aria-label="Ask PulseAI"
      className="fixed bottom-10 right-10 w-16 h-16 bg-primary text-white rounded-full shadow-lg flex items-center justify-center hover:scale-110 active:scale-95 transition-transform z-50"
    >
      <ChatText size={30} weight="regular" />
      <span className="absolute -top-1 -right-1 w-5 h-5 bg-charcoal border-2 border-surface rounded-full flex items-center justify-center">
        <span className="w-1.5 h-1.5 bg-primary rounded-full animate-pulse" />
      </span>
    </Link>
  )
}
