import { SettingsContent } from "./settings-content"

export const dynamic = "force-dynamic"

export default function ProjectSettingsPage({ params }: { params: { id: string } }) {
  return <SettingsContent projectId={params.id} />
}
