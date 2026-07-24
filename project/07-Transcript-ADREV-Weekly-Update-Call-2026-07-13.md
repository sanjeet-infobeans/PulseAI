# Call Transcript — ADREV Weekly Update

*Project: Advertising & Programmatic Revenue (`ADREV`) · Customer: Media House*
*Weekly status call, ~30 minutes. Transcribed from recording, lightly cleaned up for readability.*
*Follow-up call: [08-Transcript-ADREV-Weekly-Update-Call-2026-07-20.md](08-Transcript-ADREV-Weekly-Update-Call-2026-07-20.md)*

---

**Date:** Monday, 13 July 2026
**Time:** 4:00 PM – 4:31 PM IST
**Attendees:**
- Ananya Rao — Delivery Manager (PulseAI)
- Mayank Salunke — Tech Lead (PulseAI)
- Sanjeet Patel — Engineer (PulseAI)
- Karan Mehta — Product Owner (Media House)
- Divya Shah — Legal & Compliance Lead (Media House)

---

**[00:00] Ananya Rao:** Thanks everyone for joining, let's get started since we've got a full agenda today. Quick recap — Sprint 10 closes this Friday, and we're using today to walk through progress and flag anything we need from your side before it does. Karan, Divya, thanks for making time.

**[00:38] Karan Mehta:** Happy to be here. Divya's joining specifically for the brand-safety and messaging items, so let's make sure we get to those.

**[00:52] Ananya Rao:** Absolutely, that's most of today's agenda. Mayank, want to kick off with the engineering status?

**[01:05] Mayank Salunke:** Sure. Sprint 10 is basically wrapping up clean — the ad-server and header-bidding epics are done, ADREV-183, async ad tag loading, is in review and looking good, no issues from QA so far. We should have that fully verified by Wednesday.

**[02:10] Sanjeet Patel:** On the creative side, ADREV-195, the upload and asset library, is also in review. That one's ready for your team to poke at whenever you get a chance — would be good to get eyes on it before we move to the approval workflow piece.

**[02:48] Karan Mehta:** Noted, I'll get one of our ad ops folks to run through it this week and send feedback.

**[03:05] Ananya Rao:** Great, let's log that as an action item. Now — the reason we wanted Divya on the call. We've got three stories that are ready to start from an engineering standpoint, but they need input from your side before we can actually build them without guessing.

**[03:40] Ananya Rao:** First one — ADREV-187, ad-blocker detection and messaging. Mayank, can you walk through what's needed?

**[03:55] Mayank Salunke:** Right, so this story shows a message to users when we detect an ad blocker is active, asking them to allow ads or consider a subscription. Functionally it's ready to build, but we don't have approved copy for that message, and we don't want to ship placeholder text that then needs a legal pass later. We need the actual wording — including whatever disclosure language legal wants — signed off before we build the UI around it.

**[04:50] Divya Shah:** That makes sense. We do have draft messaging from a similar initiative on the news site, but it hasn't been reviewed for the ad platform context specifically. Let me take that back to our legal team this week.

**[05:20] Karan Mehta:** Divya, can we commit to getting that back by end of next week? That keeps it inside Sprint 11.

**[05:35] Divya Shah:** I'll push for that. Worst case it slips a few days into the sprint after, but I'll flag it as priority.

**[05:50] Ananya Rao:** Perfect, I'll note ADREV-187 as blocked, pending approved messaging copy from Media House legal, target end of next week.

**[06:15] Ananya Rao:** Second one — ADREV-6, Brand Safety & Verification. Sanjeet, over to you.

**[06:25] Sanjeet Patel:** This one's bigger scope-wise. We're building the exclusion rules engine — categories and keywords ads should never appear next to. We can build the mechanism generically, but we need your actual brand safety policy: the category list you want to block by default, any publisher-specific exceptions, and whether you're standardizing on a third-party verification vendor like DoubleVerify or IAS, or building rules purely in-house.

**[07:30] Karan Mehta:** We do have a policy doc, but it's a couple of years old and honestly needs a refresh before we hand it over — some of the category taxonomy has changed since then.

**[08:00] Divya Shah:** I can get you the current draft this week, but treat it as a working draft, not final. We're still deciding on the verification vendor — that's a commercial conversation happening at a level above me, I don't have a date for that decision yet.

**[08:40] Ananya Rao:** Okay, so two separate blockers there — the policy document, which we can get as a draft this week, and the vendor decision, which is open-ended. Sanjeet, can the engineering work start with just the policy doc, and treat the vendor integration as a separate follow-on story?

**[09:05] Sanjeet Patel:** Yes, that works. I'll split it — rules engine and default category list can start once we have the draft policy. Vendor-specific integration I'll spin into a new backlog item so it doesn't block the sprint.

**[09:40] Ananya Rao:** Good, let's do that. Divya, can you send the draft policy doc by Thursday?

**[09:50] Divya Shah:** Yes, Thursday works.

**[10:05] Ananya Rao:** Third one — ADREV-198, third-party tag creatives. This is currently unassigned on our side since it's fully blocked. Mayank?

**[10:20] Mayank Salunke:** Right, this is about rendering creatives that come from third-party ad tech vendors rather than our own creative library. To build the integration safely — sandboxing, timeout handling, macro support — we need the actual list of vendors you work with today, and ideally sample tags from each so we can test against real formats instead of guessing at a generic spec.

**[11:10] Karan Mehta:** That list exists, it's just scattered across a few people on the commercial side. Let me pull it together — vendors plus contacts who can get us sample tags.

**[11:35] Ananya Rao:** How many vendors are we talking, roughly?

**[11:40] Karan Mehta:** Four active ones today, maybe a fifth coming online next quarter. I'd say don't wait on the fifth.

**[11:55] Ananya Rao:** Understood. Let's target getting the four current vendors and sample tags by the 24th — that gives us two weeks, since I know it involves chasing a few people. I'll log ADREV-198 as blocked pending vendor list and sample tags from Media House commercial team, due 24 July.

**[12:40] Karan Mehta:** That should be doable.

**[13:00] Ananya Rao:** Great, so to summarize the three blockers before we move to sprint numbers: ADREV-187 needs approved ad-blocker messaging copy from legal, target next week. ADREV-6 needs the draft brand safety policy by Thursday, with the vendor decision split into a separate unblocked backlog item. ADREV-198 needs the third-party vendor list and sample tags, target 24 July. All three are logged as active risks against the project so they stay visible.

**[13:50] Mayank Salunke:** Sounds right from our end.

**[14:05] Ananya Rao:** Now, quick sprint numbers. Sprint 10 is at 94% commitment completion as of today, which is right on track — should close clean Friday. Velocity's held steady for the last three sprints, nothing concerning there. Sprint 11 planning is Thursday, and depending on how fast we get that brand safety draft, we may pull ADREV-6 groundwork into it.

**[15:10] Karan Mehta:** Sounds good, no concerns from our side on the numbers.

**[15:25] Ananya Rao:** Anything else before we close? ... Alright, I'll send the recap with owners and dates within the hour. Thanks all, talk next Monday.

**[15:52] — Call ended —**

---

## Action Items From This Call

| Story | Blocker | Owner | Target date |
| --- | --- | --- | --- |
| ADREV-187 — Ad-blocker detection and messaging | Approved messaging/disclosure copy | Divya Shah (Media House Legal) | End of week beginning 20 Jul |
| ADREV-6 — Brand Safety & Verification | Draft brand safety policy + category taxonomy | Divya Shah (Media House Legal) | Thu 16 Jul |
| ADREV-6 (follow-on) — Verification vendor selection | Commercial decision on DoubleVerify/IAS/other | Karan Mehta (Media House) | TBD |
| ADREV-198 — Third-party tag creatives | Vendor list + sample tags (4 vendors) | Karan Mehta (Media House) | 24 Jul |
