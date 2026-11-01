# Transcript Intelligence

Take-home submission: a pipeline that categorizes B2B SaaS call transcripts by topic,
scores sentiment and surfaces trends across call types, and documents additional insights
beyond the two required tasks.

**Start here depending on what you want:**
- Reviewing the findings → [slides/transcript_intelligence.pptx](slides/transcript_intelligence.pptx)
- Reviewing the technical approach → [notebooks/01_transcript_intelligence_analysis.ipynb](notebooks/01_transcript_intelligence_analysis.ipynb)
- Watching the demo → see [video/demo_script.md](video/demo_script.md) for what the recording covers (the recorded file itself isn't in this repo)

## A note on the data, up front

The assignment's real sample dataset wasn't provided for this exercise. Per the
assignment's own FAQ ("Can I generate additional data? Yes..."), everything here runs on a
**100% synthetic** dataset of 103 B2B SaaS call transcripts, generated to match the
assignment's three call types (support / external / internal). Full transparency on what's
synthetic and why is in [data/README.md](data/README.md) — read that before anything else
if you're evaluating this submission. Short version: three deliberate, unlabeled storylines
(a cross-channel bug, a competitor threat, a feature launch) are woven through the data so
the pipeline has real signal to find, and every technique shown is built to run unchanged on
real transcripts.

## Repository structure

```
transcript-intel/
├── data/
│   ├── transcripts.jsonl          # 103 synthetic call transcripts (the dataset)
│   ├── transcripts_index.csv      # flat index (no transcript text) for quick scanning
│   └── README.md                  # full transparency notes on the synthetic data
├── scripts/
│   ├── generate_transcripts.py    # generates data/transcripts.jsonl (seeded, reproducible)
│   ├── categorize.py              # topic categorization pipeline (embeddings + clustering)
│   └── sentiment.py               # sentiment scoring pipeline (VADER + LLM-contextual hybrid)
├── notebooks/
│   ├── 01_transcript_intelligence_analysis.ipynb   # main deliverable: narrated analysis
│   └── 01_transcript_intelligence_analysis.py      # same notebook as a jupytext percent-script
│                                                     # (easier to diff/review in a plain editor)
├── outputs/
│   ├── figures/                   # charts exported from the notebook (used in the slides)
│   └── data/                      # scored_transcripts.csv, category_priority.csv
├── slides/
│   ├── transcript_intelligence.pptx   # the slide deck deliverable
│   ├── build_deck.js              # generates the .pptx (pptxgenjs)
│   └── icons.js                   # icon-rendering helper used by build_deck.js
├── video/
│   └── demo_script.md             # beat-by-beat script/shot-list for the recorded demo
└── requirements.txt                # Python dependencies
```

## Setup

### Python (dataset generation + notebook)

```bash
python3 -m venv venv && source venv/bin/activate   # optional but recommended
pip install -r requirements.txt
```

### Node (slide deck generation only — skip if you just want to view the .pptx)

```bash
cd slides
npm install
```

## Running things

### Regenerate the synthetic dataset

```bash
cd scripts
python3 generate_transcripts.py
```

Seeded (`random.seed(42)`) — reruns produce the identical dataset. Writes
`data/transcripts.jsonl` and `data/transcripts_index.csv`.

### Run the analysis notebook

```bash
cd notebooks
jupyter notebook 01_transcript_intelligence_analysis.ipynb
# or, to re-execute top-to-bottom from the command line:
jupyter nbconvert --to notebook --execute --inplace 01_transcript_intelligence_analysis.ipynb
```

Takes a few minutes the first run (downloads two small models — a sentence-transformer for
embeddings and DistilBERT for the sentiment cross-check — both cached locally after that).
Running it regenerates everything under `outputs/figures/` and `outputs/data/`.

The `.py` file alongside the notebook is the same content in
[jupytext](https://jupytext.readthedocs.io/) "percent" format — useful for reviewing the
notebook's logic in a plain text editor or diffing changes. Regenerate the `.ipynb` from it
with `jupytext --to notebook 01_transcript_intelligence_analysis.py`.

### Rebuild the slide deck

```bash
cd slides
node build_deck.js
```

Outputs `transcript_intelligence.pptx` in the same directory. The script also renders a
standalone sentiment-trend chart (`slides/assets/sentiment_trend_notitle.png`) by re-running
the sentiment pipeline directly — if you regenerate the dataset, rerun the notebook first so
`outputs/` is current, then rebuild the deck.

## What's in each deliverable

1. **Slide deck** (`slides/transcript_intelligence.pptx`) — 18 slides, structured for a
   30-minute presentation to product/engineering leadership. Leads with the headline finding
   (a cross-channel bug that took 25 days to escalate), then walks through the categorization
   approach, the sentiment-analysis methodology (including why two off-the-shelf tools failed
   before landing on the approach actually used), and three additional insights beyond the
   required tasks.
2. **Notebook** (`notebooks/01_transcript_intelligence_analysis.ipynb`) — the technical
   reference. Every claim made in the slides is backed by executed code here, including the
   VADER-vs-DistilBERT disagreement comparison and the K-selection methodology for
   clustering. Markdown cells explain the reasoning behind each decision, not just the code.
3. **Video demo** — not included as a file in this repo (recording is done outside this
   environment); `video/demo_script.md` has the full script and shot list that the recording
   follows.

## Known limitations / things to know before digging in

- **No LLM API key is wired up.** Both the categorization labeling step and the sentiment
  scoring step describe exactly how they'd run as real LLM API calls (OpenAI/Anthropic) in
  production, but execute via a documented stand-in in this sandbox — see the module
  docstrings in `scripts/categorize.py` and `scripts/sentiment.py` for the specifics and why.
- **Synthetic accounts aren't persistent across calls** — each call gets a randomly assigned
  fictional company name, rather than a fixed roster of recurring accounts. This is why two
  of the bonus insights (account health rollup, auto-generated pre-call briefings) are
  described with reasoning rather than implemented — see §4.4/4.5 in the notebook.
- **Node dependencies for the slide deck** install to whichever `package.json` npm resolves
  to first walking up the directory tree; `slides/package.json` now pins this locally so
  `npm install` from `slides/` stays self-contained on a fresh clone.
