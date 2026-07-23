# Business Requirements Document (BRD)
## Claims Management & Processing Platform — Claims Management & Processing Platform

### Document Control

| Field | Value |
| --- | --- |
| Document Title | BRD — Claims Management & Processing Platform |
| Project Key (Jira) | `CLAIMS` |
| Jira Project URL | https://pulseaipoc.atlassian.net/jira/software/projects/CLAIMS/boards |
| Version | 1.0 |
| Status | Baselined |
| Date | 22 Jul 2026 |
| Author | Delivery / Product Team |
| Delivery Methodology | Agile (Scrum) — 2-week sprints |
| Industry Domain | Insurance |

## 1. Executive Summary

Provide an end-to-end claims platform that delivers fast, fair, and accurate claim outcomes — from omni-channel FNOL through triage, adjudication, estimation, payment, subrogation, and recovery — with strong fraud controls, tight reserve discipline, and a transparent, empathetic customer experience.

This document defines the business requirements, scope, objectives, and agile delivery plan. Delivery is organised into **14 epics** and **210 user stories**, executed across **9 completed sprints**, **1 upcoming sprint**, and a maintained backlog, aligned to **5 release milestones**. Delivery reflects realistic team dynamics: velocity varies sprint to sprint and 10–20% of committed work carries over between sprints.

## 2. Business Context & Problem Statement

Claims are handled across fragmented tools with manual triage, inconsistent decisioning, limited fraud detection, and poor claimant visibility. This drives high loss-adjustment expense, claims leakage, long cycle times, and low customer satisfaction — especially during catastrophe surges.

## 3. Business Objectives

1. Reduce average claim cycle time by 30% through automation and triage.
2. Cut claims leakage by 15% via better coverage validation and estimation.
3. Improve fraud detection savings through scoring and SIU workflows.
4. Raise claimant satisfaction (CSAT) by 20% with self-service and proactive updates.
5. Scale elastically to handle catastrophe (CAT) surge volumes.

## 4. Success Metrics & KPIs

| Metric | Target |
| --- | --- |
| Average claim cycle time | -30% vs baseline |
| Claims leakage | -15% |
| Fraud detection savings | Increase per cycle |
| Claimant CSAT / NPS | +20% |
| Straight-through settlement (simple claims) | > 40% |
| Reserve accuracy (development) | Within target tolerance |

## 5. Stakeholders & Personas

| Persona / Stakeholder | Role & Needs |
| --- | --- |
| Claimant / Policyholder | Reports and tracks claims; expects speed and transparency. |
| Claims Adjuster | Investigates, decides, and settles claims. |
| Claims Supervisor | Assigns work, approves authority, and monitors SLAs. |
| SIU Investigator | Investigates suspected fraud. |
| Vendor / Repair Provider | Performs repairs and submits invoices. |
| Finance / Actuary | Manages reserves and loss financials. |
| Compliance / Legal | Ensures fair-claims practices and handles litigation. |

## 6. Scope

### 6.1 In Scope

- Omni-channel FNOL intake and claim registration
- Triage, segmentation, and adjuster assignment
- Adjudication, coverage verification, and decisioning
- Investigation, fraud detection, and SIU workflows
- Damage estimation, payments, and settlements
- Subrogation, salvage, and recovery
- Reserves and claim financials
- Vendor network, customer communication, compliance, analytics, and platform

### 6.2 Out of Scope

- Policy administration and underwriting (covered by the PAS platform)
- General-ledger / core accounting (integration only)
- Reinsurance treaty administration (policy-side; recoverables interface only)
- Medical bill repricing engine (integration only)

## 7. Assumptions, Constraints & Dependencies

### 7.1 Assumptions

- Policy and coverage data are available from the PAS platform.
- A cloud-native environment with autoscaling is available.
- Estimating and third-party data integrations are contracted.
- Identity is provided by the enterprise IdP via SSO.

### 7.2 Constraints

- Must comply with fair-claims-practices and statutory deadlines.
- Must maintain complete audit trails for every claim action.
- Must scale elastically for catastrophe surge events.

### 7.3 Dependencies

- Policy administration system (coverage/policy data)
- Estimating platforms and third-party claim data (ISO, etc.)
- Payment disbursement and banking integrations
- Vendor/provider network integrations

## 8. Product Roadmap & Milestones

| Milestone / Release | Theme | Target Date | Status |
| --- | --- | --- | --- |
| R1 – Foundation & MVP | Core platform foundation, environments, and MVP capabilities. | 18 Mar 2026 | Released |
| R2 – Core Experience | Primary end-user experience and workflows go live. | 15 Apr 2026 | Released |
| R3 – Scale & Automate | Scaling, automation, and straight-through processing. | 13 May 2026 | Released |
| R4 – Optimize & Expand | Optimization, analytics, and platform expansion. | 10 Jun 2026 | Released |
| R5 – GA & Hardening | General availability, compliance, and reliability hardening. | 08 Jul 2026 | Released |

## 9. Agile Delivery Approach

- **Framework:** Scrum with 2-week sprints and a prioritised product backlog.
- **Ceremonies:** Sprint Planning, Daily Stand-up, Sprint Review, Retrospective, Backlog Refinement.
- **Estimation:** Story points on a modified Fibonacci scale (1, 2, 3, 5, 8, 13), estimated **before** the sprint starts.
- **Sequencing:** A sprint starts only after the previous one closes.
- **Realistic delivery:** Not all committed work completes each sprint; **10–20% carries over** to the next sprint, and velocity fluctuates (ramp-up, a mid-plan dip, and recovery). Jira **burndown charts** show work completed progressively across each sprint, and the **velocity report** shows the sprint-by-sprint completed points below.

### 9.1 Backlog Distribution

| Category | Stories | % of Total | Estimated? | State |
| --- | --- | --- | --- | --- |
| Committed to completed sprints | 168 | 80% | Yes | 9 closed sprints |
| Upcoming (planned) sprint | 21 | 10% | Yes | 1 future sprint |
| Product backlog (unplanned) | 21 | 10% | No (not estimated) | No sprint |
| **Total** | 210 | 100% | — | 10 sprints + backlog |

### 9.2 Sprint Plan, Velocity & Carryover

The table below reflects the actual delivery recorded in Jira. **Committed** = story points brought into the sprint (new commitment + carried-in). **Completed** = points delivered (the velocity). **Carried-out** = work not finished, moved to the next sprint.

| Sprint | Dates (planned) | Committed (pts) | Completed (pts) | Carried-out | Completion % | Release | State |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Sprint 1 | 18 Mar–31 Mar | 86+0=86 | 71 | 15 | 83% | R1 | Closed |
| Sprint 2 | 01 Apr–14 Apr | 81+15=96 | 78 | 18 | 81% | R1 | Closed |
| Sprint 3 | 15 Apr–28 Apr | 84+18=102 | 89 | 13 | 87% | R2 | Closed |
| Sprint 4 | 29 Apr–12 May | 87+13=100 | 74 | 26 | 74% | R2 | Closed |
| Sprint 5 | 13 May–26 May | 86+26=112 | 63 | 49 | 56% | R3 | Closed |
| Sprint 6 | 27 May–09 Jun | 84+49=133 | 84 | 49 | 63% | R3 | Closed |
| Sprint 7 | 10 Jun–23 Jun | 84+49=133 | 99 | 34 | 74% | R4 | Closed |
| Sprint 8 | 24 Jun–07 Jul | 68+34=102 | 76 | 26 | 75% | R4 | Closed |
| Sprint 9 | 08 Jul–21 Jul | 76+26=102 | 97 | 5 | 95% | R5 | Closed |
| Sprint 10 | 22 Jul–04 Aug | 94 (+1 carried) | — | — | — | R5 | Upcoming |
| Backlog | Unscheduled | not estimated | — | — | — | — | Backlog |

> **Velocity curve (completed pts/sprint):** 71, 78, 89, 74, 63, 84, 99, 76, 97  
> Average delivered velocity **~81 pts/sprint** over 9 sprints (731 pts / 167 stories delivered; 1 story carried into the current sprint).  
> *Note: sprints were executed in Jira as a compressed live simulation so that burndown charts render genuine descending curves; Jira sprint timestamps reflect that execution window rather than calendar fortnights.*

## 10. Epics & User Stories

The scope is decomposed into 14 epics. Story IDs are the live Jira issue keys. **Committed Sprint** is where a story was first planned; **Completed Sprint** is where it was actually delivered (they differ when work carried over).

### 10.1 Epic 1: Claims Intake & FNOL  `CLAIMS-1`

**Objective:** First Notice of Loss capture.  
**Stories:** 15 · **Estimated points:** 68

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| CLAIMS-15 | Build omni-channel FNOL intake (web, phone, app) | 1 | 1 | 1 | Done |
| CLAIMS-16 | Implement guided loss-report wizard | 2 | 1 | 1 | Done |
| CLAIMS-17 | Add photo and document upload at intake | 2 | 1 | 1 | Done |
| CLAIMS-18 | Support policy lookup and coverage prefill | 3 | 1 | 1 | Done |
| CLAIMS-19 | Implement duplicate claim detection at intake | 3 | 1 | 1 | Done |
| CLAIMS-20 | Add loss location and geocoding capture | 3 | 1 | 1 | Done |
| CLAIMS-21 | Support third-party (agent/adjuster) FNOL entry | 5 | 1 | 1 | Done |
| CLAIMS-22 | Implement claim number generation | 5 | 1 | 1 | Done |
| CLAIMS-23 | Add save-and-resume for incomplete FNOL | 5 | 1 | 1 | Done |
| CLAIMS-24 | Support voice-to-text loss description | 8 | 1 | 1 | Done |
| CLAIMS-25 | Implement immediate acknowledgement to claimant | 8 | 1 | 1 | Done |
| CLAIMS-26 | Add catastrophe (CAT) event tagging | 13 | 1 | 1 | Done |
| CLAIMS-27 | Support FNOL via partner integrations | 2 | 1 | 1 | Done |
| CLAIMS-28 | Implement intake validation and completeness checks | 3 | 1 | 1 | Done |
| CLAIMS-29 | Track intake channel and volume metrics | 5 | 1 | 1 | Done |

### 10.2 Epic 2: Claims Triage & Assignment  `CLAIMS-2`

**Objective:** Routing and prioritization.  
**Stories:** 15 · **Estimated points:** 58

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| CLAIMS-30 | Implement claim segmentation and complexity scoring | 3 | 1 | 1 | Done |
| CLAIMS-31 | Support automated adjuster assignment rules | 2 | 1 | 2 | Done |
| CLAIMS-32 | Add workload balancing across adjusters | 5 | 1 | 2 | Done |
| CLAIMS-33 | Implement severity-based prioritization | 8 | 1 | 2 | Done |
| CLAIMS-34 | Support skill-based routing | 3 | 2 | 2 | Done |
| CLAIMS-35 | Add reassignment and escalation workflow | 1 | 2 | 2 | Done |
| CLAIMS-36 | Implement fast-track for low-complexity claims | 2 | 2 | 2 | Done |
| CLAIMS-37 | Support CAT surge assignment | 2 | 2 | 2 | Done |
| CLAIMS-38 | Add supervisor override of assignment | 3 | 2 | 2 | Done |
| CLAIMS-39 | Implement SLA timers by claim type | 3 | 2 | 2 | Done |
| CLAIMS-40 | Support territory-based routing | 3 | 2 | 2 | Done |
| CLAIMS-41 | Add queue and worklist dashboards | 5 | 2 | 2 | Done |
| CLAIMS-42 | Implement auto-triage from FNOL data | 5 | 2 | 2 | Done |
| CLAIMS-43 | Support vendor auto-assignment | 5 | 2 | 2 | Done |
| CLAIMS-44 | Track assignment and cycle-time metrics | 8 | 2 | 2 | Done |

### 10.3 Epic 3: Claims Adjudication & Decisioning  `CLAIMS-3`

**Objective:** Claim evaluation.  
**Stories:** 15 · **Estimated points:** 63

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| CLAIMS-45 | Build claim workbench for adjusters | 8 | 2 | 2 | Done |
| CLAIMS-46 | Implement liability assessment tooling | 13 | 2 | 2 | Done |
| CLAIMS-47 | Add coverage decisioning workflow | 2 | 2 | 2 | Done |
| CLAIMS-48 | Support decision rules and authority limits | 3 | 2 | 3 | Done |
| CLAIMS-49 | Implement claim status lifecycle management | 5 | 2 | 3 | Done |
| CLAIMS-50 | Add decision rationale and notes capture | 3 | 2 | 3 | Done |
| CLAIMS-51 | Support partial and supplemental decisions | 2 | 2 | 3 | Done |
| CLAIMS-52 | Implement approve/deny with reason codes | 5 | 2 | 3 | Done |
| CLAIMS-53 | Add referral to specialists (medical/legal) | 8 | 3 | 3 | Done |
| CLAIMS-54 | Support decision audit trail | 3 | 3 | 3 | Done |
| CLAIMS-55 | Implement straight-through settlement for simple claims | 1 | 3 | 3 | Done |
| CLAIMS-56 | Add reopen and reversal handling | 2 | 3 | 3 | Done |
| CLAIMS-57 | Support multi-claimant claim handling | 2 | 3 | 3 | Done |
| CLAIMS-58 | Implement diary and follow-up tasks | 3 | 3 | 3 | Done |
| CLAIMS-59 | Track decision quality and rework metrics | 3 | 3 | 3 | Done |

### 10.4 Epic 4: Coverage Verification & Validation  `CLAIMS-4`

**Objective:** Policy/coverage checks.  
**Stories:** 15 · **Estimated points:** 78

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| CLAIMS-60 | Implement policy-in-force verification at loss date | 3 | 3 | 3 | Done |
| CLAIMS-61 | Add coverage and limit validation | 5 | 3 | 3 | Done |
| CLAIMS-62 | Support deductible application logic | 5 | 3 | 3 | Done |
| CLAIMS-63 | Implement exclusion and endorsement checks | 5 | 3 | 3 | Done |
| CLAIMS-64 | Add sub-limit and aggregate tracking | 8 | 3 | 3 | Done |
| CLAIMS-65 | Support coordination of benefits | 8 | 3 | 3 | Done |
| CLAIMS-66 | Implement waiting-period and eligibility checks | 13 | 3 | 3 | Done |
| CLAIMS-67 | Add coverage-gap identification | 2 | 3 | 3 | Done |
| CLAIMS-68 | Support multi-policy coverage stacking | 3 | 3 | 4 | Done |
| CLAIMS-69 | Implement lienholder and interest verification | 5 | 3 | 4 | Done |
| CLAIMS-70 | Add coverage decision documentation | 3 | 3 | 4 | Done |
| CLAIMS-71 | Support retroactive coverage validation | 2 | 3 | 4 | Done |
| CLAIMS-72 | Implement automated coverage summary | 5 | 4 | 4 | Done |
| CLAIMS-73 | Add coverage dispute handling | 8 | 4 | 4 | Done |
| CLAIMS-74 | Track coverage decision accuracy | 3 | 4 | 4 | Done |

### 10.5 Epic 5: Investigation & Fraud Detection  `CLAIMS-5`

**Objective:** SIU and fraud.  
**Stories:** 15 · **Estimated points:** 68

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| CLAIMS-75 | Implement claim fraud scoring model | 1 | 4 | 4 | Done |
| CLAIMS-76 | Add red-flag and indicator rules | 2 | 4 | 4 | Done |
| CLAIMS-77 | Support SIU referral and case management | 2 | 4 | 4 | Done |
| CLAIMS-78 | Implement link analysis across claims | 3 | 4 | 4 | Done |
| CLAIMS-79 | Add anomaly detection on claim patterns | 3 | 4 | 4 | Done |
| CLAIMS-80 | Support external data checks (ISO, watchlists) | 3 | 4 | 4 | Done |
| CLAIMS-81 | Implement recorded-statement management | 5 | 4 | 4 | Done |
| CLAIMS-82 | Add surveillance and evidence tracking | 5 | 4 | 4 | Done |
| CLAIMS-83 | Support provider fraud detection | 5 | 4 | 4 | Done |
| CLAIMS-84 | Implement staged/duplicate claim detection | 8 | 4 | 4 | Done |
| CLAIMS-85 | Add fraud model monitoring and feedback | 8 | 4 | 4 | Done |
| CLAIMS-86 | Support investigation task workflow | 13 | 4 | 5 | Done |
| CLAIMS-87 | Implement fraud outcome and savings tracking | 2 | 4 | 5 | Done |
| CLAIMS-88 | Add configurable fraud thresholds | 3 | 4 | 5 | Done |
| CLAIMS-89 | Track fraud detection rate and recoveries | 5 | 4 | 5 | Done |

### 10.6 Epic 6: Estimation & Damage Assessment  `CLAIMS-6`

**Objective:** Loss estimation.  
**Stories:** 15 · **Estimated points:** 58

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| CLAIMS-90 | Implement damage estimate creation tooling | 3 | 4 | 5 | Done |
| CLAIMS-91 | Add integration with estimating platforms | 2 | 5 | 5 | Done |
| CLAIMS-92 | Support photo-based/AI damage assessment | 5 | 5 | 5 | Done |
| CLAIMS-93 | Implement repair vs replace decisioning | 8 | 5 | 5 | Done |
| CLAIMS-94 | Add parts and labor rate catalogs | 3 | 5 | 5 | Done |
| CLAIMS-95 | Support total-loss valuation | 1 | 5 | 5 | Done |
| CLAIMS-96 | Implement estimate review and approval | 2 | 5 | 5 | Done |
| CLAIMS-97 | Add supplement handling | 2 | 5 | 5 | Done |
| CLAIMS-98 | Support independent appraiser assignment | 3 | 5 | 5 | Done |
| CLAIMS-99 | Implement estimate variance analysis | 3 | 5 | 5 | Done |
| CLAIMS-100 | Add depreciation and ACV calculation | 3 | 5 | 5 | Done |
| CLAIMS-101 | Support inspection scheduling | 5 | 5 | 5 | Done |
| CLAIMS-102 | Implement estimate audit trail | 5 | 5 | 6 | Done |
| CLAIMS-103 | Add estimate templates by loss type | 5 | 5 | 6 | Done |
| CLAIMS-104 | Track estimate accuracy and leakage | 8 | 5 | 6 | Done |

### 10.7 Epic 7: Payments & Settlements  `CLAIMS-7`

**Objective:** Claim disbursements.  
**Stories:** 15 · **Estimated points:** 63

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| CLAIMS-105 | Implement claim payment issuance | 8 | 5 | 6 | Done |
| CLAIMS-106 | Support multiple payee and split payments | 13 | 5 | 6 | Done |
| CLAIMS-107 | Add electronic payment (EFT/digital) options | 2 | 5 | 6 | Done |
| CLAIMS-108 | Implement payment approval and authority limits | 3 | 5 | 6 | Done |
| CLAIMS-109 | Support recurring/indemnity payments | 5 | 5 | 6 | Done |
| CLAIMS-110 | Add stop-payment and void handling | 3 | 6 | 6 | Done |
| CLAIMS-111 | Implement lienholder and mortgagee payments | 2 | 6 | 6 | Done |
| CLAIMS-112 | Support tax and 1099 handling | 5 | 6 | 6 | Done |
| CLAIMS-113 | Add payment reconciliation | 8 | 6 | 6 | Done |
| CLAIMS-114 | Implement settlement offer and release workflow | 3 | 6 | 6 | Done |
| CLAIMS-115 | Support deductible netting | 1 | 6 | 6 | Done |
| CLAIMS-116 | Add payment status tracking for claimants | 2 | 6 | 6 | Done |
| CLAIMS-117 | Implement duplicate-payment prevention | 2 | 6 | 6 | Done |
| CLAIMS-118 | Support currency handling for global claims | 3 | 6 | 6 | Done |
| CLAIMS-119 | Track payment cycle time and accuracy | 3 | 6 | 6 | Done |

### 10.8 Epic 8: Subrogation & Recovery  `CLAIMS-8`

**Objective:** Recovery management.  
**Stories:** 15 · **Estimated points:** 78

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| CLAIMS-120 | Implement subrogation identification and referral | 3 | 6 | 6 | Done |
| CLAIMS-121 | Add recovery case management | 5 | 6 | 7 | Done |
| CLAIMS-122 | Support demand letter generation | 5 | 6 | 7 | Done |
| CLAIMS-123 | Implement arbitration filing workflow | 5 | 6 | 7 | Done |
| CLAIMS-124 | Add salvage identification and tracking | 8 | 6 | 7 | Done |
| CLAIMS-125 | Support salvage vendor integration | 8 | 6 | 7 | Done |
| CLAIMS-126 | Implement recovery negotiation tracking | 13 | 6 | 7 | Done |
| CLAIMS-127 | Add liability apportionment for recovery | 2 | 6 | 7 | Done |
| CLAIMS-128 | Support recovery payment posting | 3 | 6 | 7 | Done |
| CLAIMS-129 | Implement statute-of-limitations tracking | 5 | 7 | 7 | Done |
| CLAIMS-130 | Add subrogation analytics and scoring | 3 | 7 | 7 | Done |
| CLAIMS-131 | Support recovery reserve adjustments | 2 | 7 | 7 | Done |
| CLAIMS-132 | Implement recovery document management | 5 | 7 | 7 | Done |
| CLAIMS-133 | Add deductible recovery for claimants | 8 | 7 | 7 | Done |
| CLAIMS-134 | Track recovery rate and net savings | 3 | 7 | 7 | Done |

### 10.9 Epic 9: Reserves & Financials  `CLAIMS-9`

**Objective:** Claim financials.  
**Stories:** 15 · **Estimated points:** 68

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| CLAIMS-135 | Implement reserve setting and adjustment | 1 | 7 | 7 | Done |
| CLAIMS-136 | Add automatic reserve recommendations | 2 | 7 | 7 | Done |
| CLAIMS-137 | Support reserve authority and approval | 2 | 7 | 7 | Done |
| CLAIMS-138 | Implement paid/incurred/outstanding tracking | 3 | 7 | 7 | Done |
| CLAIMS-139 | Add reserve change audit trail | 3 | 7 | 7 | Done |
| CLAIMS-140 | Support bulk reserve adjustments (CAT) | 3 | 7 | 7 | Done |
| CLAIMS-141 | Implement claim financial ledger | 5 | 7 | 7 | Done |
| CLAIMS-142 | Add expense vs indemnity separation | 5 | 7 | 7 | Done |
| CLAIMS-143 | Support reserve adequacy monitoring | 5 | 7 | 8 | Done |
| CLAIMS-144 | Implement financial reconciliation with GL | 8 | 7 | 8 | Done |
| CLAIMS-145 | Add loss run reporting | 8 | 7 | 8 | Done |
| CLAIMS-146 | Support currency and multi-entity financials | 13 | 7 | 8 | Done |
| CLAIMS-147 | Implement reserve forecasting | 2 | 8 | 8 | Done |
| CLAIMS-148 | Add IBNR data extracts for actuarial | 3 | 8 | 8 | Done |
| CLAIMS-149 | Track reserve accuracy and development | 5 | 8 | 8 | Done |

### 10.10 Epic 10: Provider/Vendor & Repair Network  `CLAIMS-10`

**Objective:** Vendor ecosystem.  
**Stories:** 15 · **Estimated points:** 58

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| CLAIMS-150 | Build vendor and provider registry | 3 | 8 | 8 | Done |
| CLAIMS-151 | Implement repair-shop network management | 2 | 8 | 8 | Done |
| CLAIMS-152 | Add vendor assignment and dispatch | 5 | 8 | 8 | Done |
| CLAIMS-153 | Support vendor performance scorecards | 8 | 8 | 8 | Done |
| CLAIMS-154 | Implement vendor invoicing and bill review | 3 | 8 | 8 | Done |
| CLAIMS-155 | Add preferred-provider steering | 1 | 8 | 8 | Done |
| CLAIMS-156 | Support vendor credentialing and compliance | 2 | 8 | 8 | Done |
| CLAIMS-157 | Implement medical provider network handling | 2 | 8 | 8 | Done |
| CLAIMS-158 | Add vendor SLA monitoring | 3 | 8 | 8 | Done |
| CLAIMS-159 | Support rental and towing coordination | 3 | 8 | 8 | Done |
| CLAIMS-160 | Implement vendor portal for updates | 3 | 8 | 9 | Done |
| CLAIMS-161 | Add vendor rate agreements | 5 | 8 | 9 | Done |
| CLAIMS-162 | Support vendor fraud/abuse detection | 5 | 8 | 9 | Done |
| CLAIMS-163 | Implement vendor payment integration | 5 | 8 | 9 | Done |
| CLAIMS-164 | Track vendor cost and quality metrics | 8 | 8 | 9 | Done |

### 10.11 Epic 11: Customer Communication & Self-service  `CLAIMS-11`

**Objective:** Claimant experience.  
**Stories:** 15 · **Estimated points:** 63

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| CLAIMS-165 | Build claim status self-service portal | 8 | 9 | 9 | Done |
| CLAIMS-166 | Implement proactive status notifications | 13 | 9 | 9 | Done |
| CLAIMS-167 | Add secure messaging with adjuster | 2 | 9 | 9 | Done |
| CLAIMS-168 | Support document upload by claimant | 3 | 9 | 9 | Done |
| CLAIMS-169 | Implement digital claim tracking timeline | 5 | 9 | 9 | Done |
| CLAIMS-170 | Add chatbot for claim FAQs | 3 | 9 | 9 | Done |
| CLAIMS-171 | Support payment status visibility | 2 | 9 | 9 | Done |
| CLAIMS-172 | Implement satisfaction (NPS/CSAT) surveys | 5 | 9 | 9 | Done |
| CLAIMS-173 | Add multi-language communication | 8 | 9 | 9 | Done |
| CLAIMS-174 | Support SMS and email preferences | 3 | 9 | 9 | Done |
| CLAIMS-175 | Implement appointment scheduling | 1 | 9 | 9 | Done |
| CLAIMS-176 | Add accessibility compliance (WCAG 2.2) | 2 | 9 | 9 | Done |
| CLAIMS-177 | Support mobile claim experience | 2 | 9 | 9 | Done |
| CLAIMS-178 | Implement escalation and callback requests | 3 | 9 | 9 | Done |
| CLAIMS-179 | Track communication engagement and CSAT | 3 | 9 | 9 | Done |

### 10.12 Epic 12: Compliance, Regulatory & Litigation  `CLAIMS-12`

**Objective:** Legal and regulatory.  
**Stories:** 15 · **Estimated points:** 78

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| CLAIMS-180 | Implement regulatory claim reporting | 3 | 9 | 9 | Done |
| CLAIMS-181 | Add state-specific claim handling rules | 5 | 9 | 9 | Done |
| CLAIMS-182 | Support fair-claims-practices compliance | 5 | 9 | — | In Progress (carried over) |
| CLAIMS-183 | Implement litigation and legal case tracking | 5 | Upcoming | — | To Do (planned) |
| CLAIMS-184 | Add reserve and settlement authority controls | 8 | Upcoming | — | To Do (planned) |
| CLAIMS-185 | Support privacy and data protection controls | 8 | Upcoming | — | To Do (planned) |
| CLAIMS-186 | Implement complaint handling and DOI response | 13 | Upcoming | — | To Do (planned) |
| CLAIMS-187 | Add mandatory notice generation | 2 | Upcoming | — | To Do (planned) |
| CLAIMS-188 | Support subpoena and records requests | 3 | Upcoming | — | To Do (planned) |
| CLAIMS-189 | Implement audit trail for all claim actions | 5 | Upcoming | — | To Do (planned) |
| CLAIMS-190 | Add sanctions and OFAC screening on payments | 3 | Upcoming | — | To Do (planned) |
| CLAIMS-191 | Support statutory deadline tracking | 2 | Upcoming | — | To Do (planned) |
| CLAIMS-192 | Implement bad-faith risk indicators | 5 | Upcoming | — | To Do (planned) |
| CLAIMS-193 | Add regulatory change management | 8 | Upcoming | — | To Do (planned) |
| CLAIMS-194 | Track compliance exceptions and outcomes | 3 | Upcoming | — | To Do (planned) |

### 10.13 Epic 13: Claims Analytics & Reporting  `CLAIMS-13`

**Objective:** Claims intelligence.  
**Stories:** 15 · **Estimated points:** 29

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| CLAIMS-195 | Build claims operational dashboards | 1 | Upcoming | — | To Do (planned) |
| CLAIMS-196 | Implement cycle-time and cost analytics | 2 | Upcoming | — | To Do (planned) |
| CLAIMS-197 | Add loss ratio and severity reporting | 2 | Upcoming | — | To Do (planned) |
| CLAIMS-198 | Support adjuster performance analytics | 3 | Upcoming | — | To Do (planned) |
| CLAIMS-199 | Implement leakage detection and reporting | 3 | Upcoming | — | To Do (planned) |
| CLAIMS-200 | Add CAT event impact dashboards | 3 | Upcoming | — | To Do (planned) |
| CLAIMS-201 | Support predictive claim-severity models | 5 | Upcoming | — | To Do (planned) |
| CLAIMS-202 | Implement litigation-propensity scoring | 5 | Upcoming | — | To Do (planned) |
| CLAIMS-203 | Add reserve development analytics | 5 | Upcoming | — | To Do (planned) |
| CLAIMS-204 | Support self-service BI for claims | — | Backlog | — | To Do (not estimated) |
| CLAIMS-205 | Implement fraud analytics dashboards | — | Backlog | — | To Do (not estimated) |
| CLAIMS-206 | Add customer-satisfaction analytics | — | Backlog | — | To Do (not estimated) |
| CLAIMS-207 | Support real-time claims monitoring | — | Backlog | — | To Do (not estimated) |
| CLAIMS-208 | Implement data quality and lineage | — | Backlog | — | To Do (not estimated) |
| CLAIMS-209 | Track KPI trends and forecasts | — | Backlog | — | To Do (not estimated) |

### 10.14 Epic 14: Platform, Integration & Security  `CLAIMS-14`

**Objective:** Foundation and integrations.  
**Stories:** 15 · **Estimated points:** 0

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| CLAIMS-210 | Set up multi-environment CI/CD pipeline | — | Backlog | — | To Do (not estimated) |
| CLAIMS-211 | Implement API gateway with versioning | — | Backlog | — | To Do (not estimated) |
| CLAIMS-212 | Add integration with policy administration system | — | Backlog | — | To Do (not estimated) |
| CLAIMS-213 | Support third-party data and estimating integrations | — | Backlog | — | To Do (not estimated) |
| CLAIMS-214 | Implement SSO and role-based access control | — | Backlog | — | To Do (not estimated) |
| CLAIMS-215 | Add encryption of data at rest and in transit | — | Backlog | — | To Do (not estimated) |
| CLAIMS-216 | Support event-driven integration bus | — | Backlog | — | To Do (not estimated) |
| CLAIMS-217 | Implement audit logging and monitoring | — | Backlog | — | To Do (not estimated) |
| CLAIMS-218 | Add disaster recovery and backup drills | — | Backlog | — | To Do (not estimated) |
| CLAIMS-219 | Support horizontal autoscaling for CAT surges | — | Backlog | — | To Do (not estimated) |
| CLAIMS-220 | Implement secrets management and rotation | — | Backlog | — | To Do (not estimated) |
| CLAIMS-221 | Add feature-flag framework | — | Backlog | — | To Do (not estimated) |
| CLAIMS-222 | Support performance and load testing | — | Backlog | — | To Do (not estimated) |
| CLAIMS-223 | Implement SLO dashboards and alerting | — | Backlog | — | To Do (not estimated) |
| CLAIMS-224 | Track platform reliability and security posture | — | Backlog | — | To Do (not estimated) |

## 11. Non-Functional Requirements

| Category | Requirement |
| --- | --- |
| Performance | Meet latency/throughput targets in KPIs; p75 within budget. |
| Scalability | Horizontally scalable; elastic for peak/CAT-surge volumes. |
| Availability | Target 99.9% uptime with health checks, failover, and DR drills. |
| Security | OWASP Top 10 controls, encryption in transit/at rest, least-privilege, secret rotation. |
| Privacy & Compliance | GDPR/CCPA, jurisdictional insurance regulation, audit trails. |
| Auditability | Complete, immutable audit trail for all financial and decision actions. |
| Accessibility | WCAG 2.2 AA on all user-facing surfaces. |
| Observability | Structured logging, tracing, metrics, SLO dashboards, alerting. |
| Maintainability | Modular services, CI/CD, automated tests (target 80%+), feature flags. |

## 12. Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Catastrophe surge overwhelms claims capacity | High | Elastic autoscaling, CAT tagging, surge assignment, and fast-track. |
| Claims leakage from coverage/estimation errors | High | Automated coverage validation, estimate variance analysis, and bill review. |
| Undetected fraud increases loss costs | Medium | Fraud scoring, red-flag rules, link analysis, and SIU workflows. |
| Bad-faith / fair-practices violations | Medium | Statutory deadline tracking, audit trails, and bad-faith risk indicators. |

## 13. Definition of Ready & Definition of Done

### 13.1 Definition of Ready (DoR)
- Clear description and acceptance criteria; estimated and sized to fit one sprint.
- Dependencies identified; design available where needed; testability understood.

### 13.2 Definition of Done (DoD)
- Acceptance criteria met and verified; code reviewed, merged, tested (target 80%+).
- NFRs (performance, security, compliance, accessibility) satisfied; docs/telemetry updated; demoed and accepted.

## 14. Requirements Traceability Summary

| Epic Key | Epic | # Stories | Points | Releases |
| --- | --- | --- | --- | --- |
| CLAIMS-1 | Claims Intake & FNOL | 15 | 68 | R1 |
| CLAIMS-2 | Claims Triage & Assignment | 15 | 58 | R1 |
| CLAIMS-3 | Claims Adjudication & Decisioning | 15 | 63 | R1, R2 |
| CLAIMS-4 | Coverage Verification & Validation | 15 | 78 | R2 |
| CLAIMS-5 | Investigation & Fraud Detection | 15 | 68 | R2 |
| CLAIMS-6 | Estimation & Damage Assessment | 15 | 58 | R2, R3 |
| CLAIMS-7 | Payments & Settlements | 15 | 63 | R3 |
| CLAIMS-8 | Subrogation & Recovery | 15 | 78 | R3, R4 |
| CLAIMS-9 | Reserves & Financials | 15 | 68 | R4 |
| CLAIMS-10 | Provider/Vendor & Repair Network | 15 | 58 | R4 |
| CLAIMS-11 | Customer Communication & Self-service | 15 | 63 | R5 |
| CLAIMS-12 | Compliance, Regulatory & Litigation | 15 | 78 | R5 |
| CLAIMS-13 | Claims Analytics & Reporting | 15 | 29 | R5 |
| CLAIMS-14 | Platform, Integration & Security | 15 | 0 | R5 |

## 15. Glossary

| Term | Definition |
| --- | --- |
| Epic | A large body of work decomposed into user stories. |
| User Story | A small, independently valuable increment. |
| Story Point | A relative estimate of effort/complexity. |
| Velocity | Story points completed per sprint. |
| Carryover | Committed work not completed in a sprint, moved to the next. |
| Burndown | Chart of remaining work across a sprint. |
| Sprint | A fixed 2-week timebox delivering a shippable increment. |
| Backlog | Prioritised, unplanned, not-yet-estimated work. |
| DoR / DoD | Definition of Ready / Definition of Done quality gates. |

## Appendix A — Jira Reference

| Item | Value |
| --- | --- |
| Jira project key | `CLAIMS` |
| Epics | 14 |
| User stories | 210 |
| Completed sprints | 9 |
| Stories delivered (in closed sprints) | 167 |
| Total completed points (velocity sum) | 731 |
| Avg velocity | ~81 pts/sprint |
| Board | https://pulseaipoc.atlassian.net/jira/software/projects/CLAIMS/boards |

---

*Generated 22 Jul 2026. Mirrors the live Jira project `CLAIMS` including its realistic velocity curve and carryover between sprints.*
