"use client"

import { useEffect, useState } from "react"
import { ArrowLeft, ArrowsClockwise, CheckCircle, WarningCircle } from "@phosphor-icons/react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { fmtRelative } from "@/lib/utils"
import { isSuperAdmin, useCurrentUser } from "@/lib/auth"
import { useProject, useProjectOutcome, useMarkProjectOutcome } from "@/hooks/use-projects"
import {
  jiraConnector,
  useAssignConnector,
  useConnectors,
  useConnectorStatus,
  useSyncConnector,
  useTestConnector,
} from "@/hooks/use-connectors"

const STATUS_BADGE = {
  unconfigured: { variant: "neutral", label: "Not configured" },
  connected: { variant: "health-good", label: "Connected" },
  syncing: { variant: "health-warn", label: "Syncing…" },
  error: { variant: "health-risk", label: "Error" },
} as const

export function SettingsContent({ projectId }: { projectId: string }) {
  const { data: project } = useProject(projectId)
  const { data: connectors } = useConnectors(projectId)
  const jira = jiraConnector(connectors)
  const user = useCurrentUser()
  const { data: outcome } = useProjectOutcome(projectId)
  const markOutcome = useMarkProjectOutcome(projectId)

  const assign = useAssignConnector(projectId)
  const test = useTestConnector(projectId)
  const sync = useSyncConnector(projectId)

  const [baseUrl, setBaseUrl] = useState("")
  const [email, setEmail] = useState("")
  const [projectKey, setProjectKey] = useState("")
  const [boardId, setBoardId] = useState("")
  const [spField, setSpField] = useState("")
  const [secretRef, setSecretRef] = useState("")

  // Poll status while syncing.
  const polling = jira?.status === "syncing" || sync.isPending
  const { data: live } = useConnectorStatus(projectId, jira?.id, polling)
  const current = live ?? jira

  useEffect(() => {
    if (!jira) return
    const c = jira.config as Record<string, string>
    setBaseUrl(c.base_url ?? "")
    setEmail(c.email ?? "")
    setProjectKey(c.project_key ?? "")
    setBoardId(c.board_id ?? "")
    setSpField(c.story_point_field ?? "")
    setSecretRef(jira.secret_ref ?? "")
  }, [jira])

  async function handleSave(e: React.FormEvent) {
    e.preventDefault()
    await assign.mutateAsync({
      type: "jira",
      mode: "real",
      config: {
        base_url: baseUrl.trim(),
        email: email.trim(),
        project_key: projectKey.trim().toUpperCase(),
        board_id: boardId.trim(),
        ...(spField.trim() ? { story_point_field: spField.trim() } : {}),
      },
      secret_ref: secretRef.trim() || null,
    })
  }

  const badge = current ? STATUS_BADGE[current.status] : STATUS_BADGE.unconfigured

  return (
    <div className="space-y-8 max-w-3xl">
      <Link href={`/projects/${projectId}`} className="inline-flex items-center gap-2 text-sm text-medium-gray hover:text-charcoal">
        <ArrowLeft size={14} /> {project?.name ?? "Project"}
      </Link>

      <div className="flex items-end justify-between">
        <div>
          <p className="eyebrow">Configuration</p>
          <h1 className="text-headline-lg text-charcoal mt-2">Jira connector</h1>
          <p className="text-medium-gray text-body-md mt-1">
            Connect a live Jira board, then sync sprints and stories into PulseAI.
          </p>
        </div>
        <Badge variant={badge.variant}>{badge.label}</Badge>
      </div>

      {isSuperAdmin(user?.role) && (
        <form onSubmit={handleSave} className="premium-card rounded-xl p-8 space-y-5">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            <Field label="Base URL" value={baseUrl} onChange={setBaseUrl} placeholder="https://acme.atlassian.net" required />
            <Field label="Account email" value={email} onChange={setEmail} placeholder="you@acme.com" required />
            <Field label="Project key" value={projectKey} onChange={setProjectKey} placeholder="ATLAS" required />
            <Field label="Board ID" value={boardId} onChange={setBoardId} placeholder="42" required />
            <Field label="Story-point field" value={spField} onChange={setSpField} placeholder="customfield_10016" />
            <Field label="Token secret ref (env var)" value={secretRef} onChange={setSecretRef} placeholder="JIRA_TOKEN_ATLAS" required maxLength={128} />
          </div>
          <p className="text-xs text-medium-gray">
            The API token is never stored. Set it as the named environment variable on the server; PulseAI reads it at sync time.
          </p>
          <div className="flex items-center gap-3">
            <Button type="submit" disabled={assign.isPending}>
              {assign.isPending ? "Saving…" : jira ? "Update connector" : "Save connector"}
            </Button>
            {jira && (
              <Button
                type="button"
                variant="outline"
                disabled={test.isPending}
                onClick={() => test.mutate(jira.id)}
              >
                {test.isPending ? "Testing…" : "Test connection"}
              </Button>
            )}
          </div>
          {assign.isError && <p className="text-xs text-primary">{(assign.error as Error).message}</p>}
          {test.isError && <p className="text-xs text-primary">{(test.error as Error).message}</p>}
          {test.isSuccess && <p className="text-xs text-good">Connection OK.</p>}
        </form>
      )}

      {jira && (
        <div className="premium-card rounded-xl p-8 border-l-4 border-l-primary flex items-center justify-between">
          <div>
            <h3 className="text-headline-md text-charcoal">Sync project</h3>
            <p className="text-medium-gray text-sm mt-1 flex items-center gap-2">
              {current?.status === "error" ? (
                <>
                  <WarningCircle size={15} className="text-primary" />
                  {current.last_error ?? "Last sync failed"}
                </>
              ) : current?.last_synced_at ? (
                <>
                  <CheckCircle size={15} className="text-good" />
                  Last synced {fmtRelative(current.last_synced_at)}
                </>
              ) : (
                "Not synced yet"
              )}
            </p>
          </div>
          {isSuperAdmin(user?.role) && (
            <Button
              variant="charcoal"
              disabled={polling}
              onClick={() => sync.mutate(jira.id)}
            >
              <ArrowsClockwise size={16} className={polling ? "animate-spin" : ""} />
              {polling ? "Syncing…" : "Sync project"}
            </Button>
          )}
        </div>
      )}

      {isSuperAdmin(user?.role) && (
        <div className="premium-card rounded-xl p-8 border-l-4 border-l-medium-gray">
          <h3 className="text-headline-md text-charcoal">Delivery outcome</h3>
          <p className="text-medium-gray text-sm mt-1">
            Marking a project complete records its outcome — the corpus future organizational-intelligence
            features (Delivery DNA) will draw on once enough projects have closed.
          </p>
          {outcome?.closed_at ? (
            <div className="mt-4 grid grid-cols-2 sm:grid-cols-4 gap-4">
              <OutcomeStat label="Duration" value={outcome.actual_duration_days != null ? `${outcome.actual_duration_days}d` : "—"} />
              <OutcomeStat label="Avg velocity" value={outcome.actual_velocity_avg != null ? String(outcome.actual_velocity_avg) : "—"} />
              <OutcomeStat label="Defect density" value={outcome.defect_density != null ? `${Math.round(outcome.defect_density * 100)}%` : "—"} />
              <OutcomeStat label="On time" value={outcome.delivered_on_time ? "Yes" : "No"} />
            </div>
          ) : (
            <div className="flex items-center gap-3 mt-4">
              <Button
                type="button"
                variant="outline"
                disabled={markOutcome.isPending}
                onClick={() => markOutcome.mutate(true)}
              >
                {markOutcome.isPending ? "Saving…" : "Mark complete — delivered on time"}
              </Button>
              <Button
                type="button"
                variant="outline"
                disabled={markOutcome.isPending}
                onClick={() => markOutcome.mutate(false)}
              >
                Mark complete — delivered late
              </Button>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function OutcomeStat({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs text-medium-gray">{label}</p>
      <p className="text-headline-md text-charcoal tabular-nums mt-1">{value}</p>
    </div>
  )
}

function Field({
  label, value, onChange, placeholder, required, maxLength,
}: {
  label: string
  value: string
  onChange: (v: string) => void
  placeholder?: string
  required?: boolean
  maxLength?: number
}) {
  return (
    <div className="flex flex-col gap-1.5">
      <Label>{label}</Label>
      <Input value={value} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} required={required} maxLength={maxLength} />
    </div>
  )
}
