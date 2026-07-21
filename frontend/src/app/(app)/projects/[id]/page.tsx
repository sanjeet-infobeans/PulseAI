import { ProjectOverviewContent } from "./project-overview-content"

export const dynamic = "force-dynamic"

export default function ProjectDashboardPage({ params }: { params: { id: string } }) {
  return <ProjectOverviewContent projectId={params.id} />
}
