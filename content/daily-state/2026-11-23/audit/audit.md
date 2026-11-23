# Executable audit, Daily State of AI 2026-11-23

Each claim is tested by a deterministic Python check against snapshotted source texts and X posts. PASS = the source sentence quoted supports the claim; FAIL = the source contradicts it or a required caveat is missing; NEEDS-HUMAN = opinion or not decidable by string/number match.

| artifact | PASS | FAIL | NEEDS-HUMAN | ERROR |
|---|---|---|---|---|
| episode | 35 | 3 | 15 | 0 |
| takeaways | 17 | 1 | 1 | 0 |

## Sources
- `primary-openai-perplexity-common-limits`: [Perplexity and Intelligence](https://openai.com/index/perplexity-and-intelligence) (sha256 c2d36c1b97e6…)
- `x-sama`: [X post by @sama (Sam Altman)](https://x.com/sama/status/2124551594691932405) (sha256 f84c8be9de4d…)
- `x-gdb`: [X post by @gdb (Greg Brockman)](https://x.com/gdb/status/2124582684840399311) (sha256 61387e9ccd38…)
- `x-swyx`: [X post by @swyx (swyx)](https://x.com/swyx/status/2124583459356373052) (sha256 4dfa6b349178…)
- `x-deredleritt3r`: [X post by @deredleritt3r (prinz)](https://x.com/deredleritt3r/status/2124568402031435962) (sha256 10ad2904e40d…)
- `primary-lingsante-3-1-flash-open-medical-moe`: [inclusionAI/LingSante-3.1-flash](https://huggingface.co/inclusionAI/LingSante-3.1-flash) (sha256 0c59bc3719d1…)
- `x-antlingagi`: [X post by @AntLingAGI (Ant Ling)](https://x.com/AntLingAGI/status/2124523916819648945) (sha256 3b8f0d2210e4…)
- `x-unknown`: [X post by @unknown](https://x.com/unknown/status/2124549218995949967) (sha256 edf0b812d5d9…)
- `scan-framing`: [Morning X-first scan: verification framing per story](https://www.signalandnoise.email/content/daily-state/2026-11-23/audit/sources/2026-11-23/scan-framing.txt) (sha256 fa470a38f407…)

## episode

### FAIL · e03-openai-single-metric-limit (attribution, OpenAI Perplexity)
> Claim: OpenAI published its internal pretraining curve and proposed an industry-wide speed limit based on a single metric: perplexity

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "I further propose common limits, based on perplexity and other measurements, that developers are committed to not crossing until our ability to understand and monitor AI behavior achieves a certain concrete milestone (such as the development of a successor to CoT monitors)."

Note: OpenAI proposed common limits based on perplexity AND other measurements, not a single metric alone

```python
def check(ctx):
    return ctx.support_or_contradict(
        'openai',
        r'common limits.*based (?:solely |only )?on a single metric',
        r'propose common limits, based on perplexity and other measurements',
        'OpenAI proposed common limits based on perplexity AND other measurements, not a single metric alone'
    )
```

### FAIL · e45-eight-h200-full-precision (number, Ant Group LingSante)
> Claim: eight H200 GPUs—to run at full precision

Source ([x-antlingagi](https://x.com/AntLingAGI/status/2124523916819648945)): "@grok (0 likes): Official FP8 weights need multi-GPU server hardware: 8× H200 (TP8+EP8) or 4× GB300 (TP4+EP4) via SGLang."

Note: Sources specify 8x H200 for FP8 weights, not full precision

```python
def check(ctx):
    s = ctx.find('antlingagi', r'Official FP8 weights.*8.?\s*H200')
    if s and ctx.absent('lingsante', r'full precision'):
        return ctx.fail('antlingagi', s, 'Sources specify 8x H200 for FP8 weights, not full precision')
    return ctx.require('lingsante', r'8\s*[×x]\s*H200', r'full precision')
```

### FAIL · oe2-openai-no-other-lab (objection, OpenAI Perplexity)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-23/audit/sources/2026-11-23/scan-framing.txt)): "framing (OpenAI): Company-authored proposal using OpenAI's own internal-codebase measurements; no other lab has committed and the numbers are not independently reproducible."

Note: Episode omits caveat that no other lab has committed to the proposed limits

```python
def check(ctx):
    s = ctx.find('framing', r'no other lab has committed')
    if ctx.art_has(r'no other lab|other labs have not|not (?:yet )?committed|unilateral'):
        return ctx.ok('framing', s, 'Episode notes that no other lab has committed to OpenAI\'s proposal')
    return ctx.fail('framing', s, 'Episode omits caveat that no other lab has committed to the proposed limits')
```

### NEEDS-HUMAN · e01-broadcast-date (number, Overview)
> Claim: November 23, 2026

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "November 22, 2026"

Note: Episode date November 23, 2026 is not in source texts; OpenAI post is dated November 22, 2026

```python
def check(ctx):
    s = ctx.find('openai', r'November 22, 2026')
    return ctx.need('openai', s, 'Episode date November 23, 2026 is not in source texts; OpenAI post is dated November 22, 2026')
```

### NEEDS-HUMAN · e02-two-stories-24h (number, Overview)
> Claim: Two big stories landed in AI over the past twenty-four hours

Note: Editorial count and 24-hour timing relative to broadcast date cannot be verified from source text alone

```python
def check(ctx):
    return ctx.need(None, None, 'Editorial count and 24-hour timing relative to broadcast date cannot be verified from source text alone')
```

### NEEDS-HUMAN · e06-separate-news-cycles (qualifier, Overview)
> Claim: Most people are treating these as two separate news cycles

Note: Editorial observation about public reception; not verifiable from sources

```python
def check(ctx):
    return ctx.need(None, None, 'Editorial observation about public reception; not verifiable from sources')
```

### NEEDS-HUMAN · e07-exact-same-day (qualifier, Overview)
> Claim: on the exact same day

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "November 22, 2026"

Note: OpenAI post is dated November 22, 2026, but LingSante sources do not print a calendar date in text

```python
def check(ctx):
    s = ctx.find('openai', r'November 22, 2026')
    return ctx.need('openai', s, 'OpenAI post is dated November 22, 2026, but LingSante sources do not print a calendar date in text')
```

### NEEDS-HUMAN · e10-lower-better-compression-training-data (comparison, OpenAI Perplexity)
> Claim: Lower numbers mean better compression of the training data

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "2, 3 Perplexity measures how well a model predicts the next token on average; lower perplexity means better predictions. … The primary way we measure progress on this key "intelligence substrate" has remained remarkably constant over the years-we have been tracking the perplexity of the models on a held-out dataset."

Note: Source ties lower perplexity to better predictions and to compression by predicting unseen or held-out data, not to compression of the training data

```python
def check(ctx):
    s_train = ctx.find('openai', r'compression of (?:the )?training data')
    if s_train:
        return ctx.ok('openai', s_train)
    s_lower = ctx.find('openai', r'lower perplexity means better (predictions|compression)')
    s_held = ctx.find('openai', r'held-out dataset|predicting unseen data')
    if s_lower and s_held:
        return ctx.need(
            'openai',
            ' … '.join([s_lower, s_held]),
            'Source ties lower perplexity to better predictions and to compression by predicting unseen or held-out data, not to compression of the training data',
        )
    if s_lower:
        return ctx.ok('openai', s_lower)
    return ctx.need('openai', None, 'Could not find source support for lower numbers meaning better compression')
```

### NEEDS-HUMAN · e11-pachocki-whole-arc (attribution, OpenAI Perplexity)
> Claim: Pachocki argues that this single curve explains the whole arc of modern AI

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "I believe tracking the pace of progress on training better compressors is key to understanding the arc of advances in AI."

Note: Source says tracking better compressors is "key to understanding the arc" and "largely described" by perplexity, while noting it omits post-training; human check needed on "whole arc"

```python
def check(ctx):
    s = ctx.find('openai', r'key to understanding the arc of advances in AI')
    return ctx.need('openai', s, 'Source says tracking better compressors is "key to understanding the arc" and "largely described" by perplexity, while noting it omits post-training; human check needed on "whole arc"')
```

### NEEDS-HUMAN · e26-unusually-candid-warning (opinion, OpenAI Perplexity)
> Claim: It is an unusually candid warning

Note: Editorial opinion; not verifiable from sources

```python
def check(ctx):
    return ctx.need(None, None, 'Editorial opinion; not verifiable from sources')
```

### NEEDS-HUMAN · e27-two-glaring-blind-spots (number, OpenAI Perplexity)
> Claim: two glaring blind spots

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "Perplexity as a shared metric has challenges:"

Note: Editorial framing selecting two blind spots; OpenAI post lists four challenges

```python
def check(ctx):
    s = ctx.find('openai', r'Perplexity as a shared metric has challenges')
    return ctx.need('openai', s, 'Editorial framing selecting two blind spots; OpenAI post lists four challenges')
```

### NEEDS-HUMAN · e33-cot-rl-tool-use-perplexity (qualifier, OpenAI Perplexity)
> Claim: Chain-of-thought reasoning, reinforcement learning, and tool use do not lower base-model perplexity

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "Most notably, chain-of-thought reasoning does not reduce perplexity achieved by the model, even though it leads to a drastic increase in capabilities. … - Not accounting for advances outside of pretraining."

Note: Source says chain-of-thought reasoning does not reduce perplexity and that the metric does not account for advances outside of pretraining, but it does not explicitly say reinforcement learning and tool use do not lower base-model perplexity

```python
def check(ctx):
    s_cot = ctx.find('openai', r'chain-of-thought reasoning does not reduce perplexity')
    s_rl = ctx.find('openai', r'reinforcement learning.{0,80}does not (?:reduce|lower) (?:base-model )?perplexity|does not (?:reduce|lower) (?:base-model )?perplexity.{0,80}reinforcement learning')
    s_tool = ctx.find('openai', r'tool use.{0,80}does not (?:reduce|lower) (?:base-model )?perplexity|does not (?:reduce|lower) (?:base-model )?perplexity.{0,80}tool use')
    s_outside = ctx.find('openai', r'Not accounting for advances outside of pretraining')
    found = [s for s in (s_cot, s_rl, s_tool) if s]
    if s_cot and s_rl and s_tool:
        return ctx.ok('openai', ' … '.join(found))
    if s_cot or s_outside:
        return ctx.need(
            'openai',
            ' … '.join([s for s in (s_cot, s_outside) if s]),
            'Source says chain-of-thought reasoning does not reduce perplexity and that the metric does not account for advances outside of pretraining, but it does not explicitly say reinforcement learning and tool use do not lower base-model perplexity',
        )
    return ctx.need('openai', None, 'Could not confirm that CoT, RL, and tool use do not lower base-model perplexity')
```

### NEEDS-HUMAN · e40-model-card-more-grounded (comparison, Ant Group LingSante)
> Claim: the model card tells a more grounded story than the launch post

Note: Editorial comparison of tone between model card and launch post

```python
def check(ctx):
    return ctx.need(None, None, 'Editorial comparison of tone between model card and launch post')
```

### NEEDS-HUMAN · e41-ant-own-inclusionmed (qualifier, Ant Group LingSante)
> Claim: on Ant's own InclusionMed benchmark

Source ([primary-lingsante-3-1-flash-open-medical-moe](https://huggingface.co/inclusionAI/LingSante-3.1-flash)): "Performance and Cost : LingSante-3.1-Flash lies on the performance-cost Pareto frontier of the InclusionMed medical AI benchmark."

Note: Model card cites InclusionMed under inclusionAI org, but does not explicitly state InclusionMed is Ant Group's own benchmark

```python
def check(ctx):
    s = ctx.find('lingsante', r'InclusionMed medical AI benchmark')
    return ctx.need('lingsante', s, 'Model card cites InclusionMed under inclusionAI org, but does not explicitly state InclusionMed is Ant Group\'s own benchmark')
```

### NEEDS-HUMAN · e47-lingsante-training-recipe (qualifier, Ant Group LingSante-3.1-flash)
> Claim: through medical-mixed training, task-specific reinforcement learning, multi-step tool workflows, and multi-teacher on-policy distillation

Source ([primary-lingsante-3-1-flash-open-medical-moe](https://huggingface.co/inclusionAI/LingSante-3.1-flash)): "To address these demands, LingSante-3.1-flash is trained to unify medical reasoning and workflow execution through native medical-mixed pretraining, mid-training, supervised fine-tuning, task-specific reinforcement learning, and multi-teacher on-policy distillation. … To address these demands, LingSante-3.1-flash is trained to unify medical reasoning and workflow execution through native medical-mixed pretraining, mid-training, supervised fine-tuning, task-specific reinforcement learning, and multi-teacher on-policy distillation. … To address these demands, LingSante-3.1-flash is trained to unify medical reasoning and workflow execution through native medical-mixed pretraining, mid-training, supervised fine-tuning, task-specific reinforcement learning, and multi-teacher on-policy distillation."

Note: Model card supports medical-mixed pretraining, task-specific reinforcement learning, and multi-teacher on-policy distillation, but does not list "multi-step tool workflows" as a training method (tool use appears as a post-training target; "multi-stage workflows" is a capability)

```python
def check(ctx):
    s1 = ctx.find('lingsante', r'medical-mixed pretraining')
    s2 = ctx.find('lingsante', r'task-specific reinforcement learning')
    s3 = ctx.find('lingsante', r'multi-teacher on-policy distillation')
    s_tool = ctx.find('lingsante', r'multi-step tool workflows|tool workflows')
    found = [s for s in (s1, s2, s3, s_tool) if s]
    if s1 and s2 and s3 and s_tool:
        return ctx.ok('lingsante', ' … '.join(found))
    if s1 and s2 and s3:
        return ctx.need(
            'lingsante',
            ' … '.join(found),
            'Model card supports medical-mixed pretraining, task-specific reinforcement learning, and multi-teacher on-policy distillation, but does not list "multi-step tool workflows" as a training method (tool use appears as a post-training target; "multi-stage workflows" is a capability)',
        )
    return ctx.need('lingsante', found[0] if found else None, 'Could not match the stated training recipe')
```

### NEEDS-HUMAN · e48-recursive-research-oversight-2027 (number, OpenAI Perplexity)
> Claim: recursive AI research could outrun human oversight by 2027

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "While this field relies more on experimentation, there is a long history of simple insights being missed for years; and so as soon as 2027 we could conceivably see a similar avalanche of fundamental pretraining advancements 5."

Note: OpenAI warns of 2027 pretraining breakthroughs outpacing alignment/monitoring, while distinguishing this from full recursive self-improvement with no human oversight

```python
def check(ctx):
    s = ctx.find('openai', r'as soon as 2027.*avalanche of fundamental pretraining advancements')
    return ctx.need('openai', s, 'OpenAI warns of 2027 pretraining breakthroughs outpacing alignment/monitoring, while distinguishing this from full recursive self-improvement with no human oversight')
```

### NEEDS-HUMAN · e49-real-risk-opinion (opinion, Overview)
> Claim: That is a real risk

Note: Editorial opinion; not verifiable from sources

```python
def check(ctx):
    return ctx.need(None, None, 'Editorial opinion; not verifiable from sources')
```

### NEEDS-HUMAN · e50-speed-limit-not-pause-race (opinion, Overview)
> Claim: A speed limit on perplexity might slow down the next unknown leap, but it will not pause the race

Note: Editorial opinion; not verifiable from sources

```python
def check(ctx):
    return ctx.need(None, None, 'Editorial opinion; not verifiable from sources')
```

### PASS · e04-ant-released-lingsante (attribution, Ant Group LingSante)
> Claim: Ant Group released an open-weight medical model called LingSante-3.1-flash

Source ([x-antlingagi](https://x.com/AntLingAGI/status/2124523916819648945)): "@AntLingAGI: Today, we release LingSante-3.1-flash, an open-weight MoE model with 560B total parameters and 25B activations per token."

Note: Confirmed release of open-weight medical model LingSante-3.1-flash

```python
def check(ctx):
    s1 = ctx.find('antlingagi', r'release LingSante-3\.1-flash, an open-weight')
    s2 = ctx.find('lingsante', r'LingSante-3\.1-flash is an open-weight.*medical')
    if s1 and s2:
        return ctx.ok('antlingagi', s1, 'Confirmed release of open-weight medical model LingSante-3.1-flash')
    return ctx.need('antlingagi', s1 or s2, 'Could not match release and medical open-weight description')
```

### PASS · e05-lingsante-beats-frontier (comparison, Ant Group LingSante)
> Claim: it says beats GPT-6 Astra, Claude Opus 5.5, and Gemini 4 Argon on several tough benchmarks

Source ([x-antlingagi](https://x.com/AntLingAGI/status/2124523916819648945)): "The model leads on HealthBench Professional (65.72), HLE (text-only, with tools: 72.22) and BrowseComp (with context: 94.10), outperforming GPT-6 Astra, Claude Opus 5.5 and Gemini 4 Argon on all three."

```python
def check(ctx):
    return ctx.require('antlingagi', r'outperforming GPT-6 Astra, Claude Opus 5\.5 and Gemini 4 Argon on all three')
```

### PASS · e08-pachocki-essay (attribution, OpenAI Perplexity)
> Claim: Chief Scientist Jakub Pachocki published an essay called Perplexity and Intelligence

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "Perplexity and Intelligence | OpenAI … By Jakub Pachocki, Chief Scientist at OpenAI"

```python
def check(ctx):
    return ctx.require('openai', r'Perplexity and Intelligence', r'By Jakub Pachocki, Chief Scientist at OpenAI')
```

### PASS · e09-altman-brockman-backing (attribution, OpenAI Perplexity)
> Claim: backed publicly by Sam Altman and Greg Brockman

Source ([x-sama](https://x.com/sama/status/2124551594691932405)): "@sama: This is the most important thing OpenAI has published in awhile."

Note: Both Sam Altman and Greg Brockman publicly endorsed the post

```python
def check(ctx):
    s1 = ctx.find('sama', r'most important thing OpenAI has published')
    s2 = ctx.find('gdb', r'foundation of industry-wide shared safety bars')
    if s1 and s2:
        return ctx.ok('sama', s1, 'Both Sam Altman and Greg Brockman publicly endorsed the post')
    return ctx.need('sama', s1 or s2, 'Could not confirm public backing from both Altman and Brockman')
```

### PASS · e12-main-held-out-dataset (qualifier, OpenAI Perplexity)
> Claim: On OpenAI's main held-out evaluation dataset

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "The primary way we measure progress on this key "intelligence substrate" has remained remarkably constant over the years-we have been tracking the perplexity of the models on a held-out dataset. … GPT-3.5, at a log-perplexity of ~0.99 on our current main evaluation dataset, was capable of fluent conversation and formed the basis for the original ChatGPT."

```python
def check(ctx):
    return ctx.require('openai', r'held-out dataset', r'main evaluation dataset')
```

### PASS · e13-gpt35-099 (number, OpenAI Perplexity)
> Claim: GPT-3.5 sat around zero point nine nine

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "GPT-3.5, at a log-perplexity of ~0.99 on our current main evaluation dataset, was capable of fluent conversation and formed the basis for the original ChatGPT."

```python
def check(ctx):
    return ctx.require('openai', r'GPT.?3\.5.*~0\.99')
```

### PASS · e14-gpt4-091 (number, OpenAI Perplexity)
> Claim: GPT-4 hit about zero point nine one

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "GPT-4, at ~0.91, was proficient at utilizing chain-of-thought reasoning productively, which motivated the subsequent targeted elicitation of this capability and the creation of modern reasoning models."

```python
def check(ctx):
    return ctx.require('openai', r'GPT.?4.*~0\.91')
```

### PASS · e15-below-08-cyber-math (number, OpenAI Perplexity)
> Claim: Dropping below zero point eight brought transformative capabilities in cybersecurity and math

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "Now, as we have reached losses below 0.8, we have seen the emergence of transformative capabilities in fields like cybersecurity and mathematics."

```python
def check(ctx):
    return ctx.require('openai', r'below 0\.8.*transformative capabilities.*cybersecurity and mathematics')
```

### PASS · e16-model-around-076 (number, OpenAI Perplexity)
> Claim: a model around zero point seven six

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "Once we upgraded to a model of log-perplexity ~0.76, it started producing groundbreaking results."

```python
def check(ctx):
    return ctx.require('openai', r'model of log-perplexity ~0\.76')
```

### PASS · e17-open-math-slack-thread (attribution, OpenAI Perplexity)
> Claim: Pachocki says it began solving open mathematics problems one after another in a single Slack thread

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "For more than a year, we have been posing open problems in mathematics to our models as one of the ways of evaluating them. … For many of us that have previously worked in mathematics and adjacent fields, seeing the resolutions to questions we've long thought about coming out of the model one after another in a single Slack thread felt deeply surreal."

```python
def check(ctx):
    return ctx.require('openai', r'open problems in mathematics', r'one after another in a single Slack thread')
```

### PASS · e18-curve-accelerated-2026 (number, OpenAI Perplexity)
> Claim: OpenAI's curve accelerated sharply in 2026

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "On the plot of losses of OpenAI models, you can see a steep acceleration in 2026."

```python
def check(ctx):
    return ctx.require('openai', r'steep acceleration in 2026')
```

### PASS · e19-ai-design-contributions (attribution, OpenAI Perplexity)
> Claim: Pachocki notes that AI is already making meaningful design contributions to their latest models

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "However, for the most recent models, we have already seen meaningful design contributions coming from AI⁠."

```python
def check(ctx):
    return ctx.require('openai', r'most recent models.*meaningful design contributions coming from AI')
```

### PASS · e20-2027-avalanche-pretraining (attribution, OpenAI Perplexity)
> Claim: He warns that as soon as 2027, we could see an avalanche of AI-driven breakthroughs in pretraining research

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "While this field relies more on experimentation, there is a long history of simple insights being missed for years; and so as soon as 2027 we could conceivably see a similar avalanche of fundamental pretraining advancements 5."

```python
def check(ctx):
    return ctx.require('openai', r'as soon as 2027.*avalanche of fundamental pretraining advancements')
```

### PASS · e21-faster-than-alignment (comparison, OpenAI Perplexity)
> Claim: faster than alignment and monitoring can keep up

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "While I expect AI will also significantly contribute to progress on alignment and monitoring, I think that progress is unlikely to be fast enough to allow the full potential acceleration in pretraining."

```python
def check(ctx):
    return ctx.require('openai', r'progress on alignment and monitoring.*unlikely to be fast enough to allow the full potential acceleration in pretraining')
```

### PASS · e22-068-to-070-window (number, OpenAI Perplexity)
> Claim: the zero point six eight to zero point seven zero window

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "Extrapolating from recent progress, we should expect further transformative capabilities as we enter the ~0.68-0.7 log-perplexity window."

```python
def check(ctx):
    return ctx.require('openai', r'~0\.68[-–]0\.70?\s+log-perplexity window')
```

### PASS · e23-unpredictable-capabilities (attribution, OpenAI Perplexity)
> Claim: he expects new, unpredictable capabilities to emerge

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "Extrapolating from recent progress, we should expect further transformative capabilities as we enter the ~0.68-0.7 log-perplexity window. … I don't know what those capabilities will be, and we may not be testing for them today."

```python
def check(ctx):
    return ctx.require('openai', r'expect further transformative capabilities', r'don.t know what those capabilities will be')
```

### PASS · e24-evaluation-awareness (comparison, OpenAI Perplexity)
> Claim: models become more aware they are being evaluated

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "At the same time, we should also expect further degradation⁠(opens in a new window) in currently dominant forms of alignment auditing and further increases in evaluation and training awareness."

```python
def check(ctx):
    return ctx.require('openai', r'further increases in evaluation and training awareness')
```

### PASS · e25-common-limits-cot-monitors (attribution, OpenAI Perplexity)
> Claim: OpenAI is proposing common industry limits: agree not to cross certain perplexity thresholds until safety monitoring hits concrete milestones, like a successor to chain-of-thought monitors

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "I further propose common limits, based on perplexity and other measurements, that developers are committed to not crossing until our ability to understand and monitor AI behavior achieves a certain concrete milestone (such as the development of a successor to CoT monitors)."

```python
def check(ctx):
    return ctx.require('openai', r'propose common limits.*not crossing until.*concrete milestone.*successor to CoT monitors')
```

### PASS · e28-pachocki-acknowledges-both (attribution, OpenAI Perplexity)
> Claim: both of which Pachocki himself acknowledges

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "- Difficulty of comparison across labs. … - Not accounting for advances outside of pretraining."

```python
def check(ctx):
    return ctx.require('openai', r'Difficulty of comparison across labs', r'Not accounting for advances outside of pretraining')
```

### PASS · e29-hard-to-compare-across-labs (comparison, OpenAI Perplexity)
> Claim: perplexity is notoriously hard to compare across labs

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "- Difficulty of comparison across labs."

```python
def check(ctx):
    return ctx.require('openai', r'Difficulty of comparison across labs')
```

### PASS · e30-snapshot-internal-codebase (qualifier, OpenAI Perplexity)
> Claim: OpenAI's numbers are measured on a snapshot of its own internal codebase

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "The primary held-out datasets we've been using since GPT-3.5 are sourced from our internal codebase, and those are the numbers reported here (for a fixed snapshot)."

```python
def check(ctx):
    return ctx.require('openai', r'sourced from our internal codebase.*fixed snapshot')
```

### PASS · e31-outside-commenters-tokenizers (attribution, OpenAI Perplexity)
> Claim: as outside commenters quickly pointed out, different labs use different tokenizers and data mixtures

Source ([x-sama](https://x.com/sama/status/2124551594691932405)): "@shengyuchufeng (0 likes): @sama Perplexity is the wrong scoreboard for cross-lab comparison - every lab tokenizes and trains differently, so the same number means different things."

Note: Outside reply cites different tokenizers/training and OpenAI notes different data mixtures

```python
def check(ctx):
    s1 = ctx.find('sama', r'every lab tokenizes and trains differently')
    s2 = ctx.find('openai', r'different data mixtures')
    if s1 and s2:
        return ctx.ok('sama', s1, 'Outside reply cites different tokenizers/training and OpenAI notes different data mixtures')
    return ctx.need('sama', s1 or s2, 'Could not confirm both tokenizer and data-mixture points')
```

### PASS · e32-does-not-measure-post-training (qualifier, OpenAI Perplexity)
> Claim: perplexity does not measure post-training

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "- Not accounting for advances outside of pretraining."

```python
def check(ctx):
    return ctx.require('openai', r'Not accounting for advances outside of pretraining')
```

### PASS · e34-open-weight-moe (qualifier, Ant Group LingSante)
> Claim: open-weight mixture-of-experts model

Source ([primary-lingsante-3-1-flash-open-medical-moe](https://huggingface.co/inclusionAI/LingSante-3.1-flash)): "LingSante-3.1-flash is an open-weight Mixture-of-Experts model that combines complex medical reasoning, professional healthcare communication, evidence-based deep research, and long-horizon medical tasks."

```python
def check(ctx):
    return ctx.require('lingsante', r'open-weight Mixture-of-Experts model')
```

### PASS · e35-560b-total-params (number, Ant Group LingSante)
> Claim: 560 billion total parameters

Source ([primary-lingsante-3-1-flash-open-medical-moe](https://huggingface.co/inclusionAI/LingSante-3.1-flash)): "Built on Ling-3.1-flash, it has 560 billion total parameters, activates 25 billion parameters per token, and supports a 1-million-token context window."

```python
def check(ctx):
    return ctx.require('lingsante', r'560 billion total parameters')
```

### PASS · e36-25b-active-per-token (number, Ant Group LingSante)
> Claim: 25 billion active per token

Source ([primary-lingsante-3-1-flash-open-medical-moe](https://huggingface.co/inclusionAI/LingSante-3.1-flash)): "Built on Ling-3.1-flash, it has 560 billion total parameters, activates 25 billion parameters per token, and supports a 1-million-token context window."

```python
def check(ctx):
    return ctx.require('lingsante', r'activates 25 billion parameters per token')
```

### PASS · e37-1m-context-window (number, Ant Group LingSante)
> Claim: a one-million-token context window

Source ([primary-lingsante-3-1-flash-open-medical-moe](https://huggingface.co/inclusionAI/LingSante-3.1-flash)): "Built on Ling-3.1-flash, it has 560 billion total parameters, activates 25 billion parameters per token, and supports a 1-million-token context window."

```python
def check(ctx):
    return ctx.require('lingsante', r'1-million-token context window')
```

### PASS · e38-ant-reported-three-benchmarks (comparison, Ant Group LingSante)
> Claim: In its announcement, Ant reports scores that top GPT-6 Astra, Claude Opus 5.5, and Gemini 4 Argon on HealthBench Professional, text-only Humanity's Last Exam with tools, and BrowseComp with context

Source ([x-antlingagi](https://x.com/AntLingAGI/status/2124523916819648945)): "The model leads on HealthBench Professional (65.72), HLE (text-only, with tools: 72.22) and BrowseComp (with context: 94.10), outperforming GPT-6 Astra, Claude Opus 5.5 and Gemini 4 Argon on all three."

```python
def check(ctx):
    return ctx.require('antlingagi', r'HealthBench Professional.*HLE \(text-only, with tools.*BrowseComp \(with context.*outperforming GPT-6 Astra, Claude Opus 5\.5 and Gemini 4 Argon on all three')
```

### PASS · e39-self-reported (qualifier, Ant Group LingSante)
> Claim: They are self-reported

Source ([x-antlingagi](https://x.com/AntLingAGI/status/2124523916819648945)): "AFFILIATION NOTE (scan): Developer's own account; benchmark numbers are self-reported."

```python
def check(ctx):
    return ctx.require('antlingagi', r'benchmark numbers are self-reported')
```

### PASS · e42-ranks-fifth-of-23 (number, Ant Group LingSante)
> Claim: LingSante actually ranks fifth out of twenty-three configurations

Source ([primary-lingsante-3-1-flash-open-medical-moe](https://huggingface.co/inclusionAI/LingSante-3.1-flash)): "With an overall score of 45.064, it ranked fifth among the 23 model configurations evaluated, delivering competitive performance on medical tasks at a relatively low inference cost."

```python
def check(ctx):
    return ctx.require('lingsante', r'ranked fifth among the 23 model configurations evaluated')
```

### PASS · e43-prized-cost-efficiency (qualifier, Ant Group LingSante)
> Claim: prized mainly for cost efficiency

Source ([primary-lingsante-3-1-flash-open-medical-moe](https://huggingface.co/inclusionAI/LingSante-3.1-flash)): "Performance and Cost : LingSante-3.1-Flash lies on the performance-cost Pareto frontier of the InclusionMed medical AI benchmark. … With an overall score of 45.064, it ranked fifth among the 23 model configurations evaluated, delivering competitive performance on medical tasks at a relatively low inference cost."

```python
def check(ctx):
    return ctx.require('lingsante', r'performance.cost Pareto frontier', r'relatively low inference cost')
```

### PASS · e44-trails-gpt6-medical-behavior (comparison, Ant Group LingSante)
> Claim: it trails GPT-6 Astra on medical professional behavior

Source ([primary-lingsante-3-1-flash-open-medical-moe](https://huggingface.co/inclusionAI/LingSante-3.1-flash)): "LingSante-3.1-flash demonstrates strong performance on benchmarks for medical professional behavior, ranking second overall behind only GPT-6 Astra."

```python
def check(ctx):
    return ctx.require('lingsante', r'medical professional behavior, ranking second overall behind only GPT-6 Astra')
```

### PASS · e46-research-not-clinical-diagnosis (attribution, Ant Group LingSante)
> Claim: Ant explicitly warns it is for research, not clinical diagnosis

Source ([primary-lingsante-3-1-flash-open-medical-moe](https://huggingface.co/inclusionAI/LingSante-3.1-flash)): "> LingSante-3.1-flash is intended for research and evaluation. … It is not a medical device and must not be used as an independent basis for diagnosis, prescriptions, or treatment."

```python
def check(ctx):
    return ctx.require('lingsante', r'intended for research and evaluation', r'must not be used as an independent basis for diagnosis')
```

### PASS · oe1-openai-company-reported (objection, OpenAI Perplexity)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-23/audit/sources/2026-11-23/scan-framing.txt)): "framing (OpenAI): Company-authored proposal using OpenAI's own internal-codebase measurements; no other lab has committed and the numbers are not independently reproducible."

Note: Episode notes OpenAI numbers are from its own internal codebase / company-reported

```python
def check(ctx):
    s = ctx.find('framing', r'Company-authored proposal.*internal-codebase measurements')
    if ctx.art_has(r'internal codebase|company[- ]reported|self[- ]reported|not independently reproduc'):
        return ctx.ok('framing', s, 'Episode notes OpenAI numbers are from its own internal codebase / company-reported')
    return ctx.fail('framing', s, 'Episode omits caveat that OpenAI measurements are company-reported / internal-codebase and not independently reproducible')
```

### PASS · oe3-lingsante-company-reported (objection, Ant Group LingSante)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-23/audit/sources/2026-11-23/scan-framing.txt)): "framing (Hugging Face (inclusionAI model card)): Developer model card; weights are public, benchmark results are company-reported and not independently reproduced."

Note: Episode notes LingSante benchmark results are self-reported

```python
def check(ctx):
    s = ctx.find('framing', r'benchmark results are company-reported and not independently reproduced')
    if ctx.art_has(r'self[- ]reported|company[- ]reported|vendor[- ]reported|not independently (?:reproduc|verif)'):
        return ctx.ok('framing', s, 'Episode notes LingSante benchmark results are self-reported')
    return ctx.fail('framing', s, 'Episode omits caveat that LingSante benchmark results are company-reported / not independently reproduced')
```

## takeaways

### FAIL · ot2-openai-no-other-lab (objection, OpenAI perplexity warning)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-23/audit/sources/2026-11-23/scan-framing.txt)): "framing (OpenAI): Company-authored proposal using OpenAI's own internal-codebase measurements; no other lab has committed and the numbers are not independently reproducible."

Note: Takeaways omit caveat that no other lab has committed to the proposed limits

```python
def check(ctx):
    s = ctx.find('framing', r'no other lab has committed')
    if ctx.art_has(r'no other lab|other labs have not|not (?:yet )?committed|unilateral'):
        return ctx.ok('framing', s, 'Takeaways note that no other lab has committed to OpenAI\'s proposal')
    return ctx.fail('framing', s, 'Takeaways omit caveat that no other lab has committed to the proposed limits')
```

### NEEDS-HUMAN · t11-ant-own-inclusionmed (attribution, Ant Group LingSante-3.1-flash)
> Claim: on Ant's own InclusionMed benchmark

Source ([primary-lingsante-3-1-flash-open-medical-moe](https://huggingface.co/inclusionAI/LingSante-3.1-flash)): "Performance and Cost : LingSante-3.1-Flash lies on the performance-cost Pareto frontier of the InclusionMed medical AI benchmark."

Note: Model card cites InclusionMed under inclusionAI org, but does not explicitly state InclusionMed is Ant Group's own benchmark

```python
def check(ctx):
    s = ctx.find('lingsante', r'InclusionMed medical AI benchmark')
    return ctx.need('lingsante', s, 'Model card cites InclusionMed under inclusionAI org, but does not explicitly state InclusionMed is Ant Group\'s own benchmark')
```

### PASS · ot1-openai-company-reported (objection, OpenAI perplexity warning)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-23/audit/sources/2026-11-23/scan-framing.txt)): "framing (OpenAI): Company-authored proposal using OpenAI's own internal-codebase measurements; no other lab has committed and the numbers are not independently reproducible."

Note: Takeaways note OpenAI internal/company-reported measurements

```python
def check(ctx):
    s = ctx.find('framing', r'Company-authored proposal.*internal-codebase measurements')
    if ctx.art_has(r'internal (?:held-out|codebase)|company[- ]reported|self[- ]reported|not independently reproduc'):
        return ctx.ok('framing', s, 'Takeaways note OpenAI internal/company-reported measurements')
    return ctx.fail('framing', s, 'Takeaways omit caveat that OpenAI measurements are company-reported / internal-codebase')
```

### PASS · ot3-lingsante-company-reported (objection, Ant Group LingSante-3.1-flash)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-23/audit/sources/2026-11-23/scan-framing.txt)): "framing (Hugging Face (inclusionAI model card)): Developer model card; weights are public, benchmark results are company-reported and not independently reproduced."

Note: Takeaways note LingSante benchmark results are self-reported

```python
def check(ctx):
    s = ctx.find('framing', r'benchmark results are company-reported and not independently reproduced')
    if ctx.art_has(r'self[- ]reported|company[- ]reported|vendor[- ]reported|not independently (?:reproduc|verif)'):
        return ctx.ok('framing', s, 'Takeaways note LingSante benchmark results are self-reported')
    return ctx.fail('framing', s, 'Takeaways omit caveat that LingSante benchmark results are company-reported / not independently reproduced')
```

### PASS · t01-openai-internal-held-out (attribution, OpenAI perplexity warning)
> Claim: OpenAI, citing its internal held-out dataset, warns

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "The primary held-out datasets we've been using since GPT-3.5 are sourced from our internal codebase, and those are the numbers reported here (for a fixed snapshot)."

```python
def check(ctx):
    return ctx.require('openai', r'held-out datasets?.*internal codebase')
```

### PASS · t02-068-070-window (number, OpenAI perplexity warning)
> Claim: 0.68 to 0.70 log-perplexity window

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "Extrapolating from recent progress, we should expect further transformative capabilities as we enter the ~0.68-0.7 log-perplexity window."

```python
def check(ctx):
    return ctx.require('openai', r'~0\.68[-–]0\.70?\s+log-perplexity window')
```

### PASS · t03-unpredictable-capabilities (qualifier, OpenAI perplexity warning)
> Claim: unpredictable capabilities could emerge

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "Extrapolating from recent progress, we should expect further transformative capabilities as we enter the ~0.68-0.7 log-perplexity window. … I don't know what those capabilities will be, and we may not be testing for them today."

```python
def check(ctx):
    return ctx.require('openai', r'expect further transformative capabilities', r'don.t know what those capabilities will be')
```

### PASS · t04-2027-outrun-alignment (number, OpenAI perplexity warning)
> Claim: AI-driven pretraining breakthroughs could outrun alignment by 2027

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "While this field relies more on experimentation, there is a long history of simple insights being missed for years; and so as soon as 2027 we could conceivably see a similar avalanche of fundamental pretraining advancements 5. … While I expect AI will also significantly contribute to progress on alignment and monitoring, I think that progress is unlikely to be fast enough to allow the full potential acceleration in pretraining."

```python
def check(ctx):
    return ctx.require('openai', r'as soon as 2027.*avalanche of fundamental pretraining advancements', r'progress on alignment and monitoring.*unlikely to be fast enough')
```

### PASS · t05-proposes-industry-limits (attribution, OpenAI perplexity warning)
> Claim: proposes industry limits until safety monitoring milestones are met

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "I further propose common limits, based on perplexity and other measurements, that developers are committed to not crossing until our ability to understand and monitor AI behavior achieves a certain concrete milestone (such as the development of a successor to CoT monitors)."

```python
def check(ctx):
    return ctx.require('openai', r'propose common limits.*not crossing until.*monitor AI behavior achieves a certain concrete milestone')
```

### PASS · t06-hard-to-compare-across-labs (qualifier, OpenAI perplexity warning)
> Claim: perplexity is hard to compare across labs

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "- Difficulty of comparison across labs."

```python
def check(ctx):
    return ctx.require('openai', r'Difficulty of comparison across labs')
```

### PASS · t07-does-not-measure-post-training (qualifier, OpenAI perplexity warning)
> Claim: does not measure post-training

Source ([primary-openai-perplexity-common-limits](https://openai.com/index/perplexity-and-intelligence)): "- Not accounting for advances outside of pretraining."

```python
def check(ctx):
    return ctx.require('openai', r'Not accounting for advances outside of pretraining')
```

### PASS · t08-ant-self-reported-results (attribution, Ant Group LingSante-3.1-flash)
> Claim: Ant Group's self-reported results claim

Source ([x-antlingagi](https://x.com/AntLingAGI/status/2124523916819648945)): "AFFILIATION NOTE (scan): Developer's own account; benchmark numbers are self-reported."

```python
def check(ctx):
    return ctx.require('antlingagi', r'benchmark numbers are self-reported')
```

### PASS · t09-560b-open-weight-lingsante (number, Ant Group LingSante-3.1-flash)
> Claim: 560B open-weight LingSante-3.1-flash

Source ([x-antlingagi](https://x.com/AntLingAGI/status/2124523916819648945)): "@AntLingAGI: Today, we release LingSante-3.1-flash, an open-weight MoE model with 560B total parameters and 25B activations per token."

```python
def check(ctx):
    return ctx.require('antlingagi', r'LingSante-3\.1-flash, an open-weight MoE model with 560B total parameters')
```

### PASS · t10-tops-frontier-benchmarks (comparison, Ant Group LingSante-3.1-flash)
> Claim: tops GPT-6 Astra, Claude Opus 5.5, and Gemini 4 Argon on several benchmarks

Source ([x-antlingagi](https://x.com/AntLingAGI/status/2124523916819648945)): "The model leads on HealthBench Professional (65.72), HLE (text-only, with tools: 72.22) and BrowseComp (with context: 94.10), outperforming GPT-6 Astra, Claude Opus 5.5 and Gemini 4 Argon on all three."

```python
def check(ctx):
    return ctx.require('antlingagi', r'outperforming GPT-6 Astra, Claude Opus 5\.5 and Gemini 4 Argon on all three')
```

### PASS · t12-ranks-fifth-of-23 (number, Ant Group LingSante-3.1-flash)
> Claim: ranks fifth of 23 configurations

Source ([primary-lingsante-3-1-flash-open-medical-moe](https://huggingface.co/inclusionAI/LingSante-3.1-flash)): "With an overall score of 45.064, it ranked fifth among the 23 model configurations evaluated, delivering competitive performance on medical tasks at a relatively low inference cost."

```python
def check(ctx):
    return ctx.require('lingsante', r'ranked fifth among the 23 model configurations evaluated')
```

### PASS · t13-trails-gpt6-medical-behavior (comparison, Ant Group LingSante-3.1-flash)
> Claim: trails GPT-6 Astra on medical professional behavior

Source ([primary-lingsante-3-1-flash-open-medical-moe](https://huggingface.co/inclusionAI/LingSante-3.1-flash)): "LingSante-3.1-flash demonstrates strong performance on benchmarks for medical professional behavior, ranking second overall behind only GPT-6 Astra."

```python
def check(ctx):
    return ctx.require('lingsante', r'medical professional behavior, ranking second overall behind only GPT-6 Astra')
```

### PASS · t14-research-not-clinical-diagnosis (qualifier, Ant Group LingSante-3.1-flash)
> Claim: for research, not clinical diagnosis

Source ([primary-lingsante-3-1-flash-open-medical-moe](https://huggingface.co/inclusionAI/LingSante-3.1-flash)): "> LingSante-3.1-flash is intended for research and evaluation. … It is not a medical device and must not be used as an independent basis for diagnosis, prescriptions, or treatment."

```python
def check(ctx):
    return ctx.require('lingsante', r'intended for research and evaluation', r'must not be used as an independent basis for diagnosis')
```

### PASS · tc01-citation (citation, takeaway 1)

Note: Takeaway 1 cites https://openai.com/index/perplexity-and-intelligence, which is listed in the episode sources.json.

```python
def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 1 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 1 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))
```

### PASS · tc02-citation (citation, takeaway 2)

Note: Takeaway 2 cites https://huggingface.co/inclusionAI/LingSante-3.1-flash, which is listed in the episode sources.json.

```python
def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 2 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 2 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))
```
