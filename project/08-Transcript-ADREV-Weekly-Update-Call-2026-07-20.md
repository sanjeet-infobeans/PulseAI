# Call Transcript — ADREV Weekly Update

*Project: Advertising & Programmatic Revenue (`ADREV`) · Customer: Media House*
*Weekly status call, ~30 minutes. Transcribed from recording, lightly cleaned up for readability.*
*Follows up on: [07-Transcript-ADREV-Weekly-Update-Call-2026-07-13.md](07-Transcript-ADREV-Weekly-Update-Call-2026-07-13.md)*

---

**Date:** Monday, 20 July 2026
**Time:** 4:00 PM – 4:29 PM IST
**Attendees:**
- Ananya Rao — Delivery Manager (PulseAI)
- Mayank Salunke — Tech Lead (PulseAI)
- Sanjeet Patel — Engineer (PulseAI)
- Karan Mehta — Product Owner (Media House)
- Divya Shah — Legal & Compliance Lead (Media House)

---

**[00:00] Ananya Rao:** Thanks for joining again. Let's follow up on last week's three blockers first, then cover Sprint 11 progress and anything new. Divya, good to have you back.

**[00:22] Divya Shah:** Good to be here. I've got updates on two of the three.

**[00:30] Ananya Rao:** Let's start with ADREV-187, the ad-blocker messaging.

**[00:38] Divya Shah:** That one's done — legal signed off Thursday. I sent the final copy and disclosure language to Mayank Friday morning.

**[00:52] Mayank Salunke:** Confirmed, got it Friday. We've already built the UI against it over the weekend deploy window, it's in QA now. Should close out ADREV-187 by Wednesday.

**[01:20] Ananya Rao:** Excellent, that one's unblocked and moving. I'll mark that risk as resolved. ADREV-6, brand safety?

**[01:35] Karan Mehta:** Partial update. Divya sent the draft policy doc Thursday as promised.

**[01:45] Sanjeet Patel:** Yes, got it, thanks. It's enough to start on — I've begun building the exclusion rules engine and loading the default category list against your draft taxonomy. Should have a first pass ready to demo next week.

**[02:20] Divya Shah:** Good. On the verification vendor decision though, I still don't have a date. That conversation's still sitting with commercial leadership.

**[02:40] Ananya Rao:** Understood, that stays as the separate backlog item Sanjeet split out last week, not blocking the sprint. Karan, is there anyone we should be nudging directly on that vendor decision, or do we just wait?

**[03:05] Karan Mehta:** Let me nudge it myself this week, I'll try to get at least a rough timeline even if the decision itself isn't final.

**[03:20] Ananya Rao:** Appreciate it. Last one — ADREV-198, third-party tag creatives, the vendor list and sample tags.

**[03:35] Karan Mehta:** I've got two of the four vendors' details and sample tags over to you already — sent them Friday.

**[03:48] Mayank Salunke:** Got those, thanks. They're enough to get the sandboxing and timeout-handling groundwork going, so this isn't fully blocked anymore, just partially. Once the other two come in we'll extend the macro and format handling to match them.

**[04:15] Karan Mehta:** The remaining two are with our ops team, they said early this week. I'll chase again today.

**[04:30] Ananya Rao:** Okay, so status update: ADREV-187 unblocked and closing out, ADREV-6 unblocked enough to start with the draft policy, vendor decision remains open on a separate track, ADREV-198 partially unblocked, two vendors still pending, expected this week.

**[05:00] Ananya Rao:** Now, one new item before we move to sprint numbers. Sanjeet, you mentioned consent and privacy needs a decision too?

**[05:15] Sanjeet Patel:** Yes — ADREV-7, consent and privacy. We're about to start the CMP integration work, but we need Media House to confirm which markets you're serving ads into for this platform. That decides whether we scope for GDPR and IAB TCF v2 consent strings, CCPA-style opt-outs, or both. It also affects which CMP vendor makes sense, since not all of them support the same combination well.

**[06:10] Karan Mehta:** We're EU and US today, with a possible APAC expansion next year, but that's not committed yet.

**[06:25] Divya Shah:** For now, let's scope for GDPR/TCF v2 and CCPA, both live markets. I'll get written confirmation from our compliance side by end of this week so it's not just a verbal answer on the transcript.

**[06:50] Ananya Rao:** That's exactly what we need. I'll log ADREV-7 as blocked pending written confirmation of target markets and applicable regulations from Media House compliance, due this Friday, 24 July.

**[07:20] Sanjeet Patel:** Once that's confirmed I can pick the CMP vendor and start integration next sprint.

**[07:35] Ananya Rao:** Good. So going into Sprint 12 planning we've got one new blocker and one partially-cleared one carrying over — I'll make sure both are visible on the risk register so nothing slips through.

**[08:00] Ananya Rao:** On the numbers — Sprint 11's underway, we're pacing normally against the committed points, nothing alarming. I do want to flag one thing on the effort side, separate from sprint velocity — we're tracking ahead of the original hours estimate for the project overall, mostly driven by the brand-safety and consent scope turning out bigger than the original sizing. It's not a blocker, just something I want on your radar before it becomes a bigger conversation.

**[09:10] Karan Mehta:** Appreciated, let's put fifteen minutes on next week's call specifically for that, rather than rushing it today.

**[09:25] Ananya Rao:** Will do, I'll add it to next week's agenda with the actual numbers pulled together. Anything else from anyone? ... Alright, I'll send today's recap with the updated action items shortly. Thanks all, talk next Monday.

**[09:48] — Call ended —**

---

## Action Items Summary (cumulative, as of this call)

| Story | Blocker | Owner | Status as of 20 Jul | Target date |
| --- | --- | --- | --- | --- |
| ADREV-187 — Ad-blocker detection and messaging | Approved messaging/disclosure copy | Divya Shah (Media House Legal) | Resolved 17 Jul; in QA | Closed |
| ADREV-6 — Brand Safety & Verification | Draft brand safety policy + category taxonomy | Divya Shah (Media House Legal) | Draft received 17 Jul; engineering started | Ongoing |
| ADREV-6 (follow-on) — Verification vendor selection | Commercial decision on DoubleVerify/IAS/other | Karan Mehta (Media House) | Still open, no date | TBD |
| ADREV-198 — Third-party tag creatives | Vendor list + sample tags (4 vendors) | Karan Mehta (Media House) | 2 of 4 received 17 Jul | Remaining 2 — week of 20 Jul |
| ADREV-7 — Consent & Privacy | Confirmed target markets / applicable regulations | Divya Shah (Media House Legal) | Verbal confirmation 20 Jul (GDPR/TCF v2 + CCPA); written confirmation pending | 24 Jul |
