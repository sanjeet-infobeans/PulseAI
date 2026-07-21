"use client"

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

export function useCurrentUser(): CurrentUser | null {
  if (typeof window === "undefined") return null
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

export function signOut(): void {
  clearToken()
  window.location.href = "/login"
}

export function isSuperAdmin(role: UserRole | undefined): boolean {
  return role === "super_admin"
}
