import { ComingSoon } from "@/components/common/coming-soon"

export const dynamic = "force-dynamic"

export default function SentimentPage() {
  return (
    <ComingSoon
      future
      eyebrow="Customer sentiment"
      title="Customer sentiment"
      body="Sentiment trends inferred from customer communications — an early-warning signal for delivery relationships."
    />
  )
}
