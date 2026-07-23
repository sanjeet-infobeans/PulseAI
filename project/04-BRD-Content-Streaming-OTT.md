# Business Requirements Document (BRD)
## Content Streaming & OTT — Content Streaming & OTT Platform

### Document Control

| Field | Value |
| --- | --- |
| Document Title | BRD — Content Streaming & OTT |
| Project Key (Jira) | `STREAM` |
| Jira Project URL | https://pulseaipoc.atlassian.net/jira/software/projects/STREAM/boards |
| Version | 1.0 |
| Status | Baselined |
| Date | 22 Jul 2026 |
| Author | Delivery / Product Team |
| Delivery Methodology | Agile (Scrum) — 2-week sprints |
| Industry Domain | Media & Publishing |

## 1. Executive Summary

Deliver a premium, reliable, multi-device video streaming experience — on-demand and live — with fast startup, high playback quality, strong content protection, and personalised discovery that keeps viewers engaged and reduces churn.

This document defines the business requirements, scope, objectives, and agile delivery plan for the platform. Delivery is organised into **14 epics** and **210 user stories**, executed across **11 completed sprints**, **1 upcoming sprint**, and a maintained product backlog, aligned to **5 release milestones**.

## 2. Business Context & Problem Statement

The organisation lacks an owned video platform to monetise its growing video and live content. There is no scalable ingest/transcoding pipeline, no adaptive multi-device playback, no DRM, and no personalisation, forcing reliance on third-party platforms that limit data ownership and monetisation.

## 3. Business Objectives

1. Achieve video startup time under 2 seconds at p75.
2. Keep rebuffering ratio under 0.5% of playback time.
3. Deliver adaptive playback across web, mobile, and major smart-TV platforms.
4. Protect premium content with multi-DRM and concurrency controls.
5. Increase viewer engagement (watch-time per session) by 25% via personalisation.

## 4. Success Metrics & KPIs

| Metric | Target |
| --- | --- |
| Video startup time | < 2s at p75 |
| Rebuffering ratio | < 0.5% |
| Playback failure rate | < 1% |
| Watch-time per session | +25% over baseline |
| Live concurrency supported | Peak-event target |
| Recommendation click-through | > 15% |

## 5. Stakeholders & Personas

| Persona / Stakeholder | Role & Needs |
| --- | --- |
| Viewer | Watches on-demand and live content across devices. |
| Content Operations | Manages catalogue, metadata, and availability. |
| Live Producer | Runs live events and linear channels. |
| Personalisation Analyst | Tunes recommendations and engagement. |
| Streaming Engineer | Operates ingest, delivery, and QoE. |
| Rights/Compliance Manager | Manages DRM, licensing, and geo-restrictions. |

## 6. Scope

### 6.1 In Scope

- Video ingest, transcoding, and adaptive packaging (HLS/DASH)
- Cross-device playback and player experience
- Content catalogue, metadata, and availability windows
- Personalisation, recommendations, search, and browse
- Live streaming, events, and linear channels
- DRM/content protection and CDN/delivery optimisation
- Profiles, watchlists, continue-watching, and offline downloads
- Smart-TV/multi-device apps, QoS monitoring, and content analytics

### 6.2 Out of Scope

- Editorial article authoring (Digital Newsroom & CMS)
- Subscription billing (Subscription & Paywall Platform) beyond entitlement checks
- Ad sales operations (Advertising platform) beyond ad-insertion interfaces
- Original content production/studio operations

## 7. Assumptions, Constraints & Dependencies

### 7.1 Assumptions

- Multi-CDN contracts and origin infrastructure are available.
- DRM licensing agreements (Widevine/PlayReady/FairPlay) are in place.
- Entitlements are provided by the shared subscription/identity platform.
- Content is delivered with the required rights metadata.

### 7.2 Constraints

- Must enforce DRM and licensing/geo windows for premium content.
- Must scale to live-event peak concurrency.
- Must meet QoE targets across constrained networks and devices.

### 7.3 Dependencies

- Multi-CDN providers and origin storage
- Multi-DRM license services
- Shared subscription/entitlement and identity platform
- Recommendation/ML infrastructure

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
| Delivered (completed sprints) | 168 | 80% | Yes | 11 closed sprints |
| Upcoming (planned) sprint | 21 | 10% | Yes | 1 future sprint |
| Product backlog (unplanned) | 21 | 10% | No (not estimated) | No sprint |
| **Total** | 210 | 100% | — | 12 sprints + backlog |

### 9.2 Sprint Plan

| Sprint | Dates | Stories | Story Points | Release | State |
| --- | --- | --- | --- | --- | --- |
| Sprint 1 | 18 Feb – 03 Mar 2026 | 16 | 71 | R1 – Foundation & MVP | Closed / Delivered |
| Sprint 2 | 04 Mar – 17 Mar 2026 | 16 | 76 | R1 – Foundation & MVP | Closed / Delivered |
| Sprint 3 | 18 Mar – 31 Mar 2026 | 16 | 55 | R1 – Foundation & MVP | Closed / Delivered |
| Sprint 4 | 01 Apr – 14 Apr 2026 | 15 | 70 | R2 – Core Experience | Closed / Delivered |
| Sprint 5 | 15 Apr – 28 Apr 2026 | 15 | 73 | R2 – Core Experience | Closed / Delivered |
| Sprint 6 | 29 Apr – 12 May 2026 | 15 | 71 | R3 – Scale & Monetize | Closed / Delivered |
| Sprint 7 | 13 May – 26 May 2026 | 15 | 53 | R3 – Scale & Monetize | Closed / Delivered |
| Sprint 8 | 27 May – 09 Jun 2026 | 15 | 70 | R3 – Scale & Monetize | Closed / Delivered |
| Sprint 9 | 10 Jun – 23 Jun 2026 | 15 | 73 | R4 – Optimize & Expand | Closed / Delivered |
| Sprint 10 | 24 Jun – 07 Jul 2026 | 15 | 71 | R4 – Optimize & Expand | Closed / Delivered |
| Sprint 11 | 08 Jul – 21 Jul 2026 | 15 | 53 | R5 – GA & Hardening | Closed / Delivered |
| Sprint 12 | 22 Jul – 04 Aug 2026 | 21 | 94 | R5 – GA & Hardening | Upcoming (planned) |
| Backlog | Unscheduled | 21 | Not estimated | R5 – GA & Hardening | Backlog |

> **Velocity note:** 168 stories (~736 points) were delivered across 11 completed sprints, giving an average delivered velocity of **~66 points/sprint**. Completed story points per sprint are visible in the Jira Velocity report.

## 10. Epics & User Stories

The scope is decomposed into 14 epics. Each user story follows the INVEST principles and carries acceptance criteria and a Definition of Done in Jira. Story IDs below are the live Jira issue keys.

### 10.1 Epic 1: Video Ingest & Transcoding  `STREAM-1`

**Objective:** Media processing pipeline.  
**Stories:** 15 · **Estimated points:** 68

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| STREAM-15 | Build video ingest pipeline with validation | 1 | Sprint 1 | R1 – Foundation & MVP | Done |
| STREAM-16 | Implement adaptive bitrate transcoding (HLS/DASH) | 2 | Sprint 1 | R1 – Foundation & MVP | Done |
| STREAM-17 | Support multiple codec profiles (H.264/H.265/AV1) | 2 | Sprint 1 | R1 – Foundation & MVP | Done |
| STREAM-18 | Add automated thumbnail and poster extraction | 3 | Sprint 1 | R1 – Foundation & MVP | Done |
| STREAM-19 | Implement audio normalization and loudness control | 3 | Sprint 1 | R1 – Foundation & MVP | Done |
| STREAM-20 | Support multi-audio-track ingestion | 3 | Sprint 1 | R1 – Foundation & MVP | Done |
| STREAM-21 | Add subtitle/caption ingestion (WebVTT/TTML) | 5 | Sprint 1 | R1 – Foundation & MVP | Done |
| STREAM-22 | Implement watermarking on encode | 5 | Sprint 1 | R1 – Foundation & MVP | Done |
| STREAM-23 | Support mezzanine file archival | 5 | Sprint 1 | R1 – Foundation & MVP | Done |
| STREAM-24 | Add transcode job queue and prioritization | 8 | Sprint 1 | R1 – Foundation & MVP | Done |
| STREAM-25 | Implement failed-encode retry and alerting | 8 | Sprint 1 | R1 – Foundation & MVP | Done |
| STREAM-26 | Support per-title encoding optimization | 13 | Sprint 1 | R1 – Foundation & MVP | Done |
| STREAM-27 | Add content fingerprinting on ingest | 2 | Sprint 1 | R1 – Foundation & MVP | Done |
| STREAM-28 | Implement ingest from partner feeds | 3 | Sprint 1 | R1 – Foundation & MVP | Done |
| STREAM-29 | Track encode throughput and failure rates | 5 | Sprint 1 | R1 – Foundation & MVP | Done |

### 10.2 Epic 2: Playback & Player Experience  `STREAM-2`

**Objective:** Video player.  
**Stories:** 15 · **Estimated points:** 58

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| STREAM-30 | Build adaptive-bitrate web video player | 3 | Sprint 1 | R1 – Foundation & MVP | Done |
| STREAM-31 | Implement resume-from-last-position playback | 2 | Sprint 2 | R1 – Foundation & MVP | Done |
| STREAM-32 | Add playback speed and quality controls | 5 | Sprint 2 | R1 – Foundation & MVP | Done |
| STREAM-33 | Support closed captions and subtitle styling | 8 | Sprint 2 | R1 – Foundation & MVP | Done |
| STREAM-34 | Implement audio-track and language selection | 3 | Sprint 2 | R1 – Foundation & MVP | Done |
| STREAM-35 | Add keyboard and accessibility controls | 1 | Sprint 2 | R1 – Foundation & MVP | Done |
| STREAM-36 | Support picture-in-picture playback | 2 | Sprint 2 | R1 – Foundation & MVP | Done |
| STREAM-37 | Implement thumbnail scrubbing preview | 2 | Sprint 2 | R1 – Foundation & MVP | Done |
| STREAM-38 | Add skip-intro and skip-recap controls | 3 | Sprint 2 | R1 – Foundation & MVP | Done |
| STREAM-39 | Support autoplay-next with countdown | 3 | Sprint 2 | R1 – Foundation & MVP | Done |
| STREAM-40 | Implement chromecast and AirPlay casting | 3 | Sprint 2 | R1 – Foundation & MVP | Done |
| STREAM-41 | Add error recovery and buffering handling | 5 | Sprint 2 | R1 – Foundation & MVP | Done |
| STREAM-42 | Support 4K/HDR playback where available | 5 | Sprint 2 | R1 – Foundation & MVP | Done |
| STREAM-43 | Implement player telemetry (QoE beacons) | 5 | Sprint 2 | R1 – Foundation & MVP | Done |
| STREAM-44 | Track startup time and rebuffering ratio | 8 | Sprint 2 | R1 – Foundation & MVP | Done |

### 10.3 Epic 3: Content Catalog & Metadata  `STREAM-3`

**Objective:** Titles and metadata.  
**Stories:** 15 · **Estimated points:** 63

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| STREAM-45 | Build catalog model for movies and series | 8 | Sprint 2 | R1 – Foundation & MVP | Done |
| STREAM-46 | Implement season and episode hierarchy | 13 | Sprint 2 | R1 – Foundation & MVP | Done |
| STREAM-47 | Add rich metadata (cast, genre, synopsis) | 2 | Sprint 3 | R1 – Foundation & MVP | Done |
| STREAM-48 | Support artwork and imagery management | 3 | Sprint 3 | R1 – Foundation & MVP | Done |
| STREAM-49 | Implement content availability windows | 5 | Sprint 3 | R1 – Foundation & MVP | Done |
| STREAM-50 | Add regional licensing and geo-restrictions | 3 | Sprint 3 | R1 – Foundation & MVP | Done |
| STREAM-51 | Support content ratings and parental info | 2 | Sprint 3 | R1 – Foundation & MVP | Done |
| STREAM-52 | Implement metadata enrichment from providers | 5 | Sprint 3 | R1 – Foundation & MVP | Done |
| STREAM-53 | Add trailer and extras association | 8 | Sprint 3 | R1 – Foundation & MVP | Done |
| STREAM-54 | Support multi-language metadata | 3 | Sprint 3 | R1 – Foundation & MVP | Done |
| STREAM-55 | Implement catalog scheduling and takedowns | 1 | Sprint 3 | R1 – Foundation & MVP | Done |
| STREAM-56 | Add editorial collections and hubs | 2 | Sprint 3 | R1 – Foundation & MVP | Done |
| STREAM-57 | Support content deep-linking | 2 | Sprint 3 | R1 – Foundation & MVP | Done |
| STREAM-58 | Implement metadata validation rules | 3 | Sprint 3 | R1 – Foundation & MVP | Done |
| STREAM-59 | Track catalog coverage and gaps | 3 | Sprint 3 | R1 – Foundation & MVP | Done |

### 10.4 Epic 4: Personalization & Recommendations  `STREAM-4`

**Objective:** Discovery engine.  
**Stories:** 15 · **Estimated points:** 78

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| STREAM-60 | Build recommendation engine integration | 3 | Sprint 3 | R1 – Foundation & MVP | Done |
| STREAM-61 | Implement 'because you watched' rows | 5 | Sprint 3 | R1 – Foundation & MVP | Done |
| STREAM-62 | Add trending and popular-now rails | 5 | Sprint 3 | R1 – Foundation & MVP | Done |
| STREAM-63 | Support personalized home layout | 5 | Sprint 4 | R2 – Core Experience | Done |
| STREAM-64 | Implement collaborative-filtering recommendations | 8 | Sprint 4 | R2 – Core Experience | Done |
| STREAM-65 | Add content-based similarity recommendations | 8 | Sprint 4 | R2 – Core Experience | Done |
| STREAM-66 | Support cold-start onboarding preferences | 13 | Sprint 4 | R2 – Core Experience | Done |
| STREAM-67 | Implement per-profile personalization | 2 | Sprint 4 | R2 – Core Experience | Done |
| STREAM-68 | Add contextual (time-of-day) recommendations | 3 | Sprint 4 | R2 – Core Experience | Done |
| STREAM-69 | Support A/B testing of recommendation models | 5 | Sprint 4 | R2 – Core Experience | Done |
| STREAM-70 | Implement diversity and freshness controls | 3 | Sprint 4 | R2 – Core Experience | Done |
| STREAM-71 | Add editorial-plus-algorithmic blending | 2 | Sprint 4 | R2 – Core Experience | Done |
| STREAM-72 | Support real-time signal updates | 5 | Sprint 4 | R2 – Core Experience | Done |
| STREAM-73 | Implement recommendation explainability | 8 | Sprint 4 | R2 – Core Experience | Done |
| STREAM-74 | Track recommendation CTR and watch conversion | 3 | Sprint 4 | R2 – Core Experience | Done |

### 10.5 Epic 5: Live Streaming & Events  `STREAM-5`

**Objective:** Live and linear.  
**Stories:** 15 · **Estimated points:** 68

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| STREAM-75 | Implement live event ingest and packaging | 1 | Sprint 4 | R2 – Core Experience | Done |
| STREAM-76 | Support low-latency live streaming | 2 | Sprint 4 | R2 – Core Experience | Done |
| STREAM-77 | Add live-to-VOD automatic recording | 2 | Sprint 4 | R2 – Core Experience | Done |
| STREAM-78 | Implement DVR/rewind on live streams | 3 | Sprint 5 | R2 – Core Experience | Done |
| STREAM-79 | Support live event scheduling and reminders | 3 | Sprint 5 | R2 – Core Experience | Done |
| STREAM-80 | Add concurrent-viewer scaling | 3 | Sprint 5 | R2 – Core Experience | Done |
| STREAM-81 | Implement live captions/subtitles | 5 | Sprint 5 | R2 – Core Experience | Done |
| STREAM-82 | Support multi-camera and angle switching | 5 | Sprint 5 | R2 – Core Experience | Done |
| STREAM-83 | Add live chat and reactions | 5 | Sprint 5 | R2 – Core Experience | Done |
| STREAM-84 | Implement live stream failover/redundancy | 8 | Sprint 5 | R2 – Core Experience | Done |
| STREAM-85 | Support linear channel playout | 8 | Sprint 5 | R2 – Core Experience | Done |
| STREAM-86 | Add blackout and geo-restriction for live | 13 | Sprint 5 | R2 – Core Experience | Done |
| STREAM-87 | Implement live QoE monitoring | 2 | Sprint 5 | R2 – Core Experience | Done |
| STREAM-88 | Support pay-per-view live events | 3 | Sprint 5 | R2 – Core Experience | Done |
| STREAM-89 | Track live concurrency and QoE | 5 | Sprint 5 | R2 – Core Experience | Done |

### 10.6 Epic 6: DRM & Content Protection  `STREAM-6`

**Objective:** Rights enforcement.  
**Stories:** 15 · **Estimated points:** 58

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| STREAM-90 | Integrate Widevine, PlayReady, FairPlay DRM | 3 | Sprint 5 | R2 – Core Experience | Done |
| STREAM-91 | Implement license server and key rotation | 2 | Sprint 5 | R2 – Core Experience | Done |
| STREAM-92 | Add multi-DRM packaging | 5 | Sprint 5 | R2 – Core Experience | Done |
| STREAM-93 | Support offline license persistence | 8 | Sprint 6 | R3 – Scale & Monetize | Done |
| STREAM-94 | Implement forensic watermarking | 3 | Sprint 6 | R3 – Scale & Monetize | Done |
| STREAM-95 | Add concurrent-stream limit enforcement | 1 | Sprint 6 | R3 – Scale & Monetize | Done |
| STREAM-96 | Support device and output protection (HDCP) | 2 | Sprint 6 | R3 – Scale & Monetize | Done |
| STREAM-97 | Implement geo and license-window enforcement | 2 | Sprint 6 | R3 – Scale & Monetize | Done |
| STREAM-98 | Add token-based playback authorization | 3 | Sprint 6 | R3 – Scale & Monetize | Done |
| STREAM-99 | Support secure key exchange | 3 | Sprint 6 | R3 – Scale & Monetize | Done |
| STREAM-100 | Implement piracy detection and takedown | 3 | Sprint 6 | R3 – Scale & Monetize | Done |
| STREAM-101 | Add DRM fallback and compatibility handling | 5 | Sprint 6 | R3 – Scale & Monetize | Done |
| STREAM-102 | Support content encryption (CENC) | 5 | Sprint 6 | R3 – Scale & Monetize | Done |
| STREAM-103 | Implement license renewal for long playback | 5 | Sprint 6 | R3 – Scale & Monetize | Done |
| STREAM-104 | Track DRM failure and license issuance rates | 8 | Sprint 6 | R3 – Scale & Monetize | Done |

### 10.7 Epic 7: CDN & Delivery Optimization  `STREAM-7`

**Objective:** Scalable delivery.  
**Stories:** 15 · **Estimated points:** 63

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| STREAM-105 | Implement multi-CDN delivery strategy | 8 | Sprint 6 | R3 – Scale & Monetize | Done |
| STREAM-106 | Add CDN switching based on QoE | 13 | Sprint 6 | R3 – Scale & Monetize | Done |
| STREAM-107 | Support origin shield and caching tiers | 2 | Sprint 6 | R3 – Scale & Monetize | Done |
| STREAM-108 | Implement per-title bitrate ladder delivery | 3 | Sprint 7 | R3 – Scale & Monetize | Done |
| STREAM-109 | Add edge-side manifest manipulation | 5 | Sprint 7 | R3 – Scale & Monetize | Done |
| STREAM-110 | Support prefetch of next segments | 3 | Sprint 7 | R3 – Scale & Monetize | Done |
| STREAM-111 | Implement traffic steering by geo/ISP | 2 | Sprint 7 | R3 – Scale & Monetize | Done |
| STREAM-112 | Add CDN cost and performance analytics | 5 | Sprint 7 | R3 – Scale & Monetize | Done |
| STREAM-113 | Support signed URLs and token auth at edge | 8 | Sprint 7 | R3 – Scale & Monetize | Done |
| STREAM-114 | Implement failover across CDNs | 3 | Sprint 7 | R3 – Scale & Monetize | Done |
| STREAM-115 | Add cache-hit ratio monitoring | 1 | Sprint 7 | R3 – Scale & Monetize | Done |
| STREAM-116 | Support peak-event capacity planning | 2 | Sprint 7 | R3 – Scale & Monetize | Done |
| STREAM-117 | Implement segment delivery latency tracking | 2 | Sprint 7 | R3 – Scale & Monetize | Done |
| STREAM-118 | Add regional origin replication | 3 | Sprint 7 | R3 – Scale & Monetize | Done |
| STREAM-119 | Track delivery QoE by CDN and region | 3 | Sprint 7 | R3 – Scale & Monetize | Done |

### 10.8 Epic 8: Search & Browse  `STREAM-8`

**Objective:** Content discovery UI.  
**Stories:** 15 · **Estimated points:** 78

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| STREAM-120 | Build search across titles, cast, genres | 3 | Sprint 7 | R3 – Scale & Monetize | Done |
| STREAM-121 | Implement typeahead and voice search | 5 | Sprint 7 | R3 – Scale & Monetize | Done |
| STREAM-122 | Add filter and sort on browse pages | 5 | Sprint 7 | R3 – Scale & Monetize | Done |
| STREAM-123 | Support genre and collection browsing | 5 | Sprint 8 | R3 – Scale & Monetize | Done |
| STREAM-124 | Implement search relevance tuning | 8 | Sprint 8 | R3 – Scale & Monetize | Done |
| STREAM-125 | Add 'no results' fallback suggestions | 8 | Sprint 8 | R3 – Scale & Monetize | Done |
| STREAM-126 | Support recently-searched and popular queries | 13 | Sprint 8 | R3 – Scale & Monetize | Done |
| STREAM-127 | Implement search on connected TV UIs | 2 | Sprint 8 | R3 – Scale & Monetize | Done |
| STREAM-128 | Add availability-aware search results | 3 | Sprint 8 | R3 – Scale & Monetize | Done |
| STREAM-129 | Support multi-language search | 5 | Sprint 8 | R3 – Scale & Monetize | Done |
| STREAM-130 | Implement search analytics | 3 | Sprint 8 | R3 – Scale & Monetize | Done |
| STREAM-131 | Add deep-link search results | 2 | Sprint 8 | R3 – Scale & Monetize | Done |
| STREAM-132 | Support fuzzy matching and typo tolerance | 5 | Sprint 8 | R3 – Scale & Monetize | Done |
| STREAM-133 | Implement content-availability filtering | 8 | Sprint 8 | R3 – Scale & Monetize | Done |
| STREAM-134 | Track search-to-play conversion | 3 | Sprint 8 | R3 – Scale & Monetize | Done |

### 10.9 Epic 9: User Profiles & Watchlists  `STREAM-9`

**Objective:** Account personalization.  
**Stories:** 15 · **Estimated points:** 68

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| STREAM-135 | Implement multiple profiles per account | 1 | Sprint 8 | R3 – Scale & Monetize | Done |
| STREAM-136 | Add kids profiles with content restrictions | 2 | Sprint 8 | R3 – Scale & Monetize | Done |
| STREAM-137 | Support profile avatars and personalization | 2 | Sprint 8 | R3 – Scale & Monetize | Done |
| STREAM-138 | Implement watchlist add/remove | 3 | Sprint 9 | R4 – Optimize & Expand | Done |
| STREAM-139 | Add profile-level viewing history | 3 | Sprint 9 | R4 – Optimize & Expand | Done |
| STREAM-140 | Support profile PIN protection | 3 | Sprint 9 | R4 – Optimize & Expand | Done |
| STREAM-141 | Implement per-profile recommendations | 5 | Sprint 9 | R4 – Optimize & Expand | Done |
| STREAM-142 | Add profile switching UX | 5 | Sprint 9 | R4 – Optimize & Expand | Done |
| STREAM-143 | Support parental controls and maturity limits | 5 | Sprint 9 | R4 – Optimize & Expand | Done |
| STREAM-144 | Implement watchlist sync across devices | 8 | Sprint 9 | R4 – Optimize & Expand | Done |
| STREAM-145 | Add profile preferences (language, subtitles) | 8 | Sprint 9 | R4 – Optimize & Expand | Done |
| STREAM-146 | Support profile deletion and management | 13 | Sprint 9 | R4 – Optimize & Expand | Done |
| STREAM-147 | Implement 'my list' notifications for new content | 2 | Sprint 9 | R4 – Optimize & Expand | Done |
| STREAM-148 | Add viewing activity export | 3 | Sprint 9 | R4 – Optimize & Expand | Done |
| STREAM-149 | Track profile engagement metrics | 5 | Sprint 9 | R4 – Optimize & Expand | Done |

### 10.10 Epic 10: Continue Watching & Resume  `STREAM-10`

**Objective:** Playback continuity.  
**Stories:** 15 · **Estimated points:** 58

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| STREAM-150 | Implement cross-device resume points | 3 | Sprint 9 | R4 – Optimize & Expand | Done |
| STREAM-151 | Add continue-watching row on home | 2 | Sprint 9 | R4 – Optimize & Expand | Done |
| STREAM-152 | Support next-episode auto-progression | 5 | Sprint 9 | R4 – Optimize & Expand | Done |
| STREAM-153 | Implement watched/unwatched state tracking | 8 | Sprint 10 | R4 – Optimize & Expand | Done |
| STREAM-154 | Add remove-from-continue-watching | 3 | Sprint 10 | R4 – Optimize & Expand | Done |
| STREAM-155 | Support resume accuracy within seconds | 1 | Sprint 10 | R4 – Optimize & Expand | Done |
| STREAM-156 | Implement binge-watching detection | 2 | Sprint 10 | R4 – Optimize & Expand | Done |
| STREAM-157 | Add mark-as-watched controls | 2 | Sprint 10 | R4 – Optimize & Expand | Done |
| STREAM-158 | Support series progress indicators | 3 | Sprint 10 | R4 – Optimize & Expand | Done |
| STREAM-159 | Implement resume expiry policy | 3 | Sprint 10 | R4 – Optimize & Expand | Done |
| STREAM-160 | Add offline-to-online progress sync | 3 | Sprint 10 | R4 – Optimize & Expand | Done |
| STREAM-161 | Support multi-profile resume isolation | 5 | Sprint 10 | R4 – Optimize & Expand | Done |
| STREAM-162 | Implement partial-credit completion logic | 5 | Sprint 10 | R4 – Optimize & Expand | Done |
| STREAM-163 | Add resume conflict resolution | 5 | Sprint 10 | R4 – Optimize & Expand | Done |
| STREAM-164 | Track resume usage and completion | 8 | Sprint 10 | R4 – Optimize & Expand | Done |

### 10.11 Epic 11: Downloads & Offline Viewing  `STREAM-11`

**Objective:** Offline experience.  
**Stories:** 15 · **Estimated points:** 63

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| STREAM-165 | Implement download-for-offline on mobile | 8 | Sprint 10 | R4 – Optimize & Expand | Done |
| STREAM-166 | Add download quality selection | 13 | Sprint 10 | R4 – Optimize & Expand | Done |
| STREAM-167 | Support offline license management | 2 | Sprint 10 | R4 – Optimize & Expand | Done |
| STREAM-168 | Implement download expiry and renewal | 3 | Sprint 11 | R5 – GA & Hardening | Done |
| STREAM-169 | Add storage management and cleanup | 5 | Sprint 11 | R5 – GA & Hardening | Done |
| STREAM-170 | Support smart downloads of next episodes | 3 | Sprint 11 | R5 – GA & Hardening | Done |
| STREAM-171 | Implement download queue and pause/resume | 2 | Sprint 11 | R5 – GA & Hardening | Done |
| STREAM-172 | Add offline playback of subtitles/audio | 5 | Sprint 11 | R5 – GA & Hardening | Done |
| STREAM-173 | Support device download limits | 8 | Sprint 11 | R5 – GA & Hardening | Done |
| STREAM-174 | Implement offline viewing analytics sync | 3 | Sprint 11 | R5 – GA & Hardening | Done |
| STREAM-175 | Add download over Wi-Fi-only setting | 1 | Sprint 11 | R5 – GA & Hardening | Done |
| STREAM-176 | Support offline watchlist availability | 2 | Sprint 11 | R5 – GA & Hardening | Done |
| STREAM-177 | Implement download failure recovery | 2 | Sprint 11 | R5 – GA & Hardening | Done |
| STREAM-178 | Add downloaded-content parental controls | 3 | Sprint 11 | R5 – GA & Hardening | Done |
| STREAM-179 | Track download adoption and playback | 3 | Sprint 11 | R5 – GA & Hardening | Done |

### 10.12 Epic 12: Multi-device & Smart TV Apps  `STREAM-12`

**Objective:** Platform apps.  
**Stories:** 15 · **Estimated points:** 78

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| STREAM-180 | Build Roku streaming app | 3 | Sprint 11 | R5 – GA & Hardening | Done |
| STREAM-181 | Build Fire TV and Android TV apps | 5 | Sprint 11 | R5 – GA & Hardening | Done |
| STREAM-182 | Implement Apple TV (tvOS) app | 5 | Sprint 11 | R5 – GA & Hardening | Done |
| STREAM-183 | Add Samsung/LG smart TV apps | 5 | Sprint 12 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| STREAM-184 | Support gaming-console app clients | 8 | Sprint 12 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| STREAM-185 | Implement device pairing and activation codes | 8 | Sprint 12 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| STREAM-186 | Add TV-optimized navigation (remote/D-pad) | 13 | Sprint 12 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| STREAM-187 | Support deep-linking from mobile to TV | 2 | Sprint 12 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| STREAM-188 | Implement device-capability detection | 3 | Sprint 12 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| STREAM-189 | Add cross-device state synchronization | 5 | Sprint 12 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| STREAM-190 | Support app-store deployment pipelines | 3 | Sprint 12 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| STREAM-191 | Implement device-specific playback tuning | 2 | Sprint 12 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| STREAM-192 | Add TV app performance optimization | 5 | Sprint 12 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| STREAM-193 | Support voice-assistant integration | 8 | Sprint 12 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| STREAM-194 | Track device mix and engagement | 3 | Sprint 12 (Upcoming) | R5 – GA & Hardening | To Do (planned) |

### 10.13 Epic 13: Quality of Service & Monitoring  `STREAM-13`

**Objective:** Streaming reliability.  
**Stories:** 15 · **Estimated points:** 29

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| STREAM-195 | Implement QoE metrics collection (startup, rebuffer) | 1 | Sprint 12 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| STREAM-196 | Add real-time streaming health dashboard | 2 | Sprint 12 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| STREAM-197 | Support alerting on QoE degradation | 2 | Sprint 12 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| STREAM-198 | Implement per-CDN and per-region QoE views | 3 | Sprint 12 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| STREAM-199 | Add error-code taxonomy and tracking | 3 | Sprint 12 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| STREAM-200 | Support synthetic playback monitoring | 3 | Sprint 12 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| STREAM-201 | Implement concurrent-stream capacity monitoring | 5 | Sprint 12 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| STREAM-202 | Add anomaly detection on playback failures | 5 | Sprint 12 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| STREAM-203 | Support incident runbooks and on-call | 5 | Sprint 12 (Upcoming) | R5 – GA & Hardening | To Do (planned) |
| STREAM-204 | Implement SLO dashboards for streaming | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| STREAM-205 | Add client-side crash reporting | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| STREAM-206 | Support A/B monitoring of player changes | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| STREAM-207 | Implement bitrate-distribution analytics | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| STREAM-208 | Add end-to-end delivery tracing | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| STREAM-209 | Track availability and QoE SLOs | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |

### 10.14 Epic 14: Content Analytics & Engagement  `STREAM-14`

**Objective:** Viewing insights.  
**Stories:** 15 · **Estimated points:** 0

| Jira Key | User Story | Pts | Sprint | Release | Status |
| --- | --- | --- | --- | --- | --- |
| STREAM-210 | Build content performance dashboard | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| STREAM-211 | Implement watch-time and completion analytics | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| STREAM-212 | Add title-level engagement reporting | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| STREAM-213 | Support cohort viewing analysis | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| STREAM-214 | Implement churn-correlated content insights | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| STREAM-215 | Add recommendation-impact analytics | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| STREAM-216 | Support A/B test analytics for UI changes | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| STREAM-217 | Implement content ROI reporting | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| STREAM-218 | Add drop-off and abandonment analysis | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| STREAM-219 | Support real-time trending detection | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| STREAM-220 | Implement audience-overlap analytics | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| STREAM-221 | Add engagement export to data warehouse | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| STREAM-222 | Support per-device engagement breakdown | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| STREAM-223 | Implement content-acquisition decision reports | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |
| STREAM-224 | Track engagement-to-retention correlation | — | Backlog (unplanned) | R5 – GA & Hardening | To Do (not estimated) |

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
| Live-event scaling failures cause outages | High | Redundant ingest, autoscaling, failover, and QoE monitoring. |
| Content piracy / DRM circumvention | High | Multi-DRM, forensic watermarking, and concurrency limits. |
| Poor QoE on constrained networks drives churn | Medium | Adaptive bitrate, multi-CDN steering, and per-title encoding. |
| Device fragmentation increases delivery defects | Medium | Device-capability detection and per-device playback tuning. |

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
| STREAM-1 | Video Ingest & Transcoding | 15 | 68 | R1 |
| STREAM-2 | Playback & Player Experience | 15 | 58 | R1 |
| STREAM-3 | Content Catalog & Metadata | 15 | 63 | R1 |
| STREAM-4 | Personalization & Recommendations | 15 | 78 | R1, R2 |
| STREAM-5 | Live Streaming & Events | 15 | 68 | R2 |
| STREAM-6 | DRM & Content Protection | 15 | 58 | R2, R3 |
| STREAM-7 | CDN & Delivery Optimization | 15 | 63 | R3 |
| STREAM-8 | Search & Browse | 15 | 78 | R3 |
| STREAM-9 | User Profiles & Watchlists | 15 | 68 | R3, R4 |
| STREAM-10 | Continue Watching & Resume | 15 | 58 | R4 |
| STREAM-11 | Downloads & Offline Viewing | 15 | 63 | R4, R5 |
| STREAM-12 | Multi-device & Smart TV Apps | 15 | 78 | R5 |
| STREAM-13 | Quality of Service & Monitoring | 15 | 29 | R5 |
| STREAM-14 | Content Analytics & Engagement | 15 | 0 | R5 |

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
| Jira project key | `STREAM` |
| Epics | 14 |
| User stories | 210 |
| Estimated stories | 189 |
| Completed sprints | 11 |
| Upcoming sprints | 1 |
| Total story points (estimated) | 830 |
| Board | https://pulseaipoc.atlassian.net/jira/software/projects/STREAM/boards |

---

*Generated 22 Jul 2026. This BRD mirrors the live Jira project `STREAM` (epics, stories, story points, sprints, and releases).*
