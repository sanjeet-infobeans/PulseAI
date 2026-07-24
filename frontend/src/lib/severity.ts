import type { RiskSeverity } from "@/types/api"

export const SEVERITY_BORDER: Record<RiskSeverity, string> = {
  high: "border-l-primary",
  medium: "border-l-charcoal",
  low: "border-l-medium-gray",
}

const SEVERITY_RANK: Record<RiskSeverity, number> = { high: 0, medium: 1, low: 2 }

export function severityBorder(severity: string): string {
  return SEVERITY_BORDER[severity as RiskSeverity] ?? SEVERITY_BORDER.medium
}

export function severityRank(severity: string): number {
  return SEVERITY_RANK[severity as RiskSeverity] ?? SEVERITY_RANK.medium
}

export function sortBySeverity<T extends { severity: string }>(items: T[]): T[] {
  return [...items].sort((a, b) => severityRank(a.severity) - severityRank(b.severity))
}
