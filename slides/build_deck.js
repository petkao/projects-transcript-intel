const pptxgen = require("pptxgenjs");
const path = require("path");
const { renderIcon } = require("./icons.js");
const {
  FiLayers, FiSmile, FiAlertTriangle, FiClock, FiTrendingUp, FiUsers,
  FiMessageSquare, FiCheckCircle, FiSearch, FiTarget, FiShield, FiDatabase,
} = require("react-icons/fi");
const { applyTheme } = require(
  "/Users/tzechungkao/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/3cef40f8-d3e7-483b-a1af-4b3547eef06f/53ee5c3d-f691-4da5-ab7a-6745d33a5527/skills/pptx/scripts/apply_theme.js"
);

const THEME = {
  name: "Transcript Intelligence",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1B1F3B",   // ink navy - primary text / dark backgrounds
    lt1: "FFFFFF",   // white
    dk2: "0F3057",   // deep blue - alt dark
    lt2: "EAF4F4",   // pale teal tint - card backgrounds on light slides
    accent1: "0F8B8D", // primary teal - brand / positive
    accent2: "D7263D", // coral red - risk / negative
    accent3: "F4A261", // amber - highlight stat
    accent4: "1C7293", // secondary blue-teal
    accent5: "2A9D8F", // mint teal
    accent6: "6B7A99", // muted slate blue
    hlink: "0F8B8D",
    folHlink: "1C7293",
  },
};

const FIG = "/Users/tzechungkao/projects/transcript-intel/outputs/figures";
const ICON_DIR = path.join(__dirname, "assets", "icons");

async function main() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.3 x 7.5
  pres.company = "Transcript Intelligence";

  const C = pres.SchemeColor;

  // ---- Pre-render icons ----
  const icons = {};
  const iconSpecs = [
    ["layers", FiLayers, THEME.colors.accent1],
    ["smile", FiSmile, THEME.colors.accent1],
    ["alert", FiAlertTriangle, THEME.colors.accent2],
    ["clock", FiClock, THEME.colors.accent3],
    ["trend", FiTrendingUp, THEME.colors.accent1],
    ["users", FiUsers, THEME.colors.accent4],
    ["message", FiMessageSquare, THEME.colors.accent4],
    ["check", FiCheckCircle, THEME.colors.accent1],
    ["search", FiSearch, THEME.colors.accent1],
    ["target", FiTarget, THEME.colors.accent2],
    ["shield", FiShield, THEME.colors.accent5],
    ["database", FiDatabase, THEME.colors.accent6],
    ["alert_white", FiAlertTriangle, "FFFFFF"],
    ["clock_white", FiClock, "FFFFFF"],
    ["trend_white", FiTrendingUp, "FFFFFF"],
    ["layers_white", FiLayers, "FFFFFF"],
    ["smile_white", FiSmile, "FFFFFF"],
    ["check_white", FiCheckCircle, "FFFFFF"],
  ];
  for (const [key, Icon, color] of iconSpecs) {
    icons[key] = await renderIcon(Icon, color, 256);
  }

  // =========================================================================
  // LAYOUTS
  // =========================================================================

  // --- Title layout (dark) ---
  pres.defineSlideMaster({
    title: "TITLE",
    background: { color: THEME.colors.dk1 },
    objects: [
      { placeholder: {
          options: { name: "title", type: "title", x: 0.9, y: 2.55, w: 11.5, h: 1.6,
            fontFace: THEME.headFontFace, fontSize: 44, bold: true, color: C.background1, align: "left" },
          text: "" } },
      { placeholder: {
          options: { name: "subtitle", type: "body", x: 0.9, y: 4.05, w: 11, h: 0.8,
            fontFace: THEME.bodyFontFace, fontSize: 18, color: C.background1, align: "left" },
          text: "" } },
    ],
  });

  // --- Section divider (dark) ---
  pres.defineSlideMaster({
    title: "SECTION",
    background: { color: THEME.colors.dk2 },
    objects: [
      { placeholder: {
          options: { name: "title", type: "title", x: 0.9, y: 3.15, w: 10.5, h: 1.4,
            fontFace: THEME.headFontFace, fontSize: 38, bold: true, color: C.background1, align: "left" },
          text: "" } },
    ],
  });

  // --- Content: title only, freeform body beneath ---
  pres.defineSlideMaster({
    title: "CONTENT",
    background: { color: THEME.colors.background1 },
    objects: [
      { placeholder: {
          options: { name: "title", type: "title", x: 0.6, y: 0.4, w: 12.1, h: 0.9,
            fontFace: THEME.headFontFace, fontSize: 30, bold: true, color: C.text1, align: "left" },
          text: "" } },
      { placeholder: { options: { name: "footer", type: "body", x: 0.6, y: 7.15, w: 8, h: 0.3,
          fontFace: THEME.bodyFontFace, fontSize: 9, color: C.text2, align: "left" },
          text: "" } },
      { text: { text: "Transcript Intelligence", options: { name: "footer-brand", x: 10.9, y: 7.15, w: 1.8, h: 0.3,
          fontFace: THEME.bodyFontFace, fontSize: 9, color: C.text2, align: "right" } } },
    ],
    slideNumber: { x: 12.9, y: 7.15, fontFace: THEME.bodyFontFace, fontSize: 9, color: C.text2 },
  });

  // --- Closing (dark) ---
  pres.defineSlideMaster({
    title: "CLOSING",
    background: { color: THEME.colors.dk1 },
    objects: [
      { placeholder: {
          options: { name: "title", type: "title", x: 0.9, y: 3.0, w: 11, h: 1.3,
            fontFace: THEME.headFontFace, fontSize: 40, bold: true, color: C.background1, align: "left" },
          text: "" } },
      { placeholder: {
          options: { name: "subtitle", type: "body", x: 0.9, y: 4.15, w: 11, h: 0.8,
            fontFace: THEME.bodyFontFace, fontSize: 16, color: C.background1, align: "left" },
          text: "" } },
    ],
  });

  // =========================================================================
  // HELPERS
  // =========================================================================

  function statCallout(slide, { x, y, w, number, label, color = THEME.colors.accent1, numSize = 44, labelSize = 12 }) {
    slide.addText(number, { x, y, w, h: 0.75, isTextBox: true, margin: 0,
      fontFace: THEME.headFontFace, fontSize: numSize, bold: true, color, align: "left" });
    slide.addText(label, { x, y: y + 0.72, w, h: 0.55, isTextBox: true, margin: 0,
      fontFace: THEME.bodyFontFace, fontSize: labelSize, color: C.text2, align: "left" });
  }

  function iconCircle(slide, { x, y, d = 0.62, icon, bg = THEME.colors.accent1 }) {
    slide.addShape("ellipse", { x, y, w: d, h: d, fill: { color: bg }, line: { type: "none" } });
    const pad = d * 0.22;
    slide.addImage({ data: icon, x: x + pad, y: y + pad, w: d - 2 * pad, h: d - 2 * pad });
  }

  function card(slide, { x, y, w, h, fill = THEME.colors.lt2 }) {
    slide.addShape("roundRect", { x, y, w, h, rectRadius: 0.08,
      fill: { color: fill }, line: { type: "none" },
      shadow: { type: "outer", color: "1B1F3B", opacity: 0.12, blur: 6, offset: 2, angle: 90 } });
  }

  // =========================================================================
  // SLIDE 1 — TITLE
  // =========================================================================
  let s = pres.addSlide({ masterName: "TITLE" });
  s.addText("Transcript Intelligence", { placeholder: "title" });
  s.addText([
    { text: "Findings & Recommendations", options: { breakLine: true } },
    { text: "Peter Kao  |  Product & Engineering Leadership Review", options: {} },
  ], { placeholder: "subtitle" });
  s.addShape("line", { x: 0.9, y: 2.3, w: 2.2, h: 0, line: { color: THEME.colors.accent1, width: 3 } });
  iconCircle(s, { x: 11.0, y: 0.7, d: 0.9, icon: icons.layers_white, bg: THEME.colors.accent1 });

  // =========================================================================
  // SLIDE 2 — EXECUTIVE SUMMARY
  // =========================================================================
  s = pres.addSlide({ masterName: "CONTENT" });
  s.addText("The headline finding", { placeholder: "title" });
  s.addText(
    "A single bug sat unescalated for 25 days — and it was visible from every seat in the company the whole time.",
    { x: 0.6, y: 1.3, w: 12.1, h: 0.75, isTextBox: true, margin: 0,
      fontFace: THEME.bodyFontFace, fontSize: 17, color: C.text1, italic: true }
  );
  const statsRow = [
    ["19 / 103", "calls touched one topic — the export bug — more than any other", THEME.colors.accent2],
    ["3 of 3", "call types it showed up in: support, AM renewal calls, and engineering syncs", THEME.colors.accent4],
    ["25 days", "from first customer complaint to internal escalation", THEME.colors.accent3],
    ["37 days", "from first complaint to shipped fix", THEME.colors.accent1],
  ];
  statsRow.forEach(([num, label, color], i) => {
    const x = 0.6 + i * 3.08;
    card(s, { x, y: 2.35, w: 2.85, h: 2.0 });
    statCallout(s, { x: x + 0.25, y: 2.6, w: 2.4, number: num, label, color, numSize: 32, labelSize: 11.5 });
  });
  s.addText(
    "The rest of this deck walks through how we found that (categorization + sentiment, the two required tasks), " +
    "then three more insights the same data surfaces once you look across channels instead of within just one.",
    { x: 0.6, y: 4.65, w: 12.1, h: 0.9, isTextBox: true, margin: 0,
      fontFace: THEME.bodyFontFace, fontSize: 14, color: C.text2 }
  );
  s.addText("Executive summary", { placeholder: "footer" });

  // =========================================================================
  // SLIDE 3 — DATA NOTE
  // =========================================================================
  s = pres.addSlide({ masterName: "CONTENT" });
  s.addText("A quick, honest note on the data", { placeholder: "title" });
  iconCircle(s, { x: 0.6, y: 1.5, d: 0.6, icon: icons.database, bg: THEME.colors.lt2 });
  s.addText(
    "The assignment's sample dataset of real transcripts wasn't provided for this exercise.",
    { x: 1.45, y: 1.48, w: 10.5, h: 0.65, isTextBox: true, margin: 0,
      fontFace: THEME.bodyFontFace, fontSize: 16, bold: true, color: C.text1 }
  );
  const dataPoints = [
    ["100% synthetic, fully disclosed", "103 fictional B2B SaaS transcripts generated to match the assignment's three call types — explicitly allowed by the assignment's own FAQ."],
    ["Built with real signal, not noise", "Three deliberate storylines (a cross-channel bug, a competitor threat, a feature launch) are woven through the data with no labels, so categorization and sentiment have something genuine to find."],
    ["The method is what's being evaluated", "Every technique shown — clustering, sentiment scoring, the insights — is built to run unchanged on real transcripts. Swap the data source; the pipeline doesn't change."],
  ];
  dataPoints.forEach(([h, body], i) => {
    const y = 2.75 + i * 1.5;
    card(s, { x: 0.6, y, w: 12.1, h: 1.3 });
    s.addShape("ellipse", { x: 0.9, y: y + 0.35, w: 0.6, h: 0.6, fill: { color: THEME.colors.accent1 }, line: { type: "none" } });
    s.addText(String(i + 1), { x: 0.9, y: y + 0.35, w: 0.6, h: 0.6, isTextBox: true, margin: 0, align: "center", valign: "middle",
      fontFace: THEME.headFontFace, fontSize: 20, bold: true, color: "FFFFFF" });
    s.addText(h, { x: 1.75, y: y + 0.22, w: 10.7, h: 0.4, isTextBox: true, margin: 0,
      fontFace: THEME.headFontFace, fontSize: 15, bold: true, color: THEME.colors.dk2 });
    s.addText(body, { x: 1.75, y: y + 0.6, w: 10.7, h: 0.6, isTextBox: true, margin: 0,
      fontFace: THEME.bodyFontFace, fontSize: 12.5, color: C.text2 });
  });
  s.addText("Full transparency notes: data/README.md in the repo", { placeholder: "footer" });

  // =========================================================================
  // SLIDE 4 — AGENDA
  // =========================================================================
  s = pres.addSlide({ masterName: "CONTENT" });
  s.addText("What we'll cover", { placeholder: "title" });
  const agendaItems = [
    ["01", "Topic categorization", "How we grouped 103 calls into 13 data-driven themes — and the one that crosses every channel"],
    ["02", "Sentiment analysis & trends", "Why off-the-shelf sentiment tools fail on polite B2B dialogue, and what actually works"],
    ["03", "Three more insights", "What else this data can tell different stakeholders, beyond the required tasks"],
    ["04", "Recommendations", "What we'd act on first"],
  ];
  agendaItems.forEach(([num, h, body], i) => {
    const y = 1.55 + i * 1.3;
    s.addText(num, { x: 0.6, y, w: 1.1, h: 1.0, isTextBox: true, margin: 0,
      fontFace: THEME.headFontFace, fontSize: 34, bold: true, color: THEME.colors.accent6, align: "left" });
    s.addText(h, { x: 1.75, y: y + 0.03, w: 5.3, h: 0.45, isTextBox: true, margin: 0,
      fontFace: THEME.headFontFace, fontSize: 18, bold: true, color: C.text1 });
    s.addText(body, { x: 1.75, y: y + 0.46, w: 10.6, h: 0.6, isTextBox: true, margin: 0,
      fontFace: THEME.bodyFontFace, fontSize: 12.5, color: C.text2 });
    if (i < agendaItems.length - 1) {
      s.addShape("line", { x: 0.6, y: y + 1.12, w: 11.9, h: 0, line: { color: "E3E7E7", width: 1 } });
    }
  });

  // =========================================================================
  // SLIDE 5 — SECTION: CATEGORIZATION
  // =========================================================================
  s = pres.addSlide({ masterName: "SECTION" });
  s.addText("01", { x: 0.9, y: 2.75, w: 2, h: 0.5, isTextBox: true, margin: 0,
    fontFace: THEME.bodyFontFace, fontSize: 16, color: THEME.colors.accent1, bold: true });
  s.addText("Topic Categorization", { placeholder: "title" });
  s.addText("Hybrid embeddings + clustering, validated against known answers", { x: 0.9, y: 4.0, w: 9, h: 0.5,
    isTextBox: true, margin: 0, fontFace: THEME.bodyFontFace, fontSize: 15, color: "C7D3E8" });
  iconCircle(s, { x: 11.1, y: 2.8, d: 1.0, icon: icons.layers_white, bg: THEME.colors.accent1 });

  // =========================================================================
  // SLIDE 6 — CATEGORIZATION APPROACH
  // =========================================================================
  s = pres.addSlide({ masterName: "CONTENT" });
  s.addText("Why hybrid, not pure rules or pure LLM-per-call", { placeholder: "title" });
  const approachCols = [
    ["Rule-based", "Requires knowing categories up front — but discovering the unexpected (a bug visible in 3 channels) is the point.", icons.search, THEME.colors.accent6],
    ["Zero-shot LLM / call", "Highest quality, but one API call per transcript, and still needs a pre-set category list. Not reproducible here without an API key.", icons.alert, THEME.colors.accent3],
    ["Hybrid (chosen)", "Embeddings + clustering find structure with no prior assumptions; a lightweight labeling pass (keywords + example) makes clusters readable — an LLM call per cluster, not per call.", icons.check, THEME.colors.accent1],
  ];
  approachCols.forEach(([h, body, icon, color], i) => {
    const x = 0.6 + i * 4.08;
    card(s, { x, y: 1.45, w: 3.85, h: 2.5, fill: i === 2 ? "DCF0EF" : THEME.colors.lt2 });
    iconCircle(s, { x: x + 0.3, y: 1.7, d: 0.55, icon, bg: color });
    s.addText(h, { x: x + 0.3, y: 2.38, w: 3.3, h: 0.4, isTextBox: true, margin: 0,
      fontFace: THEME.headFontFace, fontSize: 15, bold: true, color: C.text1 });
    s.addText(body, { x: x + 0.3, y: 2.78, w: 3.3, h: 1.1, isTextBox: true, margin: 0,
      fontFace: THEME.bodyFontFace, fontSize: 11, color: C.text2 });
  });
  s.addText(
    "K (cluster count) was chosen deliberately too: silhouette score alone keeps climbing as K approaches N on a " +
    "small dataset — that rewards singleton clusters, not meaningful themes. We picked the smallest K (13) where " +
    "cluster purity against known-synthetic labels was high (76%) and no cluster fell below n=3.",
    { x: 0.6, y: 4.3, w: 12.1, h: 1.0, isTextBox: true, margin: 0,
      fontFace: THEME.bodyFontFace, fontSize: 13, color: C.text1, fill: { color: "FFF7EC" },
      line: { color: THEME.colors.accent3, width: 0.75 } }
  );
  s.addText("scripts/categorize.py", { placeholder: "footer" });

  // =========================================================================
  // SLIDE 7 — 13 CATEGORIES (native bar chart)
  // =========================================================================
  s = pres.addSlide({ masterName: "CONTENT" });
  s.addText("13 categories fell out of the data", { placeholder: "title" });
  const catData = [
    ["Export/Reporting Bug", 19], ["Smart Alerts Launch & Upsell", 15],
    ["Mixed: Escalation + Staffing", 10], ["Routine Support Check-ins", 9],
    ["Churn Risk Review", 7], ["Competitive Threat", 7], ["Healthy Renewal", 7],
    ["Sprint Planning", 6], ["Login/SSO Resolution", 6], ["Security & Compliance", 5],
    ["Incident Postmortem", 4], ["Roadmap Prioritization", 4], ["Reference & Contract", 4],
  ].reverse();
  s.addChart("bar", [{ name: "Calls", labels: catData.map(d => d[0]), values: catData.map(d => d[1]) }], {
    x: 0.5, y: 1.3, w: 7.6, h: 5.75, barDir: "bar",
    chartColors: [THEME.colors.accent1],
    showTitle: false, showLegend: false,
    showValue: true, dataLabelColor: THEME.colors.dk1, dataLabelFontSize: 10, dataLabelFontFace: "+mn-lt",
    dataLabelPosition: "outEnd",
    catAxisLabelColor: THEME.colors.dk1, catAxisLabelFontSize: 10, catAxisLabelFontFace: "+mn-lt",
    valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" },
    barGapWidthPct: 35,
  });
  const takeaways = [
    "Largest single category: the export/reporting bug (19 calls, ~18% of everything)",
    "Second largest is a genuine good-news story: the Smart Alerts launch driving upsell conversations",
    "Most categories sit entirely within one call type — support problems stay in support, planning stays internal",
  ];
  s.addText("What stands out", { x: 8.35, y: 1.5, w: 4.4, h: 0.4, isTextBox: true, margin: 0,
    fontFace: THEME.headFontFace, fontSize: 15, bold: true, color: THEME.colors.dk2 });
  takeaways.forEach((t, i) => {
    const y = 2.05 + i * 1.3;
    card(s, { x: 8.35, y, w: 4.4, h: 1.1 });
    s.addText(t, { x: 8.6, y: y + 0.15, w: 3.9, h: 0.85, isTextBox: true, margin: 0,
      fontFace: THEME.bodyFontFace, fontSize: 12, color: C.text1 });
  });
  s.addText("13 clusters, K chosen via purity validation (see appendix in notebook)", { placeholder: "footer" });

  // =========================================================================
  // SLIDE 8 — CROSS-CHANNEL SPOTLIGHT
  // =========================================================================
  s = pres.addSlide({ masterName: "CONTENT" });
  s.addText("Only one category crosses every channel", { placeholder: "title" });
  const ctData = [
    ["Export/Reporting Bug", { support: 14, external: 3, internal: 2 }],
    ["Smart Alerts Launch & Upsell", { support: 1, external: 11, internal: 3 }],
    ["Churn Risk Review", { support: 0, external: 0, internal: 7 }],
    ["Login/SSO Resolution", { support: 6, external: 0, internal: 0 }],
    ["Healthy Renewal", { support: 0, external: 7, internal: 0 }],
  ];
  const chTypes = ["support", "external", "internal"];
  const chColors = [THEME.colors.accent3, THEME.colors.accent4, THEME.colors.accent6];
  s.addChart(
    "bar",
    chTypes.map((t, i) => ({ name: t[0].toUpperCase() + t.slice(1), labels: ctData.map(d => d[0]), values: ctData.map(d => d[1][t]) })),
    {
      x: 0.5, y: 1.3, w: 7.7, h: 5.6, barDir: "bar", barGrouping: "stacked",
      chartColors: chColors,
      showTitle: false, showLegend: true, legendPos: "b", legendFontFace: "+mn-lt", legendFontSize: 11,
      showValue: true, dataLabelColor: "FFFFFF", dataLabelFontSize: 10, dataLabelFontFace: "+mn-lt", dataLabelPosition: "ctr",
      dataLabelFormatCode: "0;-0;;",
      catAxisLabelColor: THEME.colors.dk1, catAxisLabelFontSize: 10.5, catAxisLabelFontFace: "+mn-lt",
      valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" },
      barGapWidthPct: 40,
    }
  );
  s.addText(
    "Every other major category lives almost entirely inside one call type: Smart Alerts enthusiasm shows up with " +
    "account managers, churn reviews happen internally, login issues stay in support. The export bug is the " +
    "exception — it shows up in support tickets, renewal conversations, and engineering syncs alike.",
    { x: 8.4, y: 1.5, w: 4.4, h: 2.3, isTextBox: true, margin: 0,
      fontFace: THEME.bodyFontFace, fontSize: 13, color: C.text1 }
  );
  card(s, { x: 8.4, y: 4.0, w: 4.4, h: 2.3, fill: "FDEAEA" });
  s.addText("That cross-channel footprint is itself a signal", { x: 8.65, y: 4.2, w: 3.9, h: 0.5, isTextBox: true, margin: 0,
    fontFace: THEME.headFontFace, fontSize: 14, bold: true, color: THEME.colors.accent2 });
  s.addText(
    "A topic visible from every seat in the company isn't a one-off — it's systemic enough that nobody needs a " +
    "dashboard to notice it. The real question is why it still took 25 days to escalate. (§4 below)",
    { x: 8.65, y: 4.7, w: 3.9, h: 1.5, isTextBox: true, margin: 0, fontFace: THEME.bodyFontFace, fontSize: 12, color: C.text1 }
  );

  // =========================================================================
  // SLIDE 9 — SECTION: SENTIMENT
  // =========================================================================
  s = pres.addSlide({ masterName: "SECTION" });
  s.addText("02", { x: 0.9, y: 2.75, w: 2, h: 0.5, isTextBox: true, margin: 0,
    fontFace: THEME.bodyFontFace, fontSize: 16, color: THEME.colors.accent1, bold: true });
  s.addText("Sentiment Analysis & Trends", { placeholder: "title" });
  s.addText("What the data says — and why getting there took three tries", { x: 0.9, y: 4.0, w: 9.5, h: 0.5,
    isTextBox: true, margin: 0, fontFace: THEME.bodyFontFace, fontSize: 15, color: "C7D3E8" });
  iconCircle(s, { x: 11.1, y: 2.8, d: 1.0, icon: icons.smile_white, bg: THEME.colors.accent1 });

  // =========================================================================
  // SLIDE 10 — WHY NAIVE SENTIMENT FAILS
  // =========================================================================
  s = pres.addSlide({ masterName: "CONTENT" });
  s.addText("Off-the-shelf sentiment tools don't work on polite frustration", { placeholder: "title" });
  card(s, { x: 0.6, y: 1.4, w: 7.5, h: 2.6, fill: THEME.colors.lt2 });
  s.addText("Actual customer quote from the dataset:", { x: 0.9, y: 1.6, w: 7, h: 0.4, isTextBox: true, margin: 0,
    fontFace: THEME.bodyFontFace, fontSize: 11.5, color: C.text2, italic: true });
  s.addText(
    "“I appreciate that, but this is the third time I’ve called about this exact thing — " +
    "I was told it was fixed in September.”",
    { x: 0.9, y: 2.0, w: 7, h: 1.3, isTextBox: true, margin: 0,
      fontFace: THEME.headFontFace, fontSize: 18, italic: true, color: THEME.colors.dk2 }
  );
  s.addText("VADER (lexicon-based) reads this as POSITIVE — it sees “appreciate,” not “third time.”",
    { x: 0.9, y: 3.35, w: 7, h: 0.5, isTextBox: true, margin: 0,
      fontFace: THEME.bodyFontFace, fontSize: 12.5, bold: true, color: THEME.colors.accent2 });
  statCallout(s, { x: 8.5, y: 1.5, w: 4.2, number: "96 / 103", label: "calls VADER scored “positive” — including active churn threats", color: THEME.colors.accent2, numSize: 36, labelSize: 12 });
  statCallout(s, { x: 8.5, y: 3.0, w: 4.2, number: "~50%", label: "disagreement rate between VADER and a transformer cross-check (DistilBERT)", color: THEME.colors.accent3, numSize: 36, labelSize: 12 });
  s.addText(
    "Conclusion: generic sentiment tools (trained on movie reviews / tweets) don’t transfer to professional, " +
    "consequence-heavy B2B dialogue, where tone and actual stakes are decoupled. We needed contextual judgment, not a lexicon.",
    { x: 0.6, y: 4.35, w: 12.1, h: 0.9, isTextBox: true, margin: 0,
      fontFace: THEME.bodyFontFace, fontSize: 13, color: C.text1 }
  );
  s.addText("Our approach: LLM-based contextual scoring — full rationale in scripts/sentiment.py", {
    x: 0.6, y: 5.4, w: 12.1, h: 0.5, isTextBox: true, margin: 0,
    fontFace: THEME.bodyFontFace, fontSize: 13, bold: true, color: THEME.colors.accent1 });
  s.addText("scripts/sentiment.py", { placeholder: "footer" });

  // =========================================================================
  // SLIDE 11 — SENTIMENT TREND (image from notebook)
  // =========================================================================
  s = pres.addSlide({ masterName: "CONTENT" });
  s.addText("Weekly sentiment by call type", { placeholder: "title" });
  s.addImage({ path: path.join(__dirname, "assets", "sentiment_trend_notitle.png"), x: 1.05, y: 1.4, w: 11.2, h: 4.75 });
  s.addText(
    "Support sentiment tracks the export bug cleanly — sharp dip while it’s open, recovery right as the fix ships. " +
    "The second dip in late August is unrelated noise (a cluster of login/billing complaints landing the same week), not a relapse — " +
    "called out explicitly in the notebook rather than cropped out.",
    { x: 0.9, y: 6.35, w: 10.8, h: 0.75, isTextBox: true, margin: 0,
      fontFace: THEME.bodyFontFace, fontSize: 12, color: C.text2 }
  );

  // =========================================================================
  // SLIDE 12 — THE THROUGHLINE / LAG TIMELINE
  // =========================================================================
  s = pres.addSlide({ masterName: "CONTENT" });
  s.addText("The full arc: one bug, three channels, 43 days", { placeholder: "title" });
  const milestones = [
    ["Jul 4", "First customer\ncomplaint", "Support", THEME.colors.accent2],
    ["Jul 9", "Eng acknowledges,\nsits in backlog", "Internal", THEME.colors.accent6],
    ["Jul 23", "Pulled forward\n(+14d in backlog)", "Internal", THEME.colors.accent3],
    ["Jul 29", "Tied to renewal\nrisk (+25d total)", "External", THEME.colors.accent3],
    ["Aug 10", "Fix ships\n(+37d total)", "Internal", THEME.colors.accent5],
    ["Aug 16", "Customer confirms\nresolved (+43d)", "Support", THEME.colors.accent1],
  ];
  const tlY = 2.2, tlX0 = 0.9, tlX1 = 12.4;
  s.addShape("line", { x: tlX0, y: tlY, w: tlX1 - tlX0, h: 0, line: { color: "D5DADF", width: 2 } });
  const step = (tlX1 - tlX0) / (milestones.length - 1);
  milestones.forEach(([date, label, chan, color], i) => {
    const x = tlX0 + step * i;
    s.addShape("ellipse", { x: x - 0.11, y: tlY - 0.11, w: 0.22, h: 0.22, fill: { color }, line: { color: "FFFFFF", width: 2 } });
    s.addText(date, { x: x - 0.6, y: tlY - 0.65, w: 1.2, h: 0.35, isTextBox: true, margin: 0, align: "center",
      fontFace: THEME.headFontFace, fontSize: 12.5, bold: true, color: THEME.colors.dk1 });
    s.addText(chan.toUpperCase(), { x: x - 0.6, y: tlY + 0.2, w: 1.2, h: 0.3, isTextBox: true, margin: 0, align: "center",
      fontFace: THEME.bodyFontFace, fontSize: 9, bold: true, color });
    s.addText(label, { x: x - 0.75, y: tlY + 0.52, w: 1.5, h: 0.9, isTextBox: true, margin: 0, align: "center",
      fontFace: THEME.bodyFontFace, fontSize: 10.5, color: C.text2 });
  });
  statCallout(s, { x: 0.9, y: 4.55, w: 3.7, number: "25 days", label: "before this was treated as urgent internally — despite 3 separate support calls about it", color: THEME.colors.accent2, numSize: 38 });
  statCallout(s, { x: 4.9, y: 4.55, w: 3.7, number: "37 days", label: "from first complaint to shipped fix", color: THEME.colors.accent3, numSize: 38 });
  statCallout(s, { x: 8.9, y: 4.55, w: 3.5, number: "+1.6", label: "sentiment swing in support calls, week of the fix vs. week before (−0.85 → +0.75)", color: THEME.colors.accent1, numSize: 38 });
  card(s, { x: 0.9, y: 6.2, w: 11.5, h: 0.85, fill: "FFF7EC" });
  s.addText(
    "Recommendation: surface “this topic has appeared in N calls across support/external in the last 30 days” directly " +
    "on the eng backlog — don’t rely on someone noticing the pattern from memory.",
    { x: 1.15, y: 6.3, w: 11, h: 0.65, isTextBox: true, margin: 0, fontFace: THEME.bodyFontFace, fontSize: 12.5, bold: true, color: THEME.colors.dk2 }
  );

  // =========================================================================
  // SLIDE 13 — SECTION: BONUS INSIGHTS
  // =========================================================================
  s = pres.addSlide({ masterName: "SECTION" });
  s.addText("03", { x: 0.9, y: 2.75, w: 2, h: 0.5, isTextBox: true, margin: 0,
    fontFace: THEME.bodyFontFace, fontSize: 16, color: THEME.colors.accent1, bold: true });
  s.addText("Beyond the Required Tasks", { placeholder: "title" });
  s.addText("Three more things this data can tell different stakeholders", { x: 0.9, y: 4.0, w: 9.5, h: 0.5,
    isTextBox: true, margin: 0, fontFace: THEME.bodyFontFace, fontSize: 15, color: "C7D3E8" });
  iconCircle(s, { x: 11.1, y: 2.8, d: 1.0, icon: icons.trend_white, bg: THEME.colors.accent1 });

  // =========================================================================
  // SLIDE 14 — PRIORITY RANKING (native bar chart, volume x negativity)
  // =========================================================================
  s = pres.addSlide({ masterName: "CONTENT" });
  s.addText("Insight: where should the backlog focus first", { placeholder: "title" });
  s.addText("For: support & engineering leads prioritizing a backlog", { x: 0.6, y: 1.05, w: 9, h: 0.35,
    isTextBox: true, margin: 0, fontFace: THEME.bodyFontFace, fontSize: 12, italic: true, color: C.text2 });
  // priority_score = call volume x negativity (0 where a category is net-neutral/positive) -- outputs/data/category_priority.csv
  const prio = [
    ["Export/Reporting Bug", 6.4], ["Mixed: Escalation + Staffing", 4.2],
    ["Churn Risk Review", 3.95], ["Login/SSO Resolution", 2.65],
    ["Competitive Threat", 1.7], ["Incident Postmortem", 0.6],
    ["Sprint Planning", 0.4], ["Roadmap Prioritization", 0.2],
  ].reverse();
  s.addChart("bar", [{ name: "Priority score", labels: prio.map(p => p[0]), values: prio.map(p => p[1]) }], {
    x: 0.5, y: 1.55, w: 7.6, h: 5.5, barDir: "bar",
    chartColors: [THEME.colors.accent2],
    showTitle: false, showLegend: false,
    showValue: true, dataLabelColor: THEME.colors.dk1, dataLabelFontSize: 10, dataLabelFontFace: "+mn-lt",
    dataLabelPosition: "outEnd", dataLabelFormatCode: "0.0",
    catAxisLabelColor: THEME.colors.dk1, catAxisLabelFontSize: 10.5, catAxisLabelFontFace: "+mn-lt",
    valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" },
    barGapWidthPct: 35,
  });
  s.addText(
    "Priority score = call volume × negativity, by category. Export/Reporting Bug ranks #1 by a wide margin — " +
    "it's both the single highest-volume category in the whole dataset and solidly negative. A second, independent " +
    "method agrees with the qualitative read from §2 — a useful gut-check before taking a finding to leadership.",
    { x: 8.35, y: 1.6, w: 4.4, h: 2.6, isTextBox: true, margin: 0, fontFace: THEME.bodyFontFace, fontSize: 13, color: C.text1 }
  );
  card(s, { x: 8.35, y: 4.35, w: 4.4, h: 2.15, fill: THEME.colors.lt2 });
  s.addText("Categories not shown here", { x: 8.6, y: 4.55, w: 3.9, h: 0.35, isTextBox: true, margin: 0,
    fontFace: THEME.headFontFace, fontSize: 13, bold: true, color: THEME.colors.dk2 });
  s.addText(
    "Scored net-zero or positive, so they don't need backlog attention right now — notably Smart Alerts Launch " +
    "and Healthy Renewal, both high-volume and positive. Protect what's working there; don't over-invest in fixing it.",
    { x: 8.6, y: 4.95, w: 3.9, h: 1.45, isTextBox: true, margin: 0, fontFace: THEME.bodyFontFace, fontSize: 11.5, color: C.text2 }
  );

  // =========================================================================
  // SLIDE 15 — SENTIMENT != CHURN RISK
  // =========================================================================
  s = pres.addSlide({ masterName: "CONTENT" });
  s.addText("Insight: sentiment score ≠ churn risk", { placeholder: "title" });
  s.addText("For: sales & CS leaders building a churn-risk dashboard", { x: 0.6, y: 1.05, w: 9, h: 0.35,
    isTextBox: true, margin: 0, fontFace: THEME.bodyFontFace, fontSize: 12, italic: true, color: C.text2 });

  card(s, { x: 0.6, y: 1.6, w: 5.9, h: 2.5, fill: "FDEAEA" });
  iconCircle(s, { x: 0.9, y: 1.85, d: 0.5, icon: icons.alert, bg: "FFFFFF" });
  s.addText("The quiet, dangerous signal", { x: 1.6, y: 1.92, w: 4.7, h: 0.4, isTextBox: true, margin: 0,
    fontFace: THEME.headFontFace, fontSize: 14, bold: true, color: THEME.colors.accent2 });
  s.addText(
    "“We’ve been evaluating Lumina Analytics as an alternative” scores only −0.35 — milder than an " +
    "angry call about a bug that’s already fixed. A sentiment-only alert under-ranks the more dangerous signal.",
    { x: 1.6, y: 2.35, w: 4.6, h: 1.6, isTextBox: true, margin: 0, fontFace: THEME.bodyFontFace, fontSize: 12, color: C.text1 }
  );

  card(s, { x: 6.8, y: 1.6, w: 5.9, h: 2.5, fill: THEME.colors.lt2 });
  iconCircle(s, { x: 7.1, y: 1.85, d: 0.5, icon: icons.shield, bg: "FFFFFF" });
  s.addText("Naive keyword-flagging over-fires too", { x: 7.8, y: 1.92, w: 4.7, h: 0.4, isTextBox: true, margin: 0,
    fontFace: THEME.headFontFace, fontSize: 14, bold: true, color: THEME.colors.dk2 });
  s.addText(
    "6 of 15 keyword-flagged “risk” calls are internal teams calmly discussing strategy or a feature launch " +
    "that just happens to name a competitor — not customer-expressed risk at all.",
    { x: 7.8, y: 2.35, w: 4.6, h: 1.6, isTextBox: true, margin: 0, fontFace: THEME.bodyFontFace, fontSize: 12, color: C.text1 }
  );

  const churnStats = [
    ["15", "calls mention competitor / evaluating language", THEME.colors.accent3],
    ["6", "of those scored neutral or positive — missed by a sentiment-only alert", THEME.colors.accent2],
    ["2 signals", "needed, scored separately: sentiment vs. relationship risk", THEME.colors.accent1],
  ];
  churnStats.forEach(([num, label, color], i) => {
    const x = 0.6 + i * 4.08;
    card(s, { x, y: 4.35, w: 3.85, h: 1.55 });
    statCallout(s, { x: x + 0.3, y: 4.55, w: 3.3, number: num, label, color, numSize: 32, labelSize: 11.5 });
  });
  s.addText(
    "Recommendation: build churn-risk classification as its own LLM-judged signal, not a sentiment threshold and not a keyword list.",
    { x: 0.6, y: 6.15, w: 11.8, h: 0.5, isTextBox: true, margin: 0, fontFace: THEME.bodyFontFace, fontSize: 13, bold: true, color: THEME.colors.dk2 }
  );

  // =========================================================================
  // SLIDE 16 — FUTURE IDEAS (described, not built)
  // =========================================================================
  s = pres.addSlide({ masterName: "CONTENT" });
  s.addText("Two more ideas, described but not built yet", { placeholder: "title" });
  const futureIdeas = [
    [icons.users, "Account health rollup", "Who'd use it: account managers & CS leaders",
      "Aggregate category + sentiment + recency per account into a rolling health score, refreshed after every call — so a trend is visible before a renewal, not discovered during it.",
      "Needs persistent per-account identity across calls in the data (today's synthetic accounts are assigned per-call). A data-generation change worth sign-off, not quietly built around.", THEME.colors.accent4],
    [icons.message, "Auto-generated pre-call briefings", "Who'd use it: AMs and support agents walking in cold",
      "One-paragraph summary of everything that's come up for an account recently, across all three channels, generated before any call.",
      "Directly targets the gap this data already surfaces itself in the internal roadmap call: “support tickets and account escalations aren't visible to engineering in one place.”", THEME.colors.accent1],
  ];
  futureIdeas.forEach(([icon, h, who, body, note, color], i) => {
    const x = 0.6 + i * 6.2;
    card(s, { x, y: 1.5, w: 5.95, h: 5.3 });
    iconCircle(s, { x: x + 0.3, y: 1.8, d: 0.6, icon, bg: color });
    s.addText(h, { x: x + 1.1, y: 1.85, w: 4.5, h: 0.5, isTextBox: true, margin: 0,
      fontFace: THEME.headFontFace, fontSize: 17, bold: true, color: C.text1 });
    s.addText(who, { x: x + 1.1, y: 2.3, w: 4.5, h: 0.35, isTextBox: true, margin: 0,
      fontFace: THEME.bodyFontFace, fontSize: 11, italic: true, color: THEME.colors.accent1 });
    s.addText(body, { x: x + 0.3, y: 2.85, w: 5.4, h: 1.7, isTextBox: true, margin: 0,
      fontFace: THEME.bodyFontFace, fontSize: 12.5, color: C.text1 });
    s.addShape("line", { x: x + 0.3, y: 4.75, w: 5.35, h: 0, line: { color: "D5DADF", width: 1 } });
    s.addText("Why not built here", { x: x + 0.3, y: 4.9, w: 5.4, h: 0.3, isTextBox: true, margin: 0,
      fontFace: THEME.bodyFontFace, fontSize: 10.5, bold: true, color: C.text2 });
    s.addText(note, { x: x + 0.3, y: 5.2, w: 5.4, h: 1.5, isTextBox: true, margin: 0,
      fontFace: THEME.bodyFontFace, fontSize: 11, color: C.text2 });
  });

  // =========================================================================
  // SLIDE 17 — RECOMMENDATIONS
  // =========================================================================
  s = pres.addSlide({ masterName: "CONTENT" });
  s.addText("What we'd act on first", { placeholder: "title" });
  const recs = [
    ["Surface cross-channel volume on the eng backlog", "A simple “this topic has appeared in N calls across channels in 30 days” counter would have cut the 25-day escalation lag.", icons.clock],
    ["Separate churn-risk scoring from sentiment scoring", "Build it as its own LLM-judged signal — a calm “we're evaluating alternatives” is a bigger risk than an angry resolved-bug complaint.", icons.target],
    ["Prioritize by volume × negativity, not either alone", "The priority ranking (§4) is a cheap, repeatable way to validate “what should we fix first” beyond gut feel.", icons.trend],
    ["Fix per-account identity in any future data work", "Unlocks the account health rollup and pre-call briefing ideas — the two highest-leverage ideas we didn't build yet.", icons.users],
  ];
  recs.forEach(([h, body, icon], i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = 0.6 + col * 6.2, y = 1.5 + row * 2.75;
    card(s, { x, y, w: 5.95, h: 2.5 });
    iconCircle(s, { x: x + 0.3, y: y + 0.3, d: 0.55, icon, bg: THEME.colors.accent1 });
    s.addText(h, { x: x + 1.05, y: y + 0.3, w: 4.6, h: 0.65, isTextBox: true, margin: 0,
      fontFace: THEME.headFontFace, fontSize: 14.5, bold: true, color: C.text1 });
    s.addText(body, { x: x + 0.3, y: y + 1.1, w: 5.4, h: 1.3, isTextBox: true, margin: 0,
      fontFace: THEME.bodyFontFace, fontSize: 12, color: C.text2 });
  });

  // =========================================================================
  // SLIDE 18 — CLOSING
  // =========================================================================
  s = pres.addSlide({ masterName: "CLOSING" });
  s.addText("Thank you", { placeholder: "title" });
  s.addText([
    { text: "Questions — and happy to walk through any part of the notebook live.", options: { breakLine: true } },
    { text: "Repo: notebooks/01_transcript_intelligence_analysis.ipynb  •  scripts/categorize.py  •  scripts/sentiment.py", options: {} },
  ], { placeholder: "subtitle" });
  iconCircle(s, { x: 11.0, y: 3.1, d: 0.9, icon: icons.check_white, bg: THEME.colors.accent1 });

  const outFile = path.join(__dirname, "transcript_intelligence.pptx");
  await pres.writeFile({ fileName: outFile });
  await applyTheme(outFile, THEME);
  console.log("Deck written and themed.");
}

main().catch(err => { console.error(err); process.exit(1); });
