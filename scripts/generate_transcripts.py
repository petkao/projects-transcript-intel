"""
Synthetic transcript generator for the Transcript Intelligence take-home.

WHY THIS EXISTS:
The assignment's sample dataset was not provided to the candidate. Per the
assignment's own FAQ ("Can I generate additional data? Yes..."), this script
generates a synthetic dataset of ~100 B2B SaaS call transcripts standing in
for the real one. It is fully transparent synthetic data -- see data/README.md.

DESIGN GOALS (so the downstream pipeline has something real to find):
- Three call types: support, external (AM <-> customer), internal (cross-team).
- A realistic topic taxonomy per call type (10 topics each), not just noise.
- Natural-language sentiment (frustration, relief, enthusiasm, neutrality)
  rather than explicit labels -- the pipeline has to infer it.
- Three deliberate longitudinal "story" threads woven through the data so
  sentiment/topic trends actually mean something:
    1. A CSV/report export bug (truncates >50k rows) that shows up in support
       calls starting week 1, gets escalated internally week 2-3, sits in
       backlog, finally ships a fix week 6, and support sentiment recovers
       week 7+. A customer also raises it as a renewal risk in week 5.
    2. A competitor ("Lumina Analytics") poaching attempt that surfaces in a
       handful of external renewal calls and one internal competitive-strategy
       sync, mid-dataset.
    3. A new feature launch ("Smart Alerts") that drives upsell enthusiasm in
       external calls and an internal launch-planning call, back half of the
       dataset.
  These threads are NOT labeled in the output -- they're just how the
  dialogue content is constructed. They exist so a topic/sentiment pipeline
  has genuine cross-channel correlations to surface.
"""

import json
import random
from datetime import datetime, timedelta

random.seed(42)

OUT_PATH = "../data/transcripts.jsonl"
INDEX_PATH = "../data/transcripts_index.csv"

START_DATE = datetime(2026, 7, 1)
TOTAL_DAYS = 90

CUSTOMERS = [
    "Northwind Logistics", "Brightfield Health", "Castellan Insurance",
    "Vantage Retail Group", "Summit Manufacturing", "Harborview Financial",
    "Ridgeline Energy", "Marbury Legal Services", "Clearwater Biotech",
    "Union Square Media", "Pinecrest Education", "Delacroix Hospitality",
    "Alderman Consulting", "Westbrook Logistics", "Coral Bay Analytics",
    "Granite Peak Manufacturing", "Silverline Telecom", "Ashford Realty Group",
    "Fenwick & Co", "Trestle Robotics",
]

AM_NAMES = ["Jordan Mills", "Priya Anand", "Casey Lindqvist", "Marcus Webb", "Teodora Ilic"]
SUPPORT_AGENTS = ["Dana Okafor", "Liam Chen", "Ruth Fontaine", "Omar Siddiqui", "Alexis Park"]
ENGINEERS = ["Nikhil Rao", "Sam Doyle", "Beatriz Souza", "Finn Walsh", "Yuki Tanaka", "Greta Holm"]
PMS = ["Wes Carrington", "Mina Oyelaran", "Devon Pratt"]
ENG_LEADS = ["Sofia Reyes", "Tobias Krantz"]
CUSTOMER_CONTACTS = [
    "Taylor Grant", "Morgan Reyes", "Elena Vasquez", "Chris Patel", "Nadia Brooks",
    "Sam Oduya", "Jules Ferreira", "Priya Nair", "Owen Castellan", "Robin Haas",
]

PRODUCT = "Meridian"  # fictional B2B SaaS product name


def speaker_line(name, text):
    return f"{name}: {text}"


def pick(lst):
    return random.choice(lst)


def join_turns(turns):
    return "\n".join(turns)


# ---------------------------------------------------------------------------
# SUPPORT CALL TEMPLATES
# ---------------------------------------------------------------------------

def gen_support_export_bug(agent, customer_name, contact, severity):
    """The recurring narrative bug: CSV export truncates on large datasets."""
    opener = pick([
        f"Hi, this is {contact} from {customer_name}. We're having a real problem with the reporting export again.",
        f"Hey, {contact} here from {customer_name}. Our export is cutting off data and it's starting to really hurt us.",
        f"Hi, it's {contact} at {customer_name}. Same export issue as last time -- it's back.",
    ])
    mid = pick([
        "We pulled a report with about eighty thousand rows and it just stops at fifty thousand. No error, no warning, it just truncates.",
        "Every time we export anything over fifty thousand rows the file just cuts off silently. We almost sent bad numbers to our board.",
        "Our finance team built a quarterly summary off one of these exports and didn't notice it was incomplete until a VP caught it.",
    ])
    frustration = pick([
        "Honestly this is the third time I've called about this exact thing and I was told it was fixed in September.",
        "I get that bugs happen, but this is a trust problem now, not just a technical one.",
        "I don't want to escalate this but I'm two weeks from our board meeting and I need to know we can rely on this.",
    ]) if severity == "high" else pick([
        "It's not the end of the world, but it's the second time this month.",
        "Can you at least confirm there's a ticket open for this already?",
    ])
    agent_ack = pick([
        f"{agent}: I completely understand, and I'm sorry you're hitting this again. Let me pull up the open bug on this.",
        f"{agent}: That's really frustrating to hear, especially the second time around. Let me check the status on the engineering side.",
    ])
    agent_detail = pick([
        f"{agent}: I can see there's an existing ticket (EXP-1142) tracking exactly this -- exports over fifty thousand rows silently truncate due to a pagination limit in the export worker. It's flagged as high priority but I don't have a ship date yet.",
        f"{agent}: Looking at the backlog, this is a known issue with the export worker's row limit. It's been escalated to engineering but I can't promise a date today.",
    ])
    closer = pick([
        f"{contact}: Okay. I need something more concrete than 'we're working on it.' Can someone follow up with an actual timeline by Friday?",
        f"{contact}: Alright, I'll wait, but please have your team call me directly when there's an update. This can't keep happening.",
    ])
    agent_close = pick([
        f"{agent}: Absolutely, I'll flag this as a priority follow-up and loop in our escalations team so you get a real timeline, not just a ticket number.",
        f"{agent}: I'll personally make sure this gets escalated today and someone reaches back out with a concrete date.",
    ])
    return join_turns([
        speaker_line(contact, opener),
        speaker_line(agent, "I'm sorry to hear that -- can you walk me through exactly what happened?"),
        speaker_line(contact, mid),
        speaker_line(contact, frustration),
        agent_ack,
        agent_detail,
        closer,
        agent_close,
    ])


def gen_support_export_bug_resolved(agent, customer_name, contact):
    opener = pick([
        f"Hi {agent}, it's {contact} from {customer_name} again. Wanted to follow up on the export issue.",
        f"Hey, {contact} here. Just ran the export we talked about last week.",
    ])
    good_news = pick([
        "I just want to say -- it worked. We exported about ninety thousand rows and got the full file, no truncation.",
        "The export came through complete this time, all rows, no issues. That's a relief honestly.",
    ])
    relief = pick([
        "Our finance team is pretty happy, we were starting to lose confidence in the numbers.",
        "Good timing too, we had a report due to leadership this week.",
    ])
    agent_resp = pick([
        f"{agent}: That's great to hear! The fix shipped last week, it raised the export row limit and added proper pagination so large files won't get cut off anymore.",
        f"{agent}: Glad it's working! Engineering shipped the fix last Thursday -- it removes the old row cap entirely.",
    ])
    closer = pick([
        f"{contact}: Appreciate the team staying on it. Please pass along the thanks.",
        f"{contact}: Thanks for not letting this drop. It matters more than you'd think.",
    ])
    return join_turns([
        speaker_line(contact, opener),
        speaker_line(agent, "Oh good, how did it go?"),
        speaker_line(contact, good_news),
        speaker_line(contact, relief),
        agent_resp,
        closer,
    ])


SUPPORT_TOPICS = [
    "billing", "login_sso", "export_bug", "performance", "integration_api",
    "how_to", "onboarding", "security_compliance", "cancellation_downgrade",
    "positive_checkin",
]

SUPPORT_BODY = {
    "billing": [
        ("I'm looking at our last invoice and the seat count seems off -- we removed five users last month but we're still being billed for them.",
         "Let me pull up your account... you're right, the deactivation didn't sync to billing. I'll issue a credit for the difference and fix the sync."),
        ("We were charged for the Enterprise tier but I thought we downgraded to Pro back in May?",
         "I see the downgrade request but it looks like it never got processed on our end -- I'm sorry about that. I'll backdate the correction and refund the difference."),
        ("Can you explain why there's an overage charge on this invoice? We didn't think we were near our usage limit.",
         "Good question -- looking at your usage dashboard, there was a spike from an API integration pulling data more frequently than expected. I can show you where that happened."),
    ],
    "login_sso": [
        ("Half our team got locked out this morning, nobody can log in through our SSO.",
         "That sounds like it could be a SAML assertion issue on our end -- let me check the identity provider logs for your org."),
        ("I keep getting kicked back to the login page after I authenticate through Okta. It just loops.",
         "That's usually a session cookie or clock-skew issue between our app and the IdP. Let's check your Okta app config together."),
        ("New hires aren't able to self-provision through SSO, they're stuck with no account at all.",
         "Let's check whether just-in-time provisioning is enabled for your SSO connection -- that might be turned off."),
    ],
    "export_bug": "SPECIAL",
    "performance": [
        ("The dashboard has been really slow the last few days, sometimes thirty seconds just to load a page.",
         "I'm sorry about that -- let me check if your org is on one of the clusters we flagged for a capacity issue this week."),
        ("Running any report with a date range over sixty days just times out now.",
         "That's a known strain point for us with larger date ranges, I'll log this and see if we can get you on an optimized query path."),
        ("Is something wrong on your end? Everything in the app feels sluggish today, not just one feature.",
         "We did have a brief regional slowdown about two hours ago, it should be resolved now, but let me confirm your region specifically."),
    ],
    "integration_api": [
        ("Our Salesforce sync stopped pulling new leads sometime yesterday, nothing's come through since.",
         "Let's check the integration logs -- it might be an expired OAuth token on the Salesforce side."),
        ("We're getting intermittent 500s from your API when we batch update more than a hundred records at once.",
         "That's helpful detail, batch size over a hundred sounds like it could be hitting a timeout on our ingestion endpoint. Let me check with engineering."),
        ("The webhook for deal-stage-changed just... stopped firing about a week ago.",
         "Let's verify the webhook subscription is still active -- sometimes those get disabled after repeated delivery failures."),
    ],
    "how_to": [
        ("I can't figure out how to set up a custom field that only certain roles can see.",
         "Sure, that's under Settings > Custom Fields > Visibility -- let me walk you through it."),
        ("Is there a way to schedule a report to email automatically every Monday?",
         "Yes, under Reports you can set a recurring schedule -- I'll show you where that toggle lives."),
        ("How do we bulk-import contacts without creating duplicates?",
         "There's a dedupe setting in the import wizard based on email match, let me walk you through the import flow."),
    ],
    "onboarding": [
        ("We're about two weeks into rollout and the team's still confused about permission levels.",
         "That's really common early on -- want to do a quick screen-share so I can walk your admins through the role hierarchy?"),
        ("Our implementation lead left the company mid-rollout and we're a bit lost on next steps.",
         "I'm sorry to hear that -- let's get you reassigned to someone on our side and pick up where things left off."),
        ("Can someone walk our new admins through the workspace settings? We inherited this from the last team.",
         "Of course, I can set up a session this week to go through admin settings end to end."),
    ],
    "security_compliance": [
        ("Our security team needs your latest SOC 2 report before we can expand usage.",
         "I can get that sent over today, we recertified in April so it should be current."),
        ("Can you confirm where customer data is physically stored? We have a new data residency requirement.",
         "Good question, let me get you the exact region info and loop in our compliance team if you need it in writing."),
        ("We need to understand your data retention policy for a GDPR audit we're going through.",
         "Happy to help, I'll send our data retention documentation and set up a call with our privacy team if needed."),
    ],
    "cancellation_downgrade": [
        ("We're seriously considering not renewing. Usage has dropped a lot since our main champion left.",
         "I hear you, and I don't want to just talk you out of it -- can you tell me more about what changed on your end?"),
        ("We'd like to downgrade to a smaller plan, we're just not using half the seats we're paying for.",
         "That's fair, let's look at your actual usage together and figure out the right tier instead of just guessing."),
        ("Honestly we're evaluating a couple other tools right now because the ROI case is getting harder to make internally.",
         "I appreciate you being upfront. Can I get on a call with your champion to understand what would change the math?"),
    ],
    "positive_checkin": [
        ("Just wanted to say the new dashboard update has been great, the team's actually using it daily now.",
         "That's wonderful to hear, I'll pass that along to the product team, they'll be glad to know it's landing well."),
        ("No issues to report, just checking in -- things have honestly been smooth this quarter.",
         "Great to hear, always happy when a call is just good news."),
        ("The onboarding for our new hires went way faster this time, whatever you changed worked.",
         "That's great feedback, we did rework the onboarding checklist recently, glad it's showing."),
    ],
}


def gen_support_generic(agent, contact, topic):
    body_options = SUPPORT_BODY[topic]
    customer_line, agent_line = pick(body_options)
    opener = pick([
        f"Hi, this is {contact}, calling about an issue we're seeing.",
        f"Hey, {contact} here, hoping you can help with something.",
        f"Hi, it's {contact} -- got a few minutes?",
    ])
    followup = pick([
        f"{contact}: Okay, that makes sense, thanks for explaining.",
        f"{contact}: Got it, appreciate the quick turnaround on this.",
        f"{contact}: Alright, that's good to know. Anything you need from my side?",
    ])
    agent_close = pick([
        f"{agent}: Not at the moment, I'll follow up once this is fully resolved on our end.",
        f"{agent}: Nope, I've got what I need. I'll send a summary email after this call.",
        f"{agent}: All good, I'll keep you posted if anything changes.",
    ])
    return join_turns([
        speaker_line(contact, opener),
        speaker_line(agent, "Of course, what's going on?"),
        speaker_line(contact, customer_line),
        speaker_line(agent, agent_line),
        followup,
        agent_close,
    ])


# ---------------------------------------------------------------------------
# EXTERNAL CALL TEMPLATES (Account Manager <-> Customer)
# ---------------------------------------------------------------------------

EXTERNAL_TOPICS = [
    "renewal_healthy", "renewal_risk_export_bug", "renewal_risk_competitor",
    "qbr", "upsell_smart_alerts", "escalation_unresolved",
    "feature_request", "contract_terms", "success_checkin", "reference_request",
]


def gen_external_renewal_healthy(am, customer_name, contact):
    return join_turns([
        speaker_line(am, f"Hi {contact}, thanks for making time -- wanted to talk through the renewal coming up next month."),
        speaker_line(contact, "Sure, happy to. Overall it's been a good year, usage has actually grown across a couple teams."),
        speaker_line(am, "That matches what I'm seeing on our end too -- adoption's up about thirty percent year over year for your org."),
        speaker_line(contact, "Yeah, the ops team basically lives in the tool now. I don't see any reason we wouldn't renew."),
        speaker_line(am, "Great to hear. Given the growth, would it make sense to talk about adding seats for the two newer teams?"),
        speaker_line(contact, "Possibly, let me check budget on my end, but I'm open to the conversation."),
        speaker_line(am, "Perfect, I'll send over a proposal with a couple options and we can regroup next week."),
    ])


def gen_external_renewal_risk_export(am, customer_name, contact):
    return join_turns([
        speaker_line(am, f"Hi {contact}, wanted to check in ahead of the renewal -- how's everything feeling on your end?"),
        speaker_line(contact, "Honestly, mixed. The product itself is fine but we've had real problems with the reporting export, more than once."),
        speaker_line(am, "I did see that come through on the support side. I'm sorry that's been a recurring headache."),
        speaker_line(contact, "It's more than a headache -- it's made my team nervous trusting the numbers we send up to leadership."),
        speaker_line(am, "That's completely fair, and I don't want to undersell how seriously we're taking it. I know engineering has it flagged as high priority."),
        speaker_line(contact, "I need to see it actually fixed before we commit to another year at this size. I can't keep explaining this to my VP."),
        speaker_line(am, "Understood. Let me get you a firm timeline directly from the engineering lead this week rather than another vague update, and let's hold the renewal conversation until that's resolved."),
        speaker_line(contact, "That works. I want to stay, I just need confidence it won't keep happening."),
    ])


def gen_external_renewal_risk_competitor(am, customer_name, contact):
    return join_turns([
        speaker_line(am, f"Hey {contact}, how are things going ahead of the renewal discussion?"),
        speaker_line(contact, "I'll be honest with you -- we've been evaluating Lumina Analytics as an alternative."),
        speaker_line(am, "I appreciate you telling me directly. Can I ask what's driving that?"),
        speaker_line(contact, "Mostly pricing, their quote came in meaningfully lower, and their new dashboards look pretty slick in the demo."),
        speaker_line(am, "That's useful to know. We've actually just shipped some new alerting and reporting capability that might close some of that gap -- can I show you before you decide anything?"),
        speaker_line(contact, "Sure, I'm not set on switching, it's early. But the price difference is real and I'll need a good reason to justify staying."),
        speaker_line(am, "Fair enough, let me put together a comparison and see what we can do on pricing too. I'd rather have that conversation than lose you to a feature gap we've already closed."),
    ])


def gen_external_qbr(am, customer_name, contact):
    return join_turns([
        speaker_line(am, f"Thanks for joining the QBR, {contact}. Let's walk through the last quarter."),
        speaker_line(contact, "Sounds good, go ahead."),
        speaker_line(am, "Usage is up, active users grew from about 80 to 110, and your team's running roughly 40% more reports than last quarter."),
        speaker_line(contact, "That tracks, we rolled it out to the regional ops teams in April."),
        speaker_line(am, "On the support side, you had six tickets this quarter, mostly resolved within a day except the export issue which took longer."),
        speaker_line(contact, "Yeah that one was rough, but otherwise it's been smooth. Any new features coming we should know about?"),
        speaker_line(am, "Yes, actually -- we just launched Smart Alerts, it might be relevant for your ops team's monitoring use case."),
        speaker_line(contact, "Interesting, send me more on that, could be useful."),
    ])


def gen_external_upsell_smart_alerts(am, customer_name, contact):
    return join_turns([
        speaker_line(am, f"Hi {contact}, wanted to tell you about something we just shipped -- Smart Alerts."),
        speaker_line(contact, "Oh nice, what does it do?"),
        speaker_line(am, "It lets you set threshold-based alerts on any metric in your dashboards, so instead of checking reports manually your team gets notified automatically."),
        speaker_line(contact, "That's actually exactly what we've been asking for internally. We've been manually checking dashboards every morning."),
        speaker_line(am, "That's great to hear, it's included in the Pro tier, I can get it turned on for you today if you want to try it."),
        speaker_line(contact, "Yes please, turn it on. If this works like you're describing it could save my team a lot of time."),
        speaker_line(am, "I'll get it enabled and send over a quick setup guide. Would love thirty minutes next week to hear how it's going."),
        speaker_line(contact, "Definitely, this is the kind of thing that makes the renewal conversation easy, honestly."),
    ])


def gen_external_escalation_unresolved(am, customer_name, contact):
    return join_turns([
        speaker_line(contact, f"Hey, I wanted to escalate something directly to you -- we're still waiting on the export bug fix."),
        speaker_line(am, "I know, I'm sorry it's dragged on this long. Let me get you a direct update from engineering today instead of routing through support again."),
        speaker_line(contact, "I'd appreciate that. This has come up in three support calls now and nothing's changed."),
        speaker_line(am, "Understood, that's on us. I'll personally check with the eng lead and call you back today with a real date."),
        speaker_line(contact, "Thank you, I just need to feel like this is being taken seriously at this point."),
    ])


EXTERNAL_BODY = {
    "feature_request": [
        ("Our team has been asking for a way to customize the dashboard layout per role, is that on the roadmap?",
         "That's come up from a couple other accounts too, let me check with product and see where it sits on the roadmap."),
        ("Would it be possible to get native Slack notifications instead of just email?",
         "I like that idea, let me bring it to the product team as a formal request and see if we can get visibility into timing."),
    ],
    "contract_terms": [
        ("Legal wants to revisit the data processing addendum before we sign the renewal.",
         "No problem, I'll loop in our legal team and get a redline turned around quickly."),
        ("Can we adjust the auto-renewal clause, we'd prefer a manual opt-in each year?",
         "That's a reasonable ask, let me check what flexibility we have there and get back to you."),
    ],
    "success_checkin": [
        ("Just wanted to check in, nothing urgent, things have been going well this quarter.",
         "Good to hear, always nice to have an easy call. Anything on the horizon I should know about?"),
        ("Overall really happy, the team adopted the new workflow faster than expected.",
         "That's great news, I'll make sure that gets shared internally too, it's always good to hear."),
    ],
    "reference_request": [
        ("We've had such a good experience, would you be open to us doing a case study together?",
         "Absolutely, I'd love that, let me connect you with our customer marketing team to scope it out."),
        ("A prospect reached out asking if they could talk to a reference customer, would you be willing?",
         "Happy to help if it's a good fit, let me get some context on the prospect first."),
    ],
}


def gen_external_generic(am, contact, topic):
    customer_line, am_line = pick(EXTERNAL_BODY[topic])
    return join_turns([
        speaker_line(am, f"Hi {contact}, thanks for hopping on, what's on your mind today?"),
        speaker_line(contact, customer_line),
        speaker_line(am, am_line),
        speaker_line(contact, "Sounds good, appreciate you looking into it."),
        speaker_line(am, "Of course, I'll follow up with next steps by end of week."),
    ])


# ---------------------------------------------------------------------------
# INTERNAL CALL TEMPLATES
# ---------------------------------------------------------------------------

INTERNAL_TOPICS = [
    "bug_triage_export", "cross_team_escalation_export", "roadmap_planning",
    "incident_postmortem", "sprint_planning", "launch_planning_smart_alerts",
    "hiring_discussion", "competitive_strategy", "security_review", "churn_risk_review",
]


def gen_internal_bug_triage_export(stage, eng1, eng2, lead):
    if stage == "early":
        return join_turns([
            speaker_line(lead, "Let's talk about EXP-1142, the export truncation bug. We've had three support tickets on this in the last two weeks."),
            speaker_line(eng1, "Yeah I looked at it briefly, it's the export worker -- there's a hardcoded pagination cutoff at fifty thousand rows that was meant to be temporary."),
            speaker_line(eng2, "That cutoff's been there since the original export rewrite, I think everyone just forgot about it because it rarely got hit."),
            speaker_line(lead, "It's getting hit now because our bigger accounts have way more data than they did a year ago."),
            speaker_line(eng1, "Makes sense. Fixing it properly means re-architecting the pagination rather than just raising the limit, which is a bigger lift."),
            speaker_line(lead, "How big are we talking?"),
            speaker_line(eng2, "Maybe a week of real work plus testing on large datasets. It's not trivial, but it's not a huge project either."),
            speaker_line(lead, "Okay, given we've got three tickets and at least one account threatening churn over it, I want this prioritized for next sprint, not the one after."),
        ])
    elif stage == "escalation":
        return join_turns([
            speaker_line(lead, "Support just flagged that the export bug came up again, this time with a customer explicitly tying it to renewal risk."),
            speaker_line(eng1, "We haven't started the fix yet, it's queued for next sprint per last week's call."),
            speaker_line(lead, "I need to pull it forward. Can we start this now instead of waiting for sprint planning?"),
            speaker_line(eng2, "We can, it'll bump something else, probably the API rate limit work."),
            speaker_line(lead, "That's an acceptable tradeoff given this is now a revenue risk, not just a bug."),
            speaker_line(eng1, "Understood, I'll start on the pagination rework today."),
        ])
    else:  # shipped
        return join_turns([
            speaker_line(eng1, "Good news -- the export fix is live as of this morning, removed the row cap and switched to cursor-based pagination."),
            speaker_line(lead, "That's great. Any regressions in testing?"),
            speaker_line(eng2, "Tested up to half a million rows without issues, and added monitoring so we'd catch silent truncation earlier next time."),
            speaker_line(lead, "Good call on the monitoring. Let's get support and the account team notified so they can close the loop with affected customers."),
            speaker_line(eng1, "Already pinged the support lead, they're going to proactively reach out to the accounts that complained."),
        ])


def gen_internal_cross_team_escalation(am_or_support, lead):
    return join_turns([
        speaker_line(am_or_support, "I want to flag that the export bug has now come up in a renewal call, not just support tickets. It's a real risk for at least one account."),
        speaker_line(lead, "Got it, that changes the priority. Engineering already has it on the radar but I'll push to pull it forward."),
        speaker_line(am_or_support, "I'd appreciate that. I don't want to lose this account over something that's fixable."),
        speaker_line(lead, "Agreed, let me talk to the eng lead today and get you a real timeline by tomorrow."),
    ])


def gen_internal_roadmap_planning(pm, eng_lead):
    return join_turns([
        speaker_line(pm, "For next quarter, I want to prioritize reliability work on exports and reporting given the pattern we've seen in support tickets."),
        speaker_line(eng_lead, "Agreed, that cluster of complaints has been consistent for weeks, it shouldn't have taken this long to surface as a priority honestly."),
        speaker_line(pm, "Fair, I think part of the problem is support tickets and account escalations aren't visible to engineering in one place."),
        speaker_line(eng_lead, "That's a good point, we're basically relying on someone manually noticing the pattern instead of having it surfaced automatically."),
        speaker_line(pm, "Yeah, that itself might be worth building -- some kind of cross-channel signal aggregation so we catch these patterns faster next time."),
        speaker_line(eng_lead, "I like that. Let's scope it as a smaller internal tooling project alongside the bigger roadmap items."),
    ])


def gen_internal_incident_postmortem(eng1, eng2, lead):
    return join_turns([
        speaker_line(lead, "Let's go through the postmortem for last week's regional slowdown."),
        speaker_line(eng1, "Root cause was a database connection pool exhaustion during a traffic spike from one large customer's batch job."),
        speaker_line(eng2, "We didn't have alerting on pool saturation specifically, only on overall latency, so we caught it later than we should have."),
        speaker_line(lead, "How long was the customer-visible impact?"),
        speaker_line(eng1, "About forty minutes of degraded performance, no full outage, but several customers noticed and a few filed support tickets."),
        speaker_line(lead, "Okay, action items: add pool saturation alerting, and let's look at rate-limiting batch jobs from a single tenant."),
        speaker_line(eng2, "I'll own the alerting piece, should be done by end of week."),
    ])


def gen_internal_sprint_planning(eng1, eng2, lead):
    return join_turns([
        speaker_line(lead, "Let's lock sprint scope. Top priority is the export pagination fix, that's now a must-ship."),
        speaker_line(eng1, "I can take that, I already scoped it last week."),
        speaker_line(eng2, "I'll take the API rate limit work we pushed from last sprint, plus a couple smaller bug fixes from the backlog."),
        speaker_line(lead, "Sounds good. Anything blocking either of you?"),
        speaker_line(eng1, "Just need a staging dataset large enough to properly test the export fix, over a hundred thousand rows."),
        speaker_line(lead, "I'll get that set up today so it doesn't block you."),
    ])


def gen_internal_launch_planning_smart_alerts(pm, eng_lead, am):
    return join_turns([
        speaker_line(pm, "Smart Alerts is on track to ship this week, let's talk rollout."),
        speaker_line(eng_lead, "Engineering side is ready, we finished load testing the alert evaluation service yesterday."),
        speaker_line(am, "On the account side, I've got a shortlist of accounts to pitch it to first, mostly ones that have asked for something like this before."),
        speaker_line(pm, "Good, let's prioritize the accounts we flagged as at-risk too, especially the ones evaluating competitors -- this is a good retention lever."),
        speaker_line(am, "Agreed, I've already got a couple of those conversations lined up this week."),
        speaker_line(eng_lead, "We'll keep an eye on adoption metrics the first week in case anything needs tuning."),
    ])


def gen_internal_hiring_discussion(lead, pm):
    return join_turns([
        speaker_line(lead, "We need to talk about headcount for the platform team, we're stretched thin with the export rework plus normal roadmap work."),
        speaker_line(pm, "Agreed, I think we've been underinvesting in the data pipeline side generally, it's not just this one bug."),
        speaker_line(lead, "I want to open a req for a senior backend engineer focused on the export and reporting pipeline specifically."),
        speaker_line(pm, "Makes sense, I'll support that in planning. Can you have a job description draft by next week?"),
        speaker_line(lead, "Yes, I'll have it ready for review by Wednesday."),
    ])


def gen_internal_competitive_strategy(pm, am, lead):
    return join_turns([
        speaker_line(am, "A few accounts have mentioned Lumina Analytics in renewal conversations recently, mostly on pricing."),
        speaker_line(pm, "That's useful, do we know what specifically they're pitching?"),
        speaker_line(am, "Lower price point and a slicker-looking dashboard UI from what customers describe, functionality seems comparable overall."),
        speaker_line(lead, "Smart Alerts might help close some of that gap since it's a newer capability they may not have yet."),
        speaker_line(pm, "Agreed, let's get a competitive one-pager together for the account team so they're not caught off guard in these calls."),
        speaker_line(am, "That would help a lot, right now everyone's answering these questions a little differently."),
    ])


def gen_internal_security_review(lead, eng1):
    return join_turns([
        speaker_line(lead, "We've had a few customers ask for updated SOC 2 documentation and data residency details this quarter."),
        speaker_line(eng1, "That's been coming up more as we land larger enterprise accounts, makes sense."),
        speaker_line(lead, "Let's make sure the compliance packet is easy for account teams to hand out without looping in engineering every time."),
        speaker_line(eng1, "Agreed, I can help put together a self-serve doc with the common things that get asked."),
    ])


def gen_internal_churn_risk_review(pm, am, lead):
    return join_turns([
        speaker_line(pm, "Let's review accounts flagged as at-risk this month."),
        speaker_line(am, "Two stand out -- one is evaluating Lumina Analytics on pricing, the other is blocked on the export bug and won't commit to renewal until it's fixed."),
        speaker_line(lead, "The export fix is already prioritized for this sprint, so that one should resolve itself if we ship on time."),
        speaker_line(pm, "Good. For the pricing-driven one, I think Smart Alerts plus a pricing conversation is probably our best retention play."),
        speaker_line(am, "Agreed, I'll loop in the account exec on pricing flexibility this week."),
    ])


# ---------------------------------------------------------------------------
# ASSEMBLY
# ---------------------------------------------------------------------------

records = []
call_id = 1


def add_record(call_type, day_offset, topic, transcript, account_name, participants, duration_min):
    global call_id
    date = START_DATE + timedelta(days=day_offset)
    records.append({
        "call_id": f"CALL-{call_id:04d}",
        "call_type": call_type,
        "date": date.strftime("%Y-%m-%d"),
        "duration_minutes": duration_min,
        "account_name": account_name,
        "participants": participants,
        "transcript": transcript,
        "word_count": len(transcript.split()),
        # Ground-truth label from generation, kept ONLY for validating the
        # categorization pipeline against known answers. The pipeline itself
        # must not read this field -- it's the "answer key", not an input.
        "synthetic_topic_label": topic,
    })
    call_id += 1


# --- SUPPORT: 34 calls ---
# Narrative: export bug complaints weeks 1-6 (high severity), then resolved calls week 7-9.
export_bug_days = sorted(random.sample(range(2, 40), 7))
for d in export_bug_days:
    customer = pick(CUSTOMERS)
    contact = pick(CUSTOMER_CONTACTS)
    agent = pick(SUPPORT_AGENTS)
    severity = "high" if d > 20 else "medium"
    transcript = gen_support_export_bug(agent, customer, contact, severity)
    add_record("support", d, "export_bug", transcript, customer, [agent, contact], random.randint(8, 22))

resolved_days = sorted(random.sample(range(44, 60), 4))
for d in resolved_days:
    customer = pick(CUSTOMERS)
    contact = pick(CUSTOMER_CONTACTS)
    agent = pick(SUPPORT_AGENTS)
    transcript = gen_support_export_bug_resolved(agent, customer, contact)
    add_record("support", d, "export_bug_resolved", transcript, customer, [agent, contact], random.randint(4, 10))

# Generic support topics spread across the whole window
generic_support_topics = [t for t in SUPPORT_TOPICS if t != "export_bug"]
for _ in range(23):
    topic = pick(generic_support_topics)
    d = random.randint(0, TOTAL_DAYS)
    customer = pick(CUSTOMERS)
    contact = pick(CUSTOMER_CONTACTS)
    agent = pick(SUPPORT_AGENTS)
    transcript = gen_support_generic(agent, contact, topic)
    add_record("support", d, topic, transcript, customer, [agent, contact], random.randint(5, 18))

# --- EXTERNAL: 33 calls ---
renewal_risk_export_days = sorted(random.sample(range(25, 45), 3))
for d in renewal_risk_export_days:
    customer = pick(CUSTOMERS)
    contact = pick(CUSTOMER_CONTACTS)
    am = pick(AM_NAMES)
    transcript = gen_external_renewal_risk_export(am, customer, contact)
    add_record("external", d, "renewal_risk_export_bug", transcript, customer, [am, contact], random.randint(15, 30))

escalation_days = sorted(random.sample(range(15, 35), 3))
for d in escalation_days:
    customer = pick(CUSTOMERS)
    contact = pick(CUSTOMER_CONTACTS)
    am = pick(AM_NAMES)
    transcript = gen_external_escalation_unresolved(am, customer, contact)
    add_record("external", d, "escalation_unresolved", transcript, customer, [am, contact], random.randint(6, 14))

competitor_days = sorted(random.sample(range(35, 65), 4))
for d in competitor_days:
    customer = pick(CUSTOMERS)
    contact = pick(CUSTOMER_CONTACTS)
    am = pick(AM_NAMES)
    transcript = gen_external_renewal_risk_competitor(am, customer, contact)
    add_record("external", d, "renewal_risk_competitor", transcript, customer, [am, contact], random.randint(15, 25))

upsell_days = sorted(random.sample(range(55, 88), 6))
for d in upsell_days:
    customer = pick(CUSTOMERS)
    contact = pick(CUSTOMER_CONTACTS)
    am = pick(AM_NAMES)
    transcript = gen_external_upsell_smart_alerts(am, customer, contact)
    add_record("external", d, "upsell_smart_alerts", transcript, customer, [am, contact], random.randint(12, 25))

renewal_healthy_days = sorted(random.sample(range(0, 90), 7))
for d in renewal_healthy_days:
    customer = pick(CUSTOMERS)
    contact = pick(CUSTOMER_CONTACTS)
    am = pick(AM_NAMES)
    transcript = gen_external_renewal_healthy(am, customer, contact)
    add_record("external", d, "renewal_healthy", transcript, customer, [am, contact], random.randint(15, 28))

qbr_days = sorted(random.sample(range(0, 90), 4))
for d in qbr_days:
    customer = pick(CUSTOMERS)
    contact = pick(CUSTOMER_CONTACTS)
    am = pick(AM_NAMES)
    transcript = gen_external_qbr(am, customer, contact)
    add_record("external", d, "qbr", transcript, customer, [am, contact], random.randint(20, 35))

generic_external_topics = list(EXTERNAL_BODY.keys())
for _ in range(6):
    topic = pick(generic_external_topics)
    d = random.randint(0, TOTAL_DAYS)
    customer = pick(CUSTOMERS)
    contact = pick(CUSTOMER_CONTACTS)
    am = pick(AM_NAMES)
    transcript = gen_external_generic(am, contact, topic)
    add_record("external", d, topic, transcript, customer, [am, contact], random.randint(8, 20))

# --- INTERNAL: 33 calls ---
add_record("internal", 8, "bug_triage_export_early", gen_internal_bug_triage_export("early", pick(ENGINEERS), pick(ENGINEERS), pick(ENG_LEADS)),
            "Platform Team", [pick(ENG_LEADS), pick(ENGINEERS)], 25)
add_record("internal", 22, "bug_triage_export_escalation", gen_internal_bug_triage_export("escalation", pick(ENGINEERS), pick(ENGINEERS), pick(ENG_LEADS)),
            "Platform Team", [pick(ENG_LEADS), pick(ENGINEERS)], 15)
add_record("internal", 40, "bug_triage_export_shipped", gen_internal_bug_triage_export("shipped", pick(ENGINEERS), pick(ENGINEERS), pick(ENG_LEADS)),
            "Platform Team", [pick(ENG_LEADS), pick(ENGINEERS)], 12)

for d in sorted(random.sample(range(15, 35), 3)):
    add_record("internal", d, "cross_team_escalation_export",
                gen_internal_cross_team_escalation(pick(AM_NAMES + SUPPORT_AGENTS), pick(ENG_LEADS)),
                "Cross-team", [pick(ENG_LEADS)], 10)

for d in sorted(random.sample(range(0, 90), 4)):
    add_record("internal", d, "roadmap_planning", gen_internal_roadmap_planning(pick(PMS), pick(ENG_LEADS)),
                "Product Team", [pick(PMS), pick(ENG_LEADS)], 30)

for d in sorted(random.sample(range(0, 90), 4)):
    add_record("internal", d, "incident_postmortem", gen_internal_incident_postmortem(pick(ENGINEERS), pick(ENGINEERS), pick(ENG_LEADS)),
                "Platform Team", [pick(ENG_LEADS)], 20)

for d in sorted(random.sample(range(0, 90), 5)):
    add_record("internal", d, "sprint_planning", gen_internal_sprint_planning(pick(ENGINEERS), pick(ENGINEERS), pick(ENG_LEADS)),
                "Platform Team", [pick(ENG_LEADS)], 25)

for d in sorted(random.sample(range(50, 85), 3)):
    add_record("internal", d, "launch_planning_smart_alerts", gen_internal_launch_planning_smart_alerts(pick(PMS), pick(ENG_LEADS), pick(AM_NAMES)),
                "Cross-functional", [pick(PMS), pick(ENG_LEADS)], 22)

for d in sorted(random.sample(range(0, 90), 3)):
    add_record("internal", d, "hiring_discussion", gen_internal_hiring_discussion(pick(ENG_LEADS), pick(PMS)),
                "Platform Team", [pick(ENG_LEADS), pick(PMS)], 15)

for d in sorted(random.sample(range(35, 70), 3)):
    add_record("internal", d, "competitive_strategy", gen_internal_competitive_strategy(pick(PMS), pick(AM_NAMES), pick(ENG_LEADS)),
                "Cross-functional", [pick(PMS)], 20)

for d in sorted(random.sample(range(0, 90), 3)):
    add_record("internal", d, "security_review", gen_internal_security_review(pick(ENG_LEADS), pick(ENGINEERS)),
                "Platform Team", [pick(ENG_LEADS)], 15)

for d in sorted(random.sample(range(30, 75), 5)):
    add_record("internal", d, "churn_risk_review", gen_internal_churn_risk_review(pick(PMS), pick(AM_NAMES), pick(ENG_LEADS)),
                "Cross-functional", [pick(PMS), pick(AM_NAMES)], 18)

random.shuffle(records)
records.sort(key=lambda r: r["date"])
for i, r in enumerate(records, start=1):
    r["call_id"] = f"CALL-{i:04d}"

with open(OUT_PATH, "w") as f:
    for r in records:
        f.write(json.dumps(r) + "\n")

import csv
with open(INDEX_PATH, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["call_id", "call_type", "date", "duration_minutes", "account_name", "word_count"])
    for r in records:
        writer.writerow([r["call_id"], r["call_type"], r["date"], r["duration_minutes"], r["account_name"], r["word_count"]])

print(f"Generated {len(records)} transcripts.")
from collections import Counter
print(Counter(r["call_type"] for r in records))
