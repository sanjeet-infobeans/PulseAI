import { RisksContent } from "./risks-content"

export const dynamic = "force-dynamic"

export default function RisksPage({ params }: { params: { id: string } }) {
  return <RisksContent projectId={params.id} />
}
