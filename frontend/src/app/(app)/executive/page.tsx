import { ComingSoon } from "@/components/common/coming-soon"

export const dynamic = "force-dynamic"

export default function ExecutivePage() {
  return (
    <ComingSoon
      future
      eyebrow="Executive"
      title="Executive dashboard"
      body="Board-ready KPIs — budget health, quality, delivery velocity, and predicted outcomes across the portfolio."
    />
  )
}
