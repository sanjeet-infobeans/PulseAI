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

export interface UpdateCustomerRequest {
  name?: string
  contact_email?: string | null
  industry?: string | null
  is_active?: boolean
}

export type ProjectStatus = "active" | "on_hold" | "completed"

export type ProjectIndustry = "bfsi" | "sdo" | "media_publishing" | "healthcare" | "ecom"

export const PROJECT_INDUSTRY_LABELS: Record<ProjectIndustry, string> = {
  bfsi: "BFSI",
  sdo: "SDO",
  media_publishing: "Media and Publishing",
  healthcare: "Healthcare",
  ecom: "E-com",
}

export interface Project {
  id: string
  customer_id: string
  name: string
  key: string
  description: string | null
  status: ProjectStatus
  start_date: string | null
  target_end_date: string | null
  industry: ProjectIndustry | null
  total_person_hours: number | null
}

export interface CreateProjectRequest {
  name: string
  key: string
  description?: string | null
  start_date?: string | null
  target_end_date?: string | null
  industry?: ProjectIndustry | null
  total_person_hours?: number | null
}

export interface UpdateProjectRequest {
  name?: string
  description?: string | null
  status?: ProjectStatus
  start_date?: string | null
  target_end_date?: string | null
  industry?: ProjectIndustry | null
  total_person_hours?: number | null
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

export interface ScopedChatSessionT {
  id: string
  title: string
  project_id: string | null
  customer_id: string | null
  industry: string | null
  created_at: string
}

export interface CreateScopedSessionRequest {
  project_id?: string | null
  customer_id?: string | null
  industry?: string | null
  title?: string
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
  weight: number | null
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

export interface PortfolioData {
  projects: Array<{
    project_id: string
    name: string
    customer_name: string
    confidence_score: number | null
    band: "red" | "amber" | "green" | null
    scope_growth_pct: number | null
  }>
  needing_attention_count: number
  most_common_blocker: string | null
  avg_scope_growth_pct: number | null
  highest_risk_customer: string | null
}

export interface ProjectOutcome {
  actual_duration_days: number | null
  actual_velocity_avg: number | null
  defect_density: number | null
  delivered_on_time: boolean | null
  closed_at: string | null
}

export interface WhatIfResult {
  id: string
  scenario_text: string
  estimated_weeks: number | null
  resources_needed: string[]
  risk: "low" | "medium" | "high"
  confidence_delta: number
  summary: string | null
  created_at: string
}

export interface SentimentData {
  current_score: number | null
  trend: "improving" | "steady" | "declining"
  series: number[]
  reasons: string[]
  history_points: number
}

export interface PredictionData {
  predicted_completion_date: string | null
  baseline_target_date: string | null
  probability_on_time: number
  confidence_pct: number
  reasons: string[]
  recommendations: string[]
  created_at: string
}

export interface ScopeCreepData {
  scope_growth_pct: number
  new_stories_added: number
  requirements_tracked: number
  customer_decisions: number
  baseline_points: number | null
  current_points: number | null
  has_baseline: boolean
  risk_level: "low" | "medium" | "high"
  estimated_schedule_impact_weeks: number
  estimated_cost_impact_note: string
  summary: string
}

export interface DecisionSummary {
  avg_delay_days: number | null
  decided_count: number
  pending: Array<{
    topic: string
    requested_by: string | null
    requested_at: string | null
    days_pending: number | null
  }>
  decisions: Array<{
    topic: string
    status: "pending" | "approved" | "rejected"
    source: string
    requested_at: string | null
    decided_at: string | null
    requested_by: string | null
    decided_by: string | null
    sprint_impact_days: number | null
  }>
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
  effort: {
    estimated_hours: number | null
    consumed_hours: number
    remaining_hours: number
    projected_total_hours: number
    done_points: number
    remaining_points: number
    overshoot_pct: number | null
    overshoot_risk: "low" | "medium" | "high" | null
  }
  sprint_panel: {
    active: {
      name: string
      state: string
      committed_points: number
      completed_points: number
      completion_pct: number
    } | null
    carried_forward: Array<{ key: string; title: string; from_sprint_name: string }>
    commitment_trend: number | null
    commitment_trend_sprint_count: number
  }
  risk_cards: RiskCard[]
  recommendations: Array<{ title: string; detail: string; priority: number }>
  executive_summary: string | null
  open_issues: OpenIssue[]
}

export interface ResourceLeave {
  leave_id: string
  leave_type: string
  start_date: string
  end_date: string
  total_days: number
  status: string
}

export interface Resource {
  resource_id: string
  employee_code: string
  name: string
  designation: string
  email: string
  allocation_percentage: number
  billable: boolean
  skills: string[]
  planned_leaves: ResourceLeave[]
}

export interface ResourceSummary {
  total_resources: number
  active_resources: number
  resources_on_leave_today: number
  planned_leaves_next_30_days: number
  total_planned_leave_days: number
}

export interface ResourcesData {
  resources: Resource[]
  summary: ResourceSummary
}

export interface CreateResourceRequest {
  name: string
  employee_code?: string | null
  designation?: string | null
  email?: string | null
  allocation_percentage?: number
  billable?: boolean
  skills?: string[]
}

export interface UpdateResourceRequest {
  name?: string
  employee_code?: string | null
  designation?: string | null
  email?: string | null
  allocation_percentage?: number
  billable?: boolean
  skills?: string[]
}

export interface CreateLeaveRequest {
  leave_type: string
  start_date: string
  end_date: string
  total_days: number
  status?: string
}

export interface UpdateLeaveRequest {
  leave_type?: string
  start_date?: string
  end_date?: string
  total_days?: number
  status?: string
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

export type RiskSeverity = "low" | "medium" | "high"
export type RiskStatus = "active" | "mitigated" | "closed"

export interface RiskItemT {
  id: string
  title: string
  description: string | null
  severity: RiskSeverity
  status: RiskStatus
  last_seen_at: string
}

export type ActionItemStatus = "open" | "done"

export interface ActionItemT {
  id: string
  item: string
  status: ActionItemStatus
  created_at: string
}

export interface ActionItemsSummary {
  open_count: number
  done_count: number
  by_owner: Record<string, ActionItemT[]>
}
