import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function fmtNum(n: number | null | undefined): string {
  if (n == null) return "—"
  return n.toLocaleString()
}

export function fmtPct(n: number | null | undefined, decimals = 0): string {
  if (n == null) return "—"
  return `${n.toFixed(decimals)}%`
}

export function fmtDate(iso: string | null | undefined): string {
  if (!iso) return "—"
  return new Date(iso).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  })
}

export function fmtDateTime(iso: string | null | undefined): string {
  if (!iso) return "—"
  return new Date(iso).toLocaleString("en-US", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  })
}

export function fmtRelative(iso: string | null | undefined): string {
  if (!iso) return "never"
  const diff = Date.now() - new Date(iso).getTime()
  const mins = Math.round(diff / 60000)
  if (mins < 1) return "just now"
  if (mins < 60) return `${mins}m ago`
  const hrs = Math.round(mins / 60)
  if (hrs < 24) return `${hrs}h ago`
  return fmtDate(iso)
}

/** Map a 0–100 confidence/health score to a semantic band. */
export function scoreBand(score: number | null | undefined): "red" | "amber" | "green" {
  if (score == null) return "amber"
  if (score < 50) return "red"
  if (score < 75) return "amber"
  return "green"
}

export function bandLabel(band: "red" | "amber" | "green"): string {
  return { red: "At risk", amber: "Watch", green: "On track" }[band]
}
