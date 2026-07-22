import { ResourcesContent } from "./resources-content"

export const dynamic = "force-dynamic"

export default function ResourcesPage({ params }: { params: { id: string } }) {
  return <ResourcesContent projectId={params.id} />
}
