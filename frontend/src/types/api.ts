export type UserRole = "super_admin" | "customer"

export interface TokenOut {
  token: string
}

export interface MeOut {
  id: string
  email: string
  name: string
  role: UserRole
  customer_id: string | null
  org_id: string
}

export interface Customer {
  id: string
  name: string
  slug: string
  contact_email: string | null
  industry: string | null
  is_active: boolean
}

export interface CreateCustomerRequest {
  name: string
  contact_email?: string | null
  industry?: string | null
}

export type ProjectStatus = "active" | "on_hold" | "completed"

export interface Project {
  id: string
  customer_id: string
  name: string
  key: string
  description: string | null
  status: ProjectStatus
  start_date: string | null
  target_end_date: string | null
}

export interface CreateProjectRequest {
  name: string
  key: string
  description?: string | null
  start_date?: string | null
  target_end_date?: string | null
}

// ── Connectors (Week 2) ──────────────────────────────────────────────────
export type ConnectorType =
  | "jira" | "teams" | "slack" | "clickup" | "asana" | "trello"
  | "resource" | "budget" | "timeline" | "sentiment"
export type ConnectorMode = "real" | "simulated"
export type ConnectorStatus = "unconfigured" | "connected" | "syncing" | "error"

export interface Connector {
  id: string
  project_id: string
  type: ConnectorType
  mode: ConnectorMode
  status: ConnectorStatus
  config: Record<string, unknown>
  secret_ref: string | null
  last_synced_at: string | null
  last_error: string | null
}

export interface JiraConfig {
  base_url: string
  project_key: string
  board_id: string
  story_point_field?: string
}

export interface SyncResult {
  status: string
  connector_id: string
}

export type SprintState = "future" | "active" | "closed"

export interface Sprint {
  id: string
  external_id: string
  name: string
  state: SprintState
  goal: string | null
  start_date: string | null
  end_date: string | null
  committed_points: number
  completed_points: number
}

export type AnalysisKind = "executive" | "sprint" | "risk" | "recommendations"

export interface Analysis {
  id: string
  kind: AnalysisKind
  content: string
  structured: Record<string, unknown>
  generated_by: string | null
  created_at: string
}

export interface JudgeReview {
  id: string
  analysis_id: string
  coverage_pct: number
  missing_risks_count: number
  missing_stories_count: number
  confidence_pct: number
  notes: string | null
  created_at: string
}

export interface ChatSessionT {
  id: string
  title: string
  created_at: string
}

export interface Citation {
  type: string
  ref: string
  label: string
}

export interface ChatMessageT {
  id: string
  role: "user" | "assistant" | "system"
  content: string
  citations: Citation[]
  created_at: string
}

export type DocStatusT = "uploaded" | "parsing" | "analyzing" | "complete" | "error"

export type DocTypeT = "brd" | "transcript" | "change_request" | "other"

export const DOC_TYPE_LABELS: Record<DocTypeT, string> = {
  brd: "BRD",
  transcript: "Transcript",
  change_request: "Change Request",
  other: "Other",
}

export interface DocumentT {
  id: string
  filename: string
  doc_type: DocTypeT | "meeting"
  status: DocStatusT
  error: string | null
  extraction: Record<string, unknown> | null
  summary: string | null
  created_at: string
}

export type StatusCategory = "todo" | "in_progress" | "blocked" | "in_review" | "done"

export interface ConfidenceSignal {
  name: string
  value: number
  weight: number
  contribution: number
}

export type ConfidenceCategory =
  | "requirement"
  | "engineering"
  | "testing"
  | "dependencies"
  | "resource"
  | "customer"

export interface ConfidenceData {
  score: number
  band: "red" | "amber" | "green"
  rule_score: number
  judge_score: number
  signals: ConfidenceSignal[]
  sub_scores: Partial<Record<ConfidenceCategory, number | null>> | null
  rationale: string | null
}

export interface RiskCard {
  title: string
  severity: "high" | "medium" | "low"
  impact?: string
  evidence?: string
}

export interface OpenIssue {
  key: string
  title: string
  assignee: string | null
  status: string | null
  priority: string | null
}

export interface AlignmentData {
  has_knowledge_base: boolean
  requirement_coverage_pct: number | null
  story_alignment_pct: number | null
  unmapped_requirements: string[]
  out_of_scope_stories: Array<{ key: string; title: string }>
  summary: string
}

export interface DependencyEdgeT {
  id: string
  from_type: string
  from_ref: string
  to_type: string
  to_ref: string
  relation: "blocks" | "depends_on" | "mentioned_in" | "derived_from" | "impacts"
  confidence: number
  rationale: string | null
  detected_at: string
}

export interface RequirementDriftItem {
  id: string
  text: string
  source_type: string
  first_seen_at: string
  estimated_effort_sp: number | null
  risk: "high" | "medium" | "low"
  rationale: string
}

export interface DeveloperResource {
  name: string
  skill: string
  experience_yrs: number
  availability_pct: number
  utilization_pct: number
}

export interface KnowledgeMapRow {
  module: string
  developer: string
  story_count: number
  is_sole_holder: boolean
}

export interface ResourceRiskData {
  team_size: number | null
  team_utilization_pct: number | null
  developers: DeveloperResource[]
  knowledge_concentration: KnowledgeMapRow[]
  sole_holder_modules: Array<{ module: string; developer: string; story_count: number }>
  burnout_risk: "low" | "medium" | "high"
  burnout_reason: string
  recommendations: string[]
}

export interface DashboardData {
  health: number
  confidence: ConfidenceData | null
  sprint_progress: {
    name: string
    state: string
    committed_points: number
    completed_points: number
    completion_pct: number
  } | null
  status_counts: Partial<Record<StatusCategory, number>>
  totals: { stories: number; done: number; completion_pct: number }
  timeline: Array<{ name: string; state: string; completion_pct: number }>
  risk_cards: RiskCard[]
  recommendations: Array<{ title: string; detail: string; priority: number }>
  executive_summary: string | null
  open_issues: OpenIssue[]
}

export interface Story {
  id: string
  external_id: string
  title: string
  issue_type: string
  status_category: StatusCategory
  raw_status: string | null
  story_points: number | null
  assignee: string | null
  priority: string | null
  is_blocked: boolean
}
