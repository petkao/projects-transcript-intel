# Video Demo Script — Transcript Intelligence

Target runtime: **7-8 minutes** (assignment allows 5-10). Simple screen recording with
narration — no editing required. Suggested tool on macOS: QuickTime Player → File → New
Screen Recording (or Cmd+Shift+5), full screen or a single window.

## Before you hit record

Open these in order, in separate tabs/windows, so you can switch without fumbling:

1. **Finder/terminal** at `~/projects/transcript-intel` — for the directory tour
2. **`notebooks/01_transcript_intelligence_analysis.ipynb`** open in Jupyter/VS Code, already
   executed top to bottom (outputs visible, don't re-run live — too slow for a demo)
3. **`slides/transcript_intelligence.pptx`** open in PowerPoint/Keynote, on slide 1
4. Terminal ready with `cat data/README.md` pre-typed but not yet run (for the data-honesty beat)

Keep narration conversational — read the SAY lines as a guide, not a script to recite
word-for-word. Pause briefly between sections so it can be trimmed later if needed.

---

## 0:00–0:30 — Cold open

**SHOW:** Your face/voice only, or the repo root in Finder. No slides yet.

**SAY:**
> "Hi, I'm Peter. This is my walkthrough for the Transcript Intelligence take-home. Quick
> heads up before I dive in: the real sample dataset wasn't provided for this exercise, so
> everything you're about to see runs on a synthetic dataset I generated — fully disclosed,
> and explicitly allowed by the assignment's own FAQ. I'll show you exactly how and why in a
> second. Let's get into it."

---

## 0:30–1:30 — The data, honestly

**SHOW:** Terminal — `ls` the repo root, then `cat data/README.md` (or scroll it open in an
editor). Point at the "three deliberate storylines" section.

**SAY:**
> "103 synthetic B2B SaaS call transcripts, split across the three call types the assignment
> describes — support, external account-manager calls, and internal cross-team calls. I
> didn't just generate random noise, though — I wove three deliberate storylines through the
> data with no explicit labels: a recurring export bug that escalates across channels, a
> competitor threat, and a feature launch. That gives the pipeline real signal to find,
> instead of me just eyeballing clusters on static data.
>
> Generation script is here —" *(point at `scripts/generate_transcripts.py`)* "— seeded for
> reproducibility. Everything downstream — categorization, sentiment, the insights — is built
> to run unchanged on real transcripts. Swap the data source, the pipeline doesn't change."

---

## 1:30–3:00 — Topic categorization

**SHOW:** Notebook, section **"2. Topic Categorization"**. Scroll through 2.1 (K-selection
chart), then the cluster summary table, then 2.4 (cross-channel finding).

**SAY:**
> "For categorization I went hybrid — local sentence embeddings, then clustering, then a
> lightweight labeling pass. I explain the reasoning in the notebook, but the short version:
> pure rules need you to know the categories up front, which defeats the discovery goal; pure
> per-transcript LLM classification is the strongest production option but costs an API call
> per call and I don't have a key wired up in this sandbox. Clustering finds structure with no
> prior assumptions, and I label clusters after the fact.
>
> One thing I want to call out because it matters: picking K. If you just maximize silhouette
> score on a small dataset like this, it keeps climbing as clusters shrink toward singletons —
> that's not useful. So I picked the smallest K where cluster purity against known answers was
> high and nothing degenerated to a tiny cluster. Landed on 13 categories, 76% purity.
>
> Here's the headline finding —" *(scroll to the cross-channel bar chart, 2.4)* "— one category,
> the export-slash-reporting bug, is both the single largest cluster in the whole dataset, and
> the only one that shows up meaningfully in all three call types — support, external, and
> internal. Every other category lives almost entirely in one channel. That cross-channel
> footprint turned out to be the throughline for the rest of this deck."

---

## 3:00–5:00 — Sentiment analysis: the journey, not just the score

**SHOW:** Notebook, section **"3. Sentiment Analysis"**. Show the VADER distribution output
(96/103 positive), then the trend chart in 3.1, then the export-bug arc table in 3.2.

**SAY:**
> "Sentiment took three tries, and I think the journey is more useful than the final number,
> so I kept all three in the notebook.
>
> First try: VADER, a standard lexicon-based tool. It fails badly here — B2B customers stay
> polite even when they're frustrated. 'I appreciate that, but this is the third time I've
> called about this' — VADER sees 'appreciate' and scores it positive. 96 of 103 calls came
> back positive, including calls where a customer is actively threatening to churn. Not
> usable on its own.
>
> Second try: a transformer model, DistilBERT, as a cross-check. It disagreed with VADER on
> about half a sample of calls — which told me generic sentiment models trained on movie
> reviews and tweets just don't transfer to professional, consequence-heavy B2B dialogue.
>
> Third try, what I actually shipped: LLM-based contextual scoring. The reasoning and the
> exact production prompt are in `scripts/sentiment.py` if you want to see it. And here's
> what that gets you —" *(point at the trend chart)* "— support sentiment tracks the export
> bug cleanly: sharp dip while it's open, recovery right as the fix ships. I also flagged a
> second, unrelated dip later in the chart honestly rather than cropping it out — it's just
> noise from unrelated complaints landing the same week, not a relapse. A dashboard that only
> ever shows clean stories isn't trustworthy."

---

## 5:00–6:15 — The throughline: one bug, three channels, 43 days

**SHOW:** Slide deck — jump to **slide 12** ("The full arc"). This is the strongest single
visual in the deck; give it room.

**SAY:**
> "This is the finding I'd lead with if I only had one slide. Reading across channels instead
> of within just one: the bug is first reported by a customer on July 4th. Engineering
> acknowledges it five days later, but it sits in the backlog. It doesn't get pulled forward
> until a customer explicitly ties it to renewal risk — 25 days after that first complaint, by
> which point three separate support calls had already mentioned it. The fix ships on day 37.
> Customer-confirmed resolution on day 43, and support sentiment swings from minus-0.85 to
> plus-0.75 in that same window.
>
> The recommendation that falls out of this is simple: surface 'this topic has appeared in N
> calls across channels in the last 30 days' directly on the engineering backlog. Don't rely
> on someone noticing the pattern from memory — which is exactly what happened here."

---

## 6:15–7:15 — Beyond the required tasks

**SHOW:** Slide deck — slides 14 and 15 (priority ranking, sentiment≠churn-risk). Move
quickly; these are two of the five bonus insights, the two with the clearest visuals.

**SAY:**
> "Beyond the two required tasks, I packaged five additional insights — three implemented,
> two described with reasoning but not built, which the assignment says is fine if time-boxed.
>
> First implemented one: volume times negativity, ranked. The export bug isn't just the
> biggest category, it's also the clear number-one priority by this independent method — which
> is a good sanity check before taking a qualitative finding to leadership.
>
> Second: sentiment score is not the same thing as churn risk. A customer calmly saying
> they're evaluating a competitor scores only mildly negative — milder than an angry call about
> a bug that's already fixed. A sentiment-only alert would under-rank the more dangerous
> signal. And naive keyword-flagging over-fires in the other direction — six of fifteen
> keyword-flagged calls turned out to be internal teams calmly discussing strategy, not real
> customer risk. Both signals need their own contextual judgment, scored separately.
>
> The two I described but didn't build — an account-level health rollup, and auto-generated
> pre-call briefings — both depend on the same thing: persistent per-account identity across
> calls, which today's synthetic data doesn't have. I flagged that as a data-generation change
> worth sign-off rather than quietly working around it."

---

## 7:15–8:00 — Wrap

**SHOW:** Slide deck, back to slide 17 (recommendations) or slide 1 (title).

**SAY:**
> "So, to wrap up: categorization and sentiment both needed a hybrid approach rather than
> anything off-the-shelf, and the real value wasn't in either task alone — it was in reading
> across channels, which surfaced a 25-day escalation gap that nobody would have seen looking
> at support, sales, or engineering data in isolation.
>
> Everything you saw is in the repo — the generation script, the categorization and sentiment
> modules, this notebook, and the slide deck. Happy to go deeper into any part of it. Thanks
> for watching."

---

## Quick reference: shot list

| Time | Screen | Key beat |
|---|---|---|
| 0:00 | Talking head / repo root | Data transparency heads-up |
| 0:30 | `data/README.md` + `generate_transcripts.py` | Why synthetic, what's real |
| 1:30 | Notebook §2 (categorization) | Hybrid approach, K-selection reasoning |
| 2:30 | Notebook §2.4 | Cross-channel cluster finding |
| 3:00 | Notebook §3 (sentiment) | VADER fails → DistilBERT disagrees → LLM approach |
| 4:30 | Notebook §3.1/3.2 trend chart | Bug arc visible in the data |
| 5:00 | Slide 12 | The 43-day throughline — strongest visual, give it room |
| 6:15 | Slides 14–15 | Priority ranking + sentiment≠churn-risk |
| 7:15 | Slide 17 or 1 | Close |

## Recording tips

- Record in one take if you can — a few "let me restate that" moments read as natural, not
  sloppy, in a technical walkthrough.
- If you stumble badly, pause 2 seconds, restate the sentence — easy to cut in post if you
  end up trimming, but you probably won't need to.
- Keep notebook font size large enough to read on a recording (Cmd+Plus in Jupyter/browser
  before recording).
- No need to show cells *executing* live — it's a batch pipeline, not interactive; show the
  already-computed outputs and talk through them. Mention in passing that it's one script
  (`python3 generate_transcripts.py`) to regenerate data and the notebook re-runs top to
  bottom cleanly if they want to verify.
