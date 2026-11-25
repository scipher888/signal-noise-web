# Executable audit, Daily State of AI 2026-11-25

Each claim is tested by a deterministic Python check against snapshotted source texts and X posts. PASS = the source sentence quoted supports the claim; FAIL = the source contradicts it or a required caveat is missing; NEEDS-HUMAN = opinion or not decidable by string/number match.

| artifact | PASS | FAIL | NEEDS-HUMAN | ERROR |
|---|---|---|---|---|
| episode | 52 | 16 | 16 | 0 |
| takeaways | 21 | 9 | 4 | 0 |

## Sources
- `primary-openai-gpt6-protein-design-wetlab`: [GPT-6 models demonstrate intrinsic protein-design capabilities](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/) (sha256 39d6afad75a9…)
- `x-openai`: [X post by @OpenAI (OpenAI)](https://x.com/OpenAI/status/2125334383490105601) (sha256 392ca799d94c…)
- `x-gdb`: [X post by @gdb (Greg Brockman)](https://x.com/gdb/status/2125341356503748716) (sha256 d1d97e6d4e02…)
- `primary-gpt62-astra-1808-sketchbook-attribution`: [GPT 6.2 Astra Solves a Historical Mystery](https://generativehistory.substack.com/p/gpt-62-astra-solves-a-historical) (sha256 9350234ebda8…)
- `x-emollick`: [X post by @emollick (Ethan Mollick)](https://x.com/emollick/status/2125245031842042301) (sha256 e0fd471d4cca…)
- `primary-deepmind-humanitys-first-exam-floor-reli`: [Humanity's First Exam (HFE) Leaderboard](https://www.kaggle.com/benchmarks/deepmind/hfe/leaderboard) (sha256 b5dd5b5cdd83…)
- `x-kaggle`: [X post by @kaggle (Kaggle)](https://x.com/kaggle/status/2125313430303244739) (sha256 264a4cbbf0d0…)
- `scan-framing`: [Morning X-first scan: verification framing per story](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt) (sha256 1cf847da4f4e…)

## episode

### FAIL · e02-same-model (comparison, Discovery vs. reliability)
> Claim: the same frontier AI model crack a 218-year-old historical mystery in twenty-two minutes and design new proteins that actually bind in a wet lab, yet still miscount a handful of objects in a simple picture

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "First, Onava made small proteins based on three-dimensional structures designed by a pre-released version of GPT-6.2."

Note: The lab report identifies a prerelease GPT-6.2, not the same Astra configuration; the counting-error breakdown is pooled, not an Astra-specific incident.

```python
def check(ctx):
    q = ctx.find('openai', r'structures designed by a pre-released version of GPT.6\.2')
    v = ctx.find('deepmind', r'GPT.6\.2 Astra.*miscount(?:ed|s).*objects')
    if q and not v: return ctx.fail('openai', q, 'The lab report identifies a prerelease GPT-6.2, not the same Astra configuration; the counting-error breakdown is pooled, not an Astra-specific incident.')
    return ctx.need('deepmind', v, 'Verify model identity and the individual visual failure across all three reports.')
```

### FAIL · e11-widening (comparison, Discovery vs. reliability)
> Claim: the widening gap between discovery mode and reliability mode

Source ([primary-deepmind-humanitys-first-exam-floor-reli](https://www.kaggle.com/benchmarks/deepmind/hfe/leaderboard)): "Across the 16 models on this Harbor leaderboard, models reach 98.9% to 100.0% on Family pass@4 and the top models reach 94.9% to 97.7% on pass@1, yet Family pass⁴ remains substantially lower, leaving a wide Family Reliability Gap where small pass@1 differences widen nearly fourfold under Family pass⁴."

Note: This is a difference between metrics, not a discovery-versus-reliability trend over time.

```python
def check(ctx):
    q = ctx.find('deepmind', r'small pass@1 differences widen nearly fourfold under Family pass⁴')
    return ctx.fail('deepmind', q, 'This is a difference between metrics, not a discovery-versus-reliability trend over time.') if q else ctx.need('deepmind', None, 'Need longitudinal measurements.')
```

### FAIL · e17-human-task-comparison (comparison, Humanity's First Exam)
> Claim: Instead of PhD-level questions, it tests simple, ninety-second tasks humans breeze through

Source ([primary-deepmind-humanitys-first-exam-floor-reli](https://www.kaggle.com/benchmarks/deepmind/hfe/leaderboard)): "Four independent human raters solved each candidate seed without external tools (no LLMs, web search, calculators, code, word or character counters, or copy-paste; median solve time 1.5 minutes, IQR 1.0 to 2.5 minutes)."

Note: Ninety seconds is the median human seed solve time, not a duration specified for the tasks.

```python
def check(ctx):
    q = ctx.find('deepmind', r'median solve time 1\.5 minutes, IQR 1\.0 to 2\.5 minutes')
    return ctx.fail('deepmind', q, 'Ninety seconds is the median human seed solve time, not a duration specified for the tasks.') if q else ctx.need('deepmind', None, 'Verify timing and population.')
```

### FAIL · e18-task-duration (number, Humanity's First Exam)
> Claim: ninety-second tasks

Source ([primary-deepmind-humanitys-first-exam-floor-reli](https://www.kaggle.com/benchmarks/deepmind/hfe/leaderboard)): "Four independent human raters solved each candidate seed without external tools (no LLMs, web search, calculators, code, word or character counters, or copy-paste; median solve time 1.5 minutes, IQR 1.0 to 2.5 minutes)."

Note: The reported 90 seconds is a median for seed prompts.

```python
def check(ctx):
    return ctx.support_or_contradict('deepmind', r'each task (?:takes|lasts) 90 seconds', r'median solve time 1\.5 minutes, IQR 1\.0 to 2\.5 minutes', 'The reported 90 seconds is a median for seed prompts.')
```

### FAIL · e24-coverage-draws (number, Humanity's First Exam)
> Claim: solve every task family at least once across four attempts

Source ([primary-deepmind-humanitys-first-exam-floor-reli](https://www.kaggle.com/benchmarks/deepmind/hfe/leaderboard)): "The Family Reliability Gap is Family pass@4 minus Family pass⁴, where Family pass@4 is the probability that at least 1 of 16 draws across a family succeeds, averaged over all 136 families:"

Note: The announced 100% is family coverage with four draws per prompt, not four attempts total per family.

```python
def check(ctx):
    return ctx.support_or_contradict('deepmind', r'Family pass@4 is the probability that at least 1 of 4 draws across a family succeeds', r'Family pass@4 is the probability that at least 1 of 16 draws across a family succeeds', 'The announced 100% is family coverage with four draws per prompt, not four attempts total per family.')
```

### FAIL · e34-workflow-collapse (qualifier, Humanity's First Exam)
> Claim: For unattended agents chaining dozens of steps together, that gap is where workflows collapse

Source ([primary-deepmind-humanitys-first-exam-floor-reli](https://www.kaggle.com/benchmarks/deepmind/hfe/leaderboard)): "| Interaction Protocol | Zero-shot, single user turn with no system prompt."

Note: The benchmark does not observe multi-step unattended workflows or identify where they collapse.

```python
def check(ctx):
    q = ctx.find('deepmind', r'Zero-shot, single user turn with no system prompt')
    return ctx.fail('deepmind', q, 'The benchmark does not observe multi-step unattended workflows or identify where they collapse.') if q else ctx.need('deepmind', None, 'Check evaluation scope.')
```

### FAIL · e56-archival-chain (attribution, Chabot sketchbook)
> Claim: In twenty-two minutes, the model linked a Montreal fur trader's diary, a century-old letter, and a 2014 thesis footnote to identify an obscure French aristocrat, vicomte de Chabot

Source ([primary-gpt62-astra-1808-sketchbook-attribution](https://generativehistory.substack.com/p/gpt-62-astra-solves-a-historical)): "Joseph later that month via a letter written by a man named John Askin Jr. that had been published in a document collection nearly a hundred years ago.Why Human Historians Didn't Make the Connection"

Note: The collection, not the letter, was about a century old. The thesis footnote was traced as a lead to the journal.

```python
def check(ctx):
    q = ctx.find('gpt62', r'century-old book of letters|published in a document collection nearly a hundred years ago')
    if q: return ctx.fail('gpt62', q, 'The collection, not the letter, was about a century old. The thesis footnote was traced as a lead to the journal.')
    return ctx.require('gpt62', r'22 minutes and 1 second later.*vicomte de Chabot', r'diary of Joseph Frobisher.*fur trader.*Montreal', r'(?:century-old|hundred-year-old) letter\b', r'single footnote in a 2014 PhD thesis', r'minor French aristocrat')
```

### FAIL · e57-letter-age (number, Chabot sketchbook)
> Claim: a century-old letter

Source ([primary-gpt62-astra-1808-sketchbook-attribution](https://generativehistory.substack.com/p/gpt-62-astra-solves-a-historical)): "Joseph later that month via a letter written by a man named John Askin Jr. that had been published in a document collection nearly a hundred years ago.Why Human Historians Didn't Make the Connection"

Note: The age refers to publication of the collection, not composition of the letter.

```python
def check(ctx):
    return ctx.support_or_contradict('gpt62', r'(?:century-old|hundred-year-old) letter\b', r'century-old book of letters|published in a document collection nearly a hundred years ago', 'The age refers to publication of the collection, not composition of the letter.')
```

### FAIL · e60-fable-time (number, Chabot sketchbook)
> Claim: Claude Fable 5.2 also found Chabot in thirty-five minutes

Source ([primary-gpt62-astra-1808-sketchbook-attribution](https://generativehistory.substack.com/p/gpt-62-astra-solves-a-historical)): "I subsequently ran the same test (using the same prompt) with Fable 5.2 and it reached the same conclusion in about 35 minutes."

Note: The historian gives an approximate duration, not a measured 35 minutes.

```python
def check(ctx):
    q = ctx.find('gpt62', r'Fable 5\.2 and it reached the same conclusion in about 35 minutes')
    return ctx.fail('gpt62', q, 'The historian gives an approximate duration, not a measured 35 minutes.') if q else ctx.require('gpt62', r'Fable 5\.2.*same conclusion in 35 minutes')
```

### FAIL · oe11-creator-results (objection, Humanity's First Exam)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "framing (Kaggle / Google DeepMind): Benchmark creator's own leaderboard and summary of its paper; answers are graded by a Google model; the leaderboard lists 16 models while the X post cites 18 from the paper."

Note: Clarify that the leaderboard and paper findings are creator-reported, not just hosted on Kaggle.

```python
def check(ctx):
    q = ctx.find('framing', r'Benchmark creator.s own leaderboard and summary of its paper')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:creator.s own|DeepMind.s own|Google.s own).{0,48}(?:leaderboard|results|paper)|(?:DeepMind|Kaggle).{0,35}(?:reports|summarizes|published).{0,32}(?:its own|its paper|its leaderboard)') else ctx.fail('framing', q, 'Clarify that the leaderboard and paper findings are creator-reported, not just hosted on Kaggle.')
```

### FAIL · oe12-google-grader (objection, Humanity's First Exam)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "framing (Kaggle / Google DeepMind): Benchmark creator's own leaderboard and summary of its paper; answers are graded by a Google model; the leaderboard lists 16 models while the X post cites 18 from the paper."

Note: Identify the Google model grader.

```python
def check(ctx):
    q = ctx.find('framing', r'answers are graded by a Google model')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:graded|judged|scored).{0,30}(?:Google model|Gemini)|(?:Google model|Gemini).{0,30}(?:grades|judges|scores) (?:the )?(?:answers|responses)') else ctx.fail('framing', q, 'Identify the Google model grader.')
```

### FAIL · oe13-two-cohorts (objection, Humanity's First Exam)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "framing (Kaggle / Google DeepMind): Benchmark creator's own leaderboard and summary of its paper; answers are graded by a Google model; the leaderboard lists 16 models while the X post cites 18 from the paper."

Note: Distinguish the 16-model leaderboard from the 18-model paper summarized on X.

```python
def check(ctx):
    q = ctx.find('framing', r'leaderboard lists 16 models while the X post cites 18 from the paper')
    board = ctx.art_has(r'(?:leaderboard|Kaggle run).{0,40}(?:16|sixteen) models|(?:16|sixteen)[- ]model leaderboard')
    paper = ctx.art_has(r'(?:paper|X post).{0,45}(?:18|eighteen)(?: models)?|(?:18|eighteen)[- ]model (?:paper|study)')
    return ctx.ok('framing', q) if board and paper else ctx.fail('framing', q, 'Distinguish the 16-model leaderboard from the 18-model paper summarized on X.')
```

### FAIL · oe14-benchmark-replication (objection, Humanity's First Exam)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "framing (Kaggle / Google DeepMind): Benchmark creator's own leaderboard and summary of its paper; answers are graded by a Google model; the leaderboard lists 16 models while the X post cites 18 from the paper."

Note: Disclose no independent replication of benchmark results.

```python
def check(ctx):
    q = ctx.find('framing', r'leaderboard lists 16 models')
    return ctx.ok('framing', q) if ctx.art_has(r'(?is)(?:benchmark|leaderboard|HFE|DeepMind).{0,160}(?:no independent replication|not (?:yet )?independently replicated)|(?:no independent replication|not independently replicated).{0,50}(?:benchmark|leaderboard|HFE)') else ctx.fail('framing', q, 'Disclose no independent replication of benchmark results.')
```

### FAIL · oe4-protein-replication (objection, Protein design)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "framing (OpenAI): Company-reported preprint with lab tests run by its research partner Onava; no independent replication."

Note: State that the protein results lack independent replication.

```python
def check(ctx):
    q = ctx.find('framing', r'Onava; no independent replication')
    return ctx.ok('framing', q) if ctx.art_has(r'(?is)(?:Onava|binder|protein|OpenAI.s own).{0,200}(?:no independent replication|not (?:yet )?independently replicated|hasn.t been independently replicated)|(?:no independent replication|not independently replicated).{0,80}(?:protein|binder)') else ctx.fail('framing', q, 'State that the protein results lack independent replication.')
```

### FAIL · oe5-specialist-sequences (objection, Protein design)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "OpenAI itself says specialized models still supplied sequences and filtered candidates."

Note: Filtering alone omits specialist sequence supply in the first binding experiment.

```python
def check(ctx):
    q = ctx.find('framing', r'specialized models still supplied sequences')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:speciali[sz](?:ed|t)(?: biology| protein)? models?).{0,64}(?:supplied|proposed|provided|generated|designed|wrote).{0,24}sequences') else ctx.fail('framing', q, 'Filtering alone omits specialist sequence supply in the first binding experiment.')
```

### FAIL · oe8-prerelease (objection, Chabot sketchbook)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "framing (Generative History (Mark Humphries)): Single historian's first-person account; he tested the model before release."

Note: Mention the historian’s prerelease access.

```python
def check(ctx):
    q = ctx.find('framing', r'he tested the model before release')
    return ctx.ok('framing', q) if ctx.art_has(r'(?is)(?:Humphries|historian|sketchbook).{0,120}(?:pre[- ]?release|before (?:its |public )?release|before it was released|early access)|(?:pre[- ]?release|early access).{0,60}(?:Astra|Humphries)') else ctx.fail('framing', q, 'Mention the historian’s prerelease access.')
```

### NEEDS-HUMAN · e01-issue-date (number, Daily State of AI)
> Claim: the Daily State of AI for Wednesday, November 25th, 2026

Note: no source sentence matches /(?:Daily State of AI|daily-state).*?(?:Wednesday, November 25(?:th)?, 2026|2026-11-25)/. Check the issue date, not a research publication date.

```python
def check(ctx):
    return ctx.require('framing', r'(?:Daily State of AI|daily-state).*?(?:Wednesday, November 25(?:th)?, 2026|2026-11-25)', note='Check the issue date, not a research publication date.')
```

### NEEDS-HUMAN · e03-mystery-age (number, Chabot sketchbook)
> Claim: a 218-year-old historical mystery

Source ([primary-gpt62-astra-1808-sketchbook-attribution](https://generativehistory.substack.com/p/gpt-62-astra-solves-a-historical)): "Without knowing the person's name in advance, it is almost impossible to know where to start looking, which is why the document has remained anonymous for more than 200 years.Waiting For Chabot"

Note: Source dates the sketchbook to 1808 and says it remained anonymous more than 200 years; it does not state 218 years.

```python
def check(ctx):
    q = ctx.find('gpt62', r'document has remained anonymous for more than 200 years')
    if not ctx.find('gpt62', r'anonymous 1808 sketchbook') or not ctx.find('gpt62', r'Nov 24, 2026'):
        return ctx.need('gpt62', q, 'Need the sketchbook date and the post date to assess the 218-year figure.')
    return ctx.need('gpt62', q, 'Source dates the sketchbook to 1808 and says it remained anonymous more than 200 years; it does not state 218 years.')
```

### NEEDS-HUMAN · e06-story-ranking (opinion, Discovery vs. reliability)
> Claim: today's three biggest AI stories

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "STORY: Google DeepMind's Humanity's First Exam measures whether frontier models get simple tasks right every time"

Note: Selection is documented; biggest is an editorial ranking.

```python
def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'STORY: Google DeepMind'), 'Selection is documented; biggest is an editorial ranking.')
```

### NEEDS-HUMAN · e08-canadian-historian (attribution, Chabot sketchbook)
> Claim: an archival find from a Canadian historian

Note: no source sentence matches /(?:Canadian historian.{0,40}Mark Humphries|Mark Humphries.{0,40}Canadian historian)/. Studying Canadian history does not establish nationality.

```python
def check(ctx):
    return ctx.require('gpt62', r'(?:Canadian historian.{0,40}Mark Humphries|Mark Humphries.{0,40}Canadian historian)', r'recovery of his largely unknown diary', note='Studying Canadian history does not establish nationality.')
```

### NEEDS-HUMAN · e10-coverage (qualifier, Discovery vs. reliability)
> Claim: a divide most coverage misses

Source ([x-kaggle](https://x.com/kaggle/status/2125313430303244739)): "That disconnect is called jagged intelligence and measuring it scientifically is critical to advancing AI reliability."

Note: No survey of coverage establishes how often this distinction is missed.

```python
def check(ctx):
    return ctx.need('kaggle', ctx.find('kaggle', r'That disconnect is called jagged intelligence'), 'No survey of coverage establishes how often this distinction is missed.')
```

### NEEDS-HUMAN · e12-training-thesis (opinion, Discovery vs. reliability)
> Claim: Intense training on math and code has turned frontier models into remarkable discovery engines

Source ([primary-gpt62-astra-1808-sketchbook-attribution](https://generativehistory.substack.com/p/gpt-62-astra-solves-a-historical)): "My intuition suggests this is a product of a post-training regime aimed at optimizing the model towards deterministic tasks like creating mathematical proofs."

Note: Causal interpretation across models, not a controlled training result.

```python
def check(ctx):
    return ctx.need('gpt62', ctx.find('gpt62', r'My intuition suggests.*post-training regime'), 'Causal interpretation across models, not a controlled training result.')
```

### NEEDS-HUMAN · e13-built-for-search (qualifier, Discovery vs. reliability)
> Claim: built for problems where you only need one hit out of many tries and an outside check discards the misses

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "We can design far more proteins on a computer than we can make and test in the lab."

Note: “Built for” one-hit discovery with an outside check is an interpretation of training and workflow, not a stated design goal.

```python
def check(ctx):
    return ctx.need('openai', ctx.find('openai', r'We can design far more proteins on a computer than we can make and test'), '“Built for” one-hit discovery with an outside check is an interpretation of training and workflow, not a stated design goal.')
```

### NEEDS-HUMAN · e14-training-limits (qualifier, Discovery vs. reliability)
> Claim: What that training has not delivered is everyday reliability: getting routine steps right every single time, or weighing messy real-world evidence without a formal proof

Source ([primary-gpt62-astra-1808-sketchbook-attribution](https://generativehistory.substack.com/p/gpt-62-astra-solves-a-historical)): "My sense is that GPT-6.2 Astra's prose gets weird when it must communicate a final result based on incomplete evidence, or when there is no way of completing a task but it must still provide an answer."

Note: HFE tests routine consistency; the training explanation for handling historical evidence is a historian’s conjecture.

```python
def check(ctx):
    return ctx.need('gpt62', ctx.find('gpt62', r'My sense is that GPT-6\.2 Astra.s prose gets weird.*incomplete evidence'), 'HFE tests routine consistency; the training explanation for handling historical evidence is a historian’s conjecture.')
```

### NEEDS-HUMAN · e15-kaggle-launch (attribution, Humanity's First Exam)
> Claim: Google DeepMind put hard numbers on that gap today, launching Humanity's First Exam on Google-owned Kaggle

Note: no source sentence matches /Top five models reach 96%–98% pass@1.*85\.6% on family pass\^4/. Today refers to the announcement; the measured gap is between coverage and consistency.

```python
def check(ctx):
    return ctx.require('kaggle', r'Today, @GoogleDeepMind is launching Humanity.s First Exam on Kaggle.*floor reliability', r'Kaggle is owned by Google', r'Top five models reach 96%–98% pass@1.*85\.6% on family pass\^4', note='Today refers to the announcement; the measured gap is between coverage and consistency.')
```

### NEEDS-HUMAN · e22-stark-drop (opinion, Humanity's First Exam)
> Claim: The drop-off is stark

Note: Stark is an assessment of the measured difference.

```python
def check(ctx):
    return ctx.need('kaggle', ctx.find('kaggle', r'Top five models reach 96%–98% pass@1.*85\.6%'), 'Stark is an assessment of the measured difference.')
```

### NEEDS-HUMAN · e23-single-try-range (number, Humanity's First Exam)
> Claim: The top five models score 96 to 98 percent on a single try

Note: no source sentence matches /Top five models reach 96%–98% pass@1/. 

```python
def check(ctx):
    return ctx.require('kaggle', r'Top five models reach 96%–98% pass@1')
```

### NEEDS-HUMAN · e46-discovery-game (opinion, Protein design)
> Claim: protein design is a discovery game

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "We can design far more proteins on a computer than we can make and test in the lab."

Note: Editorial analogy.

```python
def check(ctx):
    return ctx.need('openai', ctx.find('openai', r'We can design far more proteins on a computer than we can make and test'), 'Editorial analogy.')
```

### NEEDS-HUMAN · e47-breakthrough (opinion, Protein design)
> Claim: An 11 percent hit rate is a genuine breakthrough when specialized biology models filter out weak candidates upfront and a wet lab tests the winners

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "The original RFdiffusion study⁠(opens in a new window) reported higher hit rates, but rates depend heavily on how strictly researchers filter designs before lab validation and their definition of binding."

Note: The rate is measured; breakthrough is a judgment and comparisons depend on filtering.

```python
def check(ctx):
    return ctx.need('openai', ctx.find('openai', r'reported higher hit rates, but rates depend heavily on how strictly researchers filter designs'), 'The rate is measured; breakthrough is a judgment and comparisons depend on filtering.')
```

### NEEDS-HUMAN · e52-outside-science (comparison, Chabot sketchbook)
> Claim: The same split appears outside science

Source ([primary-gpt62-astra-1808-sketchbook-attribution](https://generativehistory.substack.com/p/gpt-62-astra-solves-a-historical)): "Nevertheless, GPT-6.2 Astra still had a strange tendency to shy away from its own accomplishments, which also reveals the limitations of current systems on non-deterministic tasks."

Note: Whether historical hedging illustrates the same phenomenon as benchmark inconsistency is interpretive.

```python
def check(ctx):
    return ctx.need('gpt62', ctx.find('gpt62', r'Astra still had a strange tendency to shy away from its own accomplishments'), 'Whether historical hedging illustrates the same phenomenon as benchmark inconsistency is interpretive.')
```

### NEEDS-HUMAN · e69-external-verification (opinion, Discovery vs. reliability)
> Claim: Frontier reasoners are extraordinary discovery machines when you can verify externally

Source ([primary-gpt62-astra-1808-sketchbook-attribution](https://generativehistory.substack.com/p/gpt-62-astra-solves-a-historical)): "To do so, it discovered a little known source in a paper archive, predicted that it would prove its hypothesis if examined and, in the end, it did."

Note: Generalization and value judgment from individual examples.

```python
def check(ctx):
    return ctx.need('gpt62', ctx.find('gpt62', r'it discovered a little known source in a paper archive'), 'Generalization and value judgment from individual examples.')
```

### NEEDS-HUMAN · e70-team-edge (opinion, Discovery vs. reliability)
> Claim: Until reliability catches up with brilliance, the real edge belongs to teams who know which game they are playing

Note: Editorial advice; no team-performance comparison is reported.

```python
def check(ctx):
    return ctx.need(None, None, 'Editorial advice; no team-performance comparison is reported.')
```

### PASS · e04-attribution-time (number, Chabot sketchbook)
> Claim: in twenty-two minutes

Source ([primary-gpt62-astra-1808-sketchbook-attribution](https://generativehistory.substack.com/p/gpt-62-astra-solves-a-historical)): "Only 22 minutes and 1 second later, it came back with a remarkably clear and decisive answer: "Louis-Guy-Charles-Guillaume de Rohan-Chabot, vicomte de Chabot (1780-1875), probably made the travel drawings." Moreover, it suggested that we should test the hypothesis by ordering copies of a microfilmed diary of Chabot's trip it had found in an archival inventory, which was held in the Special Collections of Cleveland State University."

Note: Rounded time to the proposed identification, not to archival verification.

```python
def check(ctx):
    return ctx.require('gpt62', r'Only 22 minutes and 1 second later.*vicomte de Chabot', note='Rounded time to the proposed identification, not to archival verification.')
```

### PASS · e05-story-count (number, Discovery vs. reliability)
> Claim: today's three biggest AI stories

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "STORY: OpenAI says GPT-6 models can design proteins with reasoning and code, with 35 of 322 lab-tested minibinders showing binding … STORY: A historian says GPT-6.2 Astra identified the anonymous artist of a Yale 1808 sketchbook and pointed him to an unknown diary … STORY: Google DeepMind's Humanity's First Exam measures whether frontier models get simple tasks right every time"

Note: Checks the three distinct selected stories only; importance is a separate judgment.

```python
def check(ctx):
    return ctx.require('framing', r'STORY: OpenAI says', r'STORY: A historian says', r'STORY: Google DeepMind', note='Checks the three distinct selected stories only; importance is a separate judgment.')
```

### PASS · e07-openai-preprint (attribution, Protein design)
> Claim: a protein-design preprint from OpenAI

Source ([x-openai](https://x.com/OpenAI/status/2125334383490105601)): "@OpenAI: We're sharing a new preprint showing wet lab validation of intrinsic protein design capabilities of the GPT-6 family of models."

```python
def check(ctx):
    return ctx.require('openai2', r'@OpenAI: We.re sharing a new preprint showing wet lab validation of intrinsic protein design capabilities')
```

### PASS · e09-benchmark-origin (attribution, Humanity's First Exam)
> Claim: a new reliability benchmark from Google DeepMind

Source ([x-kaggle](https://x.com/kaggle/status/2125313430303244739)): "Today, @GoogleDeepMind is launching Humanity's First Exam on Kaggle, a benchmark designed to measure "floor reliability": whether models get simple tasks right every time, not just once."

```python
def check(ctx):
    return ctx.require('kaggle', r'@GoogleDeepMind is launching Humanity.s First Exam on Kaggle, a benchmark designed to measure .floor reliability')
```

### PASS · e16-kaggle-owner (attribution, Humanity's First Exam)
> Claim: Google-owned Kaggle

Source ([x-kaggle](https://x.com/kaggle/status/2125313430303244739)): "AFFILIATION NOTE (scan): Kaggle is owned by Google; this is the benchmark creator's own announcement, not independent evaluation."

```python
def check(ctx):
    return ctx.require('kaggle', r'Kaggle is owned by Google')
```

### PASS · e19-task-examples (qualifier, Humanity's First Exam)
> Claim: like counting objects, tracking arrows, or spotting a false premise

Source ([primary-deepmind-humanitys-first-exam-floor-reli](https://www.kaggle.com/benchmarks/deepmind/hfe/leaderboard)): "Humanity's First Exam (HFE) evaluates whether frontier language and multimodal models can consistently solve elementary tasks that humans complete without specialized training: visual object counting, color and symbol identification, spatial tracking, basic arithmetic, strict formatting constraints, and false-premise verification. … Raising effort from low to high in the paper's ablations lifts Family pass⁴ by 17 to 32 percentage points on several reasoning models (and disabling thinking on Flash models drops Family pass⁴ below 10%), concentrated in symbolic text subcategories (+26.2 to +29.7 percentage points mean lift on Logical Deduction, Algorithmic and Symbolic Execution, and Constraint Satisfaction) vs. small gains on core Vision (+2.0 percentage points on Arrows/Pointers and +1.9 percentage points on Object Counting)."

```python
def check(ctx):
    return ctx.require('deepmind', r'visual object counting.*false-premise verification', r'Arrows/Pointers')
```

### PASS · e20-floor-definition (qualifier, Humanity's First Exam)
> Claim: it measures floor reliability, asking whether a model solves four slightly varied versions of a task consistently across repeated tries

Source ([primary-deepmind-humanitys-first-exam-floor-reli](https://www.kaggle.com/benchmarks/deepmind/hfe/leaderboard)): "HFE inverts this design, measuring whether a model solves a routine task every time across repeated draws and controlled prompt variations (Family pass⁴). … To separate underlying capability from lucky surface phrasing or sampling, each four-prompt family pairs one seed prompt with three controlled variants that rename entities, reorder clauses, or alter visual layout and attributes while preserving the isolated sub-ability and task logic (ground-truth answers vary across variants so memorized guesses do not transfer)."

```python
def check(ctx):
    return ctx.require('deepmind', r'routine task every time across repeated draws and controlled prompt variations', r'each four-prompt family pairs one seed prompt with three controlled variants')
```

### PASS · e21-four-versions (number, Humanity's First Exam)
> Claim: four slightly varied versions of a task

Source ([primary-deepmind-humanitys-first-exam-floor-reli](https://www.kaggle.com/benchmarks/deepmind/hfe/leaderboard)): "To separate underlying capability from lucky surface phrasing or sampling, each four-prompt family pairs one seed prompt with three controlled variants that rename entities, reorder clauses, or alter visual layout and attributes while preserving the isolated sub-ability and task logic (ground-truth answers vary across variants so memorized guesses do not transfer)."

```python
def check(ctx):
    return ctx.require('deepmind', r'each four-prompt family pairs one seed prompt with three controlled variants')
```

### PASS · e25-consistency-average (number, Humanity's First Exam)
> Claim: average under 86 percent when consistency is required

Source ([x-kaggle](https://x.com/kaggle/status/2125313430303244739)): "• High single-shot accuracy masks inconsistency: Top five models reach 96%-98% pass@1 and 100% family pass@4, yet average only 85.6% on family pass^4 (80.5%-92.4%), with a 7.6-80.1 percentage-point Family Reliability Gap across all 18 models."

```python
def check(ctx):
    return ctx.require('kaggle', r'Top five models reach.*yet average only 85\.6% on family pass\^4')
```

### PASS · e26-leader (number, Humanity's First Exam)
> Claim: OpenAI's GPT-6.2 Astra leads Kaggle's initial run near 91 percent

Source ([x-kaggle](https://x.com/kaggle/status/2125313430303244739)): "Current leaderboard: … 🥇 GPT- 6.2 Astra (xhigh) - 90.7%"

```python
def check(ctx):
    return ctx.require('kaggle', r'Current leaderboard:', r'🥇\s*GPT-\s*6\.2 Astra \(xhigh\) - 90\.7%')
```

### PASS · e27-interval-overlap (qualifier, Humanity's First Exam)
> Claim: within overlapping error bars

Source ([primary-deepmind-humanitys-first-exam-floor-reli](https://www.kaggle.com/benchmarks/deepmind/hfe/leaderboard)): "90.7% | ±4.7% | 85.6% | ±5.7%"

Note: Board rows 1 and 3: [86.0,95.4] and [79.9,91.3] overlap.

```python
def check(ctx):
    rows = [ctx.find('deepmind', p) for p in (r'\b90\.7%', r'±4\.7%', r'\b85\.6%', r'±5\.7%')]
    if not all(rows): return ctx.need('deepmind', None, 'Check Astra and Neon rows and their intervals.')
    return ctx.ok('deepmind', ' | '.join(rows), 'Board rows 1 and 3: [86.0,95.4] and [79.9,91.3] overlap.')
```

### PASS · e28-effort-settings (comparison, Humanity's First Exam)
> Claim: at a higher reasoning setting than Google's Gemini 4 Neon

Source ([x-kaggle](https://x.com/kaggle/status/2125313430303244739)): "🥇 GPT- 6.2 Astra (xhigh) - 90.7% … 🥉 Gemini 4 Neon (high) - 85.6%"

Note: Comparison of setting labels in this run, not calibrated compute.

```python
def check(ctx):
    return ctx.require('kaggle', r'🥇\s*GPT-\s*6\.2 Astra \(xhigh\)', r'🥉\s*Gemini 4 Neon \(high\)', note='Comparison of setting labels in this run, not calibrated compute.')
```

### PASS · e29-failure-audit (attribution, Humanity's First Exam)
> Claim: The failure logs explain why

Source ([primary-deepmind-humanitys-first-exam-floor-reli](https://www.kaggle.com/benchmarks/deepmind/hfe/leaderboard)): "In the paper's audit of 58,752 rollouts (5,823 failed rollouts, including 5,552 wrong answers), 95% of failures were wrong answers, 3% were safety refusals, 2% were output-limit truncations, and 0.1% were harness errors. … - Visual perception errors (73% of wrong rollouts): Misjudging spatial position, direction, or path in an image (31%) and miscounting distinct objects (23%)."

Note: Audit attributes errors to categories, not to a causal mechanism in training.

```python
def check(ctx):
    return ctx.require('deepmind', r'paper.s audit of 58,752 rollouts.*5,552 wrong answers', r'Visual perception errors \(73% of wrong rollouts\)', note='Audit attributes errors to categories, not to a causal mechanism in training.')
```

### PASS · e30-visual-wrong-answers (number, Humanity's First Exam)
> Claim: Nearly three-quarters of wrong answers are basic visual perception mistakes

Source ([x-kaggle](https://x.com/kaggle/status/2125313430303244739)): "• Visual perception drives 74% of wrong answers: Extra thinking time helps far less on visual tasks than on text."

```python
def check(ctx):
    return ctx.require('kaggle', r'Visual perception drives 74% of wrong answers')
```

### PASS · e31-symbolic-lift (number, Humanity's First Exam)
> Claim: Cranking up reasoning effort lifts symbolic logic by nearly 30 percentage points

Source ([primary-deepmind-humanitys-first-exam-floor-reli](https://www.kaggle.com/benchmarks/deepmind/hfe/leaderboard)): "Raising effort from low to high in the paper's ablations lifts Family pass⁴ by 17 to 32 percentage points on several reasoning models (and disabling thinking on Flash models drops Family pass⁴ below 10%), concentrated in symbolic text subcategories (+26.2 to +29.7 percentage points mean lift on Logical Deduction, Algorithmic and Symbolic Execution, and Constraint Satisfaction) vs. small gains on core Vision (+2.0 percentage points on Arrows/Pointers and +1.9 percentage points on Object Counting)."

Note: Approximation for selected symbolic subcategories, not all reasoning.

```python
def check(ctx):
    return ctx.require('deepmind', r'Raising effort from low to high.*symbolic text subcategories \(\+26\.2 to \+29\.7 percentage points mean lift on Logical Deduction', note='Approximation for selected symbolic subcategories, not all reasoning.')
```

### PASS · e32-counting-arrow-lift (number, Humanity's First Exam)
> Claim: improves object counting and arrow tracking by barely 2 points

Source ([primary-deepmind-humanitys-first-exam-floor-reli](https://www.kaggle.com/benchmarks/deepmind/hfe/leaderboard)): "Raising effort from low to high in the paper's ablations lifts Family pass⁴ by 17 to 32 percentage points on several reasoning models (and disabling thinking on Flash models drops Family pass⁴ below 10%), concentrated in symbolic text subcategories (+26.2 to +29.7 percentage points mean lift on Logical Deduction, Algorithmic and Symbolic Execution, and Constraint Satisfaction) vs. small gains on core Vision (+2.0 percentage points on Arrows/Pointers and +1.9 percentage points on Object Counting)."

```python
def check(ctx):
    return ctx.require('deepmind', r'\+2\.0 percentage points on Arrows/Pointers and \+1\.9 percentage points on Object Counting')
```

### PASS · e33-difficulty-inversion (comparison, Humanity's First Exam)
> Claim: Human and AI difficulty are literally inverted: people handle vision easily and trip over formal logic, while models do the reverse

Source ([primary-deepmind-humanitys-first-exam-floor-reli](https://www.kaggle.com/benchmarks/deepmind/hfe/leaderboard)): "Across subcategories, human seed accuracy (80.3% across 315 candidate seeds prior to 3/4 filtering) negatively correlates with model pass@1 (Spearman ρ = -0.64): humans score highest on Vision (84%) and lowest among macro-categories on Math & Algorithmic (76%) and Reasoning & Language (77%), and lowest at the subcategory level on Logical Deduction (59.4%), whereas models invert that order."

```python
def check(ctx):
    return ctx.require('deepmind', r'humans score highest on Vision \(84%\).*lowest at the subcategory level on Logical Deduction \(59\.4%\), whereas models invert that order')
```

### PASS · e35-shapes-sequences (attribution, Protein design)
> Claim: OpenAI reports that its GPT-6 models can design protein shapes and sequences

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "Our GPT-6 family of models can design new protein shapes and the sequence of their chemical building blocks using only reasoning and code, without calling specialized biology models to generate those designs."

```python
def check(ctx):
    return ctx.require('openai', r'Our GPT.6 family of models can design new protein shapes and the sequence of their chemical building blocks')
```

### PASS · e36-reasoning-code (qualifier, Protein design)
> Claim: using only reasoning and code

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "Our GPT-6 family of models can design new protein shapes and the sequence of their chemical building blocks using only reasoning and code, without calling specialized biology models to generate those designs."

```python
def check(ctx):
    return ctx.require('openai', r'design new protein shapes.*using only reasoning and code')
```

### PASS · e37-generation-only (qualifier, Protein design)
> Claim: without calling specialized biology models during generation

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "Our GPT-6 family of models can design new protein shapes and the sequence of their chemical building blocks using only reasoning and code, without calling specialized biology models to generate those designs."

```python
def check(ctx):
    return ctx.require('openai', r'without calling specialized biology models to generate those designs')
```

### PASS · e38-onava (attribution, Protein design)
> Claim: lab partner Onava

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "With our research partner, Onava⁠(opens in a new window), we also tested the models' structure and sequence designs in the lab."

```python
def check(ctx):
    return ctx.require('openai', r'our research partner, Onava.*tested the models. structure and sequence designs in the lab')
```

### PASS · e39-binder-count (number, Protein design)
> Claim: 35 of 322 small protein binders based on GPT-6.2's shapes bound to their targets

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "For the lab experiment, we made proteins based on GPT-6.2's designs and measured how strongly they bound to their targets. … We tested 322 minibinders against 5 targets in the lab. … Of those, 35 (10.9%) tested positive for binding to their intended target."

```python
def check(ctx):
    return ctx.require('openai', r'we made proteins based on GPT.6\.2.s designs and measured how strongly they bound', r'We tested 322 minibinders against 5 targets in the lab', r'Of those, 35 \(10\.9%\) tested positive for binding to their intended target')
```

### PASS · e40-hit-rate (number, Protein design)
> Claim: an 11 percent hit rate

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "Of those, 35 (10.9%) tested positive for binding to their intended target."

Note: 10.9% rounds to 11%.

```python
def check(ctx):
    return ctx.require('openai', r'35 \(10\.9%\) tested positive for binding', note='10.9% rounds to 11%.')
```

### PASS · e41-second-experiment (number, Protein design)
> Claim: In a second lab run

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "Laboratory Experiment 2: Designing new sequences for 3D protein structures … We tested whether GPT-6.2 could design the sequences itself."

```python
def check(ctx):
    return ctx.require('openai', r'Laboratory Experiment 2: Designing new sequences for 3D protein structures', r'We tested whether GPT.6\.2 could design the sequences itself')
```

### PASS · e42-unpublished-shapes (attribution, Protein design)
> Claim: GPT-6.2 also wrote working sequences itself for unpublished shapes it had generated

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "We also asked GPT-6.2 to design new sequences for three unpublished minibinder shapes it had generated earlier: two targeting PD-L1 and one targeting IL-7Rα. … Of the 107 proteins made from GPT-6.2's new sequences, 14 (13.1%) showed binding."

```python
def check(ctx):
    return ctx.require('openai', r'GPT.6\.2 to design new sequences for three unpublished minibinder shapes it had generated earlier', r'Of the 107 proteins made from GPT.6\.2.s new sequences, 14 \(13\.1%\) showed binding')
```

### PASS · e43-memorization (qualifier, Protein design)
> Claim: suggesting this goes beyond memorization

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "The unpublished structures and substantial differences in sequence give us strong evidence that GPT-6.2's capabilities extend beyond memorization."

```python
def check(ctx):
    return ctx.require('openai', r'unpublished structures and substantial differences in sequence give us strong evidence that GPT.6\.2.s capabilities extend beyond memorization')
```

### PASS · e44-review-status (qualifier, Protein design)
> Claim: OpenAI's own unreviewed preprint

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "framing (OpenAI): Company-reported preprint with lab tests run by its research partner Onava; no independent replication."

Note: Preprint status of the reported version; not an independent reviewed result.

```python
def check(ctx):
    return ctx.require('framing', r'framing \(OpenAI\): Company-reported preprint', note='Preprint status of the reported version; not an independent reviewed result.')
```

### PASS · e45-binding-not-medicine (comparison, Protein design)
> Claim: early lab binding is far from a working medicine

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "The laboratory results provide a more direct test of whether proposed designs can work, but binding is only one step toward a useful research tool or medicine. … Further work would need to establish properties such as specificity, stability, and biological activity, along with safety and efficacy for therapeutic applications."

```python
def check(ctx):
    return ctx.require('openai', r'binding is only one step toward a useful research tool or medicine', r'Further work would need to establish.*safety and efficacy for therapeutic applications')
```

### PASS · e48-candidate-selection (qualifier, Protein design)
> Claim: when specialized biology models filter out weak candidates upfront and a wet lab tests the winners

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "It is important to note that our protein design campaign relied on specialized structure prediction models such as Boltz-2, OpenDDE, and ESMFold2 to filter candidates. … Specialized models then proposed amino acid sequences-the order of the proteins' chemical building blocks-and helped select designs for our research partner Onava to make and test in the lab."

Note: Winners of selection, not known binding positives before testing.

```python
def check(ctx):
    return ctx.require('openai', r'specialized structure prediction models.*to filter candidates', r'Specialized models then proposed amino acid sequences.*helped select designs for our research partner Onava to make and test in the lab', note='Winners of selection, not known binding positives before testing.')
```

### PASS · e49-folding-task (qualifier, Protein design)
> Claim: predict how a whole protein folds from its sequence alone

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "The specialized model ESMFold2 averaged 0.93, so there's still a substantial gap in how reliably our models can predict a whole protein's structure from its sequence alone."

```python
def check(ctx):
    return ctx.require('openai', r'predict a whole protein.s structure from its sequence alone')
```

### PASS · e50-internal-score (number, Protein design)
> Claim: OpenAI's latest internal model scores under 0.4 on a one-point scale

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "Across the full test, the average score rose from 0.16 for GPT-5.6 to 0.26 for GPT-6.2 and 0.38 for our latest internal model. … A score of 1 means a perfect match to the real structure, and scores above 0.5 generally indicate that the prediction captures the overall fold."

```python
def check(ctx):
    return ctx.require('openai', r'average score rose from.*0\.38 for our latest internal model', r'A score of 1 means a perfect match to the real structure')
```

### PASS · e51-esmfold-comparison (comparison, Protein design)
> Claim: compared with 0.93 for the specialist model ESMFold2

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "Across the full test, the average score rose from 0.16 for GPT-5.6 to 0.26 for GPT-6.2 and 0.38 for our latest internal model. … The specialized model ESMFold2 averaged 0.93, so there's still a substantial gap in how reliably our models can predict a whole protein's structure from its sequence alone."

```python
def check(ctx):
    return ctx.require('openai', r'0\.38 for our latest internal model', r'The specialized model ESMFold2 averaged 0\.93')
```

### PASS · e53-blog-status (qualifier, Chabot sketchbook)
> Claim: a Substack post not yet peer-reviewed or publicly audited

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "framing (Generative History (Mark Humphries)): Single historian's first-person account; he tested the model before release. … The attribution rests on archival documents he obtained; no independent historian review is reported yet."

Note: No reported independent review; this is not a search for every possible private review.

```python
def check(ctx):
    return ctx.require('framing', r'Single historian.s first-person account', r'no independent historian review is reported yet', note='No reported independent review; this is not a search for every possible private review.') if ctx.find('gpt62', r'Substack is the home for writing') else ctx.need('gpt62', None, 'Verify publication venue.')
```

### PASS · e54-humphries-test (attribution, Chabot sketchbook)
> Claim: historian Mark Humphries describes giving GPT-6.2 Astra an anonymous 1808 sketchbook from Yale's Beinecke Library

Source ([primary-gpt62-astra-1808-sketchbook-attribution](https://generativehistory.substack.com/p/gpt-62-astra-solves-a-historical)): "With only minimal prompting, GPT-6.2 Astra was able to autonomously identify the creator of an anonymous 1808 sketchbook held at Yale's Beinecke Library. … One morning, early on in my testing, I gave GPT-6.2 Astra access to the images of the sketchbook and, in retrospect, a throwaway prompt:"

```python
def check(ctx):
    if not ctx.find('emollick', r'Historian Mark Humphries asked GPT-6\.2 Astra to look at an anonymous 1808 sketchbook at Yale'): return ctx.need('emollick', None, 'Verify attribution.')
    return ctx.require('gpt62', r'GPT-6\.2 Astra.*anonymous 1808 sketchbook held at Yale.s Beinecke Library', r'I gave GPT-6\.2 Astra access to the images of the sketchbook')
```

### PASS · e55-sketchbook-year (number, Chabot sketchbook)
> Claim: an anonymous 1808 sketchbook

Source ([primary-gpt62-astra-1808-sketchbook-attribution](https://generativehistory.substack.com/p/gpt-62-astra-solves-a-historical)): "With only minimal prompting, GPT-6.2 Astra was able to autonomously identify the creator of an anonymous 1808 sketchbook held at Yale's Beinecke Library."

```python
def check(ctx):
    return ctx.require('gpt62', r'an anonymous 1808 sketchbook held at Yale.s Beinecke Library')
```

### PASS · e58-thesis-year (number, Chabot sketchbook)
> Claim: a 2014 thesis footnote

Source ([primary-gpt62-astra-1808-sketchbook-attribution](https://generativehistory.substack.com/p/gpt-62-astra-solves-a-historical)): "How GPT-6.2 Astra actually learned about it remains a bit unclear, but it traced its finding to a single footnote in a 2014 PhD thesis on aristocratic refugee families fleeing the French Revolution, written by historian Juliette Reboul.2 Again, not somewhere a human historian of the fur trade would tend to look."

```python
def check(ctx):
    return ctx.require('gpt62', r'a single footnote in a 2014 PhD thesis')
```

### PASS · e59-microfilm-lead (attribution, Chabot sketchbook)
> Claim: pointed Humphries to an unknown microfilmed diary at Cleveland State University

Source ([primary-gpt62-astra-1808-sketchbook-attribution](https://generativehistory.substack.com/p/gpt-62-astra-solves-a-historical)): "Only 22 minutes and 1 second later, it came back with a remarkably clear and decisive answer: "Louis-Guy-Charles-Guillaume de Rohan-Chabot, vicomte de Chabot (1780-1875), probably made the travel drawings." Moreover, it suggested that we should test the hypothesis by ordering copies of a microfilmed diary of Chabot's trip it had found in an archival inventory, which was held in the Special Collections of Cleveland State University. … The identification of Count Chabot as the creator of the Yale sketchbook and the recovery of his largely unknown diary will be of real interest to historians of both Canada and the fur trade."

Note: Unknown to the historian/largely unknown, not previously uncatalogued.

```python
def check(ctx):
    return ctx.require('gpt62', r'it suggested.*microfilmed diary of Chabot.s trip.*Special Collections of Cleveland State University', r'recovery of his largely unknown diary', note='Unknown to the historian/largely unknown, not previously uncatalogued.')
```

### PASS · e61-fable-missed-diary (qualifier, Chabot sketchbook)
> Claim: though it missed the diary

Source ([primary-gpt62-astra-1808-sketchbook-attribution](https://generativehistory.substack.com/p/gpt-62-astra-solves-a-historical)): "Nevertheless, it fell a bit short of Astra's overall accomplishment: Fable failed to identify Chabot's journal, which turned out to be the most important piece of evidence for the sketchbook and a significant find on its own."

```python
def check(ctx):
    return ctx.require('gpt62', r'Fable failed to identify Chabot.s journal')
```

### PASS · e62-ordered-scans (attribution, Chabot sketchbook)
> Claim: Humphries ordered the scans

Source ([primary-gpt62-astra-1808-sketchbook-attribution](https://generativehistory.substack.com/p/gpt-62-astra-solves-a-historical)): "But order the journal I did. … After some back and forth with both archives, all three documents arrived in my inbox."

```python
def check(ctx):
    return ctx.require('gpt62', r'But order the journal I did', r'all three documents arrived in my inbox')
```

### PASS · e63-handwriting (attribution, Chabot sketchbook)
> Claim: matched the handwriting

Source ([primary-gpt62-astra-1808-sketchbook-attribution](https://generativehistory.substack.com/p/gpt-62-astra-solves-a-historical)): "The first thing I saw was the handwriting, which featured the same distinctive letter forms as the sketchbook."

```python
def check(ctx):
    return ctx.require('gpt62', r'handwriting, which featured the same distinctive letter forms as the sketchbook')
```

### PASS · e64-fort-sketch (attribution, Chabot sketchbook)
> Claim: found Chabot writing that he took a sketch of Fort St. Joseph

Source ([primary-gpt62-astra-1808-sketchbook-attribution](https://generativehistory.substack.com/p/gpt-62-astra-solves-a-historical)): "Joseph, he wrote "I took a sketch" before describing the exact view of the fort depicted in the matching drawing. … Chabot's entry for 18 June 1808, pp."

```python
def check(ctx):
    return ctx.require('gpt62', r'(?:after Chabot.s canoe reached Fort St\. Joseph, he wrote .I took a sketch|he wrote .I took a sketch. before describing the exact view of the fort)', r'Chabot.s entry for 18 June 1808')
```

### PASS · e65-returned-diary (attribution, Chabot sketchbook)
> Claim: Humphries gave that proof back to Astra

Source ([primary-gpt62-astra-1808-sketchbook-attribution](https://generativehistory.substack.com/p/gpt-62-astra-solves-a-historical)): "When given a copy of the diary, which proved the case beyond any shadow of a reasonable doubt, Astra started to hedge as it had done at the end of other long tasks: it worried that because the diary was not signed, it might not be Chabot's or that because not every sketch was mentioned in the diary, perhaps not all of them were his."

```python
def check(ctx):
    return ctx.require('gpt62', r'When given a copy of the diary, which proved the case.*Astra started to hedge')
```

### PASS · e66-hedging (attribution, Chabot sketchbook)
> Claim: the model strangely hedged and doubted its own find because the diary was unsigned

Source ([primary-gpt62-astra-1808-sketchbook-attribution](https://generativehistory.substack.com/p/gpt-62-astra-solves-a-historical)): "When given a copy of the diary, which proved the case beyond any shadow of a reasonable doubt, Astra started to hedge as it had done at the end of other long tasks: it worried that because the diary was not signed, it might not be Chabot's or that because not every sketch was mentioned in the diary, perhaps not all of them were his."

```python
def check(ctx):
    return ctx.require('gpt62', r'Astra started to hedge.*because the diary was not signed, it might not be Chabot.s')
```

### PASS · e67-unsigned (qualifier, Chabot sketchbook)
> Claim: the diary was unsigned

Source ([primary-gpt62-astra-1808-sketchbook-attribution](https://generativehistory.substack.com/p/gpt-62-astra-solves-a-historical)): "When given a copy of the diary, which proved the case beyond any shadow of a reasonable doubt, Astra started to hedge as it had done at the end of other long tasks: it worried that because the diary was not signed, it might not be Chabot's or that because not every sketch was mentioned in the diary, perhaps not all of them were his."

```python
def check(ctx):
    return ctx.require('gpt62', r'because the diary was not signed')
```

### PASS · e68-training-conjecture (attribution, Chabot sketchbook)
> Claim: Humphries suspects math-heavy post-training leaves it awkward whenever evidence falls short of a formal proof

Source ([primary-gpt62-astra-1808-sketchbook-attribution](https://generativehistory.substack.com/p/gpt-62-astra-solves-a-historical)): "My intuition suggests this is a product of a post-training regime aimed at optimizing the model towards deterministic tasks like creating mathematical proofs. … My sense is that GPT-6.2 Astra's prose gets weird when it must communicate a final result based on incomplete evidence, or when there is no way of completing a task but it must still provide an answer."

Note: Attributed hypothesis, not an established training effect.

```python
def check(ctx):
    return ctx.require('gpt62', r'My intuition suggests.*post-training regime.*mathematical proofs', r'My sense is that GPT-6\.2 Astra.s prose gets weird when it must communicate a final result based on incomplete evidence', note='Attributed hypothesis, not an established training effect.')
```

### PASS · oe1-company-report (objection, Protein design)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "framing (OpenAI): Company-reported preprint with lab tests run by its research partner Onava; no independent replication."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'Company-reported preprint')
    return ctx.ok('framing', q) if ctx.art_has(r'OpenAI (?:itself )?(?:reports|says)|OpenAI.s own.{0,24}preprint|company-reported.{0,24}(?:protein|preprint)') else ctx.fail('framing', q, 'Attribute the protein results to OpenAI itself.')
```

### PASS · oe10-historian-review (objection, Chabot sketchbook)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "The attribution rests on archival documents he obtained; no independent historian review is reported yet."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'no independent historian review is reported yet')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:Substack|attribution|sketchbook|historian.s account).{0,60}(?:not yet peer[- ]reviewed|not (?:yet )?independently (?:checked|reviewed)|no independent (?:historian )?review)|no independent historian review') else ctx.fail('framing', q, 'Disclose lack of reported independent review of the attribution.')
```

### PASS · oe2-preprint (objection, Protein design)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "framing (OpenAI): Company-reported preprint with lab tests run by its research partner Onava; no independent replication."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'Company-reported preprint')
    return ctx.ok('framing', q) if ctx.art_has(r'(?i)(?:protein.design|OpenAI).{0,48}preprint|preprint.{0,32}OpenAI') else ctx.fail('framing', q, 'Identify the protein report as a preprint.')
```

### PASS · oe3-partner-lab (objection, Protein design)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "framing (OpenAI): Company-reported preprint with lab tests run by its research partner Onava; no independent replication."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'lab tests run by its research partner Onava')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:lab|research) partner[, :]+Onava|Onava.{0,40}(?:partner|ran the lab tests)') else ctx.fail('framing', q, 'Name Onava as the partner conducting lab tests.')
```

### PASS · oe6-specialist-filter (objection, Protein design)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "OpenAI itself says specialized models still supplied sequences and filtered candidates."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'specialized models still supplied sequences and filtered candidates')
    return ctx.ok('framing', q) if ctx.art_has(r'speciali[sz](?:ed|t)(?: biology| protein)? models?.{0,90}(?:filter|select|screen|pick)\w*.{0,30}(?:candidates|designs)') else ctx.fail('framing', q, 'Mention specialist candidate filtering before lab tests.')
```

### PASS · oe7-historian-account (objection, Chabot sketchbook)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "framing (Generative History (Mark Humphries)): Single historian's first-person account; he tested the model before release."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'Single historian.s first-person account')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:historian Mark Humphries|Humphries).{0,36}(?:describes|reports|recounts|says|writes)|Humphries.s (?:own |first-person )?account') else ctx.fail('framing', q, 'Frame the attribution as the historian’s account.')
```

### PASS · oe9-archival-confirmation (objection, Chabot sketchbook)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "The attribution rests on archival documents he obtained; no independent historian review is reported yet."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'attribution rests on archival documents he obtained')
    carried = ctx.art_has(r'(?:Humphries|historian|he) (?:ordered|obtained|received).{0,40}(?:scans|diary|documents|journal)') and ctx.art_has(r'match(?:ed|ing).{0,20}handwriting|handwriting matched|took a sketch')
    return ctx.ok('framing', q) if carried else ctx.fail('framing', q, 'Identify the archival evidence the historian obtained and checked.')
```

## takeaways

### FAIL · ot10-benchmark-replication (objection, Humanity's First Exam)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "framing (Kaggle / Google DeepMind): Benchmark creator's own leaderboard and summary of its paper; answers are graded by a Google model; the leaderboard lists 16 models while the X post cites 18 from the paper."

Note: Disclose lack of independent benchmark replication.

```python
def check(ctx):
    q = ctx.find('framing', r'leaderboard lists 16 models')
    return ctx.ok('framing', q) if ctx.art_has(r'(?is)(?:benchmark|leaderboard|HFE|DeepMind).{0,160}(?:no independent replication|not (?:yet )?independently replicated)|(?:no independent replication|not independently replicated).{0,50}(?:benchmark|leaderboard|HFE)') else ctx.fail('framing', q, 'Disclose lack of independent benchmark replication.')
```

### FAIL · ot3-partner-lab (objection, GPT-6 protein binders)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "framing (OpenAI): Company-reported preprint with lab tests run by its research partner Onava; no independent replication."

Note: Identify Onava as the partner lab.

```python
def check(ctx):
    q = ctx.find('framing', r'lab tests run by its research partner Onava')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:lab|research) partner[, :]+Onava|Onava.{0,40}(?:partner|ran the lab tests)') else ctx.fail('framing', q, 'Identify Onava as the partner lab.')
```

### FAIL · ot4-protein-replication (objection, GPT-6 protein binders)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "framing (OpenAI): Company-reported preprint with lab tests run by its research partner Onava; no independent replication."

Note: Disclose no independent replication of binding results.

```python
def check(ctx):
    q = ctx.find('framing', r'Onava; no independent replication')
    return ctx.ok('framing', q) if ctx.art_has(r'(?is)(?:Onava|binder|protein|OpenAI reports).{0,200}(?:no independent replication|not (?:yet )?independently replicated|hasn.t been independently replicated)|(?:no independent replication|not independently replicated).{0,80}(?:protein|binder)') else ctx.fail('framing', q, 'Disclose no independent replication of binding results.')
```

### FAIL · ot5-specialist-sequences (objection, GPT-6 protein binders)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "OpenAI itself says specialized models still supplied sequences and filtered candidates."

Note: Mention specialist sequence supply, not only filtering.

```python
def check(ctx):
    q = ctx.find('framing', r'specialized models still supplied sequences')
    return ctx.ok('framing', q) if ctx.art_has(r'speciali[sz](?:ed|t)(?: biology| protein)? models?.{0,64}(?:supplied|proposed|provided|generated|designed|wrote).{0,24}sequences') else ctx.fail('framing', q, 'Mention specialist sequence supply, not only filtering.')
```

### FAIL · ot7-creator-results (objection, Humanity's First Exam)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "framing (Kaggle / Google DeepMind): Benchmark creator's own leaderboard and summary of its paper; answers are graded by a Google model; the leaderboard lists 16 models while the X post cites 18 from the paper."

Note: Clarify provenance of scores, not just benchmark ownership.

```python
def check(ctx):
    q = ctx.find('framing', r'Benchmark creator.s own leaderboard and summary of its paper')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:creator.s own|DeepMind.s own|Google.s own).{0,48}(?:leaderboard|results|paper)|(?:DeepMind|Kaggle).{0,35}(?:reports|summarizes|published).{0,32}(?:its own|its paper|its leaderboard)') else ctx.fail('framing', q, 'Clarify provenance of scores, not just benchmark ownership.')
```

### FAIL · ot8-google-grader (objection, Humanity's First Exam)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "framing (Kaggle / Google DeepMind): Benchmark creator's own leaderboard and summary of its paper; answers are graded by a Google model; the leaderboard lists 16 models while the X post cites 18 from the paper."

Note: Identify the Google grader.

```python
def check(ctx):
    q = ctx.find('framing', r'answers are graded by a Google model')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:graded|judged|scored).{0,30}(?:Google model|Gemini)|(?:Google model|Gemini).{0,30}(?:grades|judges|scores) (?:the )?(?:answers|responses)') else ctx.fail('framing', q, 'Identify the Google grader.')
```

### FAIL · ot9-two-cohorts (objection, Humanity's First Exam)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "framing (Kaggle / Google DeepMind): Benchmark creator's own leaderboard and summary of its paper; answers are graded by a Google model; the leaderboard lists 16 models while the X post cites 18 from the paper."

Note: Distinguish the leaderboard’s 16 from the paper’s 18.

```python
def check(ctx):
    q = ctx.find('framing', r'leaderboard lists 16 models while the X post cites 18 from the paper')
    board = ctx.art_has(r'(?:leaderboard|Kaggle run).{0,40}(?:16|sixteen) models|(?:16|sixteen)[- ]model leaderboard')
    paper = ctx.art_has(r'(?:paper|X post).{0,45}(?:18|eighteen)(?: models)?|(?:18|eighteen)[- ]model (?:paper|study)')
    return ctx.ok('framing', q) if board and paper else ctx.fail('framing', q, 'Distinguish the leaderboard’s 16 from the paper’s 18.')
```

### FAIL · t09-consistency-scope (qualifier, Humanity's First Exam)
> Claim: when required to be consistent across four variations

Source ([primary-deepmind-humanitys-first-exam-floor-reli](https://www.kaggle.com/benchmarks/deepmind/hfe/leaderboard)): "Across a four-prompt family f with correct counts across its four prompts, Family pass⁴ measures the unbiased joint probability that all 16 draws (4 per prompt across all 4 family members) succeed, averaged over all 136 families:"

Note: Family pass^4 is consistency across 16 draws (4 per prompt x 4 family members), not only across four variations.

```python
def check(ctx):
    return ctx.support_or_contradict('deepmind', r'Family pass⁴ measures the unbiased joint probability that all 4 (?:family members|variations|prompts) succeed(?: with one draw each)?', r'Family pass⁴ measures the unbiased joint probability that all 16 draws \(4 per prompt across all 4 family members\) succeed', 'Family pass^4 is consistency across 16 draws (4 per prompt x 4 family members), not only across four variations.')
```

### FAIL · t12-error-denominator (number, Humanity's First Exam)
> Claim: nearly three-quarters of errors coming from basic visual perception

Source ([primary-deepmind-humanitys-first-exam-floor-reli](https://www.kaggle.com/benchmarks/deepmind/hfe/leaderboard)): "- Visual perception errors (73% of wrong rollouts): Misjudging spatial position, direction, or path in an image (31%) and miscounting distinct objects (23%)."

Note: The measured denominator is wrong answers, not all errors including refusals, truncation and harness failures.

```python
def check(ctx):
    q = ctx.find('deepmind', r'Visual perception errors \(73% of wrong rollouts\)')
    return ctx.fail('deepmind', q, 'The measured denominator is wrong answers, not all errors including refusals, truncation and harness failures.') if q else ctx.need('deepmind', None, 'Verify denominator.')
```

### NEEDS-HUMAN · t04-top-five (number, Humanity's First Exam)
> Claim: the top five models

Note: no source sentence matches /Top five models reach 96%–98% pass@1/. 

```python
def check(ctx):
    return ctx.require('kaggle', r'Top five models reach 96%–98% pass@1')
```

### NEEDS-HUMAN · t05-single-range (number, Humanity's First Exam)
> Claim: score 96 to 98 percent

Note: no source sentence matches /Top five models reach 96%–98% pass@1/. 

```python
def check(ctx):
    return ctx.require('kaggle', r'Top five models reach 96%–98% pass@1')
```

### NEEDS-HUMAN · t06-single-try (number, Humanity's First Exam)
> Claim: on a single try

Note: no source sentence matches /High single-shot accuracy masks inconsistency: Top five models reach 96%–98% pass@1/. 

```python
def check(ctx):
    return ctx.require('kaggle', r'High single-shot accuracy masks inconsistency: Top five models reach 96%–98% pass@1')
```

### NEEDS-HUMAN · t11-combined-comparison (comparison, Humanity's First Exam)
> Claim: the top five models score 96 to 98 percent on a single try of simple tasks but average under 86 percent when required to be consistent across four variations

Note: no source sentence matches /Top five models reach 96%–98% pass@1 and 100% family pass@4, yet average only 85\.6% on family pass\^4/. 

```python
def check(ctx):
    return ctx.require('kaggle', r'Top five models reach 96%–98% pass@1 and 100% family pass@4, yet average only 85\.6% on family pass\^4', r'whether models get simple tasks right every time, not just once', r'in 136 four-prompt families')
```

### PASS · ot1-company-report (objection, GPT-6 protein binders)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "framing (OpenAI): Company-reported preprint with lab tests run by its research partner Onava; no independent replication."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'Company-reported preprint')
    return ctx.ok('framing', q) if ctx.art_has(r'OpenAI (?:itself )?(?:reports|says)|OpenAI.s own.{0,24}preprint|company-reported.{0,24}(?:protein|preprint)') else ctx.fail('framing', q, 'Attribute results to OpenAI.')
```

### PASS · ot2-preprint (objection, GPT-6 protein binders)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "framing (OpenAI): Company-reported preprint with lab tests run by its research partner Onava; no independent replication."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'Company-reported preprint')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:protein.design|OpenAI).{0,48}preprint|preprint.{0,32}OpenAI') else ctx.fail('framing', q, 'Identify the protein preprint.')
```

### PASS · ot6-specialist-filter (objection, GPT-6 protein binders)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "OpenAI itself says specialized models still supplied sequences and filtered candidates."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'specialized models still supplied sequences and filtered candidates')
    return ctx.ok('framing', q) if ctx.art_has(r'speciali[sz](?:ed|t)(?: biology| protein)? models?.{0,90}(?:filter|select|screen|pick)\w*.{0,30}(?:candidates|designs)') else ctx.fail('framing', q, 'Disclose specialist filtering.')
```

### PASS · t01-benchmark-creator (attribution, Humanity's First Exam)
> Claim: Google DeepMind's new Humanity's First Exam benchmark

Source ([x-kaggle](https://x.com/kaggle/status/2125313430303244739)): "Today, @GoogleDeepMind is launching Humanity's First Exam on Kaggle, a benchmark designed to measure "floor reliability": whether models get simple tasks right every time, not just once."

```python
def check(ctx):
    return ctx.require('kaggle', r'Today, @GoogleDeepMind is launching Humanity.s First Exam on Kaggle, a benchmark')
```

### PASS · t02-new-launch (qualifier, Humanity's First Exam)
> Claim: new

Source ([x-kaggle](https://x.com/kaggle/status/2125313430303244739)): "Today, @GoogleDeepMind is launching Humanity's First Exam on Kaggle, a benchmark designed to measure "floor reliability": whether models get simple tasks right every time, not just once."

```python
def check(ctx):
    return ctx.require('kaggle', r'Today, @GoogleDeepMind is launching Humanity.s First Exam')
```

### PASS · t03-kaggle-host (qualifier, Humanity's First Exam)
> Claim: Humanity's First Exam benchmark on Kaggle

Source ([x-kaggle](https://x.com/kaggle/status/2125313430303244739)): "Today, @GoogleDeepMind is launching Humanity's First Exam on Kaggle, a benchmark designed to measure "floor reliability": whether models get simple tasks right every time, not just once."

```python
def check(ctx):
    return ctx.require('kaggle', r'launching Humanity.s First Exam on Kaggle, a benchmark')
```

### PASS · t07-simple-tasks (qualifier, Humanity's First Exam)
> Claim: simple tasks

Source ([primary-deepmind-humanitys-first-exam-floor-reli](https://www.kaggle.com/benchmarks/deepmind/hfe/leaderboard)): "Measuring how reliably frontier models solve simple text and image tasks humans get right almost every time."

```python
def check(ctx):
    return ctx.require('deepmind', r'simple text and image tasks humans get right almost every time')
```

### PASS · t08-consistent-average (number, Humanity's First Exam)
> Claim: average under 86 percent

Source ([x-kaggle](https://x.com/kaggle/status/2125313430303244739)): "• High single-shot accuracy masks inconsistency: Top five models reach 96%-98% pass@1 and 100% family pass@4, yet average only 85.6% on family pass^4 (80.5%-92.4%), with a 7.6-80.1 percentage-point Family Reliability Gap across all 18 models."

```python
def check(ctx):
    return ctx.require('kaggle', r'Top five models reach.*average only 85\.6% on family pass\^4')
```

### PASS · t10-family-size (number, Humanity's First Exam)
> Claim: four variations

Source ([primary-deepmind-humanitys-first-exam-floor-reli](https://www.kaggle.com/benchmarks/deepmind/hfe/leaderboard)): "- Dataset size: 544 prompts organized into 136 four-prompt perturbation families (1 seed prompt + 3 logic-preserving variants per family) across 20 foundational subcategories and four macro-categories: Vision (51 families, 204 prompts), Math & Algorithmic (40 families, 160 prompts), Spatial & Positional (27 families, 108 prompts), and Reasoning & Language (18 families, 72 prompts)."

```python
def check(ctx):
    return ctx.require('deepmind', r'four-prompt perturbation families \(1 seed prompt \+ 3 logic-preserving variants per family\)')
```

### PASS · t13-openai-report (attribution, GPT-6 protein binders)
> Claim: In an unreviewed preprint, OpenAI reports

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "framing (OpenAI): Company-reported preprint with lab tests run by its research partner Onava; no independent replication."

```python
def check(ctx):
    return ctx.require('framing', r'framing \(OpenAI\): Company-reported preprint')
```

### PASS · t14-preprint-status (qualifier, GPT-6 protein binders)
> Claim: unreviewed preprint

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-25/audit/sources/2026-11-25/scan-framing.txt)): "framing (OpenAI): Company-reported preprint with lab tests run by its research partner Onava; no independent replication."

Note: Status of the cited version, not evidence of independent peer review.

```python
def check(ctx):
    return ctx.require('framing', r'Company-reported preprint with lab tests run by its research partner', note='Status of the cited version, not evidence of independent peer review.')
```

### PASS · t15-binder-design (attribution, GPT-6 protein binders)
> Claim: its GPT-6 models used reasoning and code to design protein binders

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "Our GPT-6 family of models can design new protein shapes and the sequence of their chemical building blocks using only reasoning and code, without calling specialized biology models to generate those designs. … GPT-6.2 designed shapes for small proteins intended to attach to chosen targets."

```python
def check(ctx):
    return ctx.require('openai', r'Our GPT.6 family of models can design new protein shapes.*using only reasoning and code', r'GPT.6\.2 designed shapes for small proteins intended to attach to chosen targets')
```

### PASS · t16-tested-hit-count (number, GPT-6 protein binders)
> Claim: 35 of 322 lab-tested candidates binding to their targets

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "We tested 322 minibinders against 5 targets in the lab. … Of those, 35 (10.9%) tested positive for binding to their intended target."

```python
def check(ctx):
    return ctx.require('openai', r'We tested 322 minibinders against 5 targets in the lab', r'Of those, 35 \(10\.9%\) tested positive for binding to their intended target')
```

### PASS · t17-lab-tested (qualifier, GPT-6 protein binders)
> Claim: lab-tested candidates

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "We tested 322 minibinders against 5 targets in the lab."

```python
def check(ctx):
    return ctx.require('openai', r'We tested 322 minibinders against 5 targets in the lab')
```

### PASS · t18-specialist-filter (attribution, GPT-6 protein binders)
> Claim: specialized biology models still filtered weak candidates upfront

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "It is important to note that our protein design campaign relied on specialized structure prediction models such as Boltz-2, OpenDDE, and ESMFold2 to filter candidates. … Specialized models supplied amino acid sequences and helped select candidates for testing."

```python
def check(ctx):
    return ctx.require('openai', r'protein design campaign relied on specialized structure prediction models.*to filter candidates', r'Specialized models supplied amino acid sequences and helped select candidates for testing')
```

### PASS · t19-internal-model (qualifier, GPT-6 protein binders)
> Claim: OpenAI's latest internal model

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "Across the full test, the average score rose from 0.16 for GPT-5.6 to 0.26 for GPT-6.2 and 0.38 for our latest internal model."

```python
def check(ctx):
    return ctx.require('openai', r'Across the full test, the average score rose from.*0\.38 for our latest internal model')
```

### PASS · t20-folding-score (number, GPT-6 protein binders)
> Claim: scores under 0.4 on whole-protein folding

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "Across the full test, the average score rose from 0.16 for GPT-5.6 to 0.26 for GPT-6.2 and 0.38 for our latest internal model. … The specialized model ESMFold2 averaged 0.93, so there's still a substantial gap in how reliably our models can predict a whole protein's structure from its sequence alone."

```python
def check(ctx):
    return ctx.require('openai', r'average score rose from.*0\.38 for our latest internal model', r'predict a whole protein.s structure from its sequence alone')
```

### PASS · t21-esmfold-score (number, GPT-6 protein binders)
> Claim: 0.93 for ESMFold2

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "The specialized model ESMFold2 averaged 0.93, so there's still a substantial gap in how reliably our models can predict a whole protein's structure from its sequence alone."

```python
def check(ctx):
    return ctx.require('openai', r'The specialized model ESMFold2 averaged 0\.93')
```

### PASS · t22-folding-gap (comparison, GPT-6 protein binders)
> Claim: even OpenAI's latest internal model scores under 0.4 on whole-protein folding versus 0.93 for ESMFold2

Source ([primary-openai-gpt6-protein-design-wetlab](https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/)): "Across the full test, the average score rose from 0.16 for GPT-5.6 to 0.26 for GPT-6.2 and 0.38 for our latest internal model. … The specialized model ESMFold2 averaged 0.93, so there's still a substantial gap in how reliably our models can predict a whole protein's structure from its sequence alone."

```python
def check(ctx):
    return ctx.require('openai', r'Across the full test, the average score rose from.*0\.38 for our latest internal model', r'ESMFold2 averaged 0\.93.*predict a whole protein.s structure from its sequence alone')
```

### PASS · tc01-citation (citation, takeaway 1)

Note: Takeaway 1 cites https://www.kaggle.com/benchmarks/deepmind/hfe/leaderboard, which is listed in the episode sources.json.

```python
def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 1 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 1 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))
```

### PASS · tc02-citation (citation, takeaway 2)

Note: Takeaway 2 cites https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/, which is listed in the episode sources.json.

```python
def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 2 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 2 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))
```
