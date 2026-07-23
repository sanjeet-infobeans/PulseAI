# Business Requirements Document (BRD)
## Subscription & Paywall Platform — Subscription & Paywall Platform

### Document Control

| Field | Value |
| --- | --- |
| Document Title | BRD — Subscription & Paywall Platform |
| Project Key (Jira) | `SUBS` |
| Jira Project URL | https://pulseaipoc.atlassian.net/jira/software/projects/SUBS/boards |
| Version | 1.0 |
| Status | Baselined |
| Date | 22 Jul 2026 |
| Author | Delivery / Product Team |
| Delivery Methodology | Agile (Scrum) — 2-week sprints |
| Industry Domain | Media & Publishing |

## 1. Executive Summary

Establish a reader-revenue platform that converts anonymous readers into paying subscribers through an intelligent metered paywall, flexible plans, frictionless checkout, and strong retention, creating a sustainable, diversified revenue stream for the publisher.

This document defines the business requirements, scope, objectives, and agile delivery plan for the platform. Delivery is organised into **14 epics** and **210 user stories**, executed across **8 completed sprints**, **1 upcoming sprint**, and a maintained product backlog, aligned to **5 release milestones**.

## 2. Business Context & Problem Statement

The publisher is over-reliant on volatile advertising revenue and has no first-party subscription capability. There is no paywall, no plan management, no recurring billing, and no view of subscriber lifetime value. Reader relationships and revenue potential are being left on the table.

## 3. Business Objectives

1. Launch a metered paywall and convert 3% of engaged readers to registration within two cycles.
2. Achieve a paywall stop-to-subscription conversion rate of 2%+.
3. Reduce involuntary churn from failed payments to under 1.5% monthly.
4. Support monthly, annual, bundle, and corporate plans across multiple currencies.
5. Provide a real-time subscriber revenue (MRR/ARR) and retention dashboard.

## 4. Success Metrics & KPIs

| Metric | Target |
| --- | --- |
| Paywall conversion rate | > 2% |
| Monthly recurring revenue (MRR) | Growth target per cycle |
| Involuntary churn (failed payments) | < 1.5% / month |
| Voluntary monthly churn | < 4% |
| Checkout completion rate | > 60% |
| Subscriber LTV:CAC | > 3:1 |

## 5. Stakeholders & Personas

| Persona / Stakeholder | Role & Needs |
| --- | --- |
| Anonymous Reader | Hits the paywall; may register or subscribe. |
| Subscriber | Manages plan, payment, and entitlements self-service. |
| Growth/Marketing Manager | Runs offers, trials, and conversion experiments. |
| Finance/Billing Analyst | Owns billing, dunning, tax, and revenue reporting. |
| Support Agent | Resolves billing and entitlement issues. |
| Institutional Admin | Manages group/corporate seats. |

## 6. Scope

### 6.1 In Scope

- Metered/hard/soft paywall engine with server-side enforcement
- Plan catalogue, pricing, and multi-currency support
- Conversion checkout with multiple payment methods and SCA
- Recurring billing, invoicing, dunning, refunds, and proration
- Account/entitlement management and cross-device sync
- Trials, offers, promotions, referral, and gifting
- Registration/identity, retention/churn tooling, and analytics
- Tax/compliance/fraud, mobile in-app purchases, and support tooling

### 6.2 Out of Scope

- Editorial content creation (covered by the Digital Newsroom & CMS)
- Advertising monetisation (covered by the Advertising platform)
- General-ledger accounting system (integration only)
- Streaming/OTT entitlements beyond shared identity

## 7. Assumptions, Constraints & Dependencies

### 7.1 Assumptions

- A PCI-compliant payment gateway and PSP relationships are in place.
- Identity is shared with the wider platform via SSO.
- Tax calculation is provided by a specialist tax service.
- Reader engagement signals are available from the CMS/analytics.

### 7.2 Constraints

- Must be PCI-DSS compliant; no raw card data stored.
- Must support SCA/3-D Secure and regional payment regulations.
- Must honour GDPR/CCPA data-subject rights.

### 7.3 Dependencies

- Payment service provider(s) and wallets (Apple/Google Pay)
- Tax calculation service
- App Store / Google Play billing for IAP
- Fraud-scoring and identity services

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
| Delivered (completed sprints) | 168 | 80% | Yes | 8 closed sprints |
| Upcoming (planned) sprint | 21 | 10% | Yes | 1 future sprint |
| Product backlog (unplanned) | 21 | 10% | No (not estimated) | No sprint |
| **Total** | 210 | 100% | — | 9 sprints + backlog |

### 9.2 Sprint Plan

| Sprint | Dates | Stories | Story Points | Release | State |
| --- | --- | --- | --- | --- | --- |
| Sprint 1 | 01 Apr – 14 Apr 2026 | 21 | 90 | R1 – Foundation & MVP | Closed / Delivered |
| Sprint 2 | 15 Apr – 28 Apr 2026 | 21 | 91 | R1 – Foundation & MVP | Closed / Delivered |
| Sprint 3 | 29 Apr – 12 May 2026 | 21 | 91 | R2 – Core Experience | Closed / Delivered |
| Sprint 4 | 13 May – 26 May 2026 | 21 | 92 | R2 – Core Experience | Closed / Delivered |
| Sprint 5 | 27 May – 09 Jun 2026 | 21 | 92 | R3 – Scale & Monetize | Closed / Delivered |
| Sprint 6 | 10 Jun – 23 Jun 2026 | 21 | 92 | R3 – Scale & Monetize | Closed / Delivered |
| Sprint 7 | 24 Jun – 07 Jul 2026 | 21 | 94 | R4 – Optimize & Expand | Closed / Delivered |
| Sprint 8 | 08 Jul – 21 Jul 2026 | 21 | 94 | R4 – Optimize & Expand | Closed / Delivered |
| Sprint 9 | 22 Jul – 04 Aug 2026 | 21 | 94 | R5 – GA & Hardening | Upcoming (planned) |
| Backlog | Unscheduled | 21 | Not estimated | R5 – GA & Hardening | Backlog |

> **Velocity note:** 168 stories (~736 points) were delivered across 8 completed sprints, giving an average delivered velocity of **~92 points/sprint**. Completed story points per sprint are visible in the Jira Velocity report.

## 10. Epics & User Stories

The scope is decomposed into 14 epics. Each user story follows the INVEST principles and carries acceptance criteria and a Definition of Done in Jira. Story IDs below are the live Jira issue keys.

### 10.1 Epic 1: Paywall Engine & Metering  `SUBS-1`

**Objective:** Access control and metering.  
**Stories:** 15 · **Estimated points:** 68

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| SUBS-15 | Implement configurable metered paywall counter | 1 | Sprint 1 | R1 – Foundation & MVP | Done |
| SUBS-16 | Support hard, soft, and metered paywall modes | 2 | Sprint 1 | R1 – Foundation & MVP | Done |
| SUBS-17 | Add per-section and per-content-type meter rules | 2 | Sprint 1 | R1 – Foundation & MVP | Done |
| SUBS-18 | Implement server-side meter to prevent bypass | 3 | Sprint 1 | R1 – Foundation & MVP | Done |
| SUBS-19 | Support registration wall before hard paywall | 3 | Sprint 1 | R1 – Foundation & MVP | Done |
| SUBS-20 | Add dynamic paywall based on propensity-to-subscribe | 3 | Sprint 1 | R1 – Foundation & MVP | Done |
| SUBS-21 | Support meter reset windows (daily/monthly) | 5 | Sprint 1 | R1 – Foundation & MVP | Done |
| SUBS-22 | Enable paywall preview for editors | 5 | Sprint 1 | R1 – Foundation & MVP | Done |
| SUBS-23 | Add referrer-based meter exceptions (search/social) | 5 | Sprint 1 | R1 – Foundation & MVP | Done |
| SUBS-24 | Implement paywall message A/B testing | 8 | Sprint 1 | R1 – Foundation & MVP | Done |
| SUBS-25 | Support ad-free entitlement toggle for subscribers | 8 | Sprint 1 | R1 – Foundation & MVP | Done |
| SUBS-26 | Add device-level meter syncing for logged-in users | 13 | Sprint 1 | R1 – Foundation & MVP | Done |
| SUBS-27 | Implement paywall bypass tokens for campaigns | 2 | Sprint 1 | R1 – Foundation & MVP | Done |
| SUBS-28 | Support graceful paywall on slow entitlement lookups | 3 | Sprint 1 | R1 – Foundation & MVP | Done |
| SUBS-29 | Track paywall stop-rate and conversion funnel | 5 | Sprint 1 | R1 – Foundation & MVP | Done |

### 10.2 Epic 2: Subscription Plans & Pricing  `SUBS-2`

**Objective:** Plan catalog and pricing.  
**Stories:** 15 · **Estimated points:** 58

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| SUBS-30 | Build plan catalog with monthly and annual tiers | 3 | Sprint 1 | R1 – Foundation & MVP | Done |
| SUBS-31 | Support multi-currency pricing per region | 2 | Sprint 1 | R1 – Foundation & MVP | Done |
| SUBS-32 | Add introductory and standard price transitions | 5 | Sprint 1 | R1 – Foundation & MVP | Done |
| SUBS-33 | Implement bundle plans (news + puzzles + audio) | 8 | Sprint 1 | R1 – Foundation & MVP | Done |
| SUBS-34 | Support plan comparison table on marketing pages | 3 | Sprint 1 | R1 – Foundation & MVP | Done |
| SUBS-35 | Add student and concession pricing tiers | 1 | Sprint 1 | R1 – Foundation & MVP | Done |
| SUBS-36 | Implement price experimentation framework | 2 | Sprint 2 | R1 – Foundation & MVP | Done |
| SUBS-37 | Support plan grandfathering on price changes | 2 | Sprint 2 | R1 – Foundation & MVP | Done |
| SUBS-38 | Add metered-to-unlimited upgrade paths | 3 | Sprint 2 | R1 – Foundation & MVP | Done |
| SUBS-39 | Implement plan availability by geo and channel | 3 | Sprint 2 | R1 – Foundation & MVP | Done |
| SUBS-40 | Support add-on entitlements per plan | 3 | Sprint 2 | R1 – Foundation & MVP | Done |
| SUBS-41 | Add configurable trial length per plan | 5 | Sprint 2 | R1 – Foundation & MVP | Done |
| SUBS-42 | Implement plan lifecycle (draft/active/retired) | 5 | Sprint 2 | R1 – Foundation & MVP | Done |
| SUBS-43 | Support localized plan naming and descriptions | 5 | Sprint 2 | R1 – Foundation & MVP | Done |
| SUBS-44 | Track plan mix and ARPU reporting | 8 | Sprint 2 | R1 – Foundation & MVP | Done |

### 10.3 Epic 3: Checkout & Payment Processing  `SUBS-3`

**Objective:** Conversion checkout flow.  
**Stories:** 15 · **Estimated points:** 63

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| SUBS-45 | Build single-page checkout with plan summary | 8 | Sprint 2 | R1 – Foundation & MVP | Done |
| SUBS-46 | Integrate primary card payment gateway | 13 | Sprint 2 | R1 – Foundation & MVP | Done |
| SUBS-47 | Add PayPal and digital wallet options | 2 | Sprint 2 | R1 – Foundation & MVP | Done |
| SUBS-48 | Support Apple Pay and Google Pay express checkout | 3 | Sprint 2 | R1 – Foundation & MVP | Done |
| SUBS-49 | Implement SCA / 3-D Secure authentication | 5 | Sprint 2 | R1 – Foundation & MVP | Done |
| SUBS-50 | Add saved payment methods for returning users | 3 | Sprint 2 | R1 – Foundation & MVP | Done |
| SUBS-51 | Support coupon and promo code entry | 2 | Sprint 2 | R1 – Foundation & MVP | Done |
| SUBS-52 | Implement address and tax collection at checkout | 5 | Sprint 2 | R1 – Foundation & MVP | Done |
| SUBS-53 | Add checkout abandonment recovery emails | 8 | Sprint 2 | R1 – Foundation & MVP | Done |
| SUBS-54 | Support one-click upsell on confirmation | 3 | Sprint 2 | R1 – Foundation & MVP | Done |
| SUBS-55 | Implement idempotent payment submission | 1 | Sprint 2 | R1 – Foundation & MVP | Done |
| SUBS-56 | Add localized checkout language and currency | 2 | Sprint 2 | R1 – Foundation & MVP | Done |
| SUBS-57 | Support alternative regional payment methods | 2 | Sprint 3 | R2 – Core Experience | Done |
| SUBS-58 | Implement PCI-compliant tokenized card handling | 3 | Sprint 3 | R2 – Core Experience | Done |
| SUBS-59 | Track checkout funnel drop-off by step | 3 | Sprint 3 | R2 – Core Experience | Done |

### 10.4 Epic 4: Billing, Invoicing & Dunning  `SUBS-4`

**Objective:** Recurring billing lifecycle.  
**Stories:** 15 · **Estimated points:** 78

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| SUBS-60 | Implement recurring billing scheduler | 3 | Sprint 3 | R2 – Core Experience | Done |
| SUBS-61 | Support proration on upgrades and downgrades | 5 | Sprint 3 | R2 – Core Experience | Done |
| SUBS-62 | Add invoice and receipt generation with PDF | 5 | Sprint 3 | R2 – Core Experience | Done |
| SUBS-63 | Implement failed-payment retry (smart dunning) | 5 | Sprint 3 | R2 – Core Experience | Done |
| SUBS-64 | Support configurable dunning email sequences | 8 | Sprint 3 | R2 – Core Experience | Done |
| SUBS-65 | Add grace period before entitlement revocation | 8 | Sprint 3 | R2 – Core Experience | Done |
| SUBS-66 | Implement refunds and partial credits | 13 | Sprint 3 | R2 – Core Experience | Done |
| SUBS-67 | Support pause and resume of subscriptions | 2 | Sprint 3 | R2 – Core Experience | Done |
| SUBS-68 | Add automatic card-expiry updater | 3 | Sprint 3 | R2 – Core Experience | Done |
| SUBS-69 | Implement tax-inclusive vs exclusive invoicing | 5 | Sprint 3 | R2 – Core Experience | Done |
| SUBS-70 | Support billing anchor date alignment | 3 | Sprint 3 | R2 – Core Experience | Done |
| SUBS-71 | Add credit note handling for disputes | 2 | Sprint 3 | R2 – Core Experience | Done |
| SUBS-72 | Implement revenue recognition export | 5 | Sprint 3 | R2 – Core Experience | Done |
| SUBS-73 | Support currency conversion on cross-border billing | 8 | Sprint 3 | R2 – Core Experience | Done |
| SUBS-74 | Track involuntary churn from failed payments | 3 | Sprint 3 | R2 – Core Experience | Done |

### 10.5 Epic 5: Account & Entitlement Management  `SUBS-5`

**Objective:** Subscriber account center.  
**Stories:** 15 · **Estimated points:** 68

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| SUBS-75 | Build self-service account dashboard | 1 | Sprint 3 | R2 – Core Experience | Done |
| SUBS-76 | Show current plan, renewal date, and status | 2 | Sprint 3 | R2 – Core Experience | Done |
| SUBS-77 | Support plan change from the account center | 2 | Sprint 3 | R2 – Core Experience | Done |
| SUBS-78 | Add payment method management UI | 3 | Sprint 4 | R2 – Core Experience | Done |
| SUBS-79 | Implement entitlement resolution service | 3 | Sprint 4 | R2 – Core Experience | Done |
| SUBS-80 | Support cross-device entitlement sync | 3 | Sprint 4 | R2 – Core Experience | Done |
| SUBS-81 | Add subscription cancellation flow | 5 | Sprint 4 | R2 – Core Experience | Done |
| SUBS-82 | Implement download of billing history | 5 | Sprint 4 | R2 – Core Experience | Done |
| SUBS-83 | Support multiple entitlements per account | 5 | Sprint 4 | R2 – Core Experience | Done |
| SUBS-84 | Add email and password change with verification | 8 | Sprint 4 | R2 – Core Experience | Done |
| SUBS-85 | Implement entitlement API for downstream apps | 8 | Sprint 4 | R2 – Core Experience | Done |
| SUBS-86 | Support session management and device list | 13 | Sprint 4 | R2 – Core Experience | Done |
| SUBS-87 | Add data export for account portability | 2 | Sprint 4 | R2 – Core Experience | Done |
| SUBS-88 | Implement account deletion with compliance | 3 | Sprint 4 | R2 – Core Experience | Done |
| SUBS-89 | Track account-center engagement metrics | 5 | Sprint 4 | R2 – Core Experience | Done |

### 10.6 Epic 6: Trials, Offers & Promotions  `SUBS-6`

**Objective:** Acquisition offers.  
**Stories:** 15 · **Estimated points:** 58

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| SUBS-90 | Implement free-trial enrollment and conversion | 3 | Sprint 4 | R2 – Core Experience | Done |
| SUBS-91 | Support time-limited promotional pricing | 2 | Sprint 4 | R2 – Core Experience | Done |
| SUBS-92 | Add campaign-specific landing pages | 5 | Sprint 4 | R2 – Core Experience | Done |
| SUBS-93 | Implement promo code generation and limits | 8 | Sprint 4 | R2 – Core Experience | Done |
| SUBS-94 | Support win-back offers for lapsed subscribers | 3 | Sprint 4 | R2 – Core Experience | Done |
| SUBS-95 | Add referral program with rewards | 1 | Sprint 4 | R2 – Core Experience | Done |
| SUBS-96 | Implement seasonal discount campaigns | 2 | Sprint 4 | R2 – Core Experience | Done |
| SUBS-97 | Support first-month-free with auto-convert | 2 | Sprint 4 | R2 – Core Experience | Done |
| SUBS-98 | Add offer eligibility rules engine | 3 | Sprint 4 | R2 – Core Experience | Done |
| SUBS-99 | Implement holdout groups for offer testing | 3 | Sprint 5 | R3 – Scale & Monetize | Done |
| SUBS-100 | Support partner and affiliate offer codes | 3 | Sprint 5 | R3 – Scale & Monetize | Done |
| SUBS-101 | Add stackable vs exclusive discount logic | 5 | Sprint 5 | R3 – Scale & Monetize | Done |
| SUBS-102 | Implement offer expiry and reminder emails | 5 | Sprint 5 | R3 – Scale & Monetize | Done |
| SUBS-103 | Support one-time vs recurring discounts | 5 | Sprint 5 | R3 – Scale & Monetize | Done |
| SUBS-104 | Track offer redemption and incrementality | 8 | Sprint 5 | R3 – Scale & Monetize | Done |

### 10.7 Epic 7: Registration & Identity  `SUBS-7`

**Objective:** Reader accounts and auth.  
**Stories:** 15 · **Estimated points:** 63

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| SUBS-105 | Implement email/password registration | 8 | Sprint 5 | R3 – Scale & Monetize | Done |
| SUBS-106 | Add social login (Google, Apple, Facebook) | 13 | Sprint 5 | R3 – Scale & Monetize | Done |
| SUBS-107 | Support passwordless magic-link sign-in | 2 | Sprint 5 | R3 – Scale & Monetize | Done |
| SUBS-108 | Implement single sign-on across owned properties | 3 | Sprint 5 | R3 – Scale & Monetize | Done |
| SUBS-109 | Add email verification and re-verification | 5 | Sprint 5 | R3 – Scale & Monetize | Done |
| SUBS-110 | Support progressive profiling of readers | 3 | Sprint 5 | R3 – Scale & Monetize | Done |
| SUBS-111 | Implement password reset and account recovery | 2 | Sprint 5 | R3 – Scale & Monetize | Done |
| SUBS-112 | Add multi-factor authentication option | 5 | Sprint 5 | R3 – Scale & Monetize | Done |
| SUBS-113 | Support merge of duplicate reader accounts | 8 | Sprint 5 | R3 – Scale & Monetize | Done |
| SUBS-114 | Implement consent capture at registration | 3 | Sprint 5 | R3 – Scale & Monetize | Done |
| SUBS-115 | Add CAPTCHA and bot-signup prevention | 1 | Sprint 5 | R3 – Scale & Monetize | Done |
| SUBS-116 | Support guest checkout to account linking | 2 | Sprint 5 | R3 – Scale & Monetize | Done |
| SUBS-117 | Implement identity graph for anonymous-to-known | 2 | Sprint 5 | R3 – Scale & Monetize | Done |
| SUBS-118 | Add login rate limiting and lockout | 3 | Sprint 5 | R3 – Scale & Monetize | Done |
| SUBS-119 | Track registration-to-subscription conversion | 3 | Sprint 5 | R3 – Scale & Monetize | Done |

### 10.8 Epic 8: Retention & Churn Prevention  `SUBS-8`

**Objective:** Keep subscribers engaged.  
**Stories:** 15 · **Estimated points:** 78

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| SUBS-120 | Build churn-risk scoring model integration | 3 | Sprint 6 | R3 – Scale & Monetize | Done |
| SUBS-121 | Implement cancellation save flow with offers | 5 | Sprint 6 | R3 – Scale & Monetize | Done |
| SUBS-122 | Add pause-instead-of-cancel option | 5 | Sprint 6 | R3 – Scale & Monetize | Done |
| SUBS-123 | Support downgrade-instead-of-cancel path | 5 | Sprint 6 | R3 – Scale & Monetize | Done |
| SUBS-124 | Implement engagement-based re-onboarding emails | 8 | Sprint 6 | R3 – Scale & Monetize | Done |
| SUBS-125 | Add habit-forming feature nudges | 8 | Sprint 6 | R3 – Scale & Monetize | Done |
| SUBS-126 | Support win-back campaigns post-cancellation | 13 | Sprint 6 | R3 – Scale & Monetize | Done |
| SUBS-127 | Implement subscriber milestone celebrations | 2 | Sprint 6 | R3 – Scale & Monetize | Done |
| SUBS-128 | Add personalized content digests for retention | 3 | Sprint 6 | R3 – Scale & Monetize | Done |
| SUBS-129 | Support proactive outreach to at-risk cohorts | 5 | Sprint 6 | R3 – Scale & Monetize | Done |
| SUBS-130 | Implement NPS and satisfaction surveys | 3 | Sprint 6 | R3 – Scale & Monetize | Done |
| SUBS-131 | Add renewal reminder communications | 2 | Sprint 6 | R3 – Scale & Monetize | Done |
| SUBS-132 | Support loyalty benefits for long-tenure subs | 5 | Sprint 6 | R3 – Scale & Monetize | Done |
| SUBS-133 | Implement feedback capture on cancellation | 8 | Sprint 6 | R3 – Scale & Monetize | Done |
| SUBS-134 | Track retention curves and LTV by cohort | 3 | Sprint 6 | R3 – Scale & Monetize | Done |

### 10.9 Epic 9: Corporate & Group Subscriptions  `SUBS-9`

**Objective:** B2B and institutional.  
**Stories:** 15 · **Estimated points:** 68

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| SUBS-135 | Implement group/organization account model | 1 | Sprint 6 | R3 – Scale & Monetize | Done |
| SUBS-136 | Support seat-based licensing and allocation | 2 | Sprint 6 | R3 – Scale & Monetize | Done |
| SUBS-137 | Add IP-range authentication for institutions | 2 | Sprint 6 | R3 – Scale & Monetize | Done |
| SUBS-138 | Implement admin console for group managers | 3 | Sprint 6 | R3 – Scale & Monetize | Done |
| SUBS-139 | Support bulk seat provisioning via CSV | 3 | Sprint 6 | R3 – Scale & Monetize | Done |
| SUBS-140 | Add SSO/SAML for enterprise customers | 3 | Sprint 6 | R3 – Scale & Monetize | Done |
| SUBS-141 | Implement usage reporting per organization | 5 | Sprint 7 | R4 – Optimize & Expand | Done |
| SUBS-142 | Support invoicing and PO-based billing | 5 | Sprint 7 | R4 – Optimize & Expand | Done |
| SUBS-143 | Add domain-based auto-enrollment | 5 | Sprint 7 | R4 – Optimize & Expand | Done |
| SUBS-144 | Implement seat reclamation for inactive users | 8 | Sprint 7 | R4 – Optimize & Expand | Done |
| SUBS-145 | Support tiered volume pricing | 8 | Sprint 7 | R4 – Optimize & Expand | Done |
| SUBS-146 | Add contract and renewal management | 13 | Sprint 7 | R4 – Optimize & Expand | Done |
| SUBS-147 | Implement group entitlement overrides | 2 | Sprint 7 | R4 – Optimize & Expand | Done |
| SUBS-148 | Support multi-admin roles and permissions | 3 | Sprint 7 | R4 – Optimize & Expand | Done |
| SUBS-149 | Track institutional engagement and renewals | 5 | Sprint 7 | R4 – Optimize & Expand | Done |

### 10.10 Epic 10: Gifting & Redemption  `SUBS-10`

**Objective:** Gift subscriptions.  
**Stories:** 15 · **Estimated points:** 58

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| SUBS-150 | Implement gift subscription purchase flow | 3 | Sprint 7 | R4 – Optimize & Expand | Done |
| SUBS-151 | Support scheduled gift delivery by date | 2 | Sprint 7 | R4 – Optimize & Expand | Done |
| SUBS-152 | Add gift redemption with code entry | 5 | Sprint 7 | R4 – Optimize & Expand | Done |
| SUBS-153 | Implement personalized gift messages | 8 | Sprint 7 | R4 – Optimize & Expand | Done |
| SUBS-154 | Support gift-to-recurring conversion prompts | 3 | Sprint 7 | R4 – Optimize & Expand | Done |
| SUBS-155 | Add printable and e-gift card options | 1 | Sprint 7 | R4 – Optimize & Expand | Done |
| SUBS-156 | Implement gift purchase for existing subscribers | 2 | Sprint 7 | R4 – Optimize & Expand | Done |
| SUBS-157 | Support corporate bulk gifting | 2 | Sprint 7 | R4 – Optimize & Expand | Done |
| SUBS-158 | Add gift refund and reissue handling | 3 | Sprint 7 | R4 – Optimize & Expand | Done |
| SUBS-159 | Implement gift expiry policy and reminders | 3 | Sprint 7 | R4 – Optimize & Expand | Done |
| SUBS-160 | Support multi-recipient gift orders | 3 | Sprint 7 | R4 – Optimize & Expand | Done |
| SUBS-161 | Add gifter dashboard to track redemptions | 5 | Sprint 7 | R4 – Optimize & Expand | Done |
| SUBS-162 | Implement anti-fraud checks on gift purchases | 5 | Sprint 8 | R4 – Optimize & Expand | Done |
| SUBS-163 | Support localized gifting by region | 5 | Sprint 8 | R4 – Optimize & Expand | Done |
| SUBS-164 | Track gift-driven new subscriber acquisition | 8 | Sprint 8 | R4 – Optimize & Expand | Done |

### 10.11 Epic 11: Subscriber Analytics & Reporting  `SUBS-11`

**Objective:** Revenue intelligence.  
**Stories:** 15 · **Estimated points:** 63

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| SUBS-165 | Build MRR/ARR executive dashboard | 8 | Sprint 8 | R4 – Optimize & Expand | Done |
| SUBS-166 | Add acquisition funnel analytics | 13 | Sprint 8 | R4 – Optimize & Expand | Done |
| SUBS-167 | Implement cohort retention reporting | 2 | Sprint 8 | R4 – Optimize & Expand | Done |
| SUBS-168 | Support churn and reactivation dashboards | 3 | Sprint 8 | R4 – Optimize & Expand | Done |
| SUBS-169 | Add LTV and CAC reporting | 5 | Sprint 8 | R4 – Optimize & Expand | Done |
| SUBS-170 | Implement subscription movement (MRR waterfall) | 3 | Sprint 8 | R4 – Optimize & Expand | Done |
| SUBS-171 | Support paywall conversion analytics | 2 | Sprint 8 | R4 – Optimize & Expand | Done |
| SUBS-172 | Add plan-mix and ARPU trends | 5 | Sprint 8 | R4 – Optimize & Expand | Done |
| SUBS-173 | Implement offer performance reporting | 8 | Sprint 8 | R4 – Optimize & Expand | Done |
| SUBS-174 | Support export to BI and data warehouse | 3 | Sprint 8 | R4 – Optimize & Expand | Done |
| SUBS-175 | Add real-time subscription event stream | 1 | Sprint 8 | R4 – Optimize & Expand | Done |
| SUBS-176 | Implement forecast of subscriber growth | 2 | Sprint 8 | R4 – Optimize & Expand | Done |
| SUBS-177 | Support attribution of subs to content | 2 | Sprint 8 | R4 – Optimize & Expand | Done |
| SUBS-178 | Add anomaly detection on revenue metrics | 3 | Sprint 8 | R4 – Optimize & Expand | Done |
| SUBS-179 | Track engagement-to-retention correlation | 3 | Sprint 8 | R4 – Optimize & Expand | Done |

### 10.12 Epic 12: Tax, Compliance & Fraud  `SUBS-12`

**Objective:** Legal and risk.  
**Stories:** 15 · **Estimated points:** 78

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| SUBS-180 | Implement automated sales-tax/VAT calculation | 3 | Sprint 8 | R4 – Optimize & Expand | Done |
| SUBS-181 | Support tax-exempt customer handling | 5 | Sprint 8 | R4 – Optimize & Expand | Done |
| SUBS-182 | Add GDPR/CCPA data subject request tooling | 5 | Sprint 8 | R4 – Optimize & Expand | Done |
| SUBS-183 | Implement PCI-DSS compliant data handling | 5 | Sprint 9 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| SUBS-184 | Support Strong Customer Authentication mandates | 8 | Sprint 9 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| SUBS-185 | Add fraud scoring on checkout | 8 | Sprint 9 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| SUBS-186 | Implement chargeback and dispute management | 13 | Sprint 9 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| SUBS-187 | Support age and region purchase restrictions | 2 | Sprint 9 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| SUBS-188 | Add audit logging for financial operations | 3 | Sprint 9 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| SUBS-189 | Implement consent and cookie compliance | 5 | Sprint 9 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| SUBS-190 | Support data retention and deletion policies | 3 | Sprint 9 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| SUBS-191 | Add velocity checks for card testing attacks | 2 | Sprint 9 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| SUBS-192 | Implement invoice legal-field compliance by country | 5 | Sprint 9 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| SUBS-193 | Support sanctions and denied-party screening | 8 | Sprint 9 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| SUBS-194 | Track fraud loss and false-positive rates | 3 | Sprint 9 (Upcoming) | R5 – GA & Hardening | To Do (planned) |

### 10.13 Epic 13: Mobile App Subscriptions (IAP)  `SUBS-13`

**Objective:** In-app purchase integration.  
**Stories:** 15 · **Estimated points:** 29

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| SUBS-195 | Integrate Apple App Store in-app purchases | 1 | Sprint 9 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| SUBS-196 | Integrate Google Play Billing subscriptions | 2 | Sprint 9 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| SUBS-197 | Implement receipt validation server-side | 2 | Sprint 9 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| SUBS-198 | Support entitlement sync across web and app | 3 | Sprint 9 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| SUBS-199 | Add restore-purchases flow | 3 | Sprint 9 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| SUBS-200 | Implement IAP price tier mapping | 3 | Sprint 9 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| SUBS-201 | Support upgrade/downgrade within app stores | 5 | Sprint 9 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| SUBS-202 | Add server-to-server notification handling | 5 | Sprint 9 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| SUBS-203 | Implement grace-period and billing-retry sync | 5 | Sprint 9 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| SUBS-204 | Support promotional offers via StoreKit | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| SUBS-205 | Add reconciliation of store payouts | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| SUBS-206 | Implement refund notification handling | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| SUBS-207 | Support family sharing entitlements | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| SUBS-208 | Add cross-platform single-account entitlement | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| SUBS-209 | Track app-store vs web subscription mix | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |

### 10.14 Epic 14: Customer Support & Self-service  `SUBS-14`

**Objective:** Support tooling.  
**Stories:** 15 · **Estimated points:** 0

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| SUBS-210 | Build help center with searchable articles | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| SUBS-211 | Add subscription troubleshooting self-service | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| SUBS-212 | Implement agent console with account lookup | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| SUBS-213 | Support agent-initiated refunds and credits | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| SUBS-214 | Add live chat and chatbot triage | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| SUBS-215 | Implement ticketing integration for escalations | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| SUBS-216 | Support impersonation for account debugging | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| SUBS-217 | Add canned responses for common issues | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| SUBS-218 | Implement entitlement repair tooling | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| SUBS-219 | Support proactive status/incident banners | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| SUBS-220 | Add satisfaction survey after support | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| SUBS-221 | Implement callback and email support queues | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| SUBS-222 | Support macros for billing dispute handling | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| SUBS-223 | Add knowledge-base analytics for gaps | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| SUBS-224 | Track first-contact resolution and CSAT | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |

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
| Payment failures drive involuntary churn | High | Smart dunning, card-updater, and grace periods (Billing epic). |
| Paywall too aggressive harms traffic and SEO | High | Referrer exceptions, propensity-based metering, and A/B testing. |
| Fraud and card-testing attacks | Medium | Velocity checks, fraud scoring, and SCA enforcement. |
| Tax/regulatory non-compliance across regions | Medium | Automated tax service and country-specific invoice compliance. |

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
| SUBS-1 | Paywall Engine & Metering | 15 | 68 | R1 |
| SUBS-2 | Subscription Plans & Pricing | 15 | 58 | R1 |
| SUBS-3 | Checkout & Payment Processing | 15 | 63 | R1, R2 |
| SUBS-4 | Billing, Invoicing & Dunning | 15 | 78 | R2 |
| SUBS-5 | Account & Entitlement Management | 15 | 68 | R2 |
| SUBS-6 | Trials, Offers & Promotions | 15 | 58 | R2, R3 |
| SUBS-7 | Registration & Identity | 15 | 63 | R3 |
| SUBS-8 | Retention & Churn Prevention | 15 | 78 | R3 |
| SUBS-9 | Corporate & Group Subscriptions | 15 | 68 | R3, R4 |
| SUBS-10 | Gifting & Redemption | 15 | 58 | R4 |
| SUBS-11 | Subscriber Analytics & Reporting | 15 | 63 | R4 |
| SUBS-12 | Tax, Compliance & Fraud | 15 | 78 | R4, R5 |
| SUBS-13 | Mobile App Subscriptions (IAP) | 15 | 29 | R5 |
| SUBS-14 | Customer Support & Self-service | 15 | 0 | R5 |

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
| Jira project key | `SUBS` |
| Epics | 14 |
| User stories | 210 |
| Estimated stories | 189 |
| Completed sprints | 8 |
| Upcoming sprints | 1 |
| Total story points (estimated) | 830 |
| Board | https://pulseaipoc.atlassian.net/jira/software/projects/SUBS/boards |

---

*Generated 22 Jul 2026. This BRD mirrors the live Jira project `SUBS` (epics, stories, story points, sprints, and releases).*
