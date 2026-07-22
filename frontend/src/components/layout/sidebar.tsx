"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import {
  SquaresFour,
  Brain,
  ChatCircleDots,
  FileText,
  WarningCircle,
  UsersThree,
  Buildings,
  FolderOpen,
  Presentation,
  Gauge,
  SignOut,
  PlusCircle,
} from "@phosphor-icons/react"
import { cn } from "@/lib/utils"
import { useCurrentUser, signOut, isSuperAdmin } from "@/lib/auth"

type NavItem = { label: string; href: string; Icon: React.ElementType; future?: boolean }
type NavGroup = { section: string | null; items: NavItem[]; superAdminOnly?: boolean }

/** Build nav groups; workspace links resolve against the active project when present. */
function navGroups(projectId: string | null): NavGroup[] {
  const p = projectId ? `/projects/${projectId}` : null
  const groups: NavGroup[] = []

  if (p) {
    groups.push({
      section: null,
      items: [
        { label: "Executive view", href: p, Icon: SquaresFour },
        { label: "Project intelligence", href: `${p}/analysis`, Icon: Brain },
        { label: "Ask PulseAI", href: `${p}/chat`, Icon: ChatCircleDots },
        { label: "Documents", href: `${p}/documents`, Icon: FileText },
        { label: "Risk management", href: `${p}/risks`, Icon: WarningCircle },
        { label: "Resource risk", href: `${p}/resources`, Icon: UsersThree },
        { label: "Sentiment", href: `${p}/sentiment`, Icon: Gauge },
      ],
    })
  }

  groups.push({
    section: "Administration",
    superAdminOnly: true,
    items: [
      { label: "Portfolio", href: "/portfolio", Icon: SquaresFour },
      { label: "Customers", href: "/customers", Icon: Buildings },
      { label: "Projects", href: "/projects", Icon: FolderOpen },
    ],
  })

  groups.push({
    section: "Roadmap",
    items: [
      { label: "Executive dashboard", href: "/executive", Icon: Presentation, future: true },
      { label: "Resource planning", href: "/resources", Icon: UsersThree, future: true },
      { label: "Sentiment", href: "/sentiment", Icon: Gauge, future: true },
    ],
  })

  return groups
}

const ROLE_LABEL: Record<string, string> = {
  super_admin: "Super Admin",
  customer: "Customer",
}

export function Sidebar() {
  const path = usePathname()
  const user = useCurrentUser()
  const projectId = path.match(/\/projects\/([^/]+)/)?.[1] ?? null
  const groups = navGroups(projectId)

  return (
    <aside className="w-[280px] h-screen fixed left-0 top-0 flex flex-col bg-surface border-r border-light-gray z-50">
      {/* Logo */}
      <div className="p-8 flex items-center gap-3">
        <div className="w-10 h-10 bg-primary flex items-center justify-center rounded-md">
          <Gauge size={22} weight="regular" className="text-white" />
        </div>
        <div>
          <h1 className="text-xl font-medium text-charcoal tracking-tight leading-none">PulseAI</h1>
          <p className="text-[10px] uppercase tracking-[0.2em] text-medium-gray mt-1">Deliver confidence</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 mt-2 overflow-y-auto no-scrollbar">
        {groups.map((group, gi) => {
          if (group.superAdminOnly && !isSuperAdmin(user?.role)) return null
          return (
            <div key={gi}>
              {group.section && (
                <>
                  <div className="border-t border-light-gray mx-8 my-3" />
                  <p className="px-8 pb-1 text-[10px] uppercase tracking-[0.2em] text-medium-gray/70">
                    {group.section}
                  </p>
                </>
              )}
              {group.items.map(({ label, href, Icon, future }) => {
                const active = path === href
                return (
                  <Link
                    key={href}
                    href={href}
                    className={cn(
                      "flex items-center gap-4 px-8 py-3 text-body-md border-r-4 transition-colors",
                      active
                        ? "bg-background text-primary border-primary"
                        : "border-transparent text-medium-gray hover:text-charcoal hover:bg-background/50"
                    )}
                  >
                    <Icon size={20} weight="regular" />
                    <span className="flex-1">{label}</span>
                    {future && (
                      <span className="text-[9px] uppercase tracking-wider text-medium-gray/70 border border-light-gray rounded-sm px-1.5 py-0.5">
                        Soon
                      </span>
                    )}
                  </Link>
                )
              })}
            </div>
          )
        })}
      </nav>

      {/* Footer */}
      <div className="mt-auto p-6 border-t border-light-gray">
        <Link
          href="/customers"
          className="w-full bg-charcoal hover:bg-primary text-white py-3 px-4 rounded-md text-label-md transition-colors flex items-center justify-center gap-2 mb-4"
        >
          <PlusCircle size={18} weight="regular" />
          Analyze new project
        </Link>
        {user && (
          <div className="flex items-center justify-between px-1">
            <span className="text-xs text-medium-gray">{ROLE_LABEL[user.role] ?? user.role}</span>
            <button
              onClick={signOut}
              className="flex items-center gap-1 text-[11px] text-medium-gray hover:text-primary transition-colors"
              title="Sign out"
            >
              <SignOut size={13} weight="regular" />
              Sign out
            </button>
          </div>
        )}
      </div>
    </aside>
  )
}
