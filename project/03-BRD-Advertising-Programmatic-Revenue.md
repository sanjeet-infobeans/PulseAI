# Business Requirements Document (BRD)
## Advertising & Programmatic Revenue — Advertising & Programmatic Revenue Platform

### Document Control

| Field | Value |
| --- | --- |
| Document Title | BRD — Advertising & Programmatic Revenue |
| Project Key (Jira) | `ADREV` |
| Jira Project URL | https://pulseaipoc.atlassian.net/jira/software/projects/ADREV/boards |
| Version | 1.0 |
| Status | Baselined |
| Date | 22 Jul 2026 |
| Author | Delivery / Product Team |
| Delivery Methodology | Agile (Scrum) — 2-week sprints |
| Industry Domain | Media & Publishing |

## 1. Executive Summary

Maximise and diversify advertising revenue through a unified ad server, direct and programmatic demand, first-party audience data, and rigorous brand safety and privacy compliance, while protecting reader experience and page performance.

This document defines the business requirements, scope, objectives, and agile delivery plan for the platform. Delivery is organised into **14 epics** and **210 user stories**, executed across **10 completed sprints**, **1 upcoming sprint**, and a maintained product backlog, aligned to **5 release milestones**.

## 2. Business Context & Problem Statement

Advertising operations are fragmented across manual processes and point tools, yield is left unoptimised, brand-safety and privacy controls are inconsistent, and ad-induced page slowdowns hurt reader experience and Core Web Vitals. There is no unified reporting or reliable inventory forecasting.

## 3. Business Objectives

1. Increase revenue per thousand impressions (RPM) by 20% through yield optimisation.
2. Unify direct and programmatic demand under a single auction with dynamic floors.
3. Achieve full IAB TCF v2 / CCPA consent compliance across all ad calls.
4. Keep ad-induced CLS < 0.1 and protect Core Web Vitals.
5. Deliver accurate inventory forecasting with < 10% error for sold campaigns.

## 4. Success Metrics & KPIs

| Metric | Target |
| --- | --- |
| Revenue per mille (RPM) | +20% over baseline |
| Fill rate | > 92% |
| Viewability (MRC standard) | > 70% |
| Ad-induced CLS | < 0.1 |
| Consent capture compliance | 100% of ad calls |
| Forecast accuracy (sold) | > 90% |

## 5. Stakeholders & Personas

| Persona / Stakeholder | Role & Needs |
| --- | --- |
| Ad Operations Manager | Traffics campaigns, manages inventory and pacing. |
| Direct Sales Rep | Books guaranteed campaigns and proposals. |
| Programmatic/Yield Analyst | Optimises floors, demand, and yield. |
| Data/Audience Manager | Builds and activates first-party segments. |
| Privacy/Compliance Officer | Ensures consent and regulatory compliance. |
| Advertiser | Buys inventory and reviews campaign performance. |

## 6. Scope

### 6.1 In Scope

- Ad server, inventory management, and decisioning
- Direct sales, trafficking, and campaign pacing
- Programmatic, header bidding, PMP, and deals
- Audience segmentation, first-party data, and CDP integration
- Native/sponsored content and video/CTV advertising
- Brand safety, verification, and privacy/consent management
- Yield optimisation, reporting, billing, and reconciliation
- Ad rendering performance, creative management, and forecasting

### 6.2 Out of Scope

- Editorial content creation (Digital Newsroom & CMS)
- Reader subscription/paywall revenue (Subscription platform)
- OTT content delivery (Streaming platform), except ad insertion interfaces
- Corporate marketing spend management

## 7. Assumptions, Constraints & Dependencies

### 7.1 Assumptions

- Relationships with SSPs and verification vendors are established.
- A consent management platform (CMP) is available.
- First-party identity is available from shared SSO.
- Ad inventory taxonomy is agreed with commercial teams.

### 7.2 Constraints

- Must comply with IAB TCF v2, GDPR, CCPA, and ads.txt/sellers.json.
- Ad rendering must not breach Core Web Vitals budgets.
- MRC-accredited viewability measurement required.

### 7.3 Dependencies

- Supply-side platforms and header-bidding partners
- Consent management platform (CMP)
- Third-party verification (viewability/IVT/brand safety)
- Customer data platform (CDP) / clean room

## 8. Product Roadmap & Milestones

| Milestone / Release | Theme | Target Date | Status |
| --- | --- | --- | --- |
| R1 – Foundation & MVP | Core platform foundation, environments, and MVP capabilities. | 18 Mar 2026 | Released |
| R2 – Core Experience | Primary end-user experience and workflows go live. | 15 Apr 2026 | Released |
| R3 – Scale & Monetize | Scaling, performance hardening, and revenue features. | 13 May 2026 | Released |
| R4 – Optimize & Expand | Optimization, analytics, and platform expansion. | 10 Jun 2026 | Released |
| R5 – GA & Hardening | General availability, compliance, and reliability hardening. | 08 Jul 2026 | Released |

## 9. Agile Delivery Approach

- **Framework:** Scrum with 2-week sprints and a prioritised product backlog.
- **Ceremonies:** Sprint Planning, Daily Stand-up, Sprint Review, Sprint Retrospective, Backlog Refinement.
- **Estimation:** Story points on a modified Fibonacci scale (1, 2, 3, 5, 8, 13). Stories are estimated during backlog refinement **before** a sprint starts.
- **Sequencing:** A sprint is started only after the previous sprint is closed; work is completed and demoed each sprint.

### 9.1 Backlog Distribution

| Category | Stories | % of Total | Estimated? | Sprint State |
| --- | --- | --- | --- | --- |
| Delivered (completed sprints) | 168 | 80% | Yes | 10 closed sprints |
| Upcoming (planned) sprint | 21 | 10% | Yes | 1 future sprint |
| Product backlog (unplanned) | 21 | 10% | No (not estimated) | No sprint |
| **Total** | 210 | 100% | — | 11 sprints + backlog |

### 9.2 Sprint Plan

| Sprint | Dates | Stories | Story Points | Release | State |
| --- | --- | --- | --- | --- | --- |
| Sprint 1 | 04 Mar – 17 Mar 2026 | 17 | 73 | R1 – Foundation & MVP | Closed / Delivered |
| Sprint 2 | 18 Mar – 31 Mar 2026 | 17 | 79 | R1 – Foundation & MVP | Closed / Delivered |
| Sprint 3 | 01 Apr – 14 Apr 2026 | 17 | 71 | R1 – Foundation & MVP | Closed / Delivered |
| Sprint 4 | 15 Apr – 28 Apr 2026 | 17 | 68 | R2 – Core Experience | Closed / Delivered |
| Sprint 5 | 29 Apr – 12 May 2026 | 17 | 76 | R2 – Core Experience | Closed / Delivered |
| Sprint 6 | 13 May – 26 May 2026 | 17 | 81 | R3 – Scale & Monetize | Closed / Delivered |
| Sprint 7 | 27 May – 09 Jun 2026 | 17 | 83 | R3 – Scale & Monetize | Closed / Delivered |
| Sprint 8 | 10 Jun – 23 Jun 2026 | 17 | 74 | R4 – Optimize & Expand | Closed / Delivered |
| Sprint 9 | 24 Jun – 07 Jul 2026 | 16 | 76 | R4 – Optimize & Expand | Closed / Delivered |
| Sprint 10 | 08 Jul – 21 Jul 2026 | 16 | 55 | R5 – GA & Hardening | Closed / Delivered |
| Sprint 11 | 22 Jul – 04 Aug 2026 | 21 | 94 | R5 – GA & Hardening | Upcoming (planned) |
| Backlog | Unscheduled | 21 | Not estimated | R5 – GA & Hardening | Backlog |

> **Velocity note:** 168 stories (~736 points) were delivered across 10 completed sprints, giving an average delivered velocity of **~73 points/sprint**. Completed story points per sprint are visible in the Jira Velocity report.

## 10. Epics & User Stories

The scope is decomposed into 14 epics. Each user story follows the INVEST principles and carries acceptance criteria and a Definition of Done in Jira. Story IDs below are the live Jira issue keys.

### 10.1 Epic 1: Ad Server & Inventory  `ADREV-1`

**Objective:** Core ad serving and inventory.  
**Stories:** 15 · **Estimated points:** 68

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| ADREV-15 | Build ad slot definition and placement registry | 1 | Sprint 1 | R1 – Foundation & MVP | Done |
| ADREV-16 | Implement ad decisioning engine | 2 | Sprint 1 | R1 – Foundation & MVP | Done |
| ADREV-17 | Support responsive and fluid ad sizes | 2 | Sprint 1 | R1 – Foundation & MVP | Done |
| ADREV-18 | Add frequency capping per user and campaign | 3 | Sprint 1 | R1 – Foundation & MVP | Done |
| ADREV-19 | Implement house-ad fallback fill | 3 | Sprint 1 | R1 – Foundation & MVP | Done |
| ADREV-20 | Support lazy-loading of below-fold ad slots | 3 | Sprint 1 | R1 – Foundation & MVP | Done |
| ADREV-21 | Add competitive separation rules | 5 | Sprint 1 | R1 – Foundation & MVP | Done |
| ADREV-22 | Implement ad refresh with viewability gating | 5 | Sprint 1 | R1 – Foundation & MVP | Done |
| ADREV-23 | Support roadblock and takeover placements | 5 | Sprint 1 | R1 – Foundation & MVP | Done |
| ADREV-24 | Add inventory availability API | 8 | Sprint 1 | R1 – Foundation & MVP | Done |
| ADREV-25 | Implement ad slot targeting keys | 8 | Sprint 1 | R1 – Foundation & MVP | Done |
| ADREV-26 | Support AMP and app ad rendering | 13 | Sprint 1 | R1 – Foundation & MVP | Done |
| ADREV-27 | Add ad slot debugging and preview mode | 2 | Sprint 1 | R1 – Foundation & MVP | Done |
| ADREV-28 | Implement inventory taxonomy and naming | 3 | Sprint 1 | R1 – Foundation & MVP | Done |
| ADREV-29 | Track fill rate and unfilled impressions | 5 | Sprint 1 | R1 – Foundation & MVP | Done |

### 10.2 Epic 2: Direct Sales & Trafficking  `ADREV-2`

**Objective:** Sold campaigns and orders.  
**Stories:** 15 · **Estimated points:** 58

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| ADREV-30 | Build campaign and line-item management | 3 | Sprint 1 | R1 – Foundation & MVP | Done |
| ADREV-31 | Implement insertion order workflow | 2 | Sprint 1 | R1 – Foundation & MVP | Done |
| ADREV-32 | Support flight dates and delivery goals | 5 | Sprint 2 | R1 – Foundation & MVP | Done |
| ADREV-33 | Add creative-to-line-item association | 8 | Sprint 2 | R1 – Foundation & MVP | Done |
| ADREV-34 | Implement priority and delivery pacing | 3 | Sprint 2 | R1 – Foundation & MVP | Done |
| ADREV-35 | Support guaranteed vs non-guaranteed line items | 1 | Sprint 2 | R1 – Foundation & MVP | Done |
| ADREV-36 | Add makegood and under-delivery handling | 2 | Sprint 2 | R1 – Foundation & MVP | Done |
| ADREV-37 | Implement campaign approval workflow | 2 | Sprint 2 | R1 – Foundation & MVP | Done |
| ADREV-38 | Support day-parting and geo targeting | 3 | Sprint 2 | R1 – Foundation & MVP | Done |
| ADREV-39 | Add creative rotation and weighting | 3 | Sprint 2 | R1 – Foundation & MVP | Done |
| ADREV-40 | Implement campaign cloning and templates | 3 | Sprint 2 | R1 – Foundation & MVP | Done |
| ADREV-41 | Support proposal-to-order conversion | 5 | Sprint 2 | R1 – Foundation & MVP | Done |
| ADREV-42 | Add delivery pacing alerts | 5 | Sprint 2 | R1 – Foundation & MVP | Done |
| ADREV-43 | Implement campaign change audit log | 5 | Sprint 2 | R1 – Foundation & MVP | Done |
| ADREV-44 | Track delivery vs booked goals | 8 | Sprint 2 | R1 – Foundation & MVP | Done |

### 10.3 Epic 3: Programmatic & Header Bidding  `ADREV-3`

**Objective:** RTB and auctions.  
**Stories:** 15 · **Estimated points:** 63

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| ADREV-45 | Integrate header-bidding wrapper (Prebid) | 8 | Sprint 2 | R1 – Foundation & MVP | Done |
| ADREV-46 | Support multiple SSP demand partners | 13 | Sprint 2 | R1 – Foundation & MVP | Done |
| ADREV-47 | Implement server-side header bidding | 2 | Sprint 2 | R1 – Foundation & MVP | Done |
| ADREV-48 | Add open-market and private-marketplace deals | 3 | Sprint 2 | R1 – Foundation & MVP | Done |
| ADREV-49 | Support preferred deals and programmatic guaranteed | 5 | Sprint 3 | R1 – Foundation & MVP | Done |
| ADREV-50 | Implement unified auction with floor pricing | 3 | Sprint 3 | R1 – Foundation & MVP | Done |
| ADREV-51 | Add bid timeout and latency budgeting | 2 | Sprint 3 | R1 – Foundation & MVP | Done |
| ADREV-52 | Support deal-ID targeting | 5 | Sprint 3 | R1 – Foundation & MVP | Done |
| ADREV-53 | Implement bidder analytics and win rates | 8 | Sprint 3 | R1 – Foundation & MVP | Done |
| ADREV-54 | Add supply-path optimization | 3 | Sprint 3 | R1 – Foundation & MVP | Done |
| ADREV-55 | Support ads.txt and sellers.json compliance | 1 | Sprint 3 | R1 – Foundation & MVP | Done |
| ADREV-56 | Implement bid caching and refresh strategy | 2 | Sprint 3 | R1 – Foundation & MVP | Done |
| ADREV-57 | Add auction transparency logging | 2 | Sprint 3 | R1 – Foundation & MVP | Done |
| ADREV-58 | Support currency handling across demand partners | 3 | Sprint 3 | R1 – Foundation & MVP | Done |
| ADREV-59 | Track programmatic revenue by partner | 3 | Sprint 3 | R1 – Foundation & MVP | Done |

### 10.4 Epic 4: Audience Segmentation & Targeting  `ADREV-4`

**Objective:** Audience data.  
**Stories:** 15 · **Estimated points:** 78

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| ADREV-60 | Build audience segment builder | 3 | Sprint 3 | R1 – Foundation & MVP | Done |
| ADREV-61 | Support behavioral segmentation from on-site events | 5 | Sprint 3 | R1 – Foundation & MVP | Done |
| ADREV-62 | Implement contextual targeting by content taxonomy | 5 | Sprint 3 | R1 – Foundation & MVP | Done |
| ADREV-63 | Add demographic and geo targeting | 5 | Sprint 3 | R1 – Foundation & MVP | Done |
| ADREV-64 | Support lookalike audience modeling | 8 | Sprint 3 | R1 – Foundation & MVP | Done |
| ADREV-65 | Implement segment activation to ad server | 8 | Sprint 3 | R1 – Foundation & MVP | Done |
| ADREV-66 | Add real-time segment qualification | 13 | Sprint 4 | R2 – Core Experience | Done |
| ADREV-67 | Support third-party data onboarding | 2 | Sprint 4 | R2 – Core Experience | Done |
| ADREV-68 | Implement segment size estimation | 3 | Sprint 4 | R2 – Core Experience | Done |
| ADREV-69 | Add recency and frequency segment rules | 5 | Sprint 4 | R2 – Core Experience | Done |
| ADREV-70 | Support cross-device audience stitching | 3 | Sprint 4 | R2 – Core Experience | Done |
| ADREV-71 | Implement segment expiry and refresh | 2 | Sprint 4 | R2 – Core Experience | Done |
| ADREV-72 | Add privacy-safe cohort targeting | 5 | Sprint 4 | R2 – Core Experience | Done |
| ADREV-73 | Support suppression and exclusion segments | 8 | Sprint 4 | R2 – Core Experience | Done |
| ADREV-74 | Track segment performance and reach | 3 | Sprint 4 | R2 – Core Experience | Done |

### 10.5 Epic 5: Native & Sponsored Content  `ADREV-5`

**Objective:** Branded content.  
**Stories:** 15 · **Estimated points:** 68

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| ADREV-75 | Build native ad unit templates | 1 | Sprint 4 | R2 – Core Experience | Done |
| ADREV-76 | Implement sponsored article labeling compliance | 2 | Sprint 4 | R2 – Core Experience | Done |
| ADREV-77 | Support in-feed native placements | 2 | Sprint 4 | R2 – Core Experience | Done |
| ADREV-78 | Add branded content CMS workflow | 3 | Sprint 4 | R2 – Core Experience | Done |
| ADREV-79 | Implement native ad targeting and pacing | 3 | Sprint 4 | R2 – Core Experience | Done |
| ADREV-80 | Support recommendation-widget native units | 3 | Sprint 4 | R2 – Core Experience | Done |
| ADREV-81 | Add sponsor disclosure and transparency | 5 | Sprint 4 | R2 – Core Experience | Done |
| ADREV-82 | Implement native creative approval | 5 | Sprint 4 | R2 – Core Experience | Done |
| ADREV-83 | Support content-recommendation partners | 5 | Sprint 5 | R2 – Core Experience | Done |
| ADREV-84 | Add sponsored content performance dashboard | 8 | Sprint 5 | R2 – Core Experience | Done |
| ADREV-85 | Implement native ad viewability tracking | 8 | Sprint 5 | R2 – Core Experience | Done |
| ADREV-86 | Support multi-format native (image/video) | 13 | Sprint 5 | R2 – Core Experience | Done |
| ADREV-87 | Add advertiser self-service native builder | 2 | Sprint 5 | R2 – Core Experience | Done |
| ADREV-88 | Implement native fallback rendering | 3 | Sprint 5 | R2 – Core Experience | Done |
| ADREV-89 | Track native engagement and CTR | 5 | Sprint 5 | R2 – Core Experience | Done |

### 10.6 Epic 6: Brand Safety & Verification  `ADREV-6`

**Objective:** Ad quality and safety.  
**Stories:** 15 · **Estimated points:** 58

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| ADREV-90 | Integrate third-party verification (viewability/IVT) | 3 | Sprint 5 | R2 – Core Experience | Done |
| ADREV-91 | Implement brand-safety keyword blocklists | 2 | Sprint 5 | R2 – Core Experience | Done |
| ADREV-92 | Add category exclusion controls | 5 | Sprint 5 | R2 – Core Experience | Done |
| ADREV-93 | Support malware and creative scanning | 8 | Sprint 5 | R2 – Core Experience | Done |
| ADREV-94 | Implement ad quality user-feedback controls | 3 | Sprint 5 | R2 – Core Experience | Done |
| ADREV-95 | Add invalid-traffic detection and filtering | 1 | Sprint 5 | R2 – Core Experience | Done |
| ADREV-96 | Support MRC-accredited viewability measurement | 2 | Sprint 5 | R2 – Core Experience | Done |
| ADREV-97 | Implement creative policy enforcement | 2 | Sprint 5 | R2 – Core Experience | Done |
| ADREV-98 | Add auto-blocking of policy-violating creatives | 3 | Sprint 5 | R2 – Core Experience | Done |
| ADREV-99 | Support contextual brand-safety classification | 3 | Sprint 5 | R2 – Core Experience | Done |
| ADREV-100 | Implement bad-ad reporting and takedown | 3 | Sprint 6 | R3 – Scale & Monetize | Done |
| ADREV-101 | Add heavy-ad and performance guardrails | 5 | Sprint 6 | R3 – Scale & Monetize | Done |
| ADREV-102 | Support advertiser and domain blocklists | 5 | Sprint 6 | R3 – Scale & Monetize | Done |
| ADREV-103 | Implement landing-page safety checks | 5 | Sprint 6 | R3 – Scale & Monetize | Done |
| ADREV-104 | Track blocked-ad and IVT rates | 8 | Sprint 6 | R3 – Scale & Monetize | Done |

### 10.7 Epic 7: Consent & Privacy  `ADREV-7`

**Objective:** Privacy compliance.  
**Stories:** 15 · **Estimated points:** 63

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| ADREV-105 | Implement IAB TCF v2 consent management | 8 | Sprint 6 | R3 – Scale & Monetize | Done |
| ADREV-106 | Support GDPR consent gating of ad calls | 13 | Sprint 6 | R3 – Scale & Monetize | Done |
| ADREV-107 | Add CCPA/US privacy opt-out signals | 2 | Sprint 6 | R3 – Scale & Monetize | Done |
| ADREV-108 | Implement Global Privacy Control handling | 3 | Sprint 6 | R3 – Scale & Monetize | Done |
| ADREV-109 | Support consent-based bid filtering | 5 | Sprint 6 | R3 – Scale & Monetize | Done |
| ADREV-110 | Add geo-based consent policy selection | 3 | Sprint 6 | R3 – Scale & Monetize | Done |
| ADREV-111 | Implement consent string propagation to partners | 2 | Sprint 6 | R3 – Scale & Monetize | Done |
| ADREV-112 | Support non-personalized ad fallback | 5 | Sprint 6 | R3 – Scale & Monetize | Done |
| ADREV-113 | Add cookie-less identity solutions (Prebid ID) | 8 | Sprint 6 | R3 – Scale & Monetize | Done |
| ADREV-114 | Implement data-processing agreements tracking | 3 | Sprint 6 | R3 – Scale & Monetize | Done |
| ADREV-115 | Support children's privacy (COPPA) controls | 1 | Sprint 6 | R3 – Scale & Monetize | Done |
| ADREV-116 | Add consent audit and versioning | 2 | Sprint 6 | R3 – Scale & Monetize | Done |
| ADREV-117 | Implement preference center for ad tracking | 2 | Sprint 7 | R3 – Scale & Monetize | Done |
| ADREV-118 | Support first-party consent syncing | 3 | Sprint 7 | R3 – Scale & Monetize | Done |
| ADREV-119 | Track consent rates by region | 3 | Sprint 7 | R3 – Scale & Monetize | Done |

### 10.8 Epic 8: Yield Optimization & Pricing  `ADREV-8`

**Objective:** Revenue maximization.  
**Stories:** 15 · **Estimated points:** 78

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| ADREV-120 | Implement dynamic price floors | 3 | Sprint 7 | R3 – Scale & Monetize | Done |
| ADREV-121 | Support unified pricing rules | 5 | Sprint 7 | R3 – Scale & Monetize | Done |
| ADREV-122 | Add A/B testing of floor strategies | 5 | Sprint 7 | R3 – Scale & Monetize | Done |
| ADREV-123 | Implement demand-partner yield analysis | 5 | Sprint 7 | R3 – Scale & Monetize | Done |
| ADREV-124 | Support ad layout optimization testing | 8 | Sprint 7 | R3 – Scale & Monetize | Done |
| ADREV-125 | Add revenue-per-session optimization | 8 | Sprint 7 | R3 – Scale & Monetize | Done |
| ADREV-126 | Implement machine-learning floor prediction | 13 | Sprint 7 | R3 – Scale & Monetize | Done |
| ADREV-127 | Support seasonal pricing adjustments | 2 | Sprint 7 | R3 – Scale & Monetize | Done |
| ADREV-128 | Add fill vs CPM trade-off tuning | 3 | Sprint 7 | R3 – Scale & Monetize | Done |
| ADREV-129 | Implement auction pressure analysis | 5 | Sprint 7 | R3 – Scale & Monetize | Done |
| ADREV-130 | Support format-level yield reporting | 3 | Sprint 7 | R3 – Scale & Monetize | Done |
| ADREV-131 | Add refresh-rate yield experiments | 2 | Sprint 7 | R3 – Scale & Monetize | Done |
| ADREV-132 | Implement header-bidding timeout tuning | 5 | Sprint 7 | R3 – Scale & Monetize | Done |
| ADREV-133 | Support geo-level pricing strategies | 8 | Sprint 7 | R3 – Scale & Monetize | Done |
| ADREV-134 | Track RPM and revenue uplift from experiments | 3 | Sprint 8 | R4 – Optimize & Expand | Done |

### 10.9 Epic 9: Reporting, Billing & Reconciliation  `ADREV-9`

**Objective:** Ad finance.  
**Stories:** 15 · **Estimated points:** 68

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| ADREV-135 | Build advertiser-facing campaign reports | 1 | Sprint 8 | R4 – Optimize & Expand | Done |
| ADREV-136 | Implement revenue reporting by dimension | 2 | Sprint 8 | R4 – Optimize & Expand | Done |
| ADREV-137 | Add discrepancy reconciliation with SSPs | 2 | Sprint 8 | R4 – Optimize & Expand | Done |
| ADREV-138 | Support billing based on delivered impressions | 3 | Sprint 8 | R4 – Optimize & Expand | Done |
| ADREV-139 | Implement invoice generation for direct deals | 3 | Sprint 8 | R4 – Optimize & Expand | Done |
| ADREV-140 | Add revenue attribution to content | 3 | Sprint 8 | R4 – Optimize & Expand | Done |
| ADREV-141 | Support export to finance/ERP systems | 5 | Sprint 8 | R4 – Optimize & Expand | Done |
| ADREV-142 | Implement daily revenue close reports | 5 | Sprint 8 | R4 – Optimize & Expand | Done |
| ADREV-143 | Add third-party ad-server discrepancy alerts | 5 | Sprint 8 | R4 – Optimize & Expand | Done |
| ADREV-144 | Support multi-currency revenue reporting | 8 | Sprint 8 | R4 – Optimize & Expand | Done |
| ADREV-145 | Implement forecast-vs-actual reporting | 8 | Sprint 8 | R4 – Optimize & Expand | Done |
| ADREV-146 | Add self-service reporting API | 13 | Sprint 8 | R4 – Optimize & Expand | Done |
| ADREV-147 | Support scheduled report delivery | 2 | Sprint 8 | R4 – Optimize & Expand | Done |
| ADREV-148 | Implement data-warehouse revenue pipeline | 3 | Sprint 8 | R4 – Optimize & Expand | Done |
| ADREV-149 | Track revenue by placement and format | 5 | Sprint 8 | R4 – Optimize & Expand | Done |

### 10.10 Epic 10: Video & Connected TV Ads  `ADREV-10`

**Objective:** Video monetization.  
**Stories:** 15 · **Estimated points:** 58

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| ADREV-150 | Implement VAST/VPAID video ad tags | 3 | Sprint 8 | R4 – Optimize & Expand | Done |
| ADREV-151 | Support pre-roll, mid-roll, post-roll ads | 2 | Sprint 9 | R4 – Optimize & Expand | Done |
| ADREV-152 | Add server-side ad insertion (SSAI) | 5 | Sprint 9 | R4 – Optimize & Expand | Done |
| ADREV-153 | Implement VMAP ad scheduling | 8 | Sprint 9 | R4 – Optimize & Expand | Done |
| ADREV-154 | Support CTV/OTT ad pods | 3 | Sprint 9 | R4 – Optimize & Expand | Done |
| ADREV-155 | Add video ad viewability and completion tracking | 1 | Sprint 9 | R4 – Optimize & Expand | Done |
| ADREV-156 | Implement adaptive ad-break decisioning | 2 | Sprint 9 | R4 – Optimize & Expand | Done |
| ADREV-157 | Support outstream video ad units | 2 | Sprint 9 | R4 – Optimize & Expand | Done |
| ADREV-158 | Add video ad frequency capping | 3 | Sprint 9 | R4 – Optimize & Expand | Done |
| ADREV-159 | Implement companion banner support | 3 | Sprint 9 | R4 – Optimize & Expand | Done |
| ADREV-160 | Support live-stream ad insertion | 3 | Sprint 9 | R4 – Optimize & Expand | Done |
| ADREV-161 | Add video ad quality and latency monitoring | 5 | Sprint 9 | R4 – Optimize & Expand | Done |
| ADREV-162 | Implement CTV audience targeting | 5 | Sprint 9 | R4 – Optimize & Expand | Done |
| ADREV-163 | Support skippable ad formats | 5 | Sprint 9 | R4 – Optimize & Expand | Done |
| ADREV-164 | Track video ad revenue and completion rates | 8 | Sprint 9 | R4 – Optimize & Expand | Done |

### 10.11 Epic 11: First-party Data & CDP  `ADREV-11`

**Objective:** Owned data platform.  
**Stories:** 15 · **Estimated points:** 63

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| ADREV-165 | Build first-party data collection pipeline | 8 | Sprint 9 | R4 – Optimize & Expand | Done |
| ADREV-166 | Implement customer data platform integration | 13 | Sprint 9 | R4 – Optimize & Expand | Done |
| ADREV-167 | Add identity resolution for logged-in users | 2 | Sprint 10 | R5 – GA & Hardening | Done |
| ADREV-168 | Support consented data enrichment | 3 | Sprint 10 | R5 – GA & Hardening | Done |
| ADREV-169 | Implement audience export to activation channels | 5 | Sprint 10 | R5 – GA & Hardening | Done |
| ADREV-170 | Add data clean-room integration | 3 | Sprint 10 | R5 – GA & Hardening | Done |
| ADREV-171 | Support event-based audience triggers | 2 | Sprint 10 | R5 – GA & Hardening | Done |
| ADREV-172 | Implement data-quality monitoring | 5 | Sprint 10 | R5 – GA & Hardening | Done |
| ADREV-173 | Add privacy-preserving aggregation | 8 | Sprint 10 | R5 – GA & Hardening | Done |
| ADREV-174 | Support subscriber-signal-based targeting | 3 | Sprint 10 | R5 – GA & Hardening | Done |
| ADREV-175 | Implement first-party ID graph | 1 | Sprint 10 | R5 – GA & Hardening | Done |
| ADREV-176 | Add data governance and access controls | 2 | Sprint 10 | R5 – GA & Hardening | Done |
| ADREV-177 | Support real-time profile updates | 2 | Sprint 10 | R5 – GA & Hardening | Done |
| ADREV-178 | Implement seed audience creation | 3 | Sprint 10 | R5 – GA & Hardening | Done |
| ADREV-179 | Track first-party addressable reach | 3 | Sprint 10 | R5 – GA & Hardening | Done |

### 10.12 Epic 12: Ad Rendering & Performance  `ADREV-12`

**Objective:** Page speed and UX.  
**Stories:** 15 · **Estimated points:** 78

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| ADREV-180 | Optimize ad script loading for Core Web Vitals | 3 | Sprint 10 | R5 – GA & Hardening | Done |
| ADREV-181 | Implement lazy and intersection-based rendering | 5 | Sprint 10 | R5 – GA & Hardening | Done |
| ADREV-182 | Add CLS-safe ad slot reservations | 5 | Sprint 10 | R5 – GA & Hardening | Done |
| ADREV-183 | Support asynchronous ad tag loading | 5 | Sprint 11 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| ADREV-184 | Implement ad SLA and latency monitoring | 8 | Sprint 11 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| ADREV-185 | Add heavy-ad intervention handling | 8 | Sprint 11 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| ADREV-186 | Support single-request architecture | 13 | Sprint 11 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| ADREV-187 | Implement ad-blocker detection and messaging | 2 | Sprint 11 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| ADREV-188 | Add graceful degradation on ad failures | 3 | Sprint 11 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| ADREV-189 | Support consent-gated deferred loading | 5 | Sprint 11 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| ADREV-190 | Implement ad performance real-user monitoring | 3 | Sprint 11 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| ADREV-191 | Add sticky-ad UX with dismiss controls | 2 | Sprint 11 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| ADREV-192 | Support responsive ad reflow on resize | 5 | Sprint 11 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| ADREV-193 | Implement ad error and timeout logging | 8 | Sprint 11 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| ADREV-194 | Track ad-induced page-speed impact | 3 | Sprint 11 (Upcoming) | R5 – GA & Hardening | To Do (planned) |

### 10.13 Epic 13: Creative Management & Preview  `ADREV-13`

**Objective:** Creative lifecycle.  
**Stories:** 15 · **Estimated points:** 29

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| ADREV-195 | Build creative upload and asset library | 1 | Sprint 11 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| ADREV-196 | Implement creative approval workflow | 2 | Sprint 11 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| ADREV-197 | Add creative preview across devices | 2 | Sprint 11 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| ADREV-198 | Support third-party tag creatives | 3 | Sprint 11 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| ADREV-199 | Implement creative versioning | 3 | Sprint 11 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| ADREV-200 | Add rich-media and expandable creatives | 3 | Sprint 11 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| ADREV-201 | Support creative weighting and rotation | 5 | Sprint 11 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| ADREV-202 | Implement creative policy validation | 5 | Sprint 11 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| ADREV-203 | Add dynamic creative optimization | 5 | Sprint 11 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| ADREV-204 | Support creative expiry and archiving | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| ADREV-205 | Implement creative performance comparison | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| ADREV-206 | Add creative macros and click-tracking | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| ADREV-207 | Support HTML5 creative sandboxing | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| ADREV-208 | Implement creative A/B testing | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| ADREV-209 | Track creative-level CTR and conversions | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |

### 10.14 Epic 14: Forecasting & Inventory Prediction  `ADREV-14`

**Objective:** Availability planning.  
**Stories:** 15 · **Estimated points:** 0

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| ADREV-210 | Build impression forecasting model | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| ADREV-211 | Implement availability check for proposals | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| ADREV-212 | Add contending-demand forecast adjustments | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| ADREV-213 | Support scenario-based what-if forecasting | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| ADREV-214 | Implement seasonal and trend forecasting | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| ADREV-215 | Add sell-through rate reporting | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| ADREV-216 | Support forecast accuracy monitoring | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| ADREV-217 | Implement inventory reservation on booking | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| ADREV-218 | Add forecast by segment and geo | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| ADREV-219 | Support overbooking risk alerts | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| ADREV-220 | Implement demand-supply balancing view | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| ADREV-221 | Add forecast API for sales tools | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| ADREV-222 | Support long-range capacity planning | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| ADREV-223 | Implement forecast recalculation scheduling | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| ADREV-224 | Track forecast vs actual delivery accuracy | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |

## 11. Non-Functional Requirements

| Category | Requirement |
| --- | --- |
| Performance | Meet Core Web Vitals / latency targets defined in KPIs; p75 within budget. |
| Scalability | Horizontally scalable; handle peak/seasonal traffic spikes without degradation. |
| Availability | Target 99.9% uptime with health checks, failover, and DR/backup drills. |
| Security | OWASP Top 10 controls, encrypted data in transit/at rest, least-privilege access, secret rotation. |
| Privacy & Compliance | GDPR/CCPA compliant; consent capture; data retention and deletion policies. |
| Accessibility | WCAG 2.2 AA on all user-facing surfaces; keyboard and screen-reader support. |
| Observability | Structured logging, distributed tracing, metrics, SLO dashboards, and alerting. |
| Maintainability | Modular architecture, CI/CD, automated tests (target 80%+ coverage), feature flags. |
| Internationalisation | Locale-aware formatting and multi-language support where applicable. |

## 12. Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Ad tech degrades page performance and Core Web Vitals | High | Lazy loading, CLS-safe slots, and performance monitoring (Ad Rendering epic). |
| Privacy non-compliance leads to fines or blocked demand | High | TCF v2 consent gating and non-personalised fallback. |
| Invalid traffic and brand-safety incidents | Medium | Third-party verification, IVT filtering, and blocklists. |
| Revenue discrepancies with demand partners | Medium | Automated reconciliation and discrepancy alerting. |

## 13. Definition of Ready & Definition of Done

### 13.1 Definition of Ready (DoR)
- Story has a clear description and acceptance criteria.
- Story is estimated and sized to fit within one sprint.
- Dependencies identified; design/UX available where needed.
- Testability and success metrics understood.

### 13.2 Definition of Done (DoD)
- Acceptance criteria met and verified.
- Code reviewed, merged, and covered by automated tests (target 80%+).
- Non-functional requirements (performance, security, accessibility) satisfied.
- Documentation and telemetry updated; demoed and accepted by the Product Owner.

## 14. Requirements Traceability Summary

| Epic Key | Epic | # Stories | Points | Releases |
| --- | --- | --- | --- | --- |
| ADREV-1 | Ad Server & Inventory | 15 | 68 | R1 |
| ADREV-2 | Direct Sales & Trafficking | 15 | 58 | R1 |
| ADREV-3 | Programmatic & Header Bidding | 15 | 63 | R1 |
| ADREV-4 | Audience Segmentation & Targeting | 15 | 78 | R1, R2 |
| ADREV-5 | Native & Sponsored Content | 15 | 68 | R2 |
| ADREV-6 | Brand Safety & Verification | 15 | 58 | R2, R3 |
| ADREV-7 | Consent & Privacy | 15 | 63 | R3 |
| ADREV-8 | Yield Optimization & Pricing | 15 | 78 | R3, R4 |
| ADREV-9 | Reporting, Billing & Reconciliation | 15 | 68 | R4 |
| ADREV-10 | Video & Connected TV Ads | 15 | 58 | R4 |
| ADREV-11 | First-party Data & CDP | 15 | 63 | R4, R5 |
| ADREV-12 | Ad Rendering & Performance | 15 | 78 | R5 |
| ADREV-13 | Creative Management & Preview | 15 | 29 | R5 |
| ADREV-14 | Forecasting & Inventory Prediction | 15 | 0 | R5 |

## 15. Glossary

| Term | Definition |
| --- | --- |
| Epic | A large body of work decomposed into user stories. |
| User Story | A small, independently valuable increment of functionality. |
| Story Point | A relative estimate of effort/complexity. |
| Velocity | Story points completed per sprint. |
| Sprint | A fixed 2-week timebox delivering a potentially shippable increment. |
| Backlog | Prioritised, not-yet-scheduled work; unplanned and not estimated. |
| Milestone / Release | A grouped set of outcomes delivered by a target date. |
| DoR / DoD | Definition of Ready / Definition of Done quality gates. |

## Appendix A — Jira Reference

| Item | Value |
| --- | --- |
| Jira project key | `ADREV` |
| Epics | 14 |
| User stories | 210 |
| Estimated stories | 189 |
| Completed sprints | 10 |
| Upcoming sprints | 1 |
| Total story points (estimated) | 830 |
| Board | https://pulseaipoc.atlassian.net/jira/software/projects/ADREV/boards |

---

*Generated 22 Jul 2026. This BRD mirrors the live Jira project `ADREV` (epics, stories, story points, sprints, and releases).*
