import { AnalysisContent } from "./analysis-content"

export const dynamic = "force-dynamic"

export default function AnalysisPage({ params }: { params: { id: string } }) {
  return <AnalysisContent projectId={params.id} />
}
