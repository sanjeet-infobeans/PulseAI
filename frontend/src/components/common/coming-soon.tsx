import { Sparkle } from "@phosphor-icons/react/dist/ssr"
import { Badge } from "@/components/ui/badge"

export function ComingSoon({
  eyebrow,
  title,
  body,
  milestone,
  future = false,
}: {
  eyebrow: string
  title: string
  body: string
  milestone?: string
  future?: boolean
}) {
  return (
    <div className="space-y-8">
      {future && (
        <div className="rounded-xl border-l-4 border-l-primary bg-primary/5 px-6 py-4 text-sm text-charcoal">
          Projection mode — seeded demo data illustrating a future PulseAI capability.
        </div>
      )}
      <div>
        <p className="eyebrow">{eyebrow}</p>
        <div className="flex items-center gap-3 mt-2">
          <h1 className="text-headline-lg text-charcoal">{title}</h1>
          {future && <Badge variant="future">Future capability</Badge>}
          {milestone && !future && <Badge variant="neutral">{milestone}</Badge>}
        </div>
      </div>
      <div className="premium-card rounded-xl p-12 flex flex-col items-center text-center">
        <div className="w-14 h-14 rounded-full bg-background flex items-center justify-center">
          <Sparkle size={26} className="text-primary" />
        </div>
        <p className="text-charcoal text-body-lg mt-5 max-w-md">{body}</p>
      </div>
    </div>
  )
}
