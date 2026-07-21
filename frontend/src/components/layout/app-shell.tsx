"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { getToken } from "@/lib/api"
import { Sidebar } from "./sidebar"
import { Topbar } from "./topbar"
import { ChatFab } from "@/components/chat/chat-fab"

export function AppShell({
  children,
  title,
  showFab = true,
}: {
  children: React.ReactNode
  title?: string
  showFab?: boolean
}) {
  const router = useRouter()

  // Belt-and-suspenders auth guard alongside the layout guard.
  useEffect(() => {
    if (!getToken()) router.replace("/login")
  }, [router])

  return (
    <div className="min-h-screen bg-background">
      <Sidebar />
      <Topbar title={title} />
      <main className="ml-[280px] min-h-screen pt-20">
        <div className="p-12 max-w-[1400px] mx-auto">{children}</div>
      </main>
      {showFab && <ChatFab />}
    </div>
  )
}
