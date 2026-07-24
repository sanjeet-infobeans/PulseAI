import { Badge } from "@/components/ui/badge"
import { severityBorder } from "@/lib/severity"
import type { RiskCard as RiskCardT } from "@/types/api"

export function RiskCard({ risk, index }: { risk: RiskCardT; index: number }) {
  return (
    <div className={`premium-card rounded-xl p-6 border-t-4 ${severityBorder(risk.severity).replace("border-l", "border-t")}`}>
      <div className="flex justify-between items-center mb-4">
        <Badge variant={risk.severity === "high" ? "severity-high" : risk.severity === "medium" ? "severity-med" : "severity-low"}>
          {risk.severity} impact
        </Badge>
        <span className="text-xs text-medium-gray tabular-nums">R-{String(index + 1).padStart(3, "0")}</span>
      </div>
      <h4 className="text-body-lg text-charcoal">{risk.title}</h4>
      {risk.impact && <p className="text-sm text-medium-gray mt-2 leading-relaxed">{risk.impact}</p>}
      {risk.evidence && (
        <div className="mt-4 p-3 bg-background border border-light-gray rounded">
          <p className="text-[10px] font-medium text-primary uppercase mb-1 tracking-wider">Evidence</p>
          <p className="text-xs text-charcoal leading-snug">{risk.evidence}</p>
        </div>
      )}
    </div>
  )
}
