"use client"

import { useEffect, useState } from "react"
import type { UserRole } from "@/types/api"
import { clearToken, getToken } from "@/lib/api"

interface JwtPayload {
  sub: string
  type: string
  role: UserRole
  customer_id: string | null
  org_id: string
  exp: number
}

export interface CurrentUser {
  id: string
  role: UserRole
  customerId: string | null
  orgId: string
}

function readCurrentUser(): CurrentUser | null {
  const token = getToken()
  if (!token) return null
  try {
    const payload = JSON.parse(atob(token.split(".")[1])) as JwtPayload
    if (payload.type !== "user") return null
    return {
      id: payload.sub,
      role: payload.role,
      customerId: payload.customer_id,
      orgId: payload.org_id,
    }
  } catch {
    return null
  }
}

/**
 * The current user, decoded from the stored JWT.
 *
 * Returns null on the server and on the first client render so the initial
 * client tree matches the server-rendered HTML, then resolves the real user
 * after mount. Reading the token during render desyncs SSR/CSR and triggers a
 * hydration mismatch (the sidebar's super-admin nav group would render on the
 * client but not the server).
 */
export function useCurrentUser(): CurrentUser | null {
  const [user, setUser] = useState<CurrentUser | null>(null)
  useEffect(() => {
    setUser(readCurrentUser())
  }, [])
  return user
}

export function signOut(): void {
  clearToken()
  window.location.href = "/login"
}

export function isSuperAdmin(role: UserRole | undefined): boolean {
  return role === "super_admin"
}
