# Call Transcript — ADREV Weekly Update

*Project: Advertising & Programmatic Revenue (`ADREV`) · Customer: Media House*
*Weekly status call, ~30 minutes. Transcribed from recording, lightly cleaned up for readability.*
*Chronologically the earliest of the three weekly calls on file — followed by [07-Transcript-ADREV-Weekly-Update-Call-2026-07-13.md](07-Transcript-ADREV-Weekly-Update-Call-2026-07-13.md) and [08-Transcript-ADREV-Weekly-Update-Call-2026-07-20.md](08-Transcript-ADREV-Weekly-Update-Call-2026-07-20.md).*

---

**Date:** Monday, 6 July 2026
**Time:** 4:00 PM – 4:30 PM IST
**Attendees:**
- Ananya Rao — Delivery Manager (PulseAI)
- Mayank Salunke — Tech Lead (PulseAI)
- Sanjeet Patel — Engineer (PulseAI)
- Karan Mehta — Product Owner (Media House)
- Divya Shah — Legal & Compliance Lead (Media House)

---

**[00:00] Ananya Rao:** Thanks all for joining. Agenda today — two items that need input from your side to unblock, and then Karan flagged something on the reconciliation dashboard he wants to walk through. Let's start with engineering status. Mayank?

**[00:20] Mayank Salunke:** Sprint 9 closed clean last week, Sprint 10's underway now. One item I want to flag today — ADREV-190, real-user monitoring for ad performance. We're ready to build it, but we need two things from you before we do: the actual Core Web Vitals thresholds you want us to alert on, and whether the data should feed into your existing analytics stack or a new dashboard we stand up.

**[01:15] Karan Mehta:** What's the existing stack, Divya, do you know? I think ops uses Adobe Analytics for the site overall.

**[01:30] Divya Shah:** That's right, Adobe Analytics is the standard across the site. I don't see a reason to fragment that for ads specifically.

**[01:45] Mayank Salunke:** Good, that's useful — piping into an existing vendor is a very different integration than building a standalone dashboard, so knowing that now saves us from building the wrong thing. I still need the actual threshold numbers though — what LCP, CLS, INP values count as a violation for you.

**[02:15] Karan Mehta:** I don't have those off the top of my head. Let me check with our web performance team and get you numbers this week.

**[02:30] Ananya Rao:** Great, I'll log ADREV-190 as blocked pending Core Web Vitals thresholds from Media House web performance team, target end of this week, with Adobe Analytics confirmed as the integration target.

**[02:50] Ananya Rao:** Second one — ADREV-204, creative expiry and archiving. Sanjeet?

**[03:00] Sanjeet Patel:** This is about what happens to a creative asset once a campaign ends — do we archive it, for how long, and when does it actually get deleted. We can build the mechanism either way, but we need your retention policy before we hardcode a number, especially since Divya's team will care about this from a compliance angle.

**[03:35] Divya Shah:** Good catch. We don't have a formalized retention period for ad creative specifically — it's covered generically under our broader data retention policy, but I'd want to confirm the exact number applies here before you build against it.

**[03:55] Karan Mehta:** Can you check that this week too, Divya? Might as well bundle it with the Core Web Vitals ask.

**[04:05] Divya Shah:** Sure, I'll come back with both by Friday.

**[04:15] Ananya Rao:** Perfect. ADREV-204 logged as blocked pending confirmed creative retention/archival period from Media House legal, target Friday.

**[04:35] Ananya Rao:** Alright, that covers the two blockers. Karan, you wanted to raise something on reconciliation?

**[04:50] Karan Mehta:** Yeah, so I was reviewing the Sprint 10 backlog and I noticed the reconciliation dashboard scope looks narrower than what we discussed. We need it to show total marketing spend across all our channels — social, search, direct, everything — reconciled against actual ad revenue, not just the ad platform's own numbers. That's always been the requirement, it's literally what "reconciliation" means to us.

**[05:40] Ananya Rao:** Let me pull up the BRD section on this while we talk it through. The scope we baselined has reporting, billing, and reconciliation, but specifically for ad revenue — matching booked campaigns against delivered impressions and invoiced amounts. Cross-channel marketing spend, bringing in social and search budgets from other systems, isn't in that section. It's actually called out separately, under corporate marketing spend management, which is listed as out of scope for this project.

**[06:35] Karan Mehta:** I understand what the document says, but that's not how we understood it going in. When we talked about reconciliation in the kickoff, cross-channel was absolutely part of that conversation. This isn't a new ask, it's just showing up in the sprint plan narrower than what we agreed.

**[07:10] Ananya Rao:** I hear you, and I don't doubt that's genuinely your recollection of the kickoff conversation. What I want to avoid is us quietly absorbing a much bigger scope — pulling in spend data from social and search platforms is a whole separate set of integrations, credentials, and data mapping work that isn't sized anywhere in the current estimate.

**[07:55] Karan Mehta:** I get that it's more work, I'm not saying it's free. I'm saying it shouldn't need a change request process, since it was already part of what we signed up for.

**[08:30] Ananya Rao:** Here's what I'd propose — let's not argue the history right now, since neither of us has the kickoff notes in front of us. Let me have the team do a quick scope and effort assessment on cross-channel reconciliation this week, and we bring a number back next Monday. If it turns out it's a small add, we just fold it in. If it's bigger, we treat it as a formal scope item so it's properly reflected in the plan and the estimate, whichever way it goes.

**[09:20] Karan Mehta:** That's fair, as long as it's genuinely being scoped and not just parked. I want it back on the agenda next week with real numbers, not a maybe.

**[09:40] Ananya Rao:** Agreed, I'll make sure it's there. Sanjeet, Mayank, can one of you take a first pass at what a social and search spend integration would actually involve, just enough to size it?

**[09:55] Sanjeet Patel:** I can take that. I'll need to know which platforms specifically — is it just the two major ones, or a longer list?

**[10:10] Karan Mehta:** Google and Meta at minimum, there might be a couple of smaller ones too, I'll send the full list.

**[10:25] Sanjeet Patel:** That helps, thanks.

**[10:40] Ananya Rao:** Okay, logging that as a scope item to size and revisit next Monday — cross-channel marketing spend reconciliation, currently outside the baselined scope per the BRD, pending joint review of the effort estimate and a decision on whether it's absorbed or treated as a formal change.

**[11:10] Ananya Rao:** Quick numbers before we close — Sprint 10 is tracking normally, nothing to flag on velocity. Anything else from anyone?

**[11:30] Karan Mehta:** Nothing from me, thanks for hearing me out on the reconciliation piece.

**[11:40] Ananya Rao:** Of course. I'll send today's recap shortly, including the two blockers and the reconciliation scope item. Talk next Monday.

**[11:52] — Call ended —**

---

## Action Items From This Call

| Item | Type | Owner | Target date |
| --- | --- | --- | --- |
| ADREV-190 — Ad performance real-user monitoring | Blocked — needs Core Web Vitals thresholds; Adobe Analytics confirmed as integration target | Karan Mehta (Media House) | Fri 10 Jul |
| ADREV-204 — Creative expiry and archiving | Blocked — needs confirmed creative retention/archival period | Divya Shah (Media House Legal) | Fri 10 Jul |
| Cross-channel marketing spend reconciliation | Requirement raised by customer as already in scope; not present in baselined BRD scope (listed there under "corporate marketing spend management," out of scope) — logged for joint effort sizing, not yet added to the backlog | Ananya Rao / Sanjeet Patel (PulseAI), pending Karan Mehta's platform list | Revisit Mon 13 Jul |
