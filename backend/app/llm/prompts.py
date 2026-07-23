"""Prompt builders. System prompt frames PulseAI as a delivery-intelligence
analyst for an executive/director audience; user prompts carry compact JSON context.
"""
import json

from app.models.ai_analysis import AnalysisKind

SYSTEM = (
    "You are PulseAI, a project delivery-intelligence analyst for InfoBeans. "
    "Your audience is executives and delivery directors. Be outcome-first, direct, and specific. "
    "Ground every statement in the delivery data provided. Do not invent metrics. "
    "Write in clear prose with short markdown sections; no hyperbole."
)

_ANALYSIS_TASK = {
    AnalysisKind.executive: (
        "Write a concise executive summary of delivery health: where the project stands, "
        "momentum, and the one thing leadership should focus on. If `confidence_trend` or "
        "`scope_change_pct` are present in the data, reference the direction of movement "
        "explicitly (e.g. confidence rising/falling, scope growing). 3-4 short paragraphs."
    ),
    AnalysisKind.sprint: (
        "Analyze the current/most-recent sprint: scope vs completion, notable movement, and "
        "whether the sprint goal is on track. Reference specific numbers."
    ),
    AnalysisKind.risk: (
        "Identify the top delivery risks. Return concrete, evidence-backed risks with severity."
    ),
    AnalysisKind.recommendations: (
        "Give 3-5 prioritized, actionable recommendations to improve delivery confidence."
    ),
}

# For risk/recommendations/executive we also want structured output for the UI.
_JSON_SCHEMA_HINT = {
    AnalysisKind.executive: (
        'Also return strict JSON: {"stories_completed":int,"stories_blocked":int,'
        '"customer_risk":"low|medium|high","scope_change_pct":number,"confidence_pct":number,'
        '"intervention_needed":bool,"intervention_reason":str}. Use `confidence_trend`/'
        '`scope_change_pct` from the data if present; otherwise infer conservatively from '
        '`totals`/`blockers`. Set intervention_needed=true only for material risk (e.g. '
        "confidence dropping into red/amber, blockers piling up, scope growing >15%)."
    ),
    AnalysisKind.risk: (
        'Also return strict JSON: {"risks":[{"title":str,"severity":"high|medium|low",'
        '"impact":str,"evidence":str}]}'
    ),
    AnalysisKind.recommendations: (
        'Also return strict JSON: {"recommendations":[{"title":str,"detail":str,"priority":int}]}'
    ),
}


def analysis_messages(kind: AnalysisKind, context: dict) -> list[dict]:
    task = _ANALYSIS_TASK[kind]
    return [
        {"role": "system", "content": SYSTEM},
        {
            "role": "user",
            "content": (
                f"Delivery data (JSON):\n{json.dumps(context, indent=2, default=str)}\n\n"
                f"Task: {task}"
            ),
        },
    ]


def analysis_json_messages(kind: AnalysisKind, context: dict) -> list[dict] | None:
    """Second, JSON-only pass for kinds that populate structured UI (risk/recs)."""
    hint = _JSON_SCHEMA_HINT.get(kind)
    if not hint:
        return None
    return [
        {"role": "system", "content": SYSTEM + " Respond with strict JSON only."},
        {
            "role": "user",
            "content": f"Delivery data (JSON):\n{json.dumps(context, default=str)}\n\n{hint}",
        },
    ]


CHAT_CAPABILITIES = (
    " You have both the Jira delivery data and the analyzed documents (BRDs, transcripts, change "
    "requests) in `documents`, each with a `requirements` list. You can:\n"
    "- Build a REQUIREMENT TRACEABILITY MATRIX: map each documented requirement to the current-sprint "
    "story(ies) that implement it (match by meaning, not exact words). Render as a markdown table with "
    "columns: Requirement | Source doc | Sprint story (key) | Status. Mark unmatched requirements as "
    "'Not in sprint'.\n"
    "- Report BRD COVERAGE %: of the BRD's requirements, how many are traceable to a current-sprint "
    "story. Give the fraction and percentage, and list the uncovered ones.\n"
    "- Flag OUT-OF-SCOPE items: current-sprint stories that do NOT correspond to any requirement in any "
    "uploaded document — these are risks/scope-creep. List their keys and titles.\n"
    "When you cite a story, use its key (e.g. CLEAR-12). If no documents are available, say so plainly. "
    "Keep answers tight and evidence-based."
)


def chat_messages(context: dict, history: list[dict], question: str) -> list[dict]:
    msgs = [
        {"role": "system", "content": SYSTEM + CHAT_CAPABILITIES},
        {"role": "user", "content": f"Delivery data + documents (JSON):\n{json.dumps(context, default=str)}"},
    ]
    msgs.extend(history)
    msgs.append({"role": "user", "content": question})
    return msgs


def alignment_messages(context: dict) -> list[dict]:
    return [
        {"role": "system", "content": (
            SYSTEM + " You validate delivery against the requirements knowledge base. "
            "The `documents` are the source of truth (BRDs, transcripts, change requests), each with a "
            "`requirements` list. `all_stories` is every Jira story in the project. Match by meaning. "
            "Respond with strict JSON only."
        )},
        {"role": "user", "content": (
            f"Data (JSON):\n{json.dumps(context, default=str)}\n\n"
            "Assess how well the delivered/planned stories align to the documented requirements. "
            'Return strict JSON: {'
            '"requirement_coverage_pct": number (0-100, share of documented requirements traceable to a story), '
            '"story_alignment_pct": number (0-100, share of stories that trace to a documented requirement), '
            '"unmapped_requirements": [string] (documented requirements with no story), '
            '"out_of_scope_stories": [{"key": string, "title": string}] (stories with no documented requirement), '
            '"summary": string (one sentence)}'
        )},
    ]


def confidence_judge_messages(context: dict, signals: list[dict], rule_score: float) -> list[dict]:
    return [
        {"role": "system", "content": (
            SYSTEM + " You are acting as a delivery-confidence judge. Respond with strict JSON only."
        )},
        {"role": "user", "content": (
            f"Delivery data:\n{json.dumps(context, default=str)}\n\n"
            f"Rule-based signals:\n{json.dumps(signals, default=str)}\n"
            f"Rule score: {rule_score}\n\n"
            'Assess overall delivery confidence 0-100 considering these signals and the narrative. '
            'Return strict JSON: {"judge_score": number, "rationale": string}'
        )},
    ]


def dependency_messages(context: dict, simulated: dict) -> list[dict]:
    """Hidden Dependency Detection (#4): infer chains like "Story(Payment
    Gateway) depends_on Story/topic(Tax API) which blocks QA/release" by
    reading across stories, documents, and Teams/Slack decisions — links a
    human would otherwise have to notice manually across separate tools."""
    return [
        {"role": "system", "content": (
            SYSTEM + " Infer hidden delivery dependencies by connecting stories, blockers, documented "
            "decisions, and simulated Teams/Slack signals. Only report dependencies with reasonable "
            "textual evidence — do not invent connections. Respond with strict JSON only."
        )},
        {"role": "user", "content": (
            f"Delivery data (JSON):\n{json.dumps(context, default=str)}\n\n"
            f"Simulated Teams/Slack signals (JSON):\n{json.dumps(simulated, default=str)}\n\n"
            'Return strict JSON: {"edges": [{"from_type": string (e.g. "story","doc","decision"), '
            '"from_ref": string (a story key, doc filename, or short topic label), '
            '"to_type": string, "to_ref": string, '
            '"relation": "blocks|depends_on|mentioned_in|derived_from|impacts", '
            '"confidence": number (0-1), "rationale": string (1 sentence, cite the evidence)}]}'
        )},
    ]


def requirement_match_messages(requirement_texts: list[dict], all_stories: list[dict]) -> list[dict]:
    """Requirement Drift Detection (#3): match each catalog requirement to a
    story by meaning (same semantic-match approach alignment_service.py
    already uses), so unmatched ones can be flagged as missing."""
    return [
        {"role": "system", "content": (
            SYSTEM + " Match each requirement to the Jira story (if any) that implements it, by "
            "meaning, not exact words. Respond with strict JSON only."
        )},
        {"role": "user", "content": (
            f"Requirements (JSON, each has an id):\n{json.dumps(requirement_texts, default=str)}\n\n"
            f"Jira stories (JSON):\n{json.dumps(all_stories, default=str)}\n\n"
            'Return strict JSON: {"matches": [{"id": string, "matched_story_keys": [string]}]} '
            "— one entry per requirement id given, matched_story_keys empty if nothing implements it."
        )},
    ]


def requirement_drift_messages(missing_items: list[dict]) -> list[dict]:
    """For requirements with no matching story: estimate effort/risk so the
    drift panel can show "MFA discussed, no Epic, no Story, 8 SP, High risk"-
    style output. Only called for the (typically small) missing subset."""
    return [
        {"role": "system", "content": (
            SYSTEM + " Estimate delivery effort and risk for requirements that have no Jira story yet. "
            "Respond with strict JSON only."
        )},
        {"role": "user", "content": (
            f"Requirements with no matching story (JSON, each has an id/text/source_type):\n"
            f"{json.dumps(missing_items, default=str)}\n\n"
            'Return strict JSON: {"items": [{"id": string, "estimated_effort_sp": number, '
            '"risk": "high|medium|low", "rationale": string (1 sentence)}]}'
        )},
    ]


def resource_risk_messages(resource_payload: dict, sole_holder_modules: list[dict]) -> list[dict]:
    """Resource Risk (#7) + Knowledge Gap Detection (#12): one LLM pass turns
    the simulated resource payload's per-developer utilization plus the
    rule-computed knowledge-concentration (sole-holder modules) into concrete
    cross-training / KT recommendations."""
    return [
        {"role": "system", "content": (
            SYSTEM + " You assess team capacity/burnout risk and knowledge-concentration risk. "
            "Respond with strict JSON only."
        )},
        {"role": "user", "content": (
            f"Resource data (JSON):\n{json.dumps(resource_payload, default=str)}\n\n"
            f"Modules with a single knowledge holder (JSON):\n{json.dumps(sole_holder_modules, default=str)}\n\n"
            "Return strict JSON: {"
            '"burnout_risk": "low|medium|high", '
            '"burnout_reason": string (1-2 sentences, reference specific developers/utilization %), '
            '"recommendations": [string] (concrete actions: cross-training, KT sessions, recorded '
            'walkthroughs, secondary owners — reference specific modules/developers by name)}'
        )},
    ]


_RISK_AGENT_PERSONA = (
    "You are the Risk Identifier agent for PulseAI: a PMP-certified, Agile/SAFe practitioner "
    "with over 12 years of experience delivering IT projects. You scan project documentation, "
    "meeting transcripts, and live sprint/delivery signals to surface concrete, evidence-backed "
    "delivery risks — the kind a seasoned delivery director would flag in a steering committee. "
    "Be specific: name the document, story, or signal that triggered each risk. Do not invent "
    "risks with no evidence. Respond with strict JSON only."
)


def risk_identification_messages(context: dict, existing_active_risks: list[dict]) -> list[dict]:
    """Risk identifier agent: scans the same delivery context (documents +
    sprint/story signal, see retrieval.build_context) already used elsewhere,
    upserted by risk_service.py into a persisted, active/mitigated/closed
    registry — not a fresh unlinked list per generation like AnalysisKind.risk."""
    return [
        {"role": "system", "content": _RISK_AGENT_PERSONA},
        {"role": "user", "content": (
            f"Delivery data + documents (JSON):\n{json.dumps(context, default=str)}\n\n"
            "Currently-tracked ACTIVE risks (JSON) — do not re-report these unless materially "
            f"changed, and explicitly say if any of these appear resolved based on the current data:\n"
            f"{json.dumps(existing_active_risks, default=str)}\n\n"
            "Return strict JSON: {"
            '"risks": [{"title": string, "description": string (1-3 sentences, evidence-backed), '
            '"severity": "low|medium|high", "source_hint": string (which document/signal this came '
            'from)}], "resolved_titles": [string] (titles from the currently-tracked list above that '
            "the current data suggests are no longer live risks)}"
        )},
    ]


def judge_review_messages(analysis_kind: str, analysis_content: str, analysis_structured: dict, context: dict) -> list[dict]:
    """AI Judge (#10): a second-pass critique of an existing AIAnalysis row —
    does it hold up against the delivery data, what did it miss. Same
    judge-pattern as confidence_judge_messages, applied to analyses."""
    return [
        {"role": "system", "content": (
            SYSTEM + " You are auditing another AI-generated analysis for coverage and accuracy "
            "against the underlying delivery data. Be skeptical — find what it missed or got wrong. "
            "Respond with strict JSON only."
        )},
        {"role": "user", "content": (
            f"Delivery data (JSON):\n{json.dumps(context, default=str)}\n\n"
            f"Analysis under review (kind={analysis_kind}):\n{analysis_content}\n\n"
            f"Its structured output:\n{json.dumps(analysis_structured, default=str)}\n\n"
            "Assess how well this analysis covers the delivery data. Return strict JSON: "
            '{"coverage_pct": number (0-100, how much of the relevant delivery data the analysis '
            'actually addresses), "missing_risks_count": number (material risks visible in the data '
            'but absent from the analysis), "missing_stories_count": number (stories/blockers relevant '
            'to the analysis topic but not mentioned), "confidence_pct": number (0-100, your confidence '
            'that the analysis\'s conclusions are correct), "notes": string (1-3 sentences on what, '
            'specifically, is missing or wrong)}'
        )},
    ]


def completion_prediction_messages(context: dict, rule_projection: dict, signals: list[dict]) -> list[dict]:
    """Delivery Completion Prediction (#1): same rule+LLM-judge blend pattern
    as confidence_service.py — the rule side already computed a projected
    date from velocity trend; the LLM reasons about probability/likely
    causes/recommendations on top of that projection."""
    return [
        {"role": "system", "content": (
            SYSTEM + " You assess whether a project will hit its target delivery date, given a "
            "rule-based velocity projection. Respond with strict JSON only."
        )},
        {"role": "user", "content": (
            f"Delivery data (JSON):\n{json.dumps(context, default=str)}\n\n"
            f"Rule-based projection (JSON):\n{json.dumps(rule_projection, default=str)}\n\n"
            f"Signals (JSON):\n{json.dumps(signals, default=str)}\n\n"
            'Return strict JSON: {"probability_on_time": number (0-100), '
            '"reasons": [string] (2-4 concrete reasons, cite numbers), '
            '"recommendations": [string] (1-3 concrete actions to protect the date)}'
        )},
    ]


def scope_creep_messages(context: dict, scope_metrics: dict) -> list[dict]:
    """Scope Creep Detection (#2): turn the measured scope-growth signals
    (story/point deltas since baseline, new requirements, customer decisions)
    into an estimated schedule/cost impact. The metrics themselves are
    computed, not invented — only the impact estimate is LLM reasoning."""
    return [
        {"role": "system", "content": (
            SYSTEM + " You estimate the schedule and cost impact of measured scope growth. Be "
            "conservative and explicit that these are estimates. Respond with strict JSON only."
        )},
        {"role": "user", "content": (
            f"Delivery data (JSON):\n{json.dumps(context, default=str)}\n\n"
            f"Measured scope-growth metrics (JSON):\n{json.dumps(scope_metrics, default=str)}\n\n"
            'Return strict JSON: {"risk_level": "low|medium|high", '
            '"estimated_schedule_impact_weeks": number, "estimated_cost_impact_note": string '
            '(a rough estimate framed in relative terms, e.g. "~2-3 additional sprints of effort" — '
            "do not invent a specific currency figure), "
            '"summary": string (1-2 sentences)}'
        )},
    ]


def sentiment_analysis_messages(context: dict, sentiment_trend: list[dict], simulated: dict) -> list[dict]:
    """Stakeholder Sentiment (#13): reasons over the trend (from
    metric_snapshots, refreshed nightly by simulated_refresh_service) plus
    Teams/Slack simulated highlights and transcript decisions, rather than
    just echoing the static seeded `note` field."""
    return [
        {"role": "system", "content": (
            SYSTEM + " You analyze stakeholder sentiment trend and explain what's driving it. "
            "Respond with strict JSON only."
        )},
        {"role": "user", "content": (
            f"Delivery data (JSON):\n{json.dumps(context, default=str)}\n\n"
            f"Sentiment score history, oldest to newest (JSON):\n{json.dumps(sentiment_trend, default=str)}\n\n"
            f"Simulated Teams/Slack signals (JSON):\n{json.dumps(simulated, default=str)}\n\n"
            'Return strict JSON: {"trend": "improving|steady|declining", '
            '"reasons": [string] (concrete, e.g. delayed approvals, repeated bug discussion, '
            'escalation keywords, blockers) — empty list if genuinely steady with no notable driver}'
        )},
    ]


def what_if_messages(
    context: dict, baseline_confidence: dict | None, baseline_prediction: dict | None, scenario_text: str
) -> list[dict]:
    """What-If Simulation (#14): LLM-only reasoning (no solver/optimizer) —
    estimate the delta a hypothetical scope change would have against the
    project's current baseline confidence/prediction."""
    return [
        {"role": "system", "content": (
            SYSTEM + " A stakeholder is asking a what-if question about adding scope. Estimate the "
            "impact against the given baseline. Be conservative and explicit these are estimates, "
            "grounded in the team's current velocity/confidence, not invented precision. "
            "Respond with strict JSON only."
        )},
        {"role": "user", "content": (
            f"Delivery data (JSON):\n{json.dumps(context, default=str)}\n\n"
            f"Baseline confidence (JSON, may be null):\n{json.dumps(baseline_confidence, default=str)}\n\n"
            f"Baseline delivery prediction (JSON, may be null):\n{json.dumps(baseline_prediction, default=str)}\n\n"
            f"Scenario: {scenario_text}\n\n"
            'Return strict JSON: {"estimated_weeks": number, "estimated_resources": [string] '
            '(e.g. "1 Backend developer"), "risk": "low|medium|high", '
            '"confidence_delta": number (negative if this scenario would lower delivery confidence), '
            '"summary": string (2-3 sentences)}'
        )},
    ]


_DOC_TASK = {
    "brd": (
        'Analyze this Business Requirements Document. Return strict JSON: '
        '{"summary":str,"features":[str],"risks":[{"title":str,"severity":"high|medium|low"}],'
        '"missing_requirements":[str]}'
    ),
    "transcript": (
        'Analyze this meeting transcript. Return strict JSON: '
        '{"summary":str,"decisions":[str],"action_items":[{"owner":str,"item":str}],"risks":[str],'
        '"decision_events":[{"topic":str,"requested_at":str|null,"decided_at":str|null,'
        '"status":"pending|approved|rejected","requested_by":str|null,"decided_by":str|null}]}. '
        "decision_events is for customer/stakeholder decisions specifically (not internal team choices) "
        "— include dates only if explicitly mentioned in the transcript (ISO format), else null."
    ),
    "change_request": (
        'Analyze this change request. Return strict JSON: '
        '{"summary":str,"requested_changes":[str],"impacted_areas":[str],'
        '"risks":[{"title":str,"severity":"high|medium|low"}],"effort_estimate":str}'
    ),
    "other": (
        'Summarize this document. Return strict JSON: '
        '{"summary":str,"key_points":[str],"risks":[str]}'
    ),
    "meeting": (  # legacy alias
        'Analyze this meeting transcript. Return strict JSON: '
        '{"summary":str,"decisions":[str],"action_items":[{"owner":str,"item":str}],"risks":[str]}'
    ),
}


def document_messages(doc_type: str, text: str) -> list[dict]:
    task = _DOC_TASK.get(doc_type, _DOC_TASK["other"])
    return [
        {"role": "system", "content": SYSTEM + " Respond with strict JSON only."},
        {"role": "user", "content": f"{task}\n\nDocument:\n\"\"\"\n{text[:20000]}\n\"\"\""},
    ]
