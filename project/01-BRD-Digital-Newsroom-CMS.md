# Business Requirements Document (BRD)
## Digital Newsroom & CMS — Digital Newsroom & Content Management System

### Document Control

| Field | Value |
| --- | --- |
| Document Title | BRD — Digital Newsroom & CMS |
| Project Key (Jira) | `NEWS` |
| Jira Project URL | https://pulseaipoc.atlassian.net/jira/software/projects/NEWS/boards |
| Version | 1.0 |
| Status | Baselined |
| Date | 22 Jul 2026 |
| Author | Delivery / Product Team |
| Delivery Methodology | Agile (Scrum) — 2-week sprints |
| Industry Domain | Media & Publishing |

## 1. Executive Summary

Build a modern, digital-first newsroom and content management platform that lets editorial teams create, curate, and distribute high-quality journalism across web, apps, and syndication channels at the speed of breaking news, while maximising audience reach and search discoverability.

This document defines the business requirements, scope, objectives, and agile delivery plan for the platform. Delivery is organised into **14 epics** and **210 user stories**, executed across **9 completed sprints**, **1 upcoming sprint**, and a maintained product backlog, aligned to **5 release milestones**.

## 2. Business Context & Problem Statement

The organisation's legacy CMS cannot support real-time collaborative editing, live coverage, or multi-channel publishing. Editorial workflows are manual and slow, SEO is inconsistent, and there is no unified view of content performance. This limits audience growth, slows breaking-news response, and increases operational cost.

## 3. Business Objectives

1. Reduce time-to-publish for breaking news to under 5 minutes from draft to live.
2. Increase organic search traffic by 30% within two release cycles through structured SEO.
3. Enable simultaneous multi-channel publishing (web, apps, Apple News, RSS, syndication) from a single source.
4. Provide the newsroom with real-time content performance analytics to guide editorial decisions.
5. Achieve WCAG 2.2 AA accessibility compliance across all reader-facing surfaces.

## 4. Success Metrics & KPIs

| Metric | Target |
| --- | --- |
| Time-to-publish (breaking news) | < 5 minutes |
| Organic search sessions | +30% over baseline |
| Homepage editorial update latency | < 30 seconds |
| Article page LCP (Core Web Vitals) | < 2.5s at p75 |
| Accessibility compliance | WCAG 2.2 AA, 0 critical issues |
| Editorial workflow SLA adherence | > 95% |

## 5. Stakeholders & Personas

| Persona / Stakeholder | Role & Needs |
| --- | --- |
| Reporter/Author | Creates and edits stories, covers live events, needs fast reliable authoring. |
| Section Editor | Reviews, approves, and curates section fronts and the homepage. |
| Copy Editor | Performs copy-editing and fact-check sign-off. |
| SEO/Audience Manager | Optimises discoverability and monitors performance. |
| Reader | Consumes content across devices; expects fast, accessible pages. |
| Platform Engineer | Operates and scales the platform reliably. |

## 6. Scope

### 6.1 In Scope

- Rich-text article authoring with collaborative editing and versioning
- Digital asset management for images, video, and audio
- Configurable editorial workflow, approvals, and editorial calendar
- Homepage and section-front curation with scheduling
- Live blogging and breaking-news alerting
- SEO, structured data, and multi-channel syndication
- Reader comments, moderation, newsletters, and on-site search
- Editorial analytics, accessibility, localisation, and platform infrastructure

### 6.2 Out of Scope

- Print production and pagination systems
- Subscription billing and paywall (covered by the Subscription & Paywall Platform)
- Advertising and monetisation (covered by the Advertising & Programmatic Revenue platform)
- Video streaming/OTT delivery (covered by the Content Streaming & OTT platform)
- Third-party newsroom HR or payroll systems

## 7. Assumptions, Constraints & Dependencies

### 7.1 Assumptions

- A cloud-native hosting environment and CI/CD tooling are available.
- Editorial staff will be trained on the new workflow before go-live.
- Existing content will be migrated under a separate migration workstream.
- Single sign-on identity is provided by the enterprise IdP.

### 7.2 Constraints

- Must meet Core Web Vitals and accessibility standards from first release.
- Must support election-night and breaking-news traffic spikes.
- Editorial data residency and privacy regulations apply.

### 7.3 Dependencies

- Enterprise SSO / identity provider
- CDN and image-optimisation provider
- Search infrastructure (managed search service)
- Email/newsletter delivery provider

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
| Delivered (completed sprints) | 168 | 80% | Yes | 9 closed sprints |
| Upcoming (planned) sprint | 21 | 10% | Yes | 1 future sprint |
| Product backlog (unplanned) | 21 | 10% | No (not estimated) | No sprint |
| **Total** | 210 | 100% | — | 10 sprints + backlog |

### 9.2 Sprint Plan

| Sprint | Dates | Stories | Story Points | Release | State |
| --- | --- | --- | --- | --- | --- |
| Sprint 1 | 18 Mar – 31 Mar 2026 | 19 | 86 | R1 – Foundation & MVP | Closed / Delivered |
| Sprint 2 | 01 Apr – 14 Apr 2026 | 19 | 81 | R1 – Foundation & MVP | Closed / Delivered |
| Sprint 3 | 15 Apr – 28 Apr 2026 | 19 | 84 | R2 – Core Experience | Closed / Delivered |
| Sprint 4 | 29 Apr – 12 May 2026 | 19 | 87 | R2 – Core Experience | Closed / Delivered |
| Sprint 5 | 13 May – 26 May 2026 | 19 | 86 | R3 – Scale & Monetize | Closed / Delivered |
| Sprint 6 | 27 May – 09 Jun 2026 | 19 | 84 | R3 – Scale & Monetize | Closed / Delivered |
| Sprint 7 | 10 Jun – 23 Jun 2026 | 18 | 84 | R4 – Optimize & Expand | Closed / Delivered |
| Sprint 8 | 24 Jun – 07 Jul 2026 | 18 | 68 | R4 – Optimize & Expand | Closed / Delivered |
| Sprint 9 | 08 Jul – 21 Jul 2026 | 18 | 76 | R5 – GA & Hardening | Closed / Delivered |
| Sprint 10 | 22 Jul – 04 Aug 2026 | 21 | 94 | R5 – GA & Hardening | Upcoming (planned) |
| Backlog | Unscheduled | 21 | Not estimated | R5 – GA & Hardening | Backlog |

> **Velocity note:** 168 stories (~736 points) were delivered across 9 completed sprints, giving an average delivered velocity of **~81 points/sprint**. Completed story points per sprint are visible in the Jira Velocity report.

## 10. Epics & User Stories

The scope is decomposed into 14 epics. Each user story follows the INVEST principles and carries acceptance criteria and a Definition of Done in Jira. Story IDs below are the live Jira issue keys.

### 10.1 Epic 1: Editorial CMS Core  `NEWS-1`

**Objective:** Article authoring, editing, and versioning.  
**Stories:** 15 · **Estimated points:** 68

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| NEWS-15 | Create rich-text article editor with inline formatting toolbar | 1 | Sprint 1 | R1 – Foundation & MVP | Done |
| NEWS-16 | Support draft auto-save every 30 seconds without data loss | 2 | Sprint 1 | R1 – Foundation & MVP | Done |
| NEWS-17 | Enable article version history with diff and rollback | 2 | Sprint 1 | R1 – Foundation & MVP | Done |
| NEWS-18 | Add co-authoring with real-time collaborative editing | 3 | Sprint 1 | R1 – Foundation & MVP | Done |
| NEWS-19 | Support scheduled publishing with timezone awareness | 3 | Sprint 1 | R1 – Foundation & MVP | Done |
| NEWS-20 | Add embargo controls for pre-published articles | 3 | Sprint 1 | R1 – Foundation & MVP | Done |
| NEWS-21 | Implement article templates for common story formats | 5 | Sprint 1 | R1 – Foundation & MVP | Done |
| NEWS-22 | Support inline image, pull-quote, and callout blocks | 5 | Sprint 1 | R1 – Foundation & MVP | Done |
| NEWS-23 | Add word count, reading time, and readability indicators | 5 | Sprint 1 | R1 – Foundation & MVP | Done |
| NEWS-24 | Enable article cloning for follow-up stories | 8 | Sprint 1 | R1 – Foundation & MVP | Done |
| NEWS-25 | Support structured bylines with multiple contributors | 8 | Sprint 1 | R1 – Foundation & MVP | Done |
| NEWS-26 | Add editorial notes visible only to internal staff | 13 | Sprint 1 | R1 – Foundation & MVP | Done |
| NEWS-27 | Implement content locking to prevent concurrent overwrites | 2 | Sprint 1 | R1 – Foundation & MVP | Done |
| NEWS-28 | Support unpublish and re-publish with audit trail | 3 | Sprint 1 | R1 – Foundation & MVP | Done |
| NEWS-29 | Add slug generation and manual URL override | 5 | Sprint 1 | R1 – Foundation & MVP | Done |

### 10.2 Epic 2: Rich Media & Asset Management  `NEWS-2`

**Objective:** DAM for images, video, audio.  
**Stories:** 15 · **Estimated points:** 58

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| NEWS-30 | Build central media library with folders and tags | 3 | Sprint 1 | R1 – Foundation & MVP | Done |
| NEWS-31 | Support drag-and-drop bulk image upload | 2 | Sprint 1 | R1 – Foundation & MVP | Done |
| NEWS-32 | Auto-generate responsive image renditions on upload | 5 | Sprint 1 | R1 – Foundation & MVP | Done |
| NEWS-33 | Add image cropping and focal-point selection | 8 | Sprint 1 | R1 – Foundation & MVP | Done |
| NEWS-34 | Store and enforce photo credit and rights metadata | 3 | Sprint 2 | R1 – Foundation & MVP | Done |
| NEWS-35 | Integrate stock photo provider search inline | 1 | Sprint 2 | R1 – Foundation & MVP | Done |
| NEWS-36 | Support video upload with automatic thumbnail extraction | 2 | Sprint 2 | R1 – Foundation & MVP | Done |
| NEWS-37 | Add audio clip embedding for podcast segments | 2 | Sprint 2 | R1 – Foundation & MVP | Done |
| NEWS-38 | Implement alt-text prompts required before publish | 3 | Sprint 2 | R1 – Foundation & MVP | Done |
| NEWS-39 | Detect and warn on duplicate asset uploads | 3 | Sprint 2 | R1 – Foundation & MVP | Done |
| NEWS-40 | Add expiring-rights alerts for licensed imagery | 3 | Sprint 2 | R1 – Foundation & MVP | Done |
| NEWS-41 | Support caption and photographer attribution fields | 5 | Sprint 2 | R1 – Foundation & MVP | Done |
| NEWS-42 | Enable asset usage report across published articles | 5 | Sprint 2 | R1 – Foundation & MVP | Done |
| NEWS-43 | Add CDN purge trigger on asset replacement | 5 | Sprint 2 | R1 – Foundation & MVP | Done |
| NEWS-44 | Support animated GIF and WebP delivery | 8 | Sprint 2 | R1 – Foundation & MVP | Done |

### 10.3 Epic 3: Editorial Workflow & Approvals  `NEWS-3`

**Objective:** Newsroom review and sign-off.  
**Stories:** 15 · **Estimated points:** 63

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| NEWS-45 | Define configurable editorial workflow states | 8 | Sprint 2 | R1 – Foundation & MVP | Done |
| NEWS-46 | Route drafts to section editors for review | 13 | Sprint 2 | R1 – Foundation & MVP | Done |
| NEWS-47 | Add copy-edit stage with tracked changes | 2 | Sprint 2 | R1 – Foundation & MVP | Done |
| NEWS-48 | Implement legal review flag for sensitive stories | 3 | Sprint 2 | R1 – Foundation & MVP | Done |
| NEWS-49 | Support fact-check checklist before approval | 5 | Sprint 2 | R1 – Foundation & MVP | Done |
| NEWS-50 | Add assignment and reassignment of stories to desks | 3 | Sprint 2 | R1 – Foundation & MVP | Done |
| NEWS-51 | Notify authors on status change and comments | 2 | Sprint 2 | R1 – Foundation & MVP | Done |
| NEWS-52 | Build editorial calendar with planned coverage | 5 | Sprint 2 | R1 – Foundation & MVP | Done |
| NEWS-53 | Add story pitching and assignment desk queue | 8 | Sprint 3 | R2 – Core Experience | Done |
| NEWS-54 | Support kill/spike workflow with reason capture | 3 | Sprint 3 | R2 – Core Experience | Done |
| NEWS-55 | Track SLA timers for review turnaround | 1 | Sprint 3 | R2 – Core Experience | Done |
| NEWS-56 | Add multi-approver sign-off for investigations | 2 | Sprint 3 | R2 – Core Experience | Done |
| NEWS-57 | Show workload dashboard per editor and desk | 2 | Sprint 3 | R2 – Core Experience | Done |
| NEWS-58 | Support quick-publish path for breaking news | 3 | Sprint 3 | R2 – Core Experience | Done |
| NEWS-59 | Log full approval audit trail per article | 3 | Sprint 3 | R2 – Core Experience | Done |

### 10.4 Epic 4: Homepage & Section Curation  `NEWS-4`

**Objective:** Front-page and section layout.  
**Stories:** 15 · **Estimated points:** 78

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| NEWS-60 | Build drag-and-drop homepage layout editor | 3 | Sprint 3 | R2 – Core Experience | Done |
| NEWS-61 | Support pinned and auto-populated story slots | 5 | Sprint 3 | R2 – Core Experience | Done |
| NEWS-62 | Add section front curation per vertical | 5 | Sprint 3 | R2 – Core Experience | Done |
| NEWS-63 | Enable scheduled homepage takeovers | 5 | Sprint 3 | R2 – Core Experience | Done |
| NEWS-64 | Preview homepage across breakpoints before publish | 8 | Sprint 3 | R2 – Core Experience | Done |
| NEWS-65 | Support A/B testing of headline variants on homepage | 8 | Sprint 3 | R2 – Core Experience | Done |
| NEWS-66 | Add trending module driven by real-time analytics | 13 | Sprint 3 | R2 – Core Experience | Done |
| NEWS-67 | Implement editor override of algorithmic modules | 2 | Sprint 3 | R2 – Core Experience | Done |
| NEWS-68 | Support regional homepage variants by geo | 3 | Sprint 3 | R2 – Core Experience | Done |
| NEWS-69 | Add curated collections and topic hubs | 5 | Sprint 3 | R2 – Core Experience | Done |
| NEWS-70 | Enable breaking-news banner across all pages | 3 | Sprint 3 | R2 – Core Experience | Done |
| NEWS-71 | Support sponsored slot placement with labeling | 2 | Sprint 3 | R2 – Core Experience | Done |
| NEWS-72 | Add homepage change history and revert | 5 | Sprint 4 | R2 – Core Experience | Done |
| NEWS-73 | Show live preview of story performance in curation UI | 8 | Sprint 4 | R2 – Core Experience | Done |
| NEWS-74 | Support dark-launch of homepage redesigns | 3 | Sprint 4 | R2 – Core Experience | Done |

### 10.5 Epic 5: Live Blogging & Breaking News  `NEWS-5`

**Objective:** Real-time coverage tools.  
**Stories:** 15 · **Estimated points:** 68

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| NEWS-75 | Create live blog with reverse-chronological updates | 1 | Sprint 4 | R2 – Core Experience | Done |
| NEWS-76 | Support key-events pinning within a live blog | 2 | Sprint 4 | R2 – Core Experience | Done |
| NEWS-77 | Add real-time push of new entries to readers | 2 | Sprint 4 | R2 – Core Experience | Done |
| NEWS-78 | Enable multiple reporters posting to one live blog | 3 | Sprint 4 | R2 – Core Experience | Done |
| NEWS-79 | Support embedding social posts into live entries | 3 | Sprint 4 | R2 – Core Experience | Done |
| NEWS-80 | Add automatic timestamps with relative time display | 3 | Sprint 4 | R2 – Core Experience | Done |
| NEWS-81 | Implement live blog SEO landing structure | 5 | Sprint 4 | R2 – Core Experience | Done |
| NEWS-82 | Support closing and archiving a live blog | 5 | Sprint 4 | R2 – Core Experience | Done |
| NEWS-83 | Add breaking-news alert dispatch from live blog | 5 | Sprint 4 | R2 – Core Experience | Done |
| NEWS-84 | Enable rich media entries with galleries | 8 | Sprint 4 | R2 – Core Experience | Done |
| NEWS-85 | Support entry editing without breaking permalinks | 8 | Sprint 4 | R2 – Core Experience | Done |
| NEWS-86 | Add reader-facing 'new updates' indicator | 13 | Sprint 4 | R2 – Core Experience | Done |
| NEWS-87 | Support liveblog summaries auto-generated at top | 2 | Sprint 4 | R2 – Core Experience | Done |
| NEWS-88 | Enable moderation of contributor entries | 3 | Sprint 4 | R2 – Core Experience | Done |
| NEWS-89 | Add analytics on live blog concurrent readership | 5 | Sprint 4 | R2 – Core Experience | Done |

### 10.6 Epic 6: SEO & Discoverability  `NEWS-6`

**Objective:** Search engine and social optimization.  
**Stories:** 15 · **Estimated points:** 58

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| NEWS-90 | Auto-generate meta title and description with overrides | 3 | Sprint 4 | R2 – Core Experience | Done |
| NEWS-91 | Add canonical URL management for syndicated content | 2 | Sprint 5 | R3 – Scale & Monetize | Done |
| NEWS-92 | Implement structured data (NewsArticle schema) | 5 | Sprint 5 | R3 – Scale & Monetize | Done |
| NEWS-93 | Generate and submit news sitemap automatically | 8 | Sprint 5 | R3 – Scale & Monetize | Done |
| NEWS-94 | Add Open Graph and Twitter card previews | 3 | Sprint 5 | R3 – Scale & Monetize | Done |
| NEWS-95 | Support AMP-equivalent fast-loading article pages | 1 | Sprint 5 | R3 – Scale & Monetize | Done |
| NEWS-96 | Add SEO scoring feedback in the editor | 2 | Sprint 5 | R3 – Scale & Monetize | Done |
| NEWS-97 | Implement redirect management for changed URLs | 2 | Sprint 5 | R3 – Scale & Monetize | Done |
| NEWS-98 | Support hreflang tags for localized editions | 3 | Sprint 5 | R3 – Scale & Monetize | Done |
| NEWS-99 | Add Google News publisher center compliance checks | 3 | Sprint 5 | R3 – Scale & Monetize | Done |
| NEWS-100 | Detect and warn on duplicate/thin content | 3 | Sprint 5 | R3 – Scale & Monetize | Done |
| NEWS-101 | Support editor-defined focus keywords | 5 | Sprint 5 | R3 – Scale & Monetize | Done |
| NEWS-102 | Add breadcrumb structured data per section | 5 | Sprint 5 | R3 – Scale & Monetize | Done |
| NEWS-103 | Implement automatic internal link suggestions | 5 | Sprint 5 | R3 – Scale & Monetize | Done |
| NEWS-104 | Track keyword ranking movement per article | 8 | Sprint 5 | R3 – Scale & Monetize | Done |

### 10.7 Epic 7: Taxonomy, Tagging & Metadata  `NEWS-7`

**Objective:** Content classification.  
**Stories:** 15 · **Estimated points:** 63

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| NEWS-105 | Build hierarchical section and category taxonomy | 8 | Sprint 5 | R3 – Scale & Monetize | Done |
| NEWS-106 | Support free-form and controlled-vocabulary tags | 13 | Sprint 5 | R3 – Scale & Monetize | Done |
| NEWS-107 | Add entity extraction for people, places, orgs | 2 | Sprint 5 | R3 – Scale & Monetize | Done |
| NEWS-108 | Implement tag pages with curated descriptions | 3 | Sprint 5 | R3 – Scale & Monetize | Done |
| NEWS-109 | Support tag merging and aliasing | 5 | Sprint 5 | R3 – Scale & Monetize | Done |
| NEWS-110 | Add content type metadata (news, opinion, review) | 3 | Sprint 6 | R3 – Scale & Monetize | Done |
| NEWS-111 | Enable topic tagging suggestions via NLP | 2 | Sprint 6 | R3 – Scale & Monetize | Done |
| NEWS-112 | Support related-article linking by taxonomy | 5 | Sprint 6 | R3 – Scale & Monetize | Done |
| NEWS-113 | Add governance approval for new taxonomy terms | 8 | Sprint 6 | R3 – Scale & Monetize | Done |
| NEWS-114 | Implement metadata bulk-edit tooling | 3 | Sprint 6 | R3 – Scale & Monetize | Done |
| NEWS-115 | Support content series and franchise grouping | 1 | Sprint 6 | R3 – Scale & Monetize | Done |
| NEWS-116 | Add author profile pages with topic expertise | 2 | Sprint 6 | R3 – Scale & Monetize | Done |
| NEWS-117 | Enable syndication metadata per partner | 2 | Sprint 6 | R3 – Scale & Monetize | Done |
| NEWS-118 | Support paywall/access-level metadata per article | 3 | Sprint 6 | R3 – Scale & Monetize | Done |
| NEWS-119 | Track tag usage analytics for editors | 3 | Sprint 6 | R3 – Scale & Monetize | Done |

### 10.8 Epic 8: Multi-channel Publishing & Syndication  `NEWS-8`

**Objective:** Distribution beyond web.  
**Stories:** 15 · **Estimated points:** 78

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| NEWS-120 | Publish articles to native mobile apps via API | 3 | Sprint 6 | R3 – Scale & Monetize | Done |
| NEWS-121 | Support Apple News format export | 5 | Sprint 6 | R3 – Scale & Monetize | Done |
| NEWS-122 | Add RSS and JSON feed generation per section | 5 | Sprint 6 | R3 – Scale & Monetize | Done |
| NEWS-123 | Implement partner syndication feeds with entitlements | 5 | Sprint 6 | R3 – Scale & Monetize | Done |
| NEWS-124 | Support AMP output for eligible articles | 8 | Sprint 6 | R3 – Scale & Monetize | Done |
| NEWS-125 | Add social auto-posting on publish | 8 | Sprint 6 | R3 – Scale & Monetize | Done |
| NEWS-126 | Implement content licensing export packages | 13 | Sprint 6 | R3 – Scale & Monetize | Done |
| NEWS-127 | Support Google Web Stories creation | 2 | Sprint 6 | R3 – Scale & Monetize | Done |
| NEWS-128 | Add newsletter-ready article rendering | 3 | Sprint 6 | R3 – Scale & Monetize | Done |
| NEWS-129 | Enable Flipboard and aggregator feeds | 5 | Sprint 7 | R4 – Optimize & Expand | Done |
| NEWS-130 | Support wire-service ingestion and re-publishing | 3 | Sprint 7 | R4 – Optimize & Expand | Done |
| NEWS-131 | Add per-channel publish scheduling | 2 | Sprint 7 | R4 – Optimize & Expand | Done |
| NEWS-132 | Implement takedown propagation across channels | 5 | Sprint 7 | R4 – Optimize & Expand | Done |
| NEWS-133 | Support canonical attribution for syndicated copies | 8 | Sprint 7 | R4 – Optimize & Expand | Done |
| NEWS-134 | Track cross-channel reach per article | 3 | Sprint 7 | R4 – Optimize & Expand | Done |

### 10.9 Epic 9: Comments & Community Moderation  `NEWS-9`

**Objective:** Reader engagement and safety.  
**Stories:** 15 · **Estimated points:** 68

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| NEWS-135 | Add threaded reader comments on articles | 1 | Sprint 7 | R4 – Optimize & Expand | Done |
| NEWS-136 | Implement pre-moderation queue for flagged terms | 2 | Sprint 7 | R4 – Optimize & Expand | Done |
| NEWS-137 | Support automated toxicity detection and filtering | 2 | Sprint 7 | R4 – Optimize & Expand | Done |
| NEWS-138 | Add reader reputation and trusted-commenter tiers | 3 | Sprint 7 | R4 – Optimize & Expand | Done |
| NEWS-139 | Enable staff replies badged as official | 3 | Sprint 7 | R4 – Optimize & Expand | Done |
| NEWS-140 | Support comment reporting by readers | 3 | Sprint 7 | R4 – Optimize & Expand | Done |
| NEWS-141 | Add moderator dashboard with bulk actions | 5 | Sprint 7 | R4 – Optimize & Expand | Done |
| NEWS-142 | Implement per-article comment enable/disable | 5 | Sprint 7 | R4 – Optimize & Expand | Done |
| NEWS-143 | Support shadow-banning of abusive accounts | 5 | Sprint 7 | R4 – Optimize & Expand | Done |
| NEWS-144 | Add comment sorting by relevance and time | 8 | Sprint 7 | R4 – Optimize & Expand | Done |
| NEWS-145 | Enable comment section for subscribers only | 8 | Sprint 7 | R4 – Optimize & Expand | Done |
| NEWS-146 | Support quote-and-reply within threads | 13 | Sprint 7 | R4 – Optimize & Expand | Done |
| NEWS-147 | Add profanity filter with configurable lexicon | 2 | Sprint 8 | R4 – Optimize & Expand | Done |
| NEWS-148 | Implement appeal workflow for removed comments | 3 | Sprint 8 | R4 – Optimize & Expand | Done |
| NEWS-149 | Track moderation SLA and volume metrics | 5 | Sprint 8 | R4 – Optimize & Expand | Done |

### 10.10 Epic 10: Newsletters & Notifications  `NEWS-10`

**Objective:** Owned-audience messaging.  
**Stories:** 15 · **Estimated points:** 58

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| NEWS-150 | Build newsletter composer with drag-and-drop blocks | 3 | Sprint 8 | R4 – Optimize & Expand | Done |
| NEWS-151 | Support automated daily digest from top stories | 2 | Sprint 8 | R4 – Optimize & Expand | Done |
| NEWS-152 | Add subscriber segmentation by topic interest | 5 | Sprint 8 | R4 – Optimize & Expand | Done |
| NEWS-153 | Implement double opt-in subscription flow | 8 | Sprint 8 | R4 – Optimize & Expand | Done |
| NEWS-154 | Support A/B testing of subject lines | 3 | Sprint 8 | R4 – Optimize & Expand | Done |
| NEWS-155 | Add send-time optimization per subscriber | 1 | Sprint 8 | R4 – Optimize & Expand | Done |
| NEWS-156 | Enable web push notifications for breaking news | 2 | Sprint 8 | R4 – Optimize & Expand | Done |
| NEWS-157 | Support unsubscribe and preference management | 2 | Sprint 8 | R4 – Optimize & Expand | Done |
| NEWS-158 | Add newsletter performance dashboard | 3 | Sprint 8 | R4 – Optimize & Expand | Done |
| NEWS-159 | Implement personalized story recommendations in email | 3 | Sprint 8 | R4 – Optimize & Expand | Done |
| NEWS-160 | Support transactional email deliverability monitoring | 3 | Sprint 8 | R4 – Optimize & Expand | Done |
| NEWS-161 | Add newsletter archive public pages | 5 | Sprint 8 | R4 – Optimize & Expand | Done |
| NEWS-162 | Enable editor-curated vs automated newsletter modes | 5 | Sprint 8 | R4 – Optimize & Expand | Done |
| NEWS-163 | Support suppression lists and compliance | 5 | Sprint 8 | R4 – Optimize & Expand | Done |
| NEWS-164 | Track newsletter-driven subscription conversions | 8 | Sprint 8 | R4 – Optimize & Expand | Done |

### 10.11 Epic 11: Search & Content Discovery  `NEWS-11`

**Objective:** On-site search and recommendations.  
**Stories:** 15 · **Estimated points:** 63

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| NEWS-165 | Implement full-text article search with facets | 8 | Sprint 9 | R5 – GA & Hardening | Done |
| NEWS-166 | Add typeahead search suggestions | 13 | Sprint 9 | R5 – GA & Hardening | Done |
| NEWS-167 | Support search filtering by date, section, author | 2 | Sprint 9 | R5 – GA & Hardening | Done |
| NEWS-168 | Implement 'more like this' related articles | 3 | Sprint 9 | R5 – GA & Hardening | Done |
| NEWS-169 | Add personalized recommendations for logged-in readers | 5 | Sprint 9 | R5 – GA & Hardening | Done |
| NEWS-170 | Support trending searches surface | 3 | Sprint 9 | R5 – GA & Hardening | Done |
| NEWS-171 | Add search analytics for editorial insight | 2 | Sprint 9 | R5 – GA & Hardening | Done |
| NEWS-172 | Implement synonym and stemming configuration | 5 | Sprint 9 | R5 – GA & Hardening | Done |
| NEWS-173 | Support boosting of premium or recent content | 8 | Sprint 9 | R5 – GA & Hardening | Done |
| NEWS-174 | Add zero-results handling with suggestions | 3 | Sprint 9 | R5 – GA & Hardening | Done |
| NEWS-175 | Enable saved searches and topic follows | 1 | Sprint 9 | R5 – GA & Hardening | Done |
| NEWS-176 | Support voice search on mobile | 2 | Sprint 9 | R5 – GA & Hardening | Done |
| NEWS-177 | Add semantic search over article archive | 2 | Sprint 9 | R5 – GA & Hardening | Done |
| NEWS-178 | Implement search result A/B ranking tests | 3 | Sprint 9 | R5 – GA & Hardening | Done |
| NEWS-179 | Track search-to-read conversion | 3 | Sprint 9 | R5 – GA & Hardening | Done |

### 10.12 Epic 12: Analytics & Editorial Insights  `NEWS-12`

**Objective:** Newsroom data and dashboards.  
**Stories:** 15 · **Estimated points:** 78

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| NEWS-180 | Build real-time content performance dashboard | 3 | Sprint 9 | R5 – GA & Hardening | Done |
| NEWS-181 | Add per-article engagement and scroll-depth metrics | 5 | Sprint 9 | R5 – GA & Hardening | Done |
| NEWS-182 | Implement author-level performance reporting | 5 | Sprint 9 | R5 – GA & Hardening | Done |
| NEWS-183 | Support attention-time and completion metrics | 5 | Sprint 10 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| NEWS-184 | Add referral source breakdown per article | 8 | Sprint 10 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| NEWS-185 | Implement content decay and evergreen scoring | 8 | Sprint 10 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| NEWS-186 | Support headline test result reporting | 13 | Sprint 10 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| NEWS-187 | Add subscriber vs anonymous engagement split | 2 | Sprint 10 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| NEWS-188 | Implement newsroom north-star KPI dashboard | 3 | Sprint 10 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| NEWS-189 | Support export of analytics to data warehouse | 5 | Sprint 10 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| NEWS-190 | Add anomaly alerts for viral content | 3 | Sprint 10 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| NEWS-191 | Implement paywall stop-rate analytics | 2 | Sprint 10 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| NEWS-192 | Support cohort analysis of returning readers | 5 | Sprint 10 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| NEWS-193 | Add editorial recommendations from analytics | 8 | Sprint 10 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| NEWS-194 | Track section-level performance trends | 3 | Sprint 10 (Upcoming) | R5 – GA & Hardening | To Do (planned) |

### 10.13 Epic 13: Accessibility & Localization  `NEWS-13`

**Objective:** Inclusive, multilingual delivery.  
**Stories:** 15 · **Estimated points:** 29

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| NEWS-195 | Ensure WCAG 2.2 AA compliance on article pages | 1 | Sprint 10 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| NEWS-196 | Add keyboard navigation across all editor tools | 2 | Sprint 10 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| NEWS-197 | Implement screen-reader friendly media captions | 2 | Sprint 10 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| NEWS-198 | Support high-contrast and text-resize modes | 3 | Sprint 10 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| NEWS-199 | Add automated accessibility linting in editor | 3 | Sprint 10 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| NEWS-200 | Implement multi-language content variants | 3 | Sprint 10 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| NEWS-201 | Support translation workflow with human review | 5 | Sprint 10 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| NEWS-202 | Add locale-aware date, number, currency formatting | 5 | Sprint 10 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| NEWS-203 | Enable right-to-left language rendering | 5 | Sprint 10 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| NEWS-204 | Support per-locale homepage and sections | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| NEWS-205 | Add captions and transcripts for video/audio | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| NEWS-206 | Implement language auto-detection for readers | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| NEWS-207 | Support glossary-consistent translation memory | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| NEWS-208 | Add accessibility statement and feedback channel | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| NEWS-209 | Track accessibility compliance across templates | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |

### 10.14 Epic 14: Platform, Performance & Infrastructure  `NEWS-14`

**Objective:** Reliability and speed.  
**Stories:** 15 · **Estimated points:** 0

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| NEWS-210 | Set up multi-environment CI/CD pipeline | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| NEWS-211 | Implement CDN caching strategy for article pages | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| NEWS-212 | Add Core Web Vitals monitoring and budgets | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| NEWS-213 | Support blue-green deployments with rollback | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| NEWS-214 | Implement image optimization at the edge | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| NEWS-215 | Add rate limiting and bot protection | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| NEWS-216 | Support horizontal autoscaling under traffic spikes | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| NEWS-217 | Implement centralized structured logging | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| NEWS-218 | Add distributed tracing across services | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| NEWS-219 | Support disaster recovery and backup restore drills | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| NEWS-220 | Implement feature-flag framework | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| NEWS-221 | Add API gateway with versioning | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| NEWS-222 | Support secrets management and rotation | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| NEWS-223 | Implement uptime SLO dashboards and alerting | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| NEWS-224 | Add load testing for election-night traffic | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |

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
| Traffic spikes during major news events overwhelm the platform | High | Autoscaling, edge caching, and load testing for peak events (see Platform epic). |
| SEO regressions during migration reduce organic traffic | High | Redirect management, canonical handling, and staged rollout with monitoring. |
| Editorial adoption resistance to new workflow | Medium | Early involvement, training, and a quick-publish path for breaking news. |
| Accessibility gaps introduced by rich media | Medium | Automated a11y linting in the editor and required alt-text before publish. |

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
| NEWS-1 | Editorial CMS Core | 15 | 68 | R1 |
| NEWS-2 | Rich Media & Asset Management | 15 | 58 | R1 |
| NEWS-3 | Editorial Workflow & Approvals | 15 | 63 | R1, R2 |
| NEWS-4 | Homepage & Section Curation | 15 | 78 | R2 |
| NEWS-5 | Live Blogging & Breaking News | 15 | 68 | R2 |
| NEWS-6 | SEO & Discoverability | 15 | 58 | R2, R3 |
| NEWS-7 | Taxonomy, Tagging & Metadata | 15 | 63 | R3 |
| NEWS-8 | Multi-channel Publishing & Syndication | 15 | 78 | R3, R4 |
| NEWS-9 | Comments & Community Moderation | 15 | 68 | R4 |
| NEWS-10 | Newsletters & Notifications | 15 | 58 | R4 |
| NEWS-11 | Search & Content Discovery | 15 | 63 | R5 |
| NEWS-12 | Analytics & Editorial Insights | 15 | 78 | R5 |
| NEWS-13 | Accessibility & Localization | 15 | 29 | R5 |
| NEWS-14 | Platform, Performance & Infrastructure | 15 | 0 | R5 |

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
| Jira project key | `NEWS` |
| Epics | 14 |
| User stories | 210 |
| Estimated stories | 189 |
| Completed sprints | 9 |
| Upcoming sprints | 1 |
| Total story points (estimated) | 830 |
| Board | https://pulseaipoc.atlassian.net/jira/software/projects/NEWS/boards |

---

*Generated 22 Jul 2026. This BRD mirrors the live Jira project `NEWS` (epics, stories, story points, sprints, and releases).*
