import { SentimentContent } from "./sentiment-content"

export const dynamic = "force-dynamic"

export default function SentimentPage({ params }: { params: { id: string } }) {
  return <SentimentContent projectId={params.id} />
}
