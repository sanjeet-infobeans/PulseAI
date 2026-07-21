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
        "momentum, and the one thing leadership should focus on. 3-4 short paragraphs."
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

# For risk/recommendations we also want structured output for the UI.
_JSON_SCHEMA_HINT = {
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


_DOC_TASK = {
    "brd": (
        'Analyze this Business Requirements Document. Return strict JSON: '
        '{"summary":str,"features":[str],"risks":[{"title":str,"severity":"high|medium|low"}],'
        '"missing_requirements":[str]}'
    ),
    "transcript": (
        'Analyze this meeting transcript. Return strict JSON: '
        '{"summary":str,"decisions":[str],"action_items":[{"owner":str,"item":str}],"risks":[str]}'
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
