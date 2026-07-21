import { DocumentsContent } from "./documents-content"

export const dynamic = "force-dynamic"

export default function DocumentsPage({ params }: { params: { id: string } }) {
  return <DocumentsContent projectId={params.id} />
}
