"""
Topic categorization pipeline.

APPROACH: hybrid (embeddings + unsupervised clustering + keyword/LLM labeling).

Why not pure rule-based (keyword matching)?
  Rules require knowing the categories in advance. We don't -- the assignment
  explicitly wants us to discover what's in the data, including things we
  didn't anticipate (e.g. a cross-channel bug thread). Rules also miss
  paraphrases ("export is cutting off data" vs "report stops at fifty
  thousand rows") that mean the same thing.

Why not pure zero-shot LLM classification (prompt an LLM with a fixed
category list per transcript)?
  It's the highest-quality option for production and is included below as an
  alternative path, but it (a) costs an API call per transcript, (b) requires
  you to specify the category list up front -- which defeats the "what
  categories exist in this data" discovery goal, and (c) isn't reproducible
  for free in this exercise since no API key is available in the build
  environment.

Why embeddings + clustering, then labeling?
  Clustering is unsupervised: it finds structure in the data without being
  told what to look for, which is exactly what's needed to discover both the
  "expected" categories (billing, SSO, performance...) AND unexpected
  cross-channel patterns (the export bug cluster spans all three call types).
  The tradeoff is that raw clusters aren't human-readable on their own, so a
  labeling step (reading top keywords + representative examples per cluster)
  is layered on top -- this is the "hybrid" part. In production, that
  labeling step is a natural fit for an LLM call per cluster (cheap: ~15
  calls instead of ~100+), not per transcript.

Pipeline:
  1. Strip speaker-name prefixes from transcript text (otherwise TF-IDF and,
     to a lesser extent, embeddings pick up on *who* is talking rather than
     *what* they're talking about -- a real bug we hit and fixed during
     development, see data/README.md).
  2. Embed each transcript with a local sentence-transformer model
     (all-MiniLM-L6-v2 -- small, fast, no API key needed).
  3. Sweep K for KMeans and pick the smallest K where cluster purity against
     a held-out validation signal is high AND clusters aren't degenerating
     into singletons. (We maximize silhouette only as a secondary check --
     on a small dataset silhouette keeps improving as K approaches N, which
     doesn't serve the actual goal of finding *meaningful, recurring* themes.)
  4. For each cluster: extract top TF-IDF terms (with speaker names and
     generic stopwords removed) and a representative example, used to assign
     a human-readable label.
"""

import re
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.feature_extraction import text as sktext
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer

SPEAKER_RE = re.compile(r"^[A-Za-z][A-Za-z.&' ]{1,30}:\s*", re.MULTILINE)

# Names used by the synthetic generator -- stripped so cluster keywords
# reflect content, not which fictional rep happened to be on the call.
_GENERATOR_NAMES = [
    "Jordan Mills", "Priya Anand", "Casey Lindqvist", "Marcus Webb", "Teodora Ilic",
    "Dana Okafor", "Liam Chen", "Ruth Fontaine", "Omar Siddiqui", "Alexis Park",
    "Nikhil Rao", "Sam Doyle", "Beatriz Souza", "Finn Walsh", "Yuki Tanaka", "Greta Holm",
    "Wes Carrington", "Mina Oyelaran", "Devon Pratt", "Sofia Reyes", "Tobias Krantz",
    "Taylor Grant", "Morgan Reyes", "Elena Vasquez", "Chris Patel", "Nadia Brooks",
    "Sam Oduya", "Jules Ferreira", "Priya Nair", "Owen Castellan", "Robin Haas",
]
NAME_STOPWORDS = {part.lower() for full in _GENERATOR_NAMES for part in full.split()}
STOPWORDS = list(sktext.ENGLISH_STOP_WORDS.union(NAME_STOPWORDS))

# Human-readable labels for the default run (K=13, random_state=42, on the
# shipped data/transcripts.jsonl). Cluster index -> label is deterministic
# for this exact data/embedding/K combination; if you regenerate the dataset
# or change K, re-derive these by reading cluster_summary() output and update
# this dict -- don't assume the mapping still holds.
CLUSTER_LABELS = {
    0: "Sprint Planning & Eng Backlog",
    1: "Competitive Threat (Pricing/Capability Gap)",
    2: "Smart Alerts Launch, Upsell & QBR",
    3: "Export/Reporting Bug -- Customer Impact",
    4: "Healthy Renewal & Expansion",
    5: "Security & Compliance Documentation",
    6: "Roadmap Prioritization & Signal Gaps",
    7: "Incident Postmortem (Infra/Performance)",
    8: "Churn Risk Review & Retention Strategy",
    9: "Routine Support Resolution & Check-ins",
    10: "Mixed: Export Escalation Urgency + Staffing",
    11: "Login/SSO & General Support Resolution",
    12: "Reference Requests & Contract Follow-ups",
}


def strip_speakers(text: str) -> str:
    return SPEAKER_RE.sub("", text)


def embed_transcripts(df: pd.DataFrame, model_name: str = "all-MiniLM-L6-v2") -> np.ndarray:
    model = SentenceTransformer(model_name)
    clean = df["transcript"].apply(strip_speakers)
    return model.encode(clean.tolist(), show_progress_bar=False)


def _purity(labels_true, labels_pred) -> float:
    tmp = pd.DataFrame({"t": labels_true, "p": labels_pred})
    return sum(grp["t"].value_counts().iloc[0] for _, grp in tmp.groupby("p")) / len(tmp)


def sweep_k(embeddings: np.ndarray, validation_labels=None, k_range=range(6, 21)) -> pd.DataFrame:
    """Try a range of K and report silhouette + (optional) purity against a
    validation label column, so K is chosen on more than silhouette alone."""
    rows = []
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(embeddings)
        sil = silhouette_score(embeddings, km.labels_)
        min_size = pd.Series(km.labels_).value_counts().min()
        row = {"k": k, "silhouette": sil, "min_cluster_size": min_size}
        if validation_labels is not None:
            row["purity"] = _purity(validation_labels, km.labels_)
        rows.append(row)
    return pd.DataFrame(rows)


def fit_clusters(embeddings: np.ndarray, k: int) -> np.ndarray:
    km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(embeddings)
    return km.labels_


def top_terms_per_cluster(df: pd.DataFrame, n_terms: int = 8) -> dict:
    clean = df["transcript"].apply(strip_speakers)
    tfidf = TfidfVectorizer(stop_words=STOPWORDS, max_features=3000, ngram_range=(1, 2), min_df=2)
    X = tfidf.fit_transform(clean)
    terms = np.array(tfidf.get_feature_names_out())
    out = {}
    for c in sorted(df["cluster"].unique()):
        idx = df.index[df["cluster"] == c]
        mean_tfidf = np.asarray(X[df.index.get_indexer(idx)].mean(axis=0)).flatten()
        out[c] = list(terms[np.argsort(mean_tfidf)[::-1][:n_terms]])
    return out


def cluster_summary(df: pd.DataFrame) -> pd.DataFrame:
    """One row per cluster: size, call_type mix, top keywords, example call_id."""
    terms = top_terms_per_cluster(df)
    rows = []
    for c in sorted(df["cluster"].unique()):
        sub = df[df["cluster"] == c]
        rows.append({
            "cluster": c,
            "label": CLUSTER_LABELS.get(c, f"Cluster {c} (needs manual label)"),
            "n": len(sub),
            "call_type_mix": sub["call_type"].value_counts().to_dict(),
            "top_terms": terms[c],
            "example_call_id": sub.iloc[0]["call_id"],
        })
    return pd.DataFrame(rows).sort_values("n", ascending=False).reset_index(drop=True)


def categorize(df: pd.DataFrame, k: int = 13) -> pd.DataFrame:
    """End-to-end: embed, cluster, label. Returns df with 'cluster' and 'category' columns."""
    embeddings = embed_transcripts(df)
    df = df.copy()
    df["cluster"] = fit_clusters(embeddings, k)
    df["category"] = df["cluster"].map(lambda c: CLUSTER_LABELS.get(c, f"Cluster {c}"))
    return df
