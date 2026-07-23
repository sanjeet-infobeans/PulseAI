# Business Requirements Document (BRD)
## Policy Administration & Underwriting Platform — Policy Administration & Underwriting Platform

### Document Control

| Field | Value |
| --- | --- |
| Document Title | BRD — Policy Administration & Underwriting Platform |
| Project Key (Jira) | `PAS` |
| Jira Project URL | https://pulseaipoc.atlassian.net/jira/software/projects/PAS/boards |
| Version | 1.0 |
| Status | Baselined |
| Date | 22 Jul 2026 |
| Author | Delivery / Product Team |
| Delivery Methodology | Agile (Scrum) — 2-week sprints |
| Industry Domain | Insurance |

## 1. Executive Summary

Deliver a modern, configurable policy administration and underwriting platform that supports the full policy lifecycle — product/rating, quoting, underwriting, issuance, servicing, billing, and renewals — with straight-through processing for clean risks, strong compliance, and a superior producer and policyholder experience across personal and commercial lines.

This document defines the business requirements, scope, objectives, and agile delivery plan. Delivery is organised into **14 epics** and **210 user stories**, executed across **10 completed sprints**, **1 upcoming sprint**, and a maintained backlog, aligned to **5 release milestones**. Delivery reflects realistic team dynamics: velocity varies sprint to sprint and 10–20% of committed work carries over between sprints.

## 2. Business Context & Problem Statement

The insurer runs on ageing, siloed policy systems that make product and rate changes slow and costly, force manual underwriting even for simple risks, and provide poor self-service for producers and policyholders. This inflates expense ratios, lengthens speed-to-market, and constrains growth and profitability.

## 3. Business Objectives

1. Reduce quote-to-issue cycle time to under 10 minutes for straight-through risks.
2. Enable rate/product changes to be configured and deployed in days, not months.
3. Achieve 60%+ straight-through processing for eligible new business.
4. Lower policy administration expense ratio through automation and self-service.
5. Ensure regulatory compliance across all operating jurisdictions.

## 4. Success Metrics & KPIs

| Metric | Target |
| --- | --- |
| Quote-to-issue cycle time (STP) | < 10 minutes |
| Straight-through processing rate | > 60% of eligible new business |
| Rate/product change lead time | < 5 business days |
| Quote-to-bind conversion | +15% over baseline |
| Policy admin expense ratio | Reduce by 20% |
| Regulatory filing compliance | 100% on-time |

## 5. Stakeholders & Personas

| Persona / Stakeholder | Role & Needs |
| --- | --- |
| Underwriter | Assesses risk, applies authority, and makes accept/decline decisions. |
| Agent / Broker | Quotes, binds, and services business via the producer portal. |
| Policyholder | Buys and self-services policies online. |
| Product Manager | Configures products, coverages, and rates. |
| Billing Specialist | Manages premium billing and collections. |
| Compliance Officer | Ensures filings and regulatory adherence. |
| Actuary | Monitors rate adequacy and profitability. |

## 6. Scope

### 6.1 In Scope

- Product configuration and rating engine
- Quoting, illustration, and proposal generation
- Automated and referral underwriting with authority controls
- Policy issuance, documents, and forms management
- Mid-term servicing, endorsements, and cancellations
- Billing, premium collection, and commissions
- Renewals, lapse management, and reinsurance/treaty handling
- Producer and policyholder portals, compliance, fraud, analytics, and platform

### 6.2 Out of Scope

- Claims management and processing (covered by the Claims platform)
- General-ledger / core accounting system (integration only)
- CRM and marketing automation (integration only)
- Investment and asset management systems

## 7. Assumptions, Constraints & Dependencies

### 7.1 Assumptions

- A cloud-native environment and CI/CD tooling are available.
- Rate and rule content is provided by product/actuarial teams.
- Identity is provided by the enterprise IdP via SSO.
- Legacy policy data migration is handled by a separate workstream.

### 7.2 Constraints

- Must comply with state/jurisdiction rate and form filing requirements.
- Must maintain full audit trails for all financial and underwriting actions.
- Must support both personal and commercial lines configurations.

### 7.3 Dependencies

- Enterprise SSO / identity provider
- Payment gateway and financial/GL systems
- Third-party risk data providers (MVR, credit, property)
- Document generation and e-signature services

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
| Committed to completed sprints | 168 | 80% | Yes | 10 closed sprints |
| Upcoming (planned) sprint | 21 | 10% | Yes | 1 future sprint |
| Product backlog (unplanned) | 21 | 10% | No (not estimated) | No sprint |
| **Total** | 210 | 100% | — | 11 sprints + backlog |

### 9.2 Sprint Plan, Velocity & Carryover

The table below reflects the actual delivery recorded in Jira. **Committed** = story points brought into the sprint (new commitment + carried-in). **Completed** = points delivered (the velocity). **Carried-out** = work not finished, moved to the next sprint.

| Sprint | Dates (planned) | Committed (pts) | Completed (pts) | Carried-out | Completion % | Release | State |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Sprint 1 | 04 Mar–17 Mar | 73+0=73 | 63 | 10 | 86% | R1 | Closed |
| Sprint 2 | 18 Mar–31 Mar | 79+10=89 | 71 | 18 | 80% | R1 | Closed |
| Sprint 3 | 01 Apr–14 Apr | 71+18=89 | 81 | 8 | 91% | R1 | Closed |
| Sprint 4 | 15 Apr–28 Apr | 68+8=76 | 66 | 10 | 87% | R2 | Closed |
| Sprint 5 | 29 Apr–12 May | 76+10=86 | 54 | 32 | 63% | R2 | Closed |
| Sprint 6 | 13 May–26 May | 81+32=113 | 79 | 34 | 70% | R3 | Closed |
| Sprint 7 | 27 May–09 Jun | 83+34=117 | 89 | 28 | 76% | R3 | Closed |
| Sprint 8 | 10 Jun–23 Jun | 74+28=102 | 68 | 34 | 67% | R4 | Closed |
| Sprint 9 | 24 Jun–07 Jul | 76+34=110 | 71 | 39 | 65% | R4 | Closed |
| Sprint 10 | 08 Jul–21 Jul | 55+39=94 | 89 | 5 | 95% | R5 | Closed |
| Sprint 11 | 22 Jul–04 Aug | 94 (+1 carried) | — | — | — | R5 | Upcoming |
| Backlog | Unscheduled | not estimated | — | — | — | — | Backlog |

> **Velocity curve (completed pts/sprint):** 63, 71, 81, 66, 54, 79, 89, 68, 71, 89  
> Average delivered velocity **~73 pts/sprint** over 10 sprints (731 pts / 167 stories delivered; 1 story carried into the current sprint).  
> *Note: sprints were executed in Jira as a compressed live simulation so that burndown charts render genuine descending curves; Jira sprint timestamps reflect that execution window rather than calendar fortnights.*

## 10. Epics & User Stories

The scope is decomposed into 14 epics. Story IDs are the live Jira issue keys. **Committed Sprint** is where a story was first planned; **Completed Sprint** is where it was actually delivered (they differ when work carried over).

### 10.1 Epic 1: Product & Rating Engine  `PAS-1`

**Objective:** Configurable products and rating.  
**Stories:** 15 · **Estimated points:** 68

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| PAS-15 | Build product configuration for coverages and options | 1 | 1 | 1 | Done |
| PAS-16 | Implement rating engine with versioned rate tables | 2 | 1 | 1 | Done |
| PAS-17 | Support rating factors by risk attributes | 2 | 1 | 1 | Done |
| PAS-18 | Add territory and zone-based rating | 3 | 1 | 1 | Done |
| PAS-19 | Implement discounts, surcharges, and fees logic | 3 | 1 | 1 | Done |
| PAS-20 | Support multi-coverage bundling and packages | 3 | 1 | 1 | Done |
| PAS-21 | Add rate versioning with effective dates | 5 | 1 | 1 | Done |
| PAS-22 | Implement what-if rating preview for underwriters | 5 | 1 | 1 | Done |
| PAS-23 | Support minimum premium and rounding rules | 5 | 1 | 1 | Done |
| PAS-24 | Add rating algorithm audit and traceability | 8 | 1 | 1 | Done |
| PAS-25 | Implement rate table import and validation | 8 | 1 | 1 | Done |
| PAS-26 | Support tiered and experience-based rating | 13 | 1 | 1 | Done |
| PAS-27 | Add rating rules testing sandbox | 2 | 1 | 1 | Done |
| PAS-28 | Implement multi-currency premium calculation | 3 | 1 | 1 | Done |
| PAS-29 | Track rate change impact analysis | 5 | 1 | 2 | Done |

### 10.2 Epic 2: Quote & Illustration  `PAS-2`

**Objective:** Quoting and proposal generation.  
**Stories:** 15 · **Estimated points:** 58

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| PAS-30 | Build guided quote intake wizard | 3 | 1 | 2 | Done |
| PAS-31 | Support save-and-resume of in-progress quotes | 2 | 1 | 2 | Done |
| PAS-32 | Implement instant premium indication | 5 | 2 | 2 | Done |
| PAS-33 | Add multi-option side-by-side quote comparison | 8 | 2 | 2 | Done |
| PAS-34 | Generate branded proposal/illustration documents | 3 | 2 | 2 | Done |
| PAS-35 | Support quote versioning and revision history | 1 | 2 | 2 | Done |
| PAS-36 | Implement quote-to-application conversion | 2 | 2 | 2 | Done |
| PAS-37 | Add prefill from third-party data sources | 2 | 2 | 2 | Done |
| PAS-38 | Support agent override with approval controls | 3 | 2 | 2 | Done |
| PAS-39 | Implement quote expiry and validity rules | 3 | 2 | 2 | Done |
| PAS-40 | Add coverage recommendation suggestions | 3 | 2 | 2 | Done |
| PAS-41 | Support bulk quoting for commercial schedules | 5 | 2 | 2 | Done |
| PAS-42 | Implement quote sharing with customers | 5 | 2 | 2 | Done |
| PAS-43 | Add quote analytics and conversion tracking | 5 | 2 | 2 | Done |
| PAS-44 | Support what-if coverage adjustments in quote | 8 | 2 | 2 | Done |

### 10.3 Epic 3: Underwriting & Risk Assessment  `PAS-3`

**Objective:** Risk evaluation and decisions.  
**Stories:** 15 · **Estimated points:** 63

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| PAS-45 | Implement automated underwriting rules engine | 8 | 2 | 2 | Done |
| PAS-46 | Support referral routing to underwriters | 13 | 2 | 3 | Done |
| PAS-47 | Add risk scoring from internal and external data | 2 | 2 | 3 | Done |
| PAS-48 | Implement underwriting worklist and queues | 3 | 2 | 3 | Done |
| PAS-49 | Support requirements ordering (inspections, reports) | 5 | 3 | 3 | Done |
| PAS-50 | Add underwriting notes and decision rationale | 3 | 3 | 3 | Done |
| PAS-51 | Implement accept/decline/refer decisioning | 2 | 3 | 3 | Done |
| PAS-52 | Support counter-offer and conditional acceptance | 5 | 3 | 3 | Done |
| PAS-53 | Add exposure and accumulation checks | 8 | 3 | 3 | Done |
| PAS-54 | Implement underwriting authority limits | 3 | 3 | 3 | Done |
| PAS-55 | Support knock-out and eligibility rules | 1 | 3 | 3 | Done |
| PAS-56 | Add straight-through processing for clean risks | 2 | 3 | 3 | Done |
| PAS-57 | Implement underwriting audit trail | 2 | 3 | 3 | Done |
| PAS-58 | Support risk appetite configuration | 3 | 3 | 3 | Done |
| PAS-59 | Track underwriting SLA and decision metrics | 3 | 3 | 3 | Done |

### 10.4 Epic 4: Policy Issuance & Documents  `PAS-4`

**Objective:** Binding and document generation.  
**Stories:** 15 · **Estimated points:** 78

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| PAS-60 | Implement policy binding and activation | 3 | 3 | 3 | Done |
| PAS-61 | Generate policy schedules and certificates | 5 | 3 | 3 | Done |
| PAS-62 | Support declarations page generation | 5 | 3 | 3 | Done |
| PAS-63 | Add configurable document templates | 5 | 3 | 3 | Done |
| PAS-64 | Implement e-signature capture on issuance | 8 | 3 | 3 | Done |
| PAS-65 | Support multi-language document output | 8 | 3 | 4 | Done |
| PAS-66 | Add document delivery via email and portal | 13 | 4 | 4 | Done |
| PAS-67 | Implement policy number generation scheme | 2 | 4 | 4 | Done |
| PAS-68 | Support forms and endorsements library | 3 | 4 | 4 | Done |
| PAS-69 | Add document versioning and archival | 5 | 4 | 4 | Done |
| PAS-70 | Implement compliance wording by jurisdiction | 3 | 4 | 4 | Done |
| PAS-71 | Support bulk document generation | 2 | 4 | 4 | Done |
| PAS-72 | Add document reprint and correction workflow | 5 | 4 | 4 | Done |
| PAS-73 | Implement welcome kit assembly | 8 | 4 | 4 | Done |
| PAS-74 | Track document delivery status | 3 | 4 | 4 | Done |

### 10.5 Epic 5: Policy Servicing & Endorsements  `PAS-5`

**Objective:** Mid-term changes.  
**Stories:** 15 · **Estimated points:** 68

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| PAS-75 | Implement mid-term endorsement workflow | 1 | 4 | 4 | Done |
| PAS-76 | Support coverage add/remove with rerating | 2 | 4 | 4 | Done |
| PAS-77 | Add insured and address change handling | 2 | 4 | 4 | Done |
| PAS-78 | Implement pro-rata and short-rate calculations | 3 | 4 | 4 | Done |
| PAS-79 | Support policy cancellation and reinstatement | 3 | 4 | 4 | Done |
| PAS-80 | Add beneficiary and interest party changes | 3 | 4 | 4 | Done |
| PAS-81 | Implement policy split and merge | 5 | 4 | 5 | Done |
| PAS-82 | Support backdated endorsement controls | 5 | 4 | 5 | Done |
| PAS-83 | Add endorsement approval and authority checks | 5 | 5 | 5 | Done |
| PAS-84 | Implement change history and audit | 8 | 5 | 5 | Done |
| PAS-85 | Support automatic document regeneration on change | 8 | 5 | 5 | Done |
| PAS-86 | Add servicing worklist and task management | 13 | 5 | 5 | Done |
| PAS-87 | Implement bulk endorsement processing | 2 | 5 | 5 | Done |
| PAS-88 | Support future-dated changes | 3 | 5 | 5 | Done |
| PAS-89 | Track servicing turnaround metrics | 5 | 5 | 5 | Done |

### 10.6 Epic 6: Billing & Premium Collection  `PAS-6`

**Objective:** Billing and payments.  
**Stories:** 15 · **Estimated points:** 58

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| PAS-90 | Implement flexible billing plans (annual, installments) | 3 | 5 | 6 | Done |
| PAS-91 | Support direct bill and agency bill | 2 | 5 | 6 | Done |
| PAS-92 | Add payment gateway integration | 5 | 5 | 6 | Done |
| PAS-93 | Implement automatic payment (autopay) setup | 8 | 5 | 6 | Done |
| PAS-94 | Support premium proration on changes | 3 | 5 | 6 | Done |
| PAS-95 | Add invoice and statement generation | 1 | 5 | 6 | Done |
| PAS-96 | Implement dunning and past-due handling | 2 | 5 | 6 | Done |
| PAS-97 | Support refunds and premium returns | 2 | 5 | 6 | Done |
| PAS-98 | Add commission calculation and payables | 3 | 5 | 6 | Done |
| PAS-99 | Implement suspense and unapplied cash handling | 3 | 5 | 6 | Done |
| PAS-100 | Support multiple payment methods | 3 | 6 | 6 | Done |
| PAS-101 | Add write-off and adjustment workflow | 5 | 6 | 6 | Done |
| PAS-102 | Implement billing reconciliation | 5 | 6 | 6 | Done |
| PAS-103 | Support installment fee configuration | 5 | 6 | 6 | Done |
| PAS-104 | Track collections and receivables aging | 8 | 6 | 6 | Done |

### 10.7 Epic 7: Renewals & Lapse Management  `PAS-7`

**Objective:** Retention lifecycle.  
**Stories:** 15 · **Estimated points:** 63

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| PAS-105 | Implement automated renewal generation | 8 | 6 | 6 | Done |
| PAS-106 | Support renewal rerating and re-underwriting | 13 | 6 | 6 | Done |
| PAS-107 | Add renewal offer and notice generation | 2 | 6 | 7 | Done |
| PAS-108 | Implement non-renewal workflow with reasons | 3 | 6 | 7 | Done |
| PAS-109 | Support renewal acceptance and payment | 5 | 6 | 7 | Done |
| PAS-110 | Add lapse and grace-period handling | 3 | 6 | 7 | Done |
| PAS-111 | Implement reinstatement after lapse | 2 | 6 | 7 | Done |
| PAS-112 | Support renewal batch processing | 5 | 6 | 7 | Done |
| PAS-113 | Add retention scoring and outreach | 8 | 6 | 7 | Done |
| PAS-114 | Implement renewal terms comparison | 3 | 6 | 7 | Done |
| PAS-115 | Support conditional renewal requirements | 1 | 6 | 7 | Done |
| PAS-116 | Add renewal document generation | 2 | 6 | 7 | Done |
| PAS-117 | Implement renewal exception handling | 2 | 7 | 7 | Done |
| PAS-118 | Support multi-year policy renewals | 3 | 7 | 7 | Done |
| PAS-119 | Track retention and lapse metrics | 3 | 7 | 7 | Done |

### 10.8 Epic 8: Reinsurance & Treaty Management  `PAS-8`

**Objective:** Ceded reinsurance.  
**Stories:** 15 · **Estimated points:** 78

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| PAS-120 | Implement treaty configuration (quota share, XoL) | 3 | 7 | 7 | Done |
| PAS-121 | Support facultative reinsurance placements | 5 | 7 | 7 | Done |
| PAS-122 | Add automatic cession calculation | 5 | 7 | 7 | Done |
| PAS-123 | Implement reinsurance premium ceding | 5 | 7 | 7 | Done |
| PAS-124 | Support reinsurer and broker management | 8 | 7 | 7 | Done |
| PAS-125 | Add reinsurance recoverables tracking | 8 | 7 | 7 | Done |
| PAS-126 | Implement bordereaux generation | 13 | 7 | 7 | Done |
| PAS-127 | Support layered and multi-treaty programs | 2 | 7 | 8 | Done |
| PAS-128 | Add reinsurance accounting entries | 3 | 7 | 8 | Done |
| PAS-129 | Implement retention and limit checks | 5 | 7 | 8 | Done |
| PAS-130 | Support treaty period and renewal management | 3 | 7 | 8 | Done |
| PAS-131 | Add reinsurance reporting | 2 | 7 | 8 | Done |
| PAS-132 | Implement commutation handling | 5 | 7 | 8 | Done |
| PAS-133 | Support proportional and non-proportional treaties | 8 | 7 | 8 | Done |
| PAS-134 | Track ceded exposure and recoveries | 3 | 8 | 8 | Done |

### 10.9 Epic 9: Distribution & Agent/Broker Portal  `PAS-9`

**Objective:** Producer experience.  
**Stories:** 15 · **Estimated points:** 68

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| PAS-135 | Build agent/broker self-service portal | 1 | 8 | 8 | Done |
| PAS-136 | Implement producer onboarding and licensing checks | 2 | 8 | 8 | Done |
| PAS-137 | Add commission statements for producers | 2 | 8 | 8 | Done |
| PAS-138 | Support book-of-business dashboards | 3 | 8 | 8 | Done |
| PAS-139 | Implement lead and opportunity tracking | 3 | 8 | 8 | Done |
| PAS-140 | Add agency hierarchy and sub-producers | 3 | 8 | 8 | Done |
| PAS-141 | Support quoting and binding via portal | 5 | 8 | 8 | Done |
| PAS-142 | Implement producer performance analytics | 5 | 8 | 8 | Done |
| PAS-143 | Add appointment and contract management | 5 | 8 | 8 | Done |
| PAS-144 | Support co-branded materials | 8 | 8 | 8 | Done |
| PAS-145 | Implement producer notifications and alerts | 8 | 8 | 9 | Done |
| PAS-146 | Add license and E&O compliance tracking | 13 | 8 | 9 | Done |
| PAS-147 | Support bulk upload for commercial submissions | 2 | 8 | 9 | Done |
| PAS-148 | Implement producer training resources | 3 | 8 | 9 | Done |
| PAS-149 | Track producer engagement metrics | 5 | 8 | 9 | Done |

### 10.10 Epic 10: Customer Portal & Self-service  `PAS-10`

**Objective:** Policyholder experience.  
**Stories:** 15 · **Estimated points:** 58

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| PAS-150 | Build policyholder self-service portal | 3 | 8 | 9 | Done |
| PAS-151 | Implement policy document access and download | 2 | 9 | 9 | Done |
| PAS-152 | Add online payment and autopay management | 5 | 9 | 9 | Done |
| PAS-153 | Support coverage and profile updates | 8 | 9 | 9 | Done |
| PAS-154 | Implement ID card and certificate access | 3 | 9 | 9 | Done |
| PAS-155 | Add claims initiation from portal | 1 | 9 | 9 | Done |
| PAS-156 | Support paperless preferences | 2 | 9 | 9 | Done |
| PAS-157 | Implement multi-policy household view | 2 | 9 | 9 | Done |
| PAS-158 | Add secure messaging with insurer | 3 | 9 | 9 | Done |
| PAS-159 | Support mobile app parity | 3 | 9 | 9 | Done |
| PAS-160 | Implement notifications and reminders | 3 | 9 | 9 | Done |
| PAS-161 | Add coverage recommendations | 5 | 9 | 9 | Done |
| PAS-162 | Support accessibility compliance (WCAG 2.2) | 5 | 9 | 10 | Done |
| PAS-163 | Implement registration and identity verification | 5 | 9 | 10 | Done |
| PAS-164 | Track self-service adoption | 8 | 9 | 10 | Done |

### 10.11 Epic 11: Compliance, Regulatory & Audit  `PAS-11`

**Objective:** Regulatory adherence.  
**Stories:** 15 · **Estimated points:** 63

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| PAS-165 | Implement state/jurisdiction filing compliance | 8 | 9 | 10 | Done |
| PAS-166 | Support regulatory reporting (statutory) | 13 | 9 | 10 | Done |
| PAS-167 | Add rate and form filing tracking | 2 | 10 | 10 | Done |
| PAS-168 | Implement data privacy controls (GDPR/CCPA) | 3 | 10 | 10 | Done |
| PAS-169 | Support audit trail across all transactions | 5 | 10 | 10 | Done |
| PAS-170 | Add complaint and grievance handling | 3 | 10 | 10 | Done |
| PAS-171 | Implement sanctions and watchlist screening | 2 | 10 | 10 | Done |
| PAS-172 | Support document retention policies | 5 | 10 | 10 | Done |
| PAS-173 | Add regulatory change management | 8 | 10 | 10 | Done |
| PAS-174 | Implement license and appointment compliance | 3 | 10 | 10 | Done |
| PAS-175 | Support disclosures and notices by jurisdiction | 1 | 10 | 10 | Done |
| PAS-176 | Add anti-money-laundering (AML) checks | 2 | 10 | 10 | Done |
| PAS-177 | Implement market conduct reporting | 2 | 10 | 10 | Done |
| PAS-178 | Support examination and audit support tooling | 3 | 10 | 10 | Done |
| PAS-179 | Track compliance exceptions and remediation | 3 | 10 | 10 | Done |

### 10.12 Epic 12: Fraud Detection & Risk Controls  `PAS-12`

**Objective:** Application fraud & risk.  
**Stories:** 15 · **Estimated points:** 78

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| PAS-180 | Implement application fraud scoring | 3 | 10 | 10 | Done |
| PAS-181 | Support identity verification and validation | 5 | 10 | 10 | Done |
| PAS-182 | Add duplicate and misrepresentation detection | 5 | 10 | — | In Progress (carried over) |
| PAS-183 | Implement watchlist and adverse-media screening | 5 | Upcoming | — | To Do (planned) |
| PAS-184 | Support rules-based fraud alerts | 8 | Upcoming | — | To Do (planned) |
| PAS-185 | Add anomaly detection on applications | 8 | Upcoming | — | To Do (planned) |
| PAS-186 | Implement fraud case management | 13 | Upcoming | — | To Do (planned) |
| PAS-187 | Support third-party data verification | 2 | Upcoming | — | To Do (planned) |
| PAS-188 | Add premium leakage detection | 3 | Upcoming | — | To Do (planned) |
| PAS-189 | Implement device and behavioral signals | 5 | Upcoming | — | To Do (planned) |
| PAS-190 | Support SIU referral workflow | 3 | Upcoming | — | To Do (planned) |
| PAS-191 | Add fraud model monitoring | 2 | Upcoming | — | To Do (planned) |
| PAS-192 | Implement risk-control dashboards | 5 | Upcoming | — | To Do (planned) |
| PAS-193 | Support configurable fraud thresholds | 8 | Upcoming | — | To Do (planned) |
| PAS-194 | Track fraud detection and prevention metrics | 3 | Upcoming | — | To Do (planned) |

### 10.13 Epic 13: Data, Analytics & Actuarial Reporting  `PAS-13`

**Objective:** Insight and actuarial.  
**Stories:** 15 · **Estimated points:** 29

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| PAS-195 | Build data warehouse for policy data | 1 | Upcoming | — | To Do (planned) |
| PAS-196 | Implement loss ratio and profitability reporting | 2 | Upcoming | — | To Do (planned) |
| PAS-197 | Add written/earned premium reporting | 2 | Upcoming | — | To Do (planned) |
| PAS-198 | Support actuarial data extracts | 3 | Upcoming | — | To Do (planned) |
| PAS-199 | Implement portfolio exposure analytics | 3 | Upcoming | — | To Do (planned) |
| PAS-200 | Add rate adequacy monitoring | 3 | Upcoming | — | To Do (planned) |
| PAS-201 | Support regulatory statistical reporting | 5 | Upcoming | — | To Do (planned) |
| PAS-202 | Implement executive KPI dashboards | 5 | Upcoming | — | To Do (planned) |
| PAS-203 | Add predictive lapse and retention models | 5 | Upcoming | — | To Do (planned) |
| PAS-204 | Support data quality monitoring | — | Backlog | — | To Do (not estimated) |
| PAS-205 | Implement self-service BI access | — | Backlog | — | To Do (not estimated) |
| PAS-206 | Add cohort and segmentation analysis | — | Backlog | — | To Do (not estimated) |
| PAS-207 | Support real-time operational dashboards | — | Backlog | — | To Do (not estimated) |
| PAS-208 | Implement data lineage and governance | — | Backlog | — | To Do (not estimated) |
| PAS-209 | Track data pipeline reliability | — | Backlog | — | To Do (not estimated) |

### 10.14 Epic 14: Platform, Integration & Security  `PAS-14`

**Objective:** Foundation and integrations.  
**Stories:** 15 · **Estimated points:** 0

| Jira Key | User Story | Pts | Committed Sprint | Completed Sprint | Status |
| --- | --- | --- | --- | --- | --- |
| PAS-210 | Set up multi-environment CI/CD pipeline | — | Backlog | — | To Do (not estimated) |
| PAS-211 | Implement API gateway with versioning | — | Backlog | — | To Do (not estimated) |
| PAS-212 | Add integration with core financial systems | — | Backlog | — | To Do (not estimated) |
| PAS-213 | Support third-party data provider integrations | — | Backlog | — | To Do (not estimated) |
| PAS-214 | Implement SSO and role-based access control | — | Backlog | — | To Do (not estimated) |
| PAS-215 | Add encryption of data at rest and in transit | — | Backlog | — | To Do (not estimated) |
| PAS-216 | Support event-driven integration bus | — | Backlog | — | To Do (not estimated) |
| PAS-217 | Implement audit logging and monitoring | — | Backlog | — | To Do (not estimated) |
| PAS-218 | Add disaster recovery and backup drills | — | Backlog | — | To Do (not estimated) |
| PAS-219 | Support horizontal autoscaling | — | Backlog | — | To Do (not estimated) |
| PAS-220 | Implement secrets management and rotation | — | Backlog | — | To Do (not estimated) |
| PAS-221 | Add feature-flag framework | — | Backlog | — | To Do (not estimated) |
| PAS-222 | Support performance and load testing | — | Backlog | — | To Do (not estimated) |
| PAS-223 | Implement SLO dashboards and alerting | — | Backlog | — | To Do (not estimated) |
| PAS-224 | Track platform reliability and security posture | — | Backlog | — | To Do (not estimated) |

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
| Rating/rule misconfiguration causes premium leakage or errors | High | Rating sandbox, versioning, automated tests, and rate-change impact analysis. |
| Regulatory non-compliance in rate/form filings | High | Filing tracking, jurisdiction wording controls, and compliance workflows. |
| Legacy migration data quality issues | Medium | Dedicated migration workstream with validation and reconciliation. |
| Underwriting automation approves out-of-appetite risks | Medium | Knock-out rules, authority limits, and referral routing with audit. |

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
| PAS-1 | Product & Rating Engine | 15 | 68 | R1 |
| PAS-2 | Quote & Illustration | 15 | 58 | R1 |
| PAS-3 | Underwriting & Risk Assessment | 15 | 63 | R1 |
| PAS-4 | Policy Issuance & Documents | 15 | 78 | R1, R2 |
| PAS-5 | Policy Servicing & Endorsements | 15 | 68 | R2 |
| PAS-6 | Billing & Premium Collection | 15 | 58 | R2, R3 |
| PAS-7 | Renewals & Lapse Management | 15 | 63 | R3 |
| PAS-8 | Reinsurance & Treaty Management | 15 | 78 | R3, R4 |
| PAS-9 | Distribution & Agent/Broker Portal | 15 | 68 | R4 |
| PAS-10 | Customer Portal & Self-service | 15 | 58 | R4 |
| PAS-11 | Compliance, Regulatory & Audit | 15 | 63 | R4, R5 |
| PAS-12 | Fraud Detection & Risk Controls | 15 | 78 | R5 |
| PAS-13 | Data, Analytics & Actuarial Reporting | 15 | 29 | R5 |
| PAS-14 | Platform, Integration & Security | 15 | 0 | R5 |

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
| Jira project key | `PAS` |
| Epics | 14 |
| User stories | 210 |
| Completed sprints | 10 |
| Stories delivered (in closed sprints) | 167 |
| Total completed points (velocity sum) | 731 |
| Avg velocity | ~73 pts/sprint |
| Board | https://pulseaipoc.atlassian.net/jira/software/projects/PAS/boards |

---

*Generated 22 Jul 2026. Mirrors the live Jira project `PAS` including its realistic velocity curve and carryover between sprints.*
