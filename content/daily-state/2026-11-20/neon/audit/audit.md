# Executable audit, Daily State of AI 2026-11-20

Each claim is tested by a deterministic Python check against snapshotted source texts and X posts. PASS = the source sentence quoted supports the claim; FAIL = the source contradicts it or a required caveat is missing; NEEDS-HUMAN = opinion or not decidable by string/number match.

| artifact | PASS | FAIL | NEEDS-HUMAN | ERROR |
|---|---|---|---|---|
| episode | 42 | 7 | 8 | 0 |
| short | 14 | 5 | 3 | 0 |

## Sources
- `primary-alphaxiv-society-of-ai-scientists`: [A Society of AI Scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists) (sha256 d8e18ed908f9…)
- `x-emollick`: [X post by @emollick (Ethan Mollick)](https://x.com/emollick/status/2123631539942801732) (sha256 468b46bb1239…)
- `primary-airbnb-gemma4-e2b-production-classifier-`: [Frontier quality at 1% of the cost: a production benchmark of LLM classifiers](https://airbnb.tech/ai-ml/frontier-quality-at-1-of-the-cost-a-production-benchmark-of-llm-classifiers/) (sha256 bb822730063f…)
- `x-googlegemma`: [X post by @googlegemma (Google Gemma)](https://x.com/googlegemma/status/2123461832656781320) (sha256 8f59a2ee01e6…)
- `primary-andon-blueprint-bench-2-gpt62-astra`: [Blueprint-Bench 2](https://andonlabs.com/evals/blueprint-bench-2) (sha256 a69fca94b840…)
- `x-gdb`: [X post by @gdb (Greg Brockman)](https://x.com/gdb/status/2123719297096990726) (sha256 2c64677df528…)
- `x-andonlabs`: [X post by @andonlabs](https://x.com/andonlabs/status/2123570732575989832) (sha256 7d087ebd8ce2…)
- `scan-framing`: [Morning X-first scan: verification framing per story](https://www.signalandnoise.email/content/daily-state/2026-11-20/neon/audit/sources/2026-11-20/scan-framing.txt) (sha256 1ceb03b6c51c…)

## episode

### FAIL · e01-journal-scope (number, Society)
> Claim: nearly a thousand AI scientists ran its own peer-reviewed journal

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "As publication volume accelerated, agents in one laboratory also founded the Journal of Agent Research, an agent-run peer-review venue whose editors inspected code and provided scrutiny over experiment results."

Note: artifact credits the whole ~1,000-agent society with running the journal; source says agents in one laboratory founded it

```python
def check(ctx):
    # Who founded the journal? The abstract scopes it to agents in ONE laboratory.
    s = ctx.find('society', r'agents in one laborator\w* also founded the Journal')
    sent = ctx.art_sentence(CLAIM['quote'])
    if s and not re.search(r'one lab', sent, re.I):
        return ctx.fail('society', s, 'artifact credits the whole ~1,000-agent society with running the journal; source says agents in one laboratory founded it')
    return ctx.ok('society', s)
```

### FAIL · e14-null-results (comparison, Society)
> Claim: published null results as often as positive ones

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "For example, peers formed topical hubs where it was common to publicly retract mistaken claims before publication[p8] as well as acknowledge negative findings as often as positive ones.[p10]"

Note: source says negative results were cited/acknowledged as often as positive ones, not published as often

```python
def check(ctx):
    # Claim: PUBLISHED nulls as often as positives. Source: CITED / ACKNOWLEDGED negatives as often.
    return ctx.support_or_contradict('society', r'publish\w* (null|negative)[^.]{0,40}as often as positive',
        r'(cited|acknowledge) negative (results|findings) as often as positive',
        'source says negative results were cited/acknowledged as often as positive ones, not published as often')
```

### FAIL · e31-latency-drop (number, Airbnb)
> Claim: median latency dropped from roughly 900 milliseconds to 35

Source ([x-googlegemma](https://x.com/googlegemma/status/2123461832656781320)): "⚡ Speed: 35ms median latency (85ms p99) vs. ~900ms for frontier models"

Note: not a drop: 35 ms is the fine-tuned Gemma, ~900 ms is the frontier models

```python
def check(ctx):
    # "dropped from 900 to 35" implies one system got faster; sources compare two different models.
    return ctx.support_or_contradict('gemma', r'(drop|fell|reduc|cut)\w*[^.]{0,40}900', r'35ms median latency \(85ms p99\) vs\. ~900ms for frontier models',
        'not a drop: 35 ms is the fine-tuned Gemma, ~900 ms is the frontier models')
```

### FAIL · e49-notepad-trend (number, Blueprint)
> Claim: general frontier models given a persistent notepad to carry lessons across apartments are climbing steadily at four-hundredths of a point per month

Source ([primary-andon-blueprint-bench-2-gpt62-astra](https://andonlabs.com/evals/blueprint-bench-2)): "SOTA frontier models are labeled and a trend line is fitted through them, with a projection into the near future. Linear fit (R² = 0.87), +0.04/month"

Note: +0.04/month is the trend of SOTA scores against model release date, not models improving via the notepad

```python
def check(ctx):
    # Is +0.04/month a notepad effect? Source: a trend line over SOTA models by release date.
    return ctx.support_or_contradict('blueprint', r'notepad[^.]{0,120}0\.04|0\.04[^.]{0,120}notepad',
        r'SOTA frontier models are labeled and a trend line is fitted .* \+0\.04/month',
        '+0.04/month is the trend of SOTA scores against model release date, not models improving via the notepad')
```

### FAIL · e50-twelve-humans (qualifier, Blueprint)
> Claim: whether a leaderboard edges past twelve humans

Source ([primary-andon-blueprint-bench-2-gpt62-astra](https://andonlabs.com/evals/blueprint-bench-2)): "*Human baseline tested on subset of 12 apartments only"

Note: the 12 is apartments in the human-baseline subset, not twelve humans

```python
def check(ctx):
    return ctx.support_or_contradict('blueprint', r'(12|twelve) (humans|people|participants)', r'Human baseline tested on subset of 12 apartments',
        'the 12 is apartments in the human-baseline subset, not twelve humans')
```

### FAIL · oe1-society-preliminary (objection, Society)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-20/neon/audit/sources/2026-11-20/scan-framing.txt)): "framing (alphaXiv): Exploratory preprint by the alphaXiv/MIT/Stanford-led team that also built the platform; findings are author-reported and not yet peer reviewed or independently replicated."

Note: artifact never states this caveat (Society paper is an exploratory preprint, not yet peer reviewed or replicated)

```python
def check(ctx):
    # Objection: Society paper is an exploratory preprint, not yet peer reviewed or replicated
    s = ctx.find('framing', r'not yet peer reviewed')
    if not s: return ctx.ok(None, None, 'no such caveat in the scan framing for this story')
    if ctx.art_has(r"not (yet )?(been )?peer[- ]reviewed|not yet reviewed|unreviewed|preliminary|exploratory|hasn'?t been (peer[- ])?reviewed|early,? author[- ]reported"): return ctx.ok('framing', s, 'caveat present in artifact')
    return ctx.fail('framing', s, 'artifact never states this caveat (Society paper is an exploratory preprint, not yet peer reviewed or replicated)')
```

### FAIL · oe2-airbnb-company-reported (objection, Airbnb)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-20/neon/audit/sources/2026-11-20/scan-framing.txt)): "framing (Airbnb Engineering & Data Science): Company-reported benchmark on Airbnb's own held-out data for one production task; not independently replicated and not a general capability ranking."

Note: artifact never states this caveat (Airbnb result is company-reported, on its own data, for one task)

```python
def check(ctx):
    # Objection: Airbnb result is company-reported, on its own data, for one task
    s = ctx.find('framing', r'Company-reported benchmark on Airbnb.s own held-out data for one production task')
    if not s: return ctx.ok(None, None, 'no such caveat in the scan framing for this story')
    if ctx.art_has(r"company[- ]reported|airbnb (says|reports|reported|claims)|according to airbnb|airbnb's own (data|benchmark|test)|its own (held-out )?data|(one|single) (production )?(task|classifier)"): return ctx.ok('framing', s, 'caveat present in artifact')
    return ctx.fail('framing', s, 'artifact never states this caveat (Airbnb result is company-reported, on its own data, for one task)')
```

### NEEDS-HUMAN · e04-headlines-miss (opinion, Intro)
> Claim: all three headlines miss the best part

Note: opinion / framing; not checkable against sources

```python
def check(ctx):
    return ctx.need(None, None, 'opinion / framing; not checkable against sources')
```

### NEEDS-HUMAN · e05-thesis (opinion, Intro)
> Claim: judging models by prose, prompts, or leaderboard headlines is breaking down

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "Executable Review Finds What Text Can Miss"

Note: opinion (episode thesis); nearest supporting source text quoted

```python
def check(ctx):
    s = ctx.find('society', r'Executable Review Finds What Text Can Miss')
    return ctx.need('society', s, 'opinion (episode thesis); nearest supporting source text quoted')
```

### NEEDS-HUMAN · e06-real-signal (opinion, Intro)
> Claim: The real signal only shows up when you execute under real constraints

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "A shared archive made peer correction and cumulative reuse possible, but the journal comparison shows why those social norms need code-and-data scrutiny to test claims."

Note: opinion; nearest supporting source text quoted

```python
def check(ctx):
    s = ctx.find('society', r'need code-and-data scrutiny to test claims')
    return ctx.need('society', s, 'opinion; nearest supporting source text quoted')
```

### NEEDS-HUMAN · e15-journal-founded (attribution, Society)
> Claim: founded the Journal of Agent Research

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "Late in the observation window, agents founded the Journal of Agent Research. … As publication volume accelerated, agents in one laboratory also founded the Journal of Agent Research, an agent-run peer-review venue whose editors inspected code and provided scrutiny over experiment results."

Note: paper says both "agents founded" and "agents in one laboratory founded"; subject "They" (all 936 agents) is ambiguous

```python
def check(ctx):
    s1 = ctx.find('society', r'agents founded the Journal of Agent Research'); s2 = ctx.find('society', r'agents in one laborator\w* also founded')
    return ctx.need('society', (s1 or '') + ' … ' + (s2 or ''), 'paper says both "agents founded" and "agents in one laboratory founded"; subject "They" (all 936 agents) is ambiguous')
```

### NEEDS-HUMAN · e18-text-review-failed (opinion, Society)
> Claim: text-only peer review failed

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "In effect they could not tell a disclosed weakness from a hidden one. [p19] A guest editor then translated 276 objections across 43 paper clusters into scripts that were run on the uploaded data."

Note: characterisation ("failed") is stronger than the source, which says text-only reviewers flagged 11 of 16 flawed drafts but could not tell disclosed from hidden weaknesses

```python
def check(ctx):
    s = ctx.find('society', r'could not tell a disclosed weakness from a hidden one')
    return ctx.need('society', s, 'characterisation ("failed") is stronger than the source, which says text-only reviewers flagged 11 of 16 flawed drafts but could not tell disclosed from hidden weaknesses')
```

### NEEDS-HUMAN · e26-theater (opinion, Society)
> Claim: Without an execution path, AI science risks becoming very polite, rigorous-sounding theater

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "Evidence Needs an Execution Path"

Note: opinion; echoes the paper section title quoted

```python
def check(ctx):
    s = ctx.find('society', r'Evidence Needs an Execution Path')
    return ctx.need('society', s, 'opinion; echoes the paper section title quoted')
```

### NEEDS-HUMAN · e29-matched-sol-sonnet (comparison, Airbnb)
> Claim: matched GPT-6.1 Sol and Claude Sonnet 5.5 on a real-time policy classifier

Source ([primary-airbnb-gemma4-e2b-production-classifier-](https://airbnb.tech/ai-ml/frontier-quality-at-1-of-the-cost-a-production-benchmark-of-llm-classifiers/)): "Fine-tuning Gemma4-E2B on hundreds of thousands of domain-specific examples lifts its F1 from 0.563 to 0.902, on par with the best proprietary models, while median latency stays at 35ms."

Note: source does not show Sol or Sonnet 5.5 are the best proprietary models on F1; names come from the latency/cost passages

```python
def check(ctx):
    # Source never gives an F1 for Sol or Sonnet; it says "on par with the best proprietary models".
    named = ctx.find('airbnb', r'(Sol|Sonnet 5\.5)[^.]*\b(F1|0\.9\d)')
    if named: return ctx.ok('airbnb', named)
    s = ctx.find('airbnb', r'on par with the best proprietary models')
    return ctx.need('airbnb', s, 'source does not show Sol or Sonnet 5.5 are the best proprietary models on F1; names come from the latency/cost passages')
```

### NEEDS-HUMAN · e39-dial (opinion, Airbnb)
> Claim: You can't prompt your way to an operational dial

Source ([primary-airbnb-gemma4-e2b-production-classifier-](https://airbnb.tech/ai-ml/frontier-quality-at-1-of-the-cost-a-production-benchmark-of-llm-classifiers/)): "Scores let you choose your tradeoff between recall and precision without rewriting the prompt."

Note: opinion; paraphrases the quoted source line

```python
def check(ctx):
    s = ctx.find('airbnb', r'Scores let you choose your tradeoff .* without rewriting the prompt')
    return ctx.need('airbnb', s, 'opinion; paraphrases the quoted source line')
```

### PASS · e00-date (number, Intro)
> Claim: November 20th, 2026

Note: edition date matches audit date 2026-11-20

```python
def check(ctx):
    return ctx.ok(None, None, 'edition date matches audit date %s' % ctx.date) if ctx.date == '2026-11-20' else ctx.fail(None, None, 'date mismatch')
```

### PASS · e02-matched-1pct (comparison, Airbnb)
> Claim: matched frontier APIs at one percent of the cost

Source ([primary-airbnb-gemma4-e2b-production-classifier-](https://airbnb.tech/ai-ml/frontier-quality-at-1-of-the-cost-a-production-benchmark-of-llm-classifiers/)): "In this blog post, we put one of these classifiers head-to-head with open-weight and proprietary models and find that it matches frontier-level quality in under 100ms at roughly 1% of the cost."

```python
def check(ctx):
    return ctx.require('airbnb', r'matches frontier-level quality .*roughly 1% of the cost')
```

### PASS · e03-astra-beat-humans (comparison, Blueprint)
> Claim: GPT-6.2 Astra beat humans at 3D spatial reasoning

Source ([primary-andon-blueprint-bench-2-gpt62-astra](https://andonlabs.com/evals/blueprint-bench-2)): "GPT-6.2 Astra 0.614 … Human* 0.586"

Note: headline framing matches @gdb: "@gdb: GPT-6.2 Astra exceeding human baseline on physical 3D understanding benchmark: https://t.co/Z4j9Na9VQW"; caveat (12-apartment subset) is checked in o-e4

```python
def check(ctx):
    # Framed as a feed headline. Leaderboard: Astra 0.614 vs human 0.586 (human on 12 of 50 apartments).
    a = ctx.find('blueprint', r'GPT-6\.2 Astra 0\.614'); h = ctx.find('blueprint', r'Human\* 0\.586')
    g = ctx.find('gdb', r'exceeding human baseline')
    if a and h and g: return ctx.ok('blueprint', a + ' … ' + h, 'headline framing matches @gdb: "' + g + '"; caveat (12-apartment subset) is checked in o-e4')
    return ctx.need('blueprint', a, 'scores not found')
```

### PASS · e07-alphaxiv-study (attribution, Society)
> Claim: the alphaXiv study

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "alphaXivMITStanford … publisher={alphaXiv},"

Note: alphaXiv-published, alphaXiv/MIT/Stanford authors

```python
def check(ctx):
    return ctx.require('society', r'alphaXivMITStanford', r'publisher=\{alphaXiv\}', note='alphaXiv-published, alphaXiv/MIT/Stanford authors')
```

### PASS · e08-title (quote, Society)
> Claim: A Society of AI Scientists

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "A Society of AI Scientists | alphaXiv"

```python
def check(ctx):
    return ctx.require('society', r'^A Society of AI Scientists')
```

### PASS · e09-twelve-weeks (number, Society)
> Claim: Over twelve weeks

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "We present an exploratory twelve-week study documenting the activity of 936 autonomous agents across 35 human-operated laboratories interacting in a shared preprint server and messaging workspace."

```python
def check(ctx):
    return ctx.require('society', r'twelve-week study')
```

### PASS · e10-labs-agents (attribution, Society)
> Claim: thirty-five human labs, including Stanford, MIT, and ETH Zurich, deployed 936 autonomous agents onto a shared preprint server

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "We present an exploratory twelve-week study documenting the activity of 936 autonomous agents across 35 human-operated laboratories interacting in a shared preprint server and messaging workspace. … For three months, nearly 1,000 agents from 35 labs (across Stanford, MIT, ETH Zurich, and more) conducted research autonomously on this server, producing 936 papers alongside their code, data, and model weights."

```python
def check(ctx):
    return ctx.require('society', r'936 autonomous agents across 35 human-operated laboratories .*shared preprint server', r'35 labs \(across Stanford, MIT, ETH Zurich')
```

### PASS · e11-936-papers (number, Society)
> Claim: published 936 papers with code and data

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "For three months, nearly 1,000 agents from 35 labs (across Stanford, MIT, ETH Zurich, and more) conducted research autonomously on this server, producing 936 papers alongside their code, data, and model weights."

```python
def check(ctx):
    return ctx.require('society', r'producing 936 papers alongside their code, data')
```

### PASS · e12-9500 (number, Society)
> Claim: exchanged 9,500 messages

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "They also exchanged 9,500 messages distributed across 229 agent-created chat rooms."

```python
def check(ctx):
    return ctx.require('society', r'exchanged 9,500 messages')
```

### PASS · e13-retract-before (attribution, Society)
> Claim: retracted mistakes publicly before upload

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "For example, peers formed topical hubs where it was common to publicly retract mistaken claims before publication[p8] as well as acknowledge negative findings as often as positive ones.[p10]"

```python
def check(ctx):
    return ctx.support_or_contradict('society', r'publicly retract mistaken claims before publication', r'correction preceded upload', 'retraction timing')
```

### PASS · e16-rigor-llm-judges (comparison, Society)
> Claim: blinded LLM judges did rate the agents' prose higher on experimental rigor than matched human preprints

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "Agent papers scored higher on experimental rigor, 9.02 versus 7.00 on a 10-point scale, a difference of +2.01 points (95% CI +1.74 to +2.29). … These are blinded LLM rubric ratings of prose, not expert human peer review, and the judges could not run code or inspect figures. [p30] … Two LLM judges rated author- and affiliation-stripped full texts in both presentation orders across 202 matched pairs of agent and human papers."

```python
def check(ctx):
    return ctx.require('society', r'Agent papers scored higher on experimental rigor, 9\.02 versus 7\.00', r'blinded LLM rubric ratings of prose', r'202 matched pairs')
```

### PASS · e17-novelty (comparison, Society)
> Claim: humans won on novelty and significance

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "Human papers scored higher on novelty and significance."

```python
def check(ctx):
    return ctx.require('society', r'Human papers scored higher on novelty and significance')
```

### PASS · e19-11of16 (number, Society)
> Claim: Text-only reviewers caught eleven of sixteen flawed drafts

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "Text-only reviewers flagged 11 of 16 flawed first-version drafts, but also flagged 10 of 16 repaired versions in which the limitation was already openly disclosed."

```python
def check(ctx):
    return ctx.require('society', r'Text-only reviewers flagged 11 of 16 flawed')
```

### PASS · e20-10of16 (number, Society)
> Claim: flagged ten of sixteen repaired versions where the limitation was already openly disclosed

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "Text-only reviewers flagged 11 of 16 flawed first-version drafts, but also flagged 10 of 16 repaired versions in which the limitation was already openly disclosed."

```python
def check(ctx):
    return ctx.require('society', r'10 of 16 repaired versions in which the limitation was already openly disclosed')
```

### PASS · e21-answer-keys (attribution, Society)
> Claim: code inspections still caught scripts using answer keys and leaked targets

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "The journal's code inspections found submissions in which scripts or prompts used answer keys or leaked targets, which is why checking values alone is insufficient. [p27]"

```python
def check(ctx):
    return ctx.require('society', r'code inspections found submissions in which scripts or prompts used answer keys or leaked targets')
```

### PASS · e22-guest-editor (attribution, Society)
> Claim: A guest editor turned referee objections into scripts and ran them on the uploaded data

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "In effect they could not tell a disclosed weakness from a hidden one. [p19] A guest editor then translated 276 objections across 43 paper clusters into scripts that were run on the uploaded data."

```python
def check(ctx):
    return ctx.require('society', r'guest editor then translated 276 objections .* into scripts that were run on the uploaded data')
```

### PASS · e23-nearly-half (number, Society)
> Claim: overturning the headline conclusion in nearly half of major-objection cases

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "For major objections, the scripts overturned the headline conclusion in 77 of 156 cases (49.4%); for minor objections, in 24 of 120 cases (20.0%). [p20] These are executed referee objections in this journal, not a random audit of all papers in the cohort."

Note: 77/156 = 49.4%; "nearly half" holds

```python
def check(ctx):
    s = ctx.find('society', r'major objections, the scripts overturned the headline conclusion in (\d+) of (\d+)')
    if not s: return ctx.need('society', None, 'figure not found')
    n, d = map(int, re.search(r'in (\d+) of (\d+)', s).groups())
    return ctx.ok('society', s, f'{n}/{d} = {n/d:.1%}; "nearly half" holds') if 0.40 <= n / d < 0.5 else ctx.fail('society', s, f'{n}/{d} = {n/d:.1%} is not "nearly half"')
```

### PASS · e24-101 (number, Society)
> Claim: 101-step citation chain

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "The longest citation chain reached 101 steps, but a recency-matched random citation null averaged 99.4 steps (P = 0.44)."

```python
def check(ctx):
    return ctx.require('society', r'longest citation chain reached 101 steps')
```

### PASS · e25-random-null (comparison, Society)
> Claim: statistically indistinguishable from randomly citing recent papers

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "The longest citation chain reached 101 steps, but a recency-matched random citation null averaged 99.4 steps (P = 0.44)."

Note: P = 0.44 > 0.05

```python
def check(ctx):
    s = ctx.find('society', r'recency-matched random citation null averaged [\d.]+ steps \(P = ([\d.]+)\)')
    if not s: return ctx.need('society', None, 'null comparison not found')
    p = float(re.search(r'P = ([\d.]+)', s).group(1))
    return ctx.ok('society', s, f'P = {p} > 0.05') if p > 0.05 else ctx.fail('society', s, f'P = {p} is significant')
```

### PASS · e27-gemma-promoting (attribution, Airbnb)
> Claim: Google's Gemma account is promoting Airbnb's new benchmark

Source ([x-googlegemma](https://x.com/googlegemma/status/2123461832656781320)): "@googlegemma: Love seeing what happens when open weights meet great engineering!"

```python
def check(ctx):
    return ctx.require('gemma', r'@googlegemma: Love seeing what happens when open weights meet great engineering')
```

### PASS · e28-e2b-rtx (qualifier, Airbnb)
> Claim: a fine-tuned Gemma 4 E2B model on a single NVIDIA RTX Pro 6000 GPU

Source ([x-googlegemma](https://x.com/googlegemma/status/2123461832656781320)): "In a new benchmark, @AirbnbEng took Gemma 4 E2B for policy classification and served it on a single @NVIDIA RTX Pro 6000 GPU:"

```python
def check(ctx):
    return ctx.require('gemma', r'Gemma 4 E2B .*single @NVIDIA RTX Pro 6000 GPU')
```

### PASS · e30-0902 (number, Airbnb)
> Claim: Quality hit 0.902 max F1

Source ([x-googlegemma](https://x.com/googlegemma/status/2123461832656781320)): "🎯 Quality: Jumped from 0.563 to 0.902 max F1, matching top frontier APIs"

```python
def check(ctx):
    return ctx.require('gemma', r'0\.563 to 0\.902 max F1')
```

### PASS · e32-1pct (number, Airbnb)
> Claim: costs fell to about one percent at high volume

Source ([x-googlegemma](https://x.com/googlegemma/status/2123461832656781320)): "💸 Cost: ~1% of frontier API spend at high volume"

Note: relative cost vs frontier APIs; "fell" is loose but the figure matches

```python
def check(ctx):
    return ctx.require('gemma', r'~1% of frontier API spend at high volume', note='relative cost vs frontier APIs; "fell" is loose but the figure matches')
```

### PASS · e33-0563 (number, Airbnb)
> Claim: Out of the box, that two-billion-parameter model scored a weak 0.563

Source ([primary-airbnb-gemma4-e2b-production-classifier-](https://airbnb.tech/ai-ml/frontier-quality-at-1-of-the-cost-a-production-benchmark-of-llm-classifiers/)): "We compare a fine-tuned classifier with 2 billion effective parameters (E2B) against open-weight and proprietary models on a held-out evaluation dataset of 10,000 weighted examples. … Fine-tuning Gemma4-E2B on hundreds of thousands of domain-specific examples lifts its F1 from 0.563 to 0.902, on par with the best proprietary models, while median latency stays at 35ms."

```python
def check(ctx):
    return ctx.require('airbnb', r'2 billion effective parameters', r'lifts its F1 from 0\.563')
```

### PASS · e34-2700 (number, Airbnb)
> Claim: even a 2,700-word prompt couldn't close the gap

Source ([primary-airbnb-gemma4-e2b-production-classifier-](https://airbnb.tech/ai-ml/frontier-quality-at-1-of-the-cost-a-production-benchmark-of-llm-classifiers/)): "A detailed prompt improves classification quality but doesn't close the gap."

```python
def check(ctx):
    return ctx.require('airbnb', r"2,700 word prompt couldn't|detailed prompt improves classification quality but doesn't close the gap")
```

### PASS · e35-hundreds-thousands (number, Airbnb)
> Claim: fine-tuning on hundreds of thousands of labeled production examples

Source ([primary-airbnb-gemma4-e2b-production-classifier-](https://airbnb.tech/ai-ml/frontier-quality-at-1-of-the-cost-a-production-benchmark-of-llm-classifiers/)): "Fine-tuning Gemma4-E2B on hundreds of thousands of domain-specific examples lifts its F1 from 0.563 to 0.902, on par with the best proprietary models, while median latency stays at 35ms."

```python
def check(ctx):
    return ctx.require('airbnb', r'hundreds of thousands of domain-specific examples')
```

### PASS · e36-rpm (qualifier, Airbnb)
> Claim: only beats APIs above fifteen to thirty requests per minute

Source ([primary-airbnb-gemma4-e2b-production-classifier-](https://airbnb.tech/ai-ml/frontier-quality-at-1-of-the-cost-a-production-benchmark-of-llm-classifiers/)): "Proprietary models only win at low traffic: below roughly 15 to 30 RPM, Claude Sonnet 5.5 and GPT-6.1 Sol are cheaper than a dedicated GPU."

```python
def check(ctx):
    return ctx.require('airbnb', r'below roughly 15 to 30 RPM, Claude Sonnet 5\.5 and GPT-6\.1 Sol are cheaper')
```

### PASS · e37-true-false (qualifier, Airbnb)
> Claim: Frontier models return a slow, fixed true-or-false verdict

Source ([primary-airbnb-gemma4-e2b-production-classifier-](https://airbnb.tech/ai-ml/frontier-quality-at-1-of-the-cost-a-production-benchmark-of-llm-classifiers/)): "And because each model returns a verdict rather than a score, it gives a single, fixed precision-recall point. … While we would normally prefer PR-AUC for imbalanced classification, most proprietary models return only a True or False verdict, so there is no curve to integrate."

Note: said of proprietary generative models; elsewhere "most proprietary models"

```python
def check(ctx):
    s = ctx.find('airbnb', r'each model returns a verdict rather than a score, it gives a single, fixed precision-recall point')
    m = ctx.find('airbnb', r'most proprietary models return only a True or False verdict')
    if s: return ctx.ok('airbnb', s + ' … ' + (m or ''), 'said of proprietary generative models; elsewhere "most proprietary models"')
    return ctx.need('airbnb', m, 'only the "most proprietary models" wording found')
```

### PASS · e38-logprobs (attribution, Airbnb)
> Claim: Extracting logprobs from a fine-tuned model gives Airbnb a continuous score they can threshold

Source ([primary-airbnb-gemma4-e2b-production-classifier-](https://airbnb.tech/ai-ml/frontier-quality-at-1-of-the-cost-a-production-benchmark-of-llm-classifiers/)): "By extracting logprobs, we're able to produce a score for thresholding."

```python
def check(ctx):
    return ctx.require('airbnb', r'By extracting logprobs, we.re able to produce a score for thresholding')
```

### PASS · e40-andon (attribution, Blueprint)
> Claim: Andon Labs' Blueprint-Bench 2

Source ([primary-andon-blueprint-bench-2-gpt62-astra](https://andonlabs.com/evals/blueprint-bench-2)): "author={Andon Labs},"

```python
def check(ctx):
    return ctx.require('blueprint', r'author=\{Andon Labs\}')
```

### PASS · e41-twenty-photos (number, Blueprint)
> Claim: agents turn roughly twenty apartment photos into 2D floor plans

Source ([primary-andon-blueprint-bench-2-gpt62-astra](https://andonlabs.com/evals/blueprint-bench-2)): "Each agent processes 50 apartments sequentially, examining ~20 interior photos per apartment and generating a floor plan showing room layouts, connections, and relative sizes. … We test this by asking them to convert apartment photographs into accurate 2D floor plans."

```python
def check(ctx):
    return ctx.require('blueprint', r'~20 interior photos', r'2D floor plans')
```

### PASS · e42-brockman (attribution, Blueprint)
> Claim: OpenAI's Greg Brockman highlighted that GPT-6.2 Astra ranked first at 0.614

Source ([x-gdb](https://x.com/gdb/status/2123719297096990726)): "@gdb: GPT-6.2 Astra exceeding human baseline on physical 3D understanding benchmark: https://t.co/Z4j9Na9VQW … leaderboard: 1 GPT-6.2 Astra 0.614"

Note: Brockman highlighted the human-baseline result; the 0.614 figure is from the leaderboard, not his post

```python
def check(ctx):
    g = ctx.find('gdb', r'GPT-6\.2 Astra exceeding human baseline'); a = ctx.find('blueprint', r'1 GPT-6\.2 Astra 0\.614')
    if g and a: return ctx.ok('gdb', g + ' … leaderboard: ' + a, 'Brockman highlighted the human-baseline result; the 0.614 figure is from the leaderboard, not his post')
    return ctx.need('gdb', g, 'post or score not found')
```

### PASS · e43-0586 (comparison, Blueprint)
> Claim: edging past the human baseline of 0.586

Source ([primary-andon-blueprint-bench-2-gpt62-astra](https://andonlabs.com/evals/blueprint-bench-2)): "Human* 0.586"

```python
def check(ctx):
    return ctx.require('blueprint', r'Human\* 0\.586')
```

### PASS · e44-12of50 (qualifier, Blueprint)
> Claim: human baseline was tested on just twelve apartments out of fifty

Source ([primary-andon-blueprint-bench-2-gpt62-astra](https://andonlabs.com/evals/blueprint-bench-2)): "*Human baseline tested on subset of 12 apartments only … Each agent processes 50 apartments sequentially, examining ~20 interior photos per apartment and generating a floor plan showing room layouts, connections, and relative sizes."

```python
def check(ctx):
    return ctx.require('blueprint', r'Human baseline tested on subset of 12 apartments only', r'processes 50 apartments')
```

### PASS · e45-carbon-tie (comparison, Blueprint)
> Claim: Gemini 4 Carbon tied it

Source ([primary-andon-blueprint-bench-2-gpt62-astra](https://andonlabs.com/evals/blueprint-bench-2)): "T2 Gemini 4 Carbon 0.586 T2 Human* 0.586"

```python
def check(ctx):
    return ctx.require('blueprint', r'T2 Gemini 4 Carbon 0\.586 T2 Human\* 0\.586')
```

### PASS · e46-neon-absent (qualifier, Blueprint)
> Claim: Google's newly released Gemini 4 Neon isn't even on the board yet

Source ([x-andonlabs](https://x.com/andonlabs/status/2123570732575989832)): "@bughuntergeek (13 likes): @andonlabs I don't understand why you would post that directly after Google released the best model in the world, Gemini 4 Neon."

Note: no "Neon" anywhere in the leaderboard page; "newly released" comes from a reply in the @andonlabs thread

```python
def check(ctx):
    if not ctx.absent('blueprint', r'Neon'): return ctx.fail('blueprint', ctx.find('blueprint', r'Neon'), 'Neon is on the leaderboard')
    r = ctx.find('andon', r'Google released the best model in the world, Gemini 4 Neon')
    return ctx.ok('andon', r, 'no "Neon" anywhere in the leaderboard page; "newly released" comes from a reply in the @andonlabs thread') if r else ctx.need('andon', None, 'release not sourced')
```

### PASS · e47-robotics-zero (number, Blueprint)
> Claim: Gemini Robotics-ER 1.6, a model built specifically for embodied spatial reasoning, scored zero

Source ([primary-andon-blueprint-bench-2-gpt62-astra](https://andonlabs.com/evals/blueprint-bench-2)): "Gemini Robotics-ER 1.6 0.000** … Despite being designed for spatial and embodied reasoning, it scores below Gemini 3 Flash."

```python
def check(ctx):
    return ctx.require('blueprint', r'Gemini Robotics-ER 1\.6 0\.000\*\*', r'designed for spatial and embodied reasoning')
```

### PASS · e48-random (comparison, Blueprint)
> Claim: at or below random chance

Source ([primary-andon-blueprint-bench-2-gpt62-astra](https://andonlabs.com/evals/blueprint-bench-2)): "**Score at or below the random baseline"

```python
def check(ctx):
    return ctx.require('blueprint', r'\*\*Score at or below the random baseline')
```

### PASS · oe3-blueprint-subset (objection, Blueprint)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-20/neon/audit/sources/2026-11-20/scan-framing.txt)): "framing (Andon Labs): Benchmark operator's own leaderboard; the human baseline covers only 12 of the 50 apartments, so the human comparison is limited."

Note: caveat present in artifact

```python
def check(ctx):
    # Objection: human baseline covers only 12 of 50 apartments
    s = ctx.find('framing', r'human baseline covers only 12 of the 50 apartments')
    if not s: return ctx.ok(None, None, 'no such caveat in the scan framing for this story')
    if ctx.art_has(r'(12|twelve) apartments'): return ctx.ok('framing', s, 'caveat present in artifact')
    return ctx.fail('framing', s, 'artifact never states this caveat (human baseline covers only 12 of 50 apartments)')
```

### PASS · oe4-blueprint-operator (objection, Blueprint)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-20/neon/audit/sources/2026-11-20/scan-framing.txt)): "framing (Andon Labs): Benchmark operator's own leaderboard; the human baseline covers only 12 of the 50 apartments, so the human comparison is limited."

Note: caveat present in artifact

```python
def check(ctx):
    # Objection: leaderboard is run by the benchmark operator (named as source)
    s = ctx.find('framing', r'Benchmark operator.s own leaderboard')
    if not s: return ctx.ok(None, None, 'no such caveat in the scan framing for this story')
    if ctx.art_has(r"andon labs'? blueprint|andon labs|on blueprint-bench"): return ctx.ok('framing', s, 'caveat present in artifact')
    return ctx.fail('framing', s, 'artifact never states this caveat (leaderboard is run by the benchmark operator (named as source))')
```

### PASS · oe5-rigor-llm-judges (objection, Society)

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "These are blinded LLM rubric ratings of prose, not expert human peer review, and the judges could not run code or inspect figures. [p30]"

Note: framed as LLM judges

```python
def check(ctx):
    # Objection: if the rigor score is cited, it must be framed as LLM ratings of prose, not human peer review.
    s = ctx.find('society', r'blinded LLM rubric ratings of prose, not expert human peer review')
    if not ctx.art_has(r'rigor'): return ctx.ok(None, None, 'rigor score not cited')
    return ctx.ok('society', s, 'framed as LLM judges') if ctx.art_has(r'LLM judges|language model judges') else ctx.fail('society', s, 'rigor score cited without LLM-judge caveat')
```

### PASS · oe6-interested-parties (objection, Airbnb/Blueprint)

Note: both promoters identified with their company

```python
def check(ctx):
    # Objection: promoters with a stake (Google's Gemma account, OpenAI's president) must be identified as such.
    g = ctx.art_has(r"Google's Gemma account"); b = ctx.art_has(r"OpenAI's Greg Brockman")
    s = ctx.find('framing', r'Company-reported')
    return ctx.ok(None, None, 'both promoters identified with their company') if g and b else ctx.fail(None, None, f'gemma identified={g}, brockman identified={b}')
```

## short

### FAIL · os1-society-preliminary (objection, Society)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-20/neon/audit/sources/2026-11-20/scan-framing.txt)): "framing (alphaXiv): Exploratory preprint by the alphaXiv/MIT/Stanford-led team that also built the platform; findings are author-reported and not yet peer reviewed or independently replicated."

Note: artifact never states this caveat (Society paper is an exploratory preprint, not yet peer reviewed or replicated)

```python
def check(ctx):
    # Objection: Society paper is an exploratory preprint, not yet peer reviewed or replicated
    s = ctx.find('framing', r'not yet peer reviewed')
    if not s: return ctx.ok(None, None, 'no such caveat in the scan framing for this story')
    if ctx.art_has(r"not (yet )?(been )?peer[- ]reviewed|not yet reviewed|unreviewed|preliminary|exploratory|hasn'?t been (peer[- ])?reviewed|early,? author[- ]reported"): return ctx.ok('framing', s, 'caveat present in artifact')
    return ctx.fail('framing', s, 'artifact never states this caveat (Society paper is an exploratory preprint, not yet peer reviewed or replicated)')
```

### FAIL · os2-airbnb-company-reported (objection, Airbnb)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-20/neon/audit/sources/2026-11-20/scan-framing.txt)): "framing (Airbnb Engineering & Data Science): Company-reported benchmark on Airbnb's own held-out data for one production task; not independently replicated and not a general capability ranking."

Note: artifact never states this caveat (Airbnb result is company-reported, on its own data, for one task)

```python
def check(ctx):
    # Objection: Airbnb result is company-reported, on its own data, for one task
    s = ctx.find('framing', r'Company-reported benchmark on Airbnb.s own held-out data for one production task')
    if not s: return ctx.ok(None, None, 'no such caveat in the scan framing for this story')
    if ctx.art_has(r"company[- ]reported|airbnb (says|reports|reported|claims)|according to airbnb|airbnb's own (data|benchmark|test)|its own (held-out )?data|(one|single) (production )?(task|classifier)"): return ctx.ok('framing', s, 'caveat present in artifact')
    return ctx.fail('framing', s, 'artifact never states this caveat (Airbnb result is company-reported, on its own data, for one task)')
```

### FAIL · s02-journal-scope (attribution, Society)
> Claim: publish 936 papers, and launch a peer-reviewed journal

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "As publication volume accelerated, agents in one laboratory also founded the Journal of Agent Research, an agent-run peer-review venue whose editors inspected code and provided scrutiny over experiment results."

Note: credits all 936 agents with launching the journal; source says agents in one laboratory founded it

```python
def check(ctx):
    s = ctx.find('society', r'agents in one laborator\w* also founded the Journal')
    sent = ctx.art_sentence(CLAIM['quote'])
    if s and not re.search(r'one lab', sent, re.I):
        return ctx.fail('society', s, 'credits all 936 agents with launching the journal; source says agents in one laboratory founded it')
    return ctx.ok('society', s)
```

### FAIL · s04-card-journal (number, Society)
> Claim: 936 agents built a journal

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "As publication volume accelerated, agents in one laboratory also founded the Journal of Agent Research, an agent-run peer-review venue whose editors inspected code and provided scrutiny over experiment results."

Note: on-screen card credits all 936 agents with the journal; source scopes it to one laboratory

```python
def check(ctx):
    s = ctx.find('society', r'agents in one laborator\w* also founded the Journal')
    return ctx.fail('society', s, 'on-screen card credits all 936 agents with the journal; source scopes it to one laboratory') if s else ctx.need('society', None, 'scope sentence not found')
```

### FAIL · s06-overturned (qualifier, Society)
> Claim: Only running scripts on the uploaded data overturned nearly half of major objections

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "For major objections, the scripts overturned the headline conclusion in 77 of 156 cases (49.4%); for minor objections, in 24 of 120 cases (20.0%). [p20] These are executed referee objections in this journal, not a random audit of all papers in the cohort."

Note: inverted: the scripts overturned the papers' headline conclusions in 49.4% of major-objection cases, not the objections themselves

```python
def check(ctx):
    # What was overturned: the objections, or the papers' headline conclusions?
    return ctx.support_or_contradict('society', r'overturned[^.]{0,30}objections', r'scripts overturned the headline conclusion in 77 of 156 cases',
        'inverted: the scripts overturned the papers\' headline conclusions in 49.4% of major-objection cases, not the objections themselves')
```

### NEEDS-HUMAN · s00-thesis (opinion, Intro)
> Claim: judging models by prose, prompts, or leaderboards is breaking down

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "Executable Review Finds What Text Can Miss"

Note: opinion (short thesis); nearest supporting source text quoted

```python
def check(ctx):
    s = ctx.find('society', r'Executable Review Finds What Text Can Miss')
    return ctx.need('society', s, 'opinion (short thesis); nearest supporting source text quoted')
```

### NEEDS-HUMAN · s15-easy-to-fake (opinion, Close)
> Claim: Polished prose and top-line scores are easy to fake

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "But a convincing paper could still describe a flawed experiment."

Note: opinion stated as fact; sources show prose can mislead reviewers, not that scores are "easy to fake"

```python
def check(ctx):
    s = ctx.find('society', r'a convincing paper could still describe a flawed experiment')
    return ctx.need('society', s, 'opinion stated as fact; sources show prose can mislead reviewers, not that scores are "easy to fake"')
```

### NEEDS-HUMAN · s16-real-signal (opinion, Close)
> Claim: The real signal only appears when you execute under real constraints

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "A shared archive made peer correction and cumulative reuse possible, but the journal comparison shows why those social norms need code-and-data scrutiny to test claims."

Note: opinion; nearest supporting source text quoted

```python
def check(ctx):
    s = ctx.find('society', r'need code-and-data scrutiny to test claims')
    return ctx.need('society', s, 'opinion; nearest supporting source text quoted')
```

### PASS · os3-blueprint-subset (objection, Blueprint)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-20/neon/audit/sources/2026-11-20/scan-framing.txt)): "framing (Andon Labs): Benchmark operator's own leaderboard; the human baseline covers only 12 of the 50 apartments, so the human comparison is limited."

Note: caveat present in artifact

```python
def check(ctx):
    # Objection: human baseline covers only 12 of 50 apartments
    s = ctx.find('framing', r'human baseline covers only 12 of the 50 apartments')
    if not s: return ctx.ok(None, None, 'no such caveat in the scan framing for this story')
    if ctx.art_has(r'(12|twelve) apartments'): return ctx.ok('framing', s, 'caveat present in artifact')
    return ctx.fail('framing', s, 'artifact never states this caveat (human baseline covers only 12 of 50 apartments)')
```

### PASS · os4-blueprint-operator (objection, Blueprint)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-20/neon/audit/sources/2026-11-20/scan-framing.txt)): "framing (Andon Labs): Benchmark operator's own leaderboard; the human baseline covers only 12 of the 50 apartments, so the human comparison is limited."

Note: caveat present in artifact

```python
def check(ctx):
    # Objection: leaderboard is run by the benchmark operator (named as source)
    s = ctx.find('framing', r'Benchmark operator.s own leaderboard')
    if not s: return ctx.ok(None, None, 'no such caveat in the scan framing for this story')
    if ctx.art_has(r"andon labs'? blueprint|andon labs|on blueprint-bench"): return ctx.ok('framing', s, 'caveat present in artifact')
    return ctx.fail('framing', s, 'artifact never states this caveat (leaderboard is run by the benchmark operator (named as source))')
```

### PASS · s01-alphaxiv-watched (attribution, Society)
> Claim: alphaXiv watched 936 AI agents run their own preprint server

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "Today we're launching a preprint server built specifically for AI agents … For three months, nearly 1,000 agents from 35 labs (across Stanford, MIT, ETH Zurich, and more) conducted research autonomously on this server, producing 936 papers alongside their code, data, and model weights."

Note: alphaXiv launched the server and co-led the study (alphaXiv/MIT/Stanford)

```python
def check(ctx):
    return ctx.require('society', r'Today we.re launching a preprint server built specifically for AI agents', r'nearly 1,000 agents from 35 labs .* on this server', note='alphaXiv launched the server and co-led the study (alphaXiv/MIT/Stanford)')
```

### PASS · s03-936-papers (number, Society)
> Claim: 936 papers

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "For three months, nearly 1,000 agents from 35 labs (across Stanford, MIT, ETH Zurich, and more) conducted research autonomously on this server, producing 936 papers alongside their code, data, and model weights."

```python
def check(ctx):
    return ctx.require('society', r'producing 936 papers')
```

### PASS · s05-honest-caveat (attribution, Society)
> Claim: text-only peer review couldn't tell an honest caveat from a hidden flaw

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "In effect they could not tell a disclosed weakness from a hidden one. [p19] A guest editor then translated 276 objections across 43 paper clusters into scripts that were run on the uploaded data."

```python
def check(ctx):
    return ctx.require('society', r'could not tell a disclosed weakness from a hidden one')
```

### PASS · s07-494 (number, Society)
> Claim: 49.4%

Source ([primary-alphaxiv-society-of-ai-scientists](https://www.alphaxiv.org/abs/2611.society-ai-scientists)): "For major objections, the scripts overturned the headline conclusion in 77 of 156 cases (49.4%); for minor objections, in 24 of 120 cases (20.0%). [p20] These are executed referee objections in this journal, not a random audit of all papers in the cohort."

```python
def check(ctx):
    return ctx.require('society', r'77 of 156 cases \(49\.4%\)')
```

### PASS · s08-airbnb-2b (attribution, Airbnb)
> Claim: Airbnb fine-tuned a tiny 2-billion-parameter Gemma model

Source ([primary-airbnb-gemma4-e2b-production-classifier-](https://airbnb.tech/ai-ml/frontier-quality-at-1-of-the-cost-a-production-benchmark-of-llm-classifiers/)): "We compare a fine-tuned classifier with 2 billion effective parameters (E2B) against open-weight and proprietary models on a held-out evaluation dataset of 10,000 weighted examples. … Fine-tuning Gemma4-E2B on hundreds of thousands of domain-specific examples lifts its F1 from 0.563 to 0.902, on par with the best proprietary models, while median latency stays at 35ms."

```python
def check(ctx):
    return ctx.require('airbnb', r'fine-tuned classifier with 2 billion effective parameters', r'Fine-tuning Gemma4-E2B')
```

### PASS · s09-matched-35ms-1pct (comparison, Airbnb)
> Claim: matched frontier APIs in 35 milliseconds at one percent of the cost

Source ([x-googlegemma](https://x.com/googlegemma/status/2123461832656781320)): "🎯 Quality: Jumped from 0.563 to 0.902 max F1, matching top frontier APIs … ⚡ Speed: 35ms median latency (85ms p99) vs. ~900ms for frontier models … 💸 Cost: ~1% of frontier API spend at high volume"

```python
def check(ctx):
    return ctx.require('gemma', r'matching top frontier APIs', r'35ms median latency', r'~1% of frontier API spend')
```

### PASS · s10-2700 (comparison, Airbnb)
> Claim: Even a 2,700-word prompt couldn't close the gap

Source ([primary-airbnb-gemma4-e2b-production-classifier-](https://airbnb.tech/ai-ml/frontier-quality-at-1-of-the-cost-a-production-benchmark-of-llm-classifiers/)): "Hundreds of thousands of in-domain examples did what a 2,700 word prompt couldn't."

```python
def check(ctx):
    return ctx.require('airbnb', r"2,700 word prompt couldn't")
```

### PASS · s11-examples-thresholds (number, Airbnb)
> Claim: Hundreds of thousands of real examples

Source ([primary-airbnb-gemma4-e2b-production-classifier-](https://airbnb.tech/ai-ml/frontier-quality-at-1-of-the-cost-a-production-benchmark-of-llm-classifiers/)): "Hundreds of thousands of in-domain examples did what a 2,700 word prompt couldn't. … Scores let you choose your tradeoff between recall and precision without rewriting the prompt."

```python
def check(ctx):
    return ctx.require('airbnb', r'hundreds of thousands of in-domain examples did what', r'Scores let you choose your tradeoff')
```

### PASS · s12-card-mega (comparison, Airbnb)
> Claim: Fine-tuning beat mega-prompts

Source ([primary-airbnb-gemma4-e2b-production-classifier-](https://airbnb.tech/ai-ml/frontier-quality-at-1-of-the-cost-a-production-benchmark-of-llm-classifiers/)): "Hundreds of thousands of in-domain examples did what a 2,700 word prompt couldn't."

```python
def check(ctx):
    return ctx.require('airbnb', r"Hundreds of thousands of in-domain examples did what a 2,700 word prompt couldn't")
```

### PASS · s13-astra-edged (comparison, Blueprint)
> Claim: GPT-6.2 Astra edged a human baseline tested on just twelve apartments

Source ([primary-andon-blueprint-bench-2-gpt62-astra](https://andonlabs.com/evals/blueprint-bench-2)): "1 GPT-6.2 Astra 0.614 … Human* 0.586 … *Human baseline tested on subset of 12 apartments only"

```python
def check(ctx):
    return ctx.require('blueprint', r'1 GPT-6\.2 Astra 0\.614', r'Human\* 0\.586', r'Human baseline tested on subset of 12 apartments')
```

### PASS · s14-robotics-zero (attribution, Blueprint)
> Claim: a dedicated robotics model scored zero

Source ([primary-andon-blueprint-bench-2-gpt62-astra](https://andonlabs.com/evals/blueprint-bench-2)): "Gemini Robotics-ER 1.6 0.000**"

```python
def check(ctx):
    return ctx.require('blueprint', r'Gemini Robotics-ER 1\.6 0\.000\*\*')
```

### PASS · s17-credit (attribution, Close)
> Claim: Sources: alphaXiv, Airbnb and Andon Labs.

Note: credit names the three primary-source outlets in index.json

```python
def check(ctx):
    return ctx.ok(None, None, 'credit names the three primary-source outlets in index.json')
```
