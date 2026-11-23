# Executable audit, Daily State of AI 2026-11-22

Each claim is tested by a deterministic Python check against snapshotted source texts and X posts. PASS = the source sentence quoted supports the claim; FAIL = the source contradicts it or a required caveat is missing; NEEDS-HUMAN = opinion or not decidable by string/number match.

| artifact | PASS | FAIL | NEEDS-HUMAN | ERROR |
|---|---|---|---|---|
| episode | 26 | 3 | 3 | 0 |
| short | 15 | 3 | 7 | 0 |
| takeaways | 10 | 2 | 4 | 0 |

## Sources
- `primary-metr-q4-2026-capability-update`: [AI R&D-relevant model capabilities are improving rapidly and are getting harder to measure](https://metr.org/blog/2026-11-20-q4-2026-capability-update) (sha256 c8a9bdb662c7…)
- `x-ramez`: [X post by @ramez (Ramez Naam)](https://x.com/ramez/status/2124298418403311694) (sha256 4f4fd1aa624b…)
- `primary-lean-mathlib-certify-riemann-proof`: [Lean verification of the Riemann Hypothesis](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/) (sha256 a746693c3c84…)
- `x-emollick`: [X post by @emollick (Ethan Mollick)](https://x.com/emollick/status/2124173181065806006) (sha256 da6bf7eb748c…)
- `x-dkthomp`: [X post by @DKThomp (Derek Thompson)](https://x.com/DKThomp/status/2124156773560902109) (sha256 006aa9775fb1…)
- `primary-lambert-open-post-training-problems`: [Pushing Frontiers in Open Language Model Post-Training](https://natolambert.com/slides/2026/cornell-post-training/talk) (sha256 0ad7ef63a2c1…)
- `x-natolambert`: [X post by @natolambert (Nathan Lambert)](https://x.com/natolambert/status/2124152733145923892) (sha256 6aa5042ef46b…)
- `x-metr_evals`: [X post by @METR_Evals](https://x.com/METR_Evals/status/2123864981506798012) (sha256 f32eb966a19e…)
- `scan-framing`: [Morning X-first scan: verification framing per story](https://www.signalandnoise.email/content/daily-state/2026-11-22/audit/sources/2026-11-22/scan-framing.txt) (sha256 9b890f579e7c…)

## episode

### FAIL · e27-certified-same-day-as-selloff (qualifier, Riemann Hypothesis proof)
> Claim: a certified Riemann proof on the same day the stock market panics about AI returns

Source ([primary-lean-mathlib-certify-riemann-proof](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/)): "On November 20, 2026, Levent Alpöge released a proof of the Riemann Hypothesis as a Lean library comprising 17 million lines of code."

Note: Proof was released Friday Nov 20 (when Nasdaq sold off) and certified Saturday Nov 21, not certified on the same trading day

```python
def check(ctx):
    q_rel = ctx.find('lean', r'On November 20, 2026, Levent Alpöge released')
    q_cert = ctx.find('lean', r'2026-11-21')
    if q_rel and q_cert:
        return ctx.fail('lean', q_rel, 'Proof was released Friday Nov 20 (when Nasdaq sold off) and certified Saturday Nov 21, not certified on the same trading day')
    return ctx.need('lean', q_rel, 'Could not verify release vs certification date')
```

### FAIL · oe1-metr-uncertainty-caveat (objection, METR capability update)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-22/audit/sources/2026-11-22/scan-framing.txt)): "framing (METR): METR's own evaluation of public models up to Opus 5.5 and GPT-6 Astra; evaluator-reported research update with wide uncertainty, not independent replication."

Note: Episode omits METR framing caveat: evaluator-reported update with wide uncertainty, not independent replication

```python
def check(ctx):
    q = ctx.find('framing', r'evaluator-reported research update with wide uncertainty, not independent replication')
    if not ctx.art_has(r'uncertain|confidence interval|not independent|independent replication|self-reported|own evaluation|evaluator-reported'):
        return ctx.fail('framing', q, 'Episode omits METR framing caveat: evaluator-reported update with wide uncertainty, not independent replication')
    return ctx.ok('framing', q)
```

### FAIL · oe2-riemann-machine-not-peer-review (objection, Riemann Hypothesis proof)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-22/audit/sources/2026-11-22/scan-framing.txt)): "This is machine verification of a formal proof, not a human-readable paper or journal peer review."

Note: Episode omits Riemann framing caveat: machine verification of a formal proof, not a human-readable paper or journal peer review

```python
def check(ctx):
    q = ctx.find('framing', r'machine verification of a formal proof, not a human-readable paper or journal peer review')
    if not ctx.art_has(r'not.*peer[- ]review|not.*human[- ]readable|not.*journal|machine verif.*not|formal.*not.*paper|nobody has read|human-readable'):
        return ctx.fail('framing', q, 'Episode omits Riemann framing caveat: machine verification of a formal proof, not a human-readable paper or journal peer review')
    return ctx.ok('framing', q)
```

### NEEDS-HUMAN · e01-episode-date (number, Daily State of AI)
> Claim: Sunday, November 22, 2026

Source ([primary-lean-mathlib-certify-riemann-proof](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/)): "2026-11-21 13:55"

Note: Broadcast date Sunday, November 22, 2026 is not stated in primary sources (dated Nov 20-21, 2026)

```python
def check(ctx):
    q = ctx.find('lean', r'2026-11-21')
    return ctx.need('lean', q, 'Broadcast date Sunday, November 22, 2026 is not stated in primary sources (dated Nov 20-21, 2026)')
```

### NEEDS-HUMAN · e02-alpoge-claude-riemann (attribution, Riemann Hypothesis proof)
> Claim: Levent Alpöge released a Claude-assisted proof of the Riemann Hypothesis

Source ([primary-lean-mathlib-certify-riemann-proof](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/)): "On November 20, 2026, Levent Alpöge released a proof of the Riemann Hypothesis as a Lean library comprising 17 million lines of code."

Note: Primary source lean confirms Alpöge released the proof but does not mention Claude

```python
def check(ctx):
    q = ctx.find('lean', r'Levent Alpöge released a proof of the Riemann Hypothesis')
    if not q:
        return ctx.need('lean', None, 'Alpöge release sentence not found in lean')
    if ctx.find('lean', r'Claude'):
        return ctx.ok('lean', q)
    return ctx.need('lean', q, 'Primary source lean confirms Alpöge released the proof but does not mention Claude')
```

### NEEDS-HUMAN · e09-ethan-mollick-attribution (attribution, Riemann Hypothesis proof)
> Claim: Ethan Mollick pointed out that it still took a world-class number theorist who had studied Riemann for years to guide the model to the finish line

Source ([x-emollick](https://x.com/emollick/status/2124173181065806006)): "It is no coincidence that people proving Millennium Problems have all been great mathematicians, the models can't (yet) do it on their own https://t.co/qr4NO1JJxD"

Note: Mollick wrote generally about great mathematicians and Millennium Problems; number theorist and studied Riemann for years are not in the post text

```python
def check(ctx):
    q = ctx.find('emollick', r'Millennium Problems.*great mathematicians')
    if ctx.find('emollick', r'number theorist|studied Riemann'):
        return ctx.ok('emollick', q)
    return ctx.need('emollick', q, 'Mollick wrote generally about great mathematicians and Millennium Problems; number theorist and studied Riemann for years are not in the post text')
```

### PASS · e03-17m-lines-lean (number, Riemann Hypothesis proof)
> Claim: 17 million lines of Lean code

Source ([primary-lean-mathlib-certify-riemann-proof](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/)): "On November 20, 2026, Levent Alpöge released a proof of the Riemann Hypothesis as a Lean library comprising 17 million lines of code."

```python
def check(ctx):
    return ctx.require('lean', r'Lean library comprising 17 million lines of code')
```

### PASS · e04-lean-mathlib-certified (attribution, Riemann Hypothesis proof)
> Claim: the Lean and Mathlib communities formally certified yesterday

Source ([primary-lean-mathlib-certify-riemann-proof](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/)): "2026-11-21 13:55 … Lean and Mathlib communities … We hereby certify that both the statement and the proof of the Riemann Hypothesis are correct."

```python
def check(ctx):
    return ctx.require('lean', r'2026-11-21', r'Lean and Mathlib communities', r'hereby certify')
```

### PASS · e05-metr-capability-update (attribution, METR capability update)
> Claim: METR dropped a major capability update

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "November 20, 2026 … This post presents evidence from our capability evaluations of public models relevant to AI R&D acceleration, up to Opus 5.5 and GPT-6 Astra."

```python
def check(ctx):
    return ctx.require('metr', r'November 20, 2026', r'capability evaluations of public models')
```

### PASS · e06-metr-doubling-3-6-months (number, METR capability update)
> Claim: the length of tasks frontier models can complete is still doubling roughly every 3.6 months

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "On the combined suite of TH1.1 and TH2, time horizons are doubling roughly every 3.6 months (Section 3.C.1)."

```python
def check(ctx):
    return ctx.require('metr', r'time horizons are doubling roughly every 3\.6\d* months')
```

### PASS · e07-nasdaq-ai-selloff (attribution, Nasdaq AI sell-off)
> Claim: the Nasdaq sold off hard as investors questioned whether the AI trade is actually paying off

Source ([x-dkthomp](https://x.com/DKThomp/status/2124156773560902109)): "You really cannot get a cleaner example of the principle that "AI capabilities ≠ real-world AI consequences" than getting news of a proof of the Riemann Hypothesis-which people have for years cited as a sign of takeoff, AGI, the beginning of the productivity boom that takes us into the transhumanist Valhalla, etc etc-at the same time that the Nasdaq absolutely vomits up all over itself as the AI Trade dies."

```python
def check(ctx):
    return ctx.require('dkthomp', r'Nasdaq.*AI Trade')
```

### PASS · e08-derek-thompson-quote (attribution, Riemann Hypothesis proof)
> Claim: The journalist Derek Thompson called it the cleanest possible example that AI capabilities don't automatically equal real-world consequences

Source ([x-dkthomp](https://x.com/DKThomp/status/2124156773560902109)): "You really cannot get a cleaner example of the principle that "AI capabilities ≠ real-world AI consequences" than getting news of a proof of the Riemann Hypothesis-which people have for years cited as a sign of takeoff, AGI, the beginning of the productivity boom that takes us into the transhumanist Valhalla, etc etc-at the same time that the Nasdaq absolutely vomits up all over itself as the AI Trade dies."

```python
def check(ctx):
    return ctx.require('dkthomp', r'cleaner example.*AI capabilities.*real-world AI consequences')
```

### PASS · e10-lambert-cornell-talk (attribution, Nathan Lambert Cornell talk)
> Claim: Nathan Lambert's talk at Cornell on the future of post-training

Source ([primary-lambert-open-post-training-problems](https://natolambert.com/slides/2026/cornell-post-training/talk)): "Nathan Lambert … Cornell University, November 20, 2026 … Pushing Frontiers in Open Language Model Post-Training"

```python
def check(ctx):
    return ctx.require('lambert', r'Nathan Lambert', r'Cornell University', r'Post-Training')
```

### PASS · e11-metr-opus-5-5-gpt6-astra (attribution, METR capability update)
> Claim: METR's update, which tested public models up to Opus 5.5 and GPT-6 Astra

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "This post presents evidence from our capability evaluations of public models relevant to AI R&D acceleration, up to Opus 5.5 and GPT-6 Astra."

```python
def check(ctx):
    return ctx.require('metr', r'public models.*up to Opus 5\.5 and GPT-6 Astra')
```

### PASS · e12-azspc-96-98-percentile (number, METR capability update)
> Claim: They hit the 96th to 98th percentile in multi-month Al Zimmermann programming contests

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "The first of these two task families was 15 Al Zimmermann contests, multi-month long optimization competitions. … We find the median placement of the strongest models (Fable 5.1, Opus 5.5 and GPT-6 Astra) is the 96th to 98th percentile of human participants (97 to 413 participants per contest)."

```python
def check(ctx):
    return ctx.require('metr', r'Al Zimmermann contests, multi-month', r'96th to 98th percentile')
```

### PASS · e13-nanogpt-competent-speedrunners (comparison, METR capability update)
> Claim: beat competent human speedrunners on NanoGPT at a fraction of the cost

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "L Budget NanoGPT … On Budget NanoGPT speedrun, we find that fully autonomous AI agents outperform many competent speedrunners, achieving better speedups whilst costing less."

```python
def check(ctx):
    return ctx.require('metr', r'NanoGPT', r'outperform.*competent speedrunners.*costing less')
```

### PASS · e14-metr-lifecycle-cost-metric (attribution, METR capability update)
> Claim: METR introduced a new metric called Lifecycle Cost—an estimate of what it takes to build, run, and score a task as a reinforcement learning environment

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "In Section 3.B.1, we introduce Lifecycle Cost, a rough proxy for how costly a task would be to build and use as an RL training environment. … This is the cost for us to develop a containerized environment for the task, and then to run and score the task 100 times.⁠26 The goal with this quantity is not to reflect the 'real cost' of RL environments per se, but rather to have some rough quantitative metric of relative costliness."

```python
def check(ctx):
    return ctx.require('metr', r'introduce Lifecycle Cost.*RL training environment', r'develop.*run and score the task 100 times')
```

### PASS · e15-doubling-lifecycle-cost-halves-horizon (comparison, METR capability update)
> Claim: Even when you control for how long a task takes a human, doubling its lifecycle cost cuts an AI agent's effective time horizon roughly in half

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "On our dataset, models perform somewhat worse on tasks that we estimate are costlier to turn into RL training environments, even after controlling for how long these tasks would take humans. … In our data, a doubling of lifecycle cost for a task of a given length imposes a difficulty penalty that is very roughly equivalent to halving the time horizon of the agent."

```python
def check(ctx):
    return ctx.require('metr', r'controlling for how long these tasks would take humans', r'doubling of lifecycle cost.*roughly equivalent to halving the time horizon')
```

### PASS · e16-metr-agent-swarms (attribution, METR capability update)
> Claim: METR ran experiments with agent swarms

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "For several of our tasks, we ran small experiments with swarms, or collections of agents working together towards a common goal without a clear leader or subagent structure."

```python
def check(ctx):
    return ctx.require('metr', r'ran small experiments with swarms')
```

### PASS · e17-swarms-beat-independent-nanogpt (comparison, METR capability update)
> Claim: On NanoGPT optimization, where agents get an exact score back quickly, swarms beat independent agents

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "The only task in our suite that experienced swarm uplift relatively consistently was nanoGPT, in which agents were tasked to optimize a language-model training script based on the nanoGPT speedrun. … For this task, submissions are independent of one another and agents see the exact grade for each submission as they went, and they could submit repeatedly within a fixed budget. … Figure 62: Swarms of size 5 outperform best-of-k counterparts in nanoGPT speedrunning"

```python
def check(ctx):
    return ctx.require('metr', r'swarm uplift.*nanoGPT', r'exact grade for each submission', r'Swarms.*outperform best-of-k.*nanoGPT')
```

### PASS · e18-swarms-worse-hidden-targets (comparison, METR capability update)
> Claim: on tasks where models had to build their own validation loops against hidden targets, swarms actually performed worse

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "Tasks that require agents to create their own feedback loops are particularly susceptible to swarm downlift. … Minecraft Bot: Build an autonomous bot that beats Minecraft, which is evaluated on hidden worlds. … Thus, they reward agents building good validation loops in the available practice settings and avoiding overfitting on individual examples."

```python
def check(ctx):
    return ctx.require('metr', r'create their own feedback loops.*swarm downlift', r'evaluated on hidden', r'building good validation loops')
```

### PASS · e19-larger-swarm-misled-themselves (comparison, METR capability update)
> Claim: the larger the swarm got, the more confidently the agents misled themselves

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "Interestingly, as swarm size increases, the gap grows significantly, suggesting agents in larger swarms were more prone to misleading themselves."

```python
def check(ctx):
    return ctx.require('metr', r'as swarm size increases.*larger swarms were more prone to misleading themselves')
```

### PASS · e20-opus-overrated-astra-tasks (attribution, METR capability update)
> Claim: When METR asked Opus 5.5 to grade evaluation tasks designed by GPT-6 Astra, it systematically overrated them

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "Frontier models show high agreement with our own ratings when the task is made by a weaker model than themselves, but give inappropriately high scores when the task is made by a stronger, or similarly strong, model, see Figure 9.⁠45 Opus 5.5, the judge that had the highest agreement with our human scorer, scores Astra's tasks on average about 0.2 (out of 1) more highly than our human.⁠46 … With the end result being that when used as judges they systematically overestimate the quality of their own solutions, and those of stronger models."

```python
def check(ctx):
    return ctx.require('metr', r'Opus 5\.5.*scores Astra.s tasks on average about 0\.2.*more highly than our human', r'systematically overestimate')
```

### PASS · e21-con-leche-con-ron-24h (attribution, Riemann Hypothesis proof)
> Claim: Independent proof checkers like con-leche and con-ron certified the entire proof in twenty-four hours

Source ([primary-lean-mathlib-certify-riemann-proof](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/)): "Over the past day, the Lean and Mathlib communities have rallied to verify the proof's correctness. … The exported raw proof has been checked by several proof checkers, including Lean's official kernel, the con-leche and con-ron checkers, and several independent checkers contributed by third parties and implemented in different programming languages."

```python
def check(ctx):
    return ctx.require('lean', r'Over the past day', r'con-leche and con-ron checkers')
```

### PASS · e22-lambert-cornell-slides (attribution, Nathan Lambert Cornell talk)
> Claim: Nathan Lambert's new Cornell slides

Source ([primary-lambert-open-post-training-problems](https://natolambert.com/slides/2026/cornell-post-training/talk)): "Nathan Lambert … Cornell University, November 20, 2026 … Slides: natolambert.com/cornell-2026"

```python
def check(ctx):
    return ctx.require('lambert', r'Nathan Lambert', r'Cornell University, November 20, 2026', r'Slides:')
```

### PASS · e23-rl-more-compute-than-pretraining (comparison, Nathan Lambert Cornell talk)
> Claim: Reinforcement learning now consumes far more compute than pretraining

Source ([primary-lambert-open-post-training-problems](https://natolambert.com/slides/2026/cornell-post-training/talk)): "Post-training (RL) now takes most of a frontier lab's compute … RL compute relative to pretraining compute for the same model, in GPU-hours:"

```python
def check(ctx):
    return ctx.require('lambert', r'Post-training \(RL\) now takes most of a frontier lab.s compute', r'RL compute relative to pretraining compute')
```

### PASS · e24-beam-nearly-twice-rl (comparison, Nathan Lambert Cornell talk)
> Claim: nearly twice as much for Beam

Source ([primary-lambert-open-post-training-problems](https://natolambert.com/slides/2026/cornell-post-training/talk)): "Beam Oct 2026 … > 1.7×"

```python
def check(ctx):
    return ctx.require('lambert', r'Beam Oct 2026', r'> 1\.7×')
```

### PASS · e25-inkling-four-times-rl (comparison, Nathan Lambert Cornell talk)
> Claim: roughly four times as much for Inkling 2 Small

Source ([primary-lambert-open-post-training-problems](https://natolambert.com/slides/2026/cornell-post-training/talk)): "Inkling 2 Small Nov 2026 … ~4×*"

```python
def check(ctx):
    return ctx.require('lambert', r'Inkling 2 Small', r'~4×')
```

### PASS · e26-50m-year-specialist-teachers (number, Nathan Lambert Cornell talk)
> Claim: Frontier labs are spending 50 million dollars a year or more training specialist teachers and distilling them into single models

Source ([primary-lambert-open-post-training-problems](https://natolambert.com/slides/2026/cornell-post-training/talk)): "Now very expensive (O($50M+/yr) to do it well). … Stages: Stage 1 SFT/reasoning foundation → Stage 2 train domain-specialist teachers (with older-style post-training recipes) → Stage 3 MOPD into a single student (final model)."

```python
def check(ctx):
    return ctx.require('lambert', r'O\(\$50M\+/yr\)', r'train domain-specialist teachers.*single student')
```

### PASS · e28-lambert-output-vs-understanding (attribution, Nathan Lambert Cornell talk)
> Claim: As Lambert warned students at Cornell, models dramatically accelerate output, but they barely accelerate understanding—and the load-bearing insight is often a tiny fraction of the work

Source ([primary-lambert-open-post-training-problems](https://natolambert.com/slides/2026/cornell-post-training/talk)): "Using LLMs accelerates output but very minimally accelerates understanding … To use a Claude-ism, the load-bearing piece of work may be a very small proportion of the overall process."

```python
def check(ctx):
    return ctx.require('lambert', r'Using LLMs accelerates output but very minimally accelerates understanding', r'load-bearing piece of work may be a very small proportion')
```

### PASS · e29-metr-improving-high-cost-tasks (qualifier, METR capability update)
> Claim: METR's data shows models are improving even on high-cost tasks, just from a lower baseline

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "Despite this, we see similar rates of progress on high and low cost subsets of our tasks, and we also see AI performance improving over time even on our most costly tasks. … When we subset our tasks by high and low Lifecycle Cost, controlling for task length, and plot time horizons over release dates, we find that models perform worse on the higher Lifecycle Cost subset of our tasks, see Figure 7."

```python
def check(ctx):
    return ctx.require('metr', r'AI performance improving over time even on our most costly tasks', r'models perform worse on the higher Lifecycle Cost subset')
```

### PASS · oe3-lambert-slides-not-peer-reviewed (objection, Nathan Lambert Cornell talk)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-22/audit/sources/2026-11-22/scan-framing.txt)): "framing (natolambert.com): Author's own talk slides (Cornell, November 20, 2026); opinion and research agenda, not peer-reviewed findings."

Note: Episode carries Lambert framing caveat (author opinion / research agenda, not peer-reviewed)

```python
def check(ctx):
    q = ctx.find('framing', r'opinion and research agenda, not peer-reviewed findings')
    if not ctx.art_has(r'not.*peer[- ]review|opinion|research agenda|author.s own'):
        return ctx.fail('framing', q, 'Episode omits Lambert framing caveat: author talk slides representing opinion and research agenda, not peer-reviewed findings')
    return ctx.ok('framing', q, 'Episode carries Lambert framing caveat (author opinion / research agenda, not peer-reviewed)')
```

## short

### FAIL · os1-metr-uncertainty-caveat (objection, AI Verification & Riemann Proof)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-22/audit/sources/2026-11-22/scan-framing.txt)): "framing (METR): METR's own evaluation of public models up to Opus 5.5 and GPT-6 Astra; evaluator-reported research update with wide uncertainty, not independent replication."

Note: Short omits METR framing caveat: evaluator-reported update with wide uncertainty, not independent replication

```python
def check(ctx):
    q = ctx.find('framing', r'evaluator-reported research update with wide uncertainty, not independent replication')
    if not ctx.art_has(r'uncertain|confidence interval|not independent|independent replication|self-reported|own evaluation|evaluator-reported'):
        return ctx.fail('framing', q, 'Short omits METR framing caveat: evaluator-reported update with wide uncertainty, not independent replication')
    return ctx.ok('framing', q)
```

### FAIL · os2-riemann-machine-not-peer-review (objection, AI Verification & Riemann Proof)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-22/audit/sources/2026-11-22/scan-framing.txt)): "This is machine verification of a formal proof, not a human-readable paper or journal peer review."

Note: Short omits Riemann framing caveat: machine verification of a formal proof, not a human-readable paper or journal peer review

```python
def check(ctx):
    q = ctx.find('framing', r'machine verification of a formal proof, not a human-readable paper or journal peer review')
    if not ctx.art_has(r'not.*peer[- ]review|not.*human[- ]readable|not.*journal|machine verif.*not|formal.*not.*paper|nobody has read|human-readable'):
        return ctx.fail('framing', q, 'Short omits Riemann framing caveat: machine verification of a formal proof, not a human-readable paper or journal peer review')
    return ctx.ok('framing', q)
```

### FAIL · os3-lambert-slides-not-peer-reviewed (objection, AI Verification & Riemann Proof)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-22/audit/sources/2026-11-22/scan-framing.txt)): "framing (natolambert.com): Author's own talk slides (Cornell, November 20, 2026); opinion and research agenda, not peer-reviewed findings."

Note: Short omits Lambert framing caveat: author talk slides representing opinion and research agenda, not peer-reviewed findings

```python
def check(ctx):
    q = ctx.find('framing', r'opinion and research agenda, not peer-reviewed findings')
    if not ctx.art_has(r'not.*peer[- ]review|opinion|research agenda|author.s own'):
        return ctx.fail('framing', q, 'Short omits Lambert framing caveat: author talk slides representing opinion and research agenda, not peer-reviewed findings')
    return ctx.ok('framing', q)
```

### NEEDS-HUMAN · s01-friday-17m-claude-riemann (number, AI Verification & Riemann Proof)
> Claim: On Friday, a 17-million-line, Claude-assisted proof of the Riemann Hypothesis dropped

Source ([primary-lean-mathlib-certify-riemann-proof](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/)): "On November 20, 2026, Levent Alpöge released a proof of the Riemann Hypothesis as a Lean library comprising 17 million lines of code."

Note: Primary source lean confirms 17 million lines released Nov 20 (Friday) but does not mention Claude

```python
def check(ctx):
    q = ctx.find('lean', r'November 20, 2026.*17 million lines of code')
    if ctx.find('lean', r'Claude'):
        return ctx.ok('lean', q)
    return ctx.need('lean', q, 'Primary source lean confirms 17 million lines released Nov 20 (Friday) but does not mention Claude')
```

### NEEDS-HUMAN · s02-claude-assisted-riemann (attribution, AI Verification & Riemann Proof)
> Claim: Claude-assisted proof of the Riemann Hypothesis

Source ([primary-lean-mathlib-certify-riemann-proof](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/)): "On November 20, 2026, Levent Alpöge released a proof of the Riemann Hypothesis as a Lean library comprising 17 million lines of code."

Note: Primary source lean does not mention Claude

```python
def check(ctx):
    q = ctx.find('lean', r'proof of the Riemann Hypothesis')
    if ctx.find('lean', r'Claude'):
        return ctx.ok('lean', q)
    return ctx.need('lean', q, 'Primary source lean does not mention Claude')
```

### NEEDS-HUMAN · s08-uniform-ladder-opinion (opinion, AI Verification & Riemann Proof)
> Claim: AI isn't climbing a uniform ladder of intelligence.

Note: Editorial synthesis/opinion

```python
def check(ctx):
    return ctx.need(None, None, 'Editorial synthesis/opinion')
```

### NEEDS-HUMAN · s09-verification-cost-opinion (opinion, AI Verification & Riemann Proof)
> Claim: It's governed by verification cost—how cheaply you can check if an answer is right.

Note: Editorial synthesis/opinion

```python
def check(ctx):
    return ctx.need(None, None, 'Editorial synthesis/opinion')
```

### NEEDS-HUMAN · s16-riemann-automated-verifier-opinion (opinion, AI Verification & Riemann Proof)
> Claim: Riemann fell because Lean turns pure math into an automated verifier.

Note: Editorial interpretation/opinion

```python
def check(ctx):
    return ctx.need(None, None, 'Editorial interpretation/opinion')
```

### NEEDS-HUMAN · s20-proof-checker-magic-opinion (opinion, AI Verification & Riemann Proof)
> Claim: Anywhere you can build a proof checker, AI feels like magic.

Note: Editorial opinion

```python
def check(ctx):
    return ctx.need(None, None, 'Editorial opinion')
```

### NEEDS-HUMAN · s21-human-judgment-swarms-opinion (opinion, AI Verification & Riemann Proof)
> Claim: Everywhere else, human judgment is all that keeps the swarms honest.

Note: Editorial opinion

```python
def check(ctx):
    return ctx.need(None, None, 'Editorial opinion')
```

### PASS · s03-certified-by-lean-yesterday (attribution, AI Verification & Riemann Proof)
> Claim: certified by Lean yesterday

Source ([primary-lean-mathlib-certify-riemann-proof](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/)): "2026-11-21 13:55 … Lean and Mathlib communities … We hereby certify that both the statement and the proof of the Riemann Hypothesis are correct."

```python
def check(ctx):
    return ctx.require('lean', r'2026-11-21', r'Lean and Mathlib communities', r'hereby certify')
```

### PASS · s04-metr-horizons-doubling-3-6 (attribution, AI Verification & Riemann Proof)
> Claim: METR showed AI task horizons doubling every 3.6 months

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "On the combined suite of TH1.1 and TH2, time horizons are doubling roughly every 3.6 months (Section 3.C.1)."

```python
def check(ctx):
    return ctx.require('metr', r'time horizons are doubling roughly every 3\.6\d* months')
```

### PASS · s05-doubling-3-6-months (number, AI Verification & Riemann Proof)
> Claim: doubling every 3.6 months

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "On the combined suite of TH1.1 and TH2, time horizons are doubling roughly every 3.6 months (Section 3.C.1)."

```python
def check(ctx):
    return ctx.require('metr', r'doubling roughly every 3\.6\d* months')
```

### PASS · s06-nasdaq-sold-off-hard (qualifier, AI Verification & Riemann Proof)
> Claim: the Nasdaq sold off hard

Source ([x-dkthomp](https://x.com/DKThomp/status/2124156773560902109)): "You really cannot get a cleaner example of the principle that "AI capabilities ≠ real-world AI consequences" than getting news of a proof of the Riemann Hypothesis-which people have for years cited as a sign of takeoff, AGI, the beginning of the productivity boom that takes us into the transhumanist Valhalla, etc etc-at the same time that the Nasdaq absolutely vomits up all over itself as the AI Trade dies."

```python
def check(ctx):
    return ctx.require('dkthomp', r'Nasdaq absolutely vomits up all over itself')
```

### PASS · s07-17m-lines (number, AI Verification & Riemann Proof)
> Claim: 17M lines

Source ([primary-lean-mathlib-certify-riemann-proof](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/)): "On November 20, 2026, Levent Alpöge released a proof of the Riemann Hypothesis as a Lean library comprising 17 million lines of code."

```python
def check(ctx):
    return ctx.require('lean', r'17 million lines of code')
```

### PASS · s10-metr-tested-opus-astra (attribution, AI Verification & Riemann Proof)
> Claim: METR tested Opus 5.5 and GPT-6 Astra

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "This post presents evidence from our capability evaluations of public models relevant to AI R&D acceleration, up to Opus 5.5 and GPT-6 Astra."

```python
def check(ctx):
    return ctx.require('metr', r'up to Opus 5\.5 and GPT-6 Astra')
```

### PASS · s11-doubling-rl-cost-halves-horizon (comparison, AI Verification & Riemann Proof)
> Claim: doubling a task's cost to run as an RL environment cuts an agent's effective horizon roughly in half

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "In Section 3.B.1, we introduce Lifecycle Cost, a rough proxy for how costly a task would be to build and use as an RL training environment. … In our data, a doubling of lifecycle cost for a task of a given length imposes a difficulty penalty that is very roughly equivalent to halving the time horizon of the agent."

```python
def check(ctx):
    return ctx.require('metr', r'Lifecycle Cost.*RL training environment', r'doubling of lifecycle cost.*roughly equivalent to halving the time horizon')
```

### PASS · s12-roughly-in-half (qualifier, AI Verification & Riemann Proof)
> Claim: roughly in half

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "In our data, a doubling of lifecycle cost for a task of a given length imposes a difficulty penalty that is very roughly equivalent to halving the time horizon of the agent."

```python
def check(ctx):
    return ctx.require('metr', r'very roughly equivalent to halving')
```

### PASS · s13-minus-50-percent-horizon (number, AI Verification & Riemann Proof)
> Claim: -50% horizon

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "In our data, a doubling of lifecycle cost for a task of a given length imposes a difficulty penalty that is very roughly equivalent to halving the time horizon of the agent."

```python
def check(ctx):
    return ctx.require('metr', r'roughly equivalent to halving the time horizon')
```

### PASS · s14-larger-swarms-performed-worse (comparison, AI Verification & Riemann Proof)
> Claim: Without a fast ground-truth check, larger agent swarms actually performed worse

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "On the other hand, tasks where models had to determine their own methods of verification without a ground truth tended to lead to propagating incorrect assumptions; further, tasks involving very long feedback loops, very limited resources, or interaction channels mostly resulted in coordination overhead. … In some agent swarms, particularly for Train a Program, increasing swarm size resulted in decreasing scores."

```python
def check(ctx):
    return ctx.require('metr', r'without a ground truth', r'increasing swarm size resulted in decreasing scores')
```

### PASS · s15-ai-judges-overrated-strong-models (comparison, AI Verification & Riemann Proof)
> Claim: AI judges systematically overrated strong models

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "With the end result being that when used as judges they systematically overestimate the quality of their own solutions, and those of stronger models."

```python
def check(ctx):
    return ctx.require('metr', r'systematically overestimate the quality of their own solutions, and those of stronger models')
```

### PASS · s17-lambert-rl-4x-pretraining (attribution, AI Verification & Riemann Proof)
> Claim: Nathan Lambert notes RL now takes up to four times more compute than pretraining

Source ([primary-lambert-open-post-training-problems](https://natolambert.com/slides/2026/cornell-post-training/talk)): "RL compute relative to pretraining compute for the same model, in GPU-hours: … ~4×*"

```python
def check(ctx):
    return ctx.require('lambert', r'RL compute relative to pretraining compute', r'~4×')
```

### PASS · s18-up-to-4x-compute-pretraining (comparison, AI Verification & Riemann Proof)
> Claim: up to four times more compute than pretraining

Source ([primary-lambert-open-post-training-problems](https://natolambert.com/slides/2026/cornell-post-training/talk)): "RL compute relative to pretraining compute for the same model, in GPU-hours: … ~4×*"

```python
def check(ctx):
    return ctx.require('lambert', r'RL compute relative to pretraining compute', r'~4×')
```

### PASS · s19-4x-pretraining (number, AI Verification & Riemann Proof)
> Claim: 4x pretraining

Source ([primary-lambert-open-post-training-problems](https://natolambert.com/slides/2026/cornell-post-training/talk)): "Inkling 2 Small Nov 2026 … ~4×*"

```python
def check(ctx):
    return ctx.require('lambert', r'Inkling 2 Small', r'~4×')
```

### PASS · s22-sources-attribution (attribution, AI Verification & Riemann Proof)
> Claim: Sources: METR, Lean Community and Nathan Lambert.

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "AI R&D-relevant model capabilities are improving rapidly and are getting harder to measure - METR"

Note: All three cited primary sources (METR, Lean Community, Nathan Lambert) are present

```python
def check(ctx):
    q1 = ctx.find('metr', r'METR')
    q2 = ctx.find('lean', r'Lean community')
    q3 = ctx.find('lambert', r'Nathan Lambert')
    if q1 and q2 and q3:
        return ctx.ok('metr', q1, 'All three cited primary sources (METR, Lean Community, Nathan Lambert) are present')
    return ctx.need(None, None, 'One or more cited sources missing')
```

## takeaways

### FAIL · ot1-metr-uncertainty-caveat (objection, METR AI agent time horizon)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-22/audit/sources/2026-11-22/scan-framing.txt)): "framing (METR): METR's own evaluation of public models up to Opus 5.5 and GPT-6 Astra; evaluator-reported research update with wide uncertainty, not independent replication."

Note: Takeaways omit METR framing caveat: evaluator-reported update with wide uncertainty, not independent replication

```python
def check(ctx):
    q = ctx.find('framing', r'evaluator-reported research update with wide uncertainty, not independent replication')
    if not ctx.art_has(r'uncertain|confidence interval|not independent|independent replication|self-reported|own evaluation|evaluator-reported'):
        return ctx.fail('framing', q, 'Takeaways omit METR framing caveat: evaluator-reported update with wide uncertainty, not independent replication')
    return ctx.ok('framing', q)
```

### FAIL · ot2-riemann-machine-not-peer-review (objection, Riemann Hypothesis Lean proof)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-22/audit/sources/2026-11-22/scan-framing.txt)): "This is machine verification of a formal proof, not a human-readable paper or journal peer review."

Note: Takeaways omit Riemann framing caveat: machine verification of a formal proof, not a human-readable paper or journal peer review

```python
def check(ctx):
    q = ctx.find('framing', r'machine verification of a formal proof, not a human-readable paper or journal peer review')
    if not ctx.art_has(r'not.*peer[- ]review|not.*human[- ]readable|not.*journal|machine verif.*not|formal.*not.*paper|nobody has read|human-readable'):
        return ctx.fail('framing', q, 'Takeaways omit Riemann framing caveat: machine verification of a formal proof, not a human-readable paper or journal peer review')
    return ctx.ok('framing', q)
```

### NEEDS-HUMAN · t06-lean-certified-claude-riemann (attribution, Riemann Hypothesis Lean proof)
> Claim: The Lean and Mathlib communities certified Levent Alpöge's Claude-assisted, 17-million-line Lean proof of the Riemann Hypothesis

Source ([primary-lean-mathlib-certify-riemann-proof](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/)): "On November 20, 2026, Levent Alpöge released a proof of the Riemann Hypothesis as a Lean library comprising 17 million lines of code."

Note: Primary source lean confirms certification of Alpöge 17M-line proof but does not mention Claude

```python
def check(ctx):
    q = ctx.find('lean', r'Levent Alpöge released a proof of the Riemann Hypothesis as a Lean library comprising 17 million lines of code')
    if ctx.find('lean', r'Claude'):
        return ctx.ok('lean', q)
    return ctx.need('lean', q, 'Primary source lean confirms certification of Alpöge 17M-line proof but does not mention Claude')
```

### NEEDS-HUMAN · t07-claude-assisted (attribution, Riemann Hypothesis Lean proof)
> Claim: Claude-assisted

Note: Primary source lean does not mention Claude

```python
def check(ctx):
    q = ctx.find('lean', r'Claude')
    if q:
        return ctx.ok('lean', q)
    return ctx.need('lean', None, 'Primary source lean does not mention Claude')
```

### NEEDS-HUMAN · t11-world-class-number-theorist (opinion, Riemann Hypothesis Lean proof)
> Claim: world-class number theorist

Note: Qualitative characterization not stated verbatim in primary sources

```python
def check(ctx):
    return ctx.need(None, None, 'Qualitative characterization not stated verbatim in primary sources')
```

### NEEDS-HUMAN · t12-number-theorist-guided-model (attribution, Riemann Hypothesis Lean proof)
> Claim: a world-class number theorist guided the model

Source ([x-emollick](https://x.com/emollick/status/2124173181065806006)): "It is no coincidence that people proving Millennium Problems have all been great mathematicians, the models can't (yet) do it on their own https://t.co/qr4NO1JJxD"

Note: emollick says great mathematicians and models cannot do it on their own, without specifically saying number theorist guided the model

```python
def check(ctx):
    q = ctx.find('emollick', r'great mathematicians.*models can.t \(yet\) do it on their own')
    if ctx.find('emollick', r'number theorist'):
        return ctx.ok('emollick', q)
    return ctx.need('emollick', q, 'emollick says great mathematicians and models cannot do it on their own, without specifically saying number theorist guided the model')
```

### PASS · t01-metr-doubling-lifecycle-cost (attribution, METR AI agent time horizon)
> Claim: METR found that doubling a task's lifecycle cost cuts an AI agent's effective time horizon roughly in half

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "In our data, a doubling of lifecycle cost for a task of a given length imposes a difficulty penalty that is very roughly equivalent to halving the time horizon of the agent."

```python
def check(ctx):
    return ctx.require('metr', r'doubling of lifecycle cost.*roughly equivalent to halving the time horizon')
```

### PASS · t02-doubling-lifecycle-cost (comparison, METR AI agent time horizon)
> Claim: doubling a task's lifecycle cost

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "In our data, a doubling of lifecycle cost for a task of a given length imposes a difficulty penalty that is very roughly equivalent to halving the time horizon of the agent."

```python
def check(ctx):
    return ctx.require('metr', r'doubling of lifecycle cost')
```

### PASS · t03-roughly-qualifier (qualifier, METR AI agent time horizon)
> Claim: roughly

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "In our data, a doubling of lifecycle cost for a task of a given length imposes a difficulty penalty that is very roughly equivalent to halving the time horizon of the agent."

```python
def check(ctx):
    return ctx.require('metr', r'very roughly equivalent to halving')
```

### PASS · t04-in-half-number (number, METR AI agent time horizon)
> Claim: in half

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "In our data, a doubling of lifecycle cost for a task of a given length imposes a difficulty penalty that is very roughly equivalent to halving the time horizon of the agent."

```python
def check(ctx):
    return ctx.require('metr', r'halving the time horizon of the agent')
```

### PASS · t05-controlling-human-time (qualifier, METR AI agent time horizon)
> Claim: even after controlling for how long the task takes a human

Source ([primary-metr-q4-2026-capability-update](https://metr.org/blog/2026-11-20-q4-2026-capability-update)): "On our dataset, models perform somewhat worse on tasks that we estimate are costlier to turn into RL training environments, even after controlling for how long these tasks would take humans."

```python
def check(ctx):
    return ctx.require('metr', r'even after controlling for how long these tasks would take humans')
```

### PASS · t08-17-million-line (number, Riemann Hypothesis Lean proof)
> Claim: 17-million-line

Source ([primary-lean-mathlib-certify-riemann-proof](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/)): "On November 20, 2026, Levent Alpöge released a proof of the Riemann Hypothesis as a Lean library comprising 17 million lines of code."

```python
def check(ctx):
    return ctx.require('lean', r'17 million lines of code')
```

### PASS · t09-independent-checkers-24h (attribution, Riemann Hypothesis Lean proof)
> Claim: independent checkers certifying it in 24 hours

Source ([primary-lean-mathlib-certify-riemann-proof](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/)): "Over the past day, the Lean and Mathlib communities have rallied to verify the proof's correctness. … The exported raw proof has been checked by several proof checkers, including Lean's official kernel, the con-leche and con-ron checkers, and several independent checkers contributed by third parties and implemented in different programming languages."

```python
def check(ctx):
    return ctx.require('lean', r'Over the past day', r'several independent checkers')
```

### PASS · t10-24-hours (number, Riemann Hypothesis Lean proof)
> Claim: 24 hours

Source ([primary-lean-mathlib-certify-riemann-proof](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/)): "Over the past day, the Lean and Mathlib communities have rallied to verify the proof's correctness."

```python
def check(ctx):
    return ctx.require('lean', r'Over the past day')
```

### PASS · tc01-citation (citation, takeaway 1)

Note: Takeaway 1 cites https://metr.org/blog/2026-11-20-q4-2026-capability-update, which is listed in the episode sources.json.

```python
def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 1 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 1 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))
```

### PASS · tc02-citation (citation, takeaway 2)

Note: Takeaway 2 cites https://leanprover-community.github.io/blog/posts/riemann-hypothesis/, which is listed in the episode sources.json.

```python
def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 2 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 2 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))
```
