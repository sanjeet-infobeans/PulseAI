"use client"

import { useCallback, useState } from "react"
import { useDropzone } from "react-dropzone"
import {
  UploadSimple, FileText, CheckCircle, CircleNotch, WarningCircle, Trash,
} from "@phosphor-icons/react"
import { Badge } from "@/components/ui/badge"
import { fmtRelative } from "@/lib/utils"
import { useDocuments, useUploadDocument, useDeleteDocument, useRequirementDrift } from "@/hooks/use-documents"
import { DOC_TYPE_LABELS, type DocTypeT, type DocumentT, type RequirementDriftItem } from "@/types/api"

const CATEGORIES: DocTypeT[] = ["brd", "transcript", "change_request", "other"]

export function DocumentsContent({ projectId }: { projectId: string }) {
  const { data: docs } = useDocuments(projectId)
  const upload = useUploadDocument(projectId)
  const remove = useDeleteDocument(projectId)
  const { data: drift } = useRequirementDrift(projectId)
  const [docType, setDocType] = useState<DocTypeT>("brd")

  const onDrop = useCallback(
    (files: File[]) => files.forEach((f) => upload.mutate({ file: f, docType })),
    [upload, docType]
  )
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "application/pdf": [".pdf"], "text/plain": [".txt"], "text/markdown": [".md"] },
    multiple: true,
  })

  return (
    <div className="space-y-8">
      <div>
        <p className="eyebrow">Documents</p>
        <h1 className="text-headline-lg text-charcoal mt-2">Document analysis</h1>
        <p className="text-medium-gray text-body-md mt-1">
          Upload a BRD, transcript, or change request. PulseAI extracts the structure and feeds it into
          traceability and coverage insights.
        </p>
      </div>

      {/* Category selector */}
      <div className="flex flex-wrap items-center gap-2">
        <span className="eyebrow mr-1">Category</span>
        {CATEGORIES.map((c) => (
          <button
            key={c}
            onClick={() => setDocType(c)}
            className={`px-3 py-1.5 rounded-sm text-sm border transition-colors ${
              docType === c
                ? "border-primary bg-primary/5 text-primary"
                : "border-light-gray text-medium-gray hover:text-charcoal"
            }`}
          >
            {DOC_TYPE_LABELS[c]}
          </button>
        ))}
      </div>

      <div
        {...getRootProps()}
        className={`premium-card rounded-xl p-12 text-center cursor-pointer border-2 border-dashed transition-colors ${
          isDragActive ? "border-primary bg-primary/5" : "border-light-gray"
        }`}
      >
        <input {...getInputProps()} />
        <UploadSimple size={36} weight="regular" className="mx-auto text-primary" />
        <p className="text-charcoal mt-4">
          {isDragActive ? "Drop to upload" : "Drag a file here, or click to browse"}
        </p>
        <p className="text-medium-gray text-sm mt-1">
          Uploading as <span className="text-primary">{DOC_TYPE_LABELS[docType]}</span> · PDF, TXT, or MD · up to 15 MB
        </p>
        {upload.isError && <p className="text-primary text-sm mt-3">{(upload.error as Error).message}</p>}
      </div>

      <div className="space-y-4">
        {docs?.map((d) => (
          <DocumentCard key={d.id} doc={d} onDelete={() => remove.mutate(d.id)} deleting={remove.isPending} />
        ))}
      </div>

      {drift && drift.length > 0 && <RequirementDriftPanel items={drift} />}
    </div>
  )
}

function RequirementDriftPanel({ items }: { items: RequirementDriftItem[] }) {
  return (
    <section className="premium-card rounded-xl p-8 border-l-4 border-l-primary space-y-4">
      <div>
        <p className="eyebrow">Requirement drift</p>
        <h2 className="text-headline-md text-charcoal mt-1">Discussed, but no story yet</h2>
        <p className="text-medium-gray text-sm mt-1">
          Requirements found in a document with no traceable Jira story.
        </p>
      </div>
      <div className="space-y-3">
        {items.map((it) => (
          <div key={it.id} className="rounded-lg border-l-4 border-l-primary bg-background p-5">
            <div className="flex items-start justify-between gap-4">
              <p className="text-charcoal text-sm">{it.text}</p>
              <Badge variant={it.risk === "high" ? "severity-high" : it.risk === "medium" ? "severity-med" : "severity-low"}>
                {it.risk} risk
              </Badge>
            </div>
            <p className="text-xs text-medium-gray mt-2">
              {typeLabel(it.source_type)} · {fmtRelative(it.first_seen_at)}
              {it.estimated_effort_sp != null && ` · ~${it.estimated_effort_sp} SP`}
            </p>
            {it.rationale && <p className="text-xs text-medium-gray mt-1">{it.rationale}</p>}
          </div>
        ))}
      </div>
    </section>
  )
}

const STATUS = {
  uploaded: { icon: CircleNotch, spin: true, variant: "neutral", label: "Uploaded" },
  parsing: { icon: CircleNotch, spin: true, variant: "health-warn", label: "Parsing" },
  analyzing: { icon: CircleNotch, spin: true, variant: "health-warn", label: "Analyzing" },
  complete: { icon: CheckCircle, spin: false, variant: "health-good", label: "Complete" },
  error: { icon: WarningCircle, spin: false, variant: "health-risk", label: "Error" },
} as const

function typeLabel(t: string): string {
  return (DOC_TYPE_LABELS as Record<string, string>)[t] ?? (t === "meeting" ? "Transcript" : "Other")
}

function DocumentCard({ doc, onDelete, deleting }: { doc: DocumentT; onDelete: () => void; deleting: boolean }) {
  const s = STATUS[doc.status]
  const Icon = s.icon
  return (
    <div className="premium-card rounded-xl p-6">
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-3 min-w-0">
          <FileText size={22} weight="regular" className="text-primary shrink-0" />
          <div className="min-w-0">
            <p className="text-charcoal truncate">{doc.filename}</p>
            <p className="text-xs text-medium-gray">{typeLabel(doc.doc_type)} · {fmtRelative(doc.created_at)}</p>
          </div>
        </div>
        <div className="flex items-center gap-3 shrink-0">
          <Badge variant={s.variant}>
            <Icon size={13} className={s.spin ? "animate-spin" : ""} /> {s.label}
          </Badge>
          <button
            onClick={onDelete}
            disabled={deleting}
            title="Delete document"
            className="text-medium-gray hover:text-primary transition-colors disabled:opacity-40"
          >
            <Trash size={17} weight="regular" />
          </button>
        </div>
      </div>

      {doc.status === "error" && <p className="text-sm text-primary mt-4">{doc.error}</p>}

      {doc.status === "complete" && doc.extraction && (
        <Extraction docType={doc.doc_type} extraction={doc.extraction} summary={doc.summary} />
      )}
    </div>
  )
}

function Extraction({
  docType, extraction, summary,
}: {
  docType: string
  extraction: Record<string, unknown>
  summary: string | null
}) {
  const list = (v: unknown): string[] => (Array.isArray(v) ? v.map(String) : [])
  const isTranscript = docType === "transcript" || docType === "meeting"

  return (
    <div className="mt-5 pt-5 border-t border-light-gray space-y-5">
      {summary && <p className="text-medium-gray text-sm">{summary}</p>}

      {docType === "brd" && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Column title="Features" items={list(extraction.features)} />
          <RiskColumn risks={extraction.risks} />
          <Column title="Missing requirements" items={list(extraction.missing_requirements)} />
        </div>
      )}

      {isTranscript && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Column title="Decisions" items={list(extraction.decisions)} />
          <ActionColumn items={extraction.action_items} />
          <Column title="Risks" items={list(extraction.risks)} />
        </div>
      )}

      {docType === "change_request" && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Column title="Requested changes" items={list(extraction.requested_changes)} />
          <Column title="Impacted areas" items={list(extraction.impacted_areas)} />
          <RiskColumn risks={extraction.risks} />
          {typeof extraction.effort_estimate === "string" && (
            <div className="md:col-span-3 text-sm text-medium-gray">
              <span className="eyebrow">Effort estimate</span>
              <p className="mt-1 text-charcoal">{extraction.effort_estimate as string}</p>
            </div>
          )}
        </div>
      )}

      {docType === "other" && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Column title="Key points" items={list(extraction.key_points)} />
          <Column title="Risks" items={list(extraction.risks)} />
        </div>
      )}
    </div>
  )
}

function Column({ title, items }: { title: string; items: string[] }) {
  return (
    <div>
      <p className="eyebrow mb-3">{title}</p>
      <ul className="space-y-2">
        {items.length === 0 && <li className="text-sm text-medium-gray/60">None</li>}
        {items.map((it, i) => (
          <li key={i} className="text-sm text-charcoal"><span className="text-primary">·</span> {it}</li>
        ))}
      </ul>
    </div>
  )
}

function RiskColumn({ risks }: { risks: unknown }) {
  const list = Array.isArray(risks) ? (risks as Array<Record<string, string>>) : []
  return (
    <div>
      <p className="eyebrow mb-3">Risks</p>
      <ul className="space-y-2">
        {list.length === 0 && <li className="text-sm text-medium-gray/60">None</li>}
        {list.map((r, i) => (
          <li key={i} className="text-sm text-charcoal flex items-start gap-2">
            <Badge variant={r.severity === "high" ? "severity-high" : "severity-med"}>{r.severity ?? "risk"}</Badge>
            <span>{r.title ?? String(r)}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}

function ActionColumn({ items }: { items: unknown }) {
  const list = Array.isArray(items) ? (items as Array<Record<string, string>>) : []
  return (
    <div>
      <p className="eyebrow mb-3">Action items</p>
      <ul className="space-y-2">
        {list.length === 0 && <li className="text-sm text-medium-gray/60">None</li>}
        {list.map((a, i) => (
          <li key={i} className="text-sm text-charcoal">
            <span className="text-primary">·</span> {a.item}
            {a.owner && <span className="text-medium-gray"> — {a.owner}</span>}
          </li>
        ))}
      </ul>
    </div>
  )
}
