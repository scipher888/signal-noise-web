# Executable audit, Daily State of AI 2026-11-21

Each claim is tested by a deterministic Python check against snapshotted source texts and X posts. PASS = the source sentence quoted supports the claim; FAIL = the source contradicts it or a required caveat is missing; NEEDS-HUMAN = opinion or not decidable by string/number match.

| artifact | PASS | FAIL | NEEDS-HUMAN | ERROR |
|---|---|---|---|---|
| episode | 42 | 2 | 1 | 0 |
| short | 20 | 1 | 1 | 1 |
| takeaways | 5 | 0 | 0 | 0 |

## Sources
- `primary-alpoge-claude-riemann-hypothesis-claim`: [Remark on the Riemann Hypothesis (alpo.ge/remark.pdf)](https://alpo.ge/remark.pdf) (sha256 9b4d7b036542…)
- `x-emollick`: [X post by @emollick (Ethan Mollick)](https://x.com/emollick/status/2123972584400204199) (sha256 6096055eb6b0…)
- `x-andrewcurran_`: [X post by @AndrewCurran_ (Andrew Curran)](https://x.com/AndrewCurran_/status/2123819916768039149) (sha256 713e65e80489…)
- `x-artificialanlys`: [X post by @ArtificialAnlys (Artificial Analysis)](https://x.com/ArtificialAnlys/status/2123865423364161861) (sha256 8af086e81f67…)
- `primary-thinking-machines-inkling-2-mini-open-we`: [Inkling 2 Mini](https://thinkingmachines.ai/news/inkling-2-mini/) (sha256 ca2fa597c8c4…)
- `x-soumithchintala`: [X post by @soumithchintala (Soumith Chintala)](https://x.com/soumithchintala/status/2123878334895436115) (sha256 5917dd5c05d7…)
- `x-0xsero`: [X post by @0xSero (0xSero)](https://x.com/0xSero/status/2123883583740006752) (sha256 41375c25f7f1…)
- `primary-naam-task-horizon-charts-critique`: [The Most Important Charts in AI are Wrong](https://www.rameznaam.com/p/the-most-important-charts-in-ai-are) (sha256 2db31f2bbe27…)
- `x-ramez`: [X post by @ramez (Ramez Naam)](https://x.com/ramez/status/2123934198868382184) (sha256 031ce4db55b5…)
- `x-random_walker`: [X post by @random_walker (Arvind Narayanan)](https://x.com/random_walker/status/2123869355431661866) (sha256 7c2141b1066c…)
- `x-unknown`: [X post by @unknown](https://x.com/unknown/status/2123871643797995872) (sha256 1ae5a664c766…)
- `scan-framing`: [Morning X-first scan: verification framing per story](https://www.signalandnoise.email/content/daily-state/2026-11-21/audit/sources/2026-11-21/scan-framing.txt) (sha256 5f01daec3eec…)

## episode

### FAIL · e42-token-prices-tenfold-year (number, Arvind Narayanan warning)
> Claim: driving token prices down tenfold a year

Source ([x-random_walker](https://x.com/random_walker/status/2123869355431661866)): "@random_walker: Reminder: racing to self-improve the verifiable subset of capabilities, which is what AI companies are currently doing, _decreases_ the window of time that they have to convert into sustainable businesses and do the boring work of turning value creation into value capture."

Note: Source post by Arvind Narayanan does not mention driving token prices down tenfold a year

```python
def check(ctx):
    s = ctx.find('random_walker', r'(?:tenfold|10x|token price|price)')
    if s:
        return ctx.ok('random_walker', s)
    return ctx.fail('random_walker', ctx.find('random_walker', r'sustainable businesses'), 'Source post by Arvind Narayanan does not mention driving token prices down tenfold a year')
```

### FAIL · oe2-inkling-company-reported (objection, Inkling 2 Mini)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-21/audit/sources/2026-11-21/scan-framing.txt)): "framing (Thinking Machines Lab): Company-reported architecture and benchmark results; evaluation setups vary by model and no independent replication is reported."

Note: Episode omits caveat that Inkling 2 Mini benchmarks are company-reported without independent replication

```python
def check(ctx):
    s = ctx.find('framing', r'Company-reported architecture and benchmark results')
    if ctx.art_has(r'(?:company[- ]reported|self[- ]reported|according to Thinking Machines|Thinking Machines(?:\'s)? (?:own |reported )?(?:benchmarks|numbers|results)|not independently (?:verified|replicated))'):
        return ctx.ok('framing', s, 'Episode carries company-reported caveat for Inkling 2 Mini')
    return ctx.fail('framing', s, 'Episode omits caveat that Inkling 2 Mini benchmarks are company-reported without independent replication')
```

### NEEDS-HUMAN · e41-narayanan-business-trap (attribution, Arvind Narayanan warning)
> Claim: Princeton's Arvind Narayanan, who warned today that racing on verifiable capabilities and efficiency is a business trap for frontier labs

Source ([x-random_walker](https://x.com/random_walker/status/2123869355431661866)): "@random_walker: Reminder: racing to self-improve the verifiable subset of capabilities, which is what AI companies are currently doing, _decreases_ the window of time that they have to convert into sustainable businesses and do the boring work of turning value creation into value capture."

Note: Narayanan warns on verifiable capabilities and sustainable businesses, but does not mention efficiency in this post

```python
def check(ctx):
    s1 = ctx.find('random_walker', r'racing to self-improve the verifiable subset of capabilities.*sustainable businesses')
    s2 = ctx.find('random_walker', r'Princeton computer scientist')
    if s1 and s2:
        if ctx.absent('random_walker', r'efficien'):
            return ctx.need('random_walker', s1, 'Narayanan warns on verifiable capabilities and sustainable businesses, but does not mention efficiency in this post')
        return ctx.ok('random_walker', s1)
    return ctx.need('random_walker', s1 or s2, 'Check Narayanan attribution')
```

### PASS · e01-episode-date (number, Episode date)
> Claim: November 21st, 2026

Source ([primary-naam-task-horizon-charts-critique](https://www.rameznaam.com/p/the-most-important-charts-in-ai-are)): "Nov 21, 2026"

```python
def check(ctx):
    return ctx.require('naam', r'Nov 21, 2026')
```

### PASS · e02-anthropic-mathematician-riemann (attribution, Riemann Hypothesis proof)
> Claim: a mathematician at Anthropic says he and Claude may have just proved the Riemann Hypothesis

Source ([primary-alpoge-claude-riemann-hypothesis-claim](https://alpo.ge/remark.pdf)): "I believe I have, working with Claude, discovered a proof1 of the Riemann"

Note: Anthropic affiliation confirmed via andrewcurran_

```python
def check(ctx):
    s1 = ctx.find('alpoge', r'working with Claude, discovered a proof')
    s2 = ctx.find('andrewcurran_', r'Levent Alpöge at Anthropic')
    if s1 and s2:
        return ctx.ok('alpoge', s1, 'Anthropic affiliation confirmed via andrewcurran_')
    return ctx.need('alpoge', s1 or s2, 'Could not verify both proof claim and Anthropic affiliation')
```

### PASS · e03-may-have-just-proved (qualifier, Riemann Hypothesis proof)
> Claim: may have just proved

Source ([primary-alpoge-claude-riemann-hypothesis-claim](https://alpo.ge/remark.pdf)): "I believe I have, working with Claude, discovered a proof1 of the Riemann"

```python
def check(ctx):
    return ctx.require('alpoge', r'I believe I have, working with Claude, discovered a proof')
```

### PASS · e04-150-year-old-millennium (number, Riemann Hypothesis proof)
> Claim: a one-hundred-and-fifty-year-old Millennium Prize problem

Source ([primary-alpoge-claude-riemann-hypothesis-claim](https://alpo.ge/remark.pdf)): "have guided mathematicians for 150 years, and its many rhymes and reflections,"

Note: Millennium Prize status confirmed via artificialanlys

```python
def check(ctx):
    s1 = ctx.find('alpoge', r'150 years')
    s2 = ctx.find('artificialanlys', r'Millennium Prize Problems')
    if s1 and s2:
        return ctx.ok('alpoge', s1, 'Millennium Prize status confirmed via artificialanlys')
    return ctx.need('alpoge', s1 or s2, 'Could not verify both 150-year age and Millennium Prize status')
```

### PASS · e05-real-world-data-9-to-16 (attribution, AI task-horizon analysis)
> Claim: a major new analysis of real-world data from inside OpenAI and Google shows AI can only work autonomously for nine to sixteen minutes before falling short

Source ([primary-naam-task-horizon-charts-critique](https://www.rameznaam.com/p/the-most-important-charts-in-ai-are)): "What the OpenAI and Google data show is that on real world tasks inside an AI company, AI models are 80% successful in accomplishing tasks of around nine minutes at Google and an adjusted 16 minutes at OpenAI."

```python
def check(ctx):
    return ctx.require('naam', r'nine minutes at Google and an adjusted 16 minutes at OpenAI')
```

### PASS · e06-nine-to-sixteen-minutes (number, AI task-horizon analysis)
> Claim: nine to sixteen minutes

Source ([primary-naam-task-horizon-charts-critique](https://www.rameznaam.com/p/the-most-important-charts-in-ai-are)): "What the OpenAI and Google data show is that on real world tasks inside an AI company, AI models are 80% successful in accomplishing tasks of around nine minutes at Google and an adjusted 16 minutes at OpenAI."

```python
def check(ctx):
    return ctx.require('naam', r'nine minutes.*16 minutes')
```

### PASS · e07-laptop-sized-model-tml (attribution, Inkling 2 Mini)
> Claim: a new laptop-sized model released by Thinking Machines Lab

Source ([primary-thinking-machines-inkling-2-mini-open-we](https://thinkingmachines.ai/news/inkling-2-mini/)): "Introducing Inkling 2 Mini - Thinking Machines Lab … Today we are releasing Inkling 2 Mini, a fast, powerful model that's small enough to run on your laptop."

```python
def check(ctx):
    return ctx.require('thinking', r'Thinking Machines Lab', r'releasing Inkling 2 Mini.*small enough to run on your laptop')
```

### PASS · e08-alpoge-personal-note-14-archives (attribution, Riemann Hypothesis proof)
> Claim: Levent Alpöge, a mathematician at Anthropic, posted a personal note along with fourteen archives of Lean code

Source ([primary-alpoge-claude-riemann-hypothesis-claim](https://alpo.ge/remark.pdf)): "1 https://alpo.ge/lean.tar.gz.part01, . . . , https://alpo.ge/lean.tar.gz.part14."

Note: Anthropic affiliation confirmed via andrewcurran_

```python
def check(ctx):
    s1 = ctx.find('alpoge', r'lean\.tar\.gz\.part01.*part14')
    s2 = ctx.find('andrewcurran_', r'Levent Alpöge at Anthropic')
    if s1 and s2:
        return ctx.ok('alpoge', s1, 'Anthropic affiliation confirmed via andrewcurran_')
    return ctx.need('alpoge', s1 or s2, 'Could not verify both 14 Lean archive parts and Anthropic affiliation')
```

### PASS · e09-fourteen-archives-lean (number, Riemann Hypothesis proof)
> Claim: fourteen archives of Lean code

Source ([primary-alpoge-claude-riemann-hypothesis-claim](https://alpo.ge/remark.pdf)): "1 https://alpo.ge/lean.tar.gz.part01, . . . , https://alpo.ge/lean.tar.gz.part14."

```python
def check(ctx):
    return ctx.require('alpoge', r'lean\.tar\.gz\.part01.*part14')
```

### PASS · e10-rh-grh-without-assumptions (attribution, Riemann Hypothesis proof)
> Claim: claiming he and Claude discovered a proof of the Riemann Hypothesis, and even the Generalized Riemann Hypothesis, formalized without assumptions

Source ([primary-alpoge-claude-riemann-hypothesis-claim](https://alpo.ge/remark.pdf)): "I believe I have, working with Claude, discovered a proof1 of the Riemann … so-called Generalized Riemann Hypothesis, and I expect, with more time, the … formalized the arguments without assumptions"

```python
def check(ctx):
    return ctx.require('alpoge', r'working with Claude, discovered a proof', r'Generalized Riemann Hypothesis', r'formalized the arguments without assumptions')
```

### PASS · e11-not-independently-verified (qualifier, Riemann Hypothesis proof)
> Claim: this has not been independently verified yet

Source ([x-artificialanlys](https://x.com/ArtificialAnlys/status/2123865423364161861)): "Both AI results are still awaiting independent verification, so scores are provisional."

```python
def check(ctx):
    return ctx.require('artificialanlys', r'awaiting independent verification')
```

### PASS · e12-openai-navier-stokes-september (attribution, Riemann Hypothesis proof)
> Claim: OpenAI's claimed Navier-Stokes proof back in September

Source ([x-artificialanlys](https://x.com/ArtificialAnlys/status/2123865423364161861)): "➤ OpenAI: claimed a solution to the Navier-Stokes problem in September, using an unreleased internal model"

```python
def check(ctx):
    return ctx.require('artificialanlys', r'OpenAI.*claimed a solution to the Navier-Stokes problem in September')
```

### PASS · e13-steered-claude-outpaced (attribution, Riemann Hypothesis proof)
> Claim: He steered Claude toward the right analogy, and near the finish line, Claude outpaced him.

Source ([primary-alpoge-claude-riemann-hypothesis-claim](https://alpo.ge/remark.pdf)): "I guided us to the right situation analogous … Claude far outpaced me near the finish line."

```python
def check(ctx):
    return ctx.require('alpoge', r'guided us to the right situation analogous', r'Claude far outpaced me near the finish line')
```

### PASS · e14-250000-pages (number, Riemann Hypothesis proof)
> Claim: more than two hundred and fifty thousand pages

Source ([primary-alpoge-claude-riemann-hypothesis-claim](https://alpo.ge/remark.pdf)): "2 I of course amused myself, and hit 250, 000+ pages."

```python
def check(ctx):
    return ctx.require('alpoge', r'250,\s*000\+\s*pages')
```

### PASS · e15-published-only-lean (attribution, Riemann Hypothesis proof)
> Claim: he published only the Lean code

Source ([primary-alpoge-claude-riemann-hypothesis-claim](https://alpo.ge/remark.pdf)): "I decided to only present Lean."

```python
def check(ctx):
    return ctx.require('alpoge', r'decided to only present Lean')
```

### PASS · e16-not-mastered-neighborhoods (attribution, Riemann Hypothesis proof)
> Claim: openly admitting he is presenting a complete proof before he has even mastered huge neighborhoods of its own mathematics

Source ([primary-alpoge-claude-riemann-hypothesis-claim](https://alpo.ge/remark.pdf)): "presenting the world with a complete argument before having mastered a massive neighbourhood"

```python
def check(ctx):
    return ctx.require('alpoge', r'presenting the world with a complete argument before having mastered a massive neighbourhood')
```

### PASS · e17-naam-viral-post-title (attribution, AI task-horizon analysis)
> Claim: Ramez Naam's viral post today, titled The Most Important Charts in AI are Wrong

Source ([primary-naam-task-horizon-charts-critique](https://www.rameznaam.com/p/the-most-important-charts-in-ai-are)): "The Most Important Charts in AI are Wrong - Ramez Naam … Nov 21, 2026"

```python
def check(ctx):
    return ctx.require('naam', r'The Most Important Charts in AI are Wrong', r'Ramez Naam', r'Nov 21, 2026')
```

### PASS · e18-naam-post-title-quote (quote, AI task-horizon analysis)
> Claim: The Most Important Charts in AI are Wrong

Source ([primary-naam-task-horizon-charts-critique](https://www.rameznaam.com/p/the-most-important-charts-in-ai-are)): "The Most Important Charts in AI are Wrong - Ramez Naam"

```python
def check(ctx):
    return ctx.require('naam', r'The Most Important Charts in AI are Wrong')
```

### PASS · e19-naam-compared-forecasts-data (attribution, AI task-horizon analysis)
> Claim: Naam compared famous task-horizon forecasts, like METR extrapolations and the original AI 2027 scenario, against actual internal usage data released by OpenAI and Google DeepMind

Source ([primary-naam-task-horizon-charts-critique](https://www.rameznaam.com/p/the-most-important-charts-in-ai-are)): "Real world data from OpenAI and Google looks nothing like the exponential charts from METR, AI 2027, AI Futures, and other extrapolations. … Both extrapolations of it using ECI scores and forecasts such as the original AI 2027 scenario dramatically over-estimate the length of task an AI can accomplish on real-world research tasks. … In the Gemini Argon release, Google DeepMind followed suit, with a very similar chart (though of only one time period)."

```python
def check(ctx):
    return ctx.require('naam', r'OpenAI and Google', r'original AI 2027 scenario', r'Google DeepMind', r'METR')
```

### PASS · e20-projected-30-hours-or-months (number, AI task-horizon analysis)
> Claim: projected autonomous horizons of thirty hours, or even months

Source ([primary-naam-task-horizon-charts-critique](https://www.rameznaam.com/p/the-most-important-charts-in-ai-are)): "Using Anthropic's internal capability index, AECI, to estimate what length tasks AI can accomplish today, Benjamin Todd, the founder of AI safety org 80,000 Hours, posted this chart estimating that the most powerful AI models available can autonomously complete tasks that are 30 - 40 hours long. … Finally, in 2025, the leaders of the AI Futures Project, in their initial "AI 2027" Forecast, published a chart like the below, predicting that in their fast-takeoff coding scenario, on a METR-style software-task scale, AI models would be able to autonomously accomplish tasks that take months by now, and more than a year by the end of 2027. [They since updated these forecasts, which we'll look at below.]"

```python
def check(ctx):
    return ctx.require('naam', r'30\s*[–-]\s*40 hours', r'tasks that take months')
```

### PASS · e21-google-80pct-9-min (number, AI task-horizon analysis)
> Claim: Inside Google, at an eighty percent success rate, the real number is nine minutes.

Source ([primary-naam-task-horizon-charts-critique](https://www.rameznaam.com/p/the-most-important-charts-in-ai-are)): "What the OpenAI and Google data show is that on real world tasks inside an AI company, AI models are 80% successful in accomplishing tasks of around nine minutes at Google and an adjusted 16 minutes at OpenAI."

```python
def check(ctx):
    return ctx.require('naam', r'80% successful.*nine minutes at Google')
```

### PASS · e22-openai-adjusted-16-min (number, AI task-horizon analysis)
> Claim: Inside OpenAI, even after adjusting for ambiguous requests and tool errors, it is sixteen minutes.

Source ([primary-naam-task-horizon-charts-critique](https://www.rameznaam.com/p/the-most-important-charts-in-ai-are)): "What the OpenAI and Google data show is that on real world tasks inside an AI company, AI models are 80% successful in accomplishing tasks of around nine minutes at Google and an adjusted 16 minutes at OpenAI. … Note that the OpenAI number above is higher than they report, as we've adjusted for possible reduction in success rate because of researchers giving AI ambiguous or unsolvable tasks, as well as errors in the tools that AI itself uses."

```python
def check(ctx):
    return ctx.require('naam', r'adjusted 16 minutes at OpenAI', r'ambiguous.*errors in the tools')
```

### PASS · e23-qualifier-adjusting-ambiguous-tool (qualifier, AI task-horizon analysis)
> Claim: even after adjusting for ambiguous requests and tool errors

Source ([primary-naam-task-horizon-charts-critique](https://www.rameznaam.com/p/the-most-important-charts-in-ai-are)): "Note that the OpenAI number above is higher than they report, as we've adjusted for possible reduction in success rate because of researchers giving AI ambiguous or unsolvable tasks, as well as errors in the tools that AI itself uses."

```python
def check(ctx):
    return ctx.require('naam', r'ambiguous.*errors in the tools')
```

### PASS · e24-30-to-40x-shorter (comparison, AI task-horizon analysis)
> Claim: thirty to forty times shorter than the benchmark extrapolations

Source ([primary-naam-task-horizon-charts-critique](https://www.rameznaam.com/p/the-most-important-charts-in-ai-are)): "At 80% success, ECI → METR estimates are 33× OpenAI's internal task length and 41× Google's."

```python
def check(ctx):
    return ctx.require('naam', r'33× OpenAI.*41× Google')
```

### PASS · e25-gap-widened-june-october (comparison, AI task-horizon analysis)
> Claim: the gap actually widened between June and October

Source ([primary-naam-task-horizon-charts-critique](https://www.rameznaam.com/p/the-most-important-charts-in-ai-are)): "It grew dramatically from June to October at 80% success for both the ECI → METR frontier trend and the original AI 2027 scenario."

```python
def check(ctx):
    return ctx.require('naam', r'grew dramatically from June to October')
```

### PASS · e26-openai-pace-3-6-pct (number, AI task-horizon analysis)
> Claim: OpenAI's pace of research experiments is rising only about three point six percent per point of capability gain

Source ([primary-naam-task-horizon-charts-critique](https://www.rameznaam.com/p/the-most-important-charts-in-ai-are)): "That said, after adjusting for using AI more (in the form of the log of the amount spent internally), that drops to 3.6% faster experimentation per point of ECI."

```python
def check(ctx):
    return ctx.require('naam', r'3\.6% faster experimentation per point of ECI')
```

### PASS · e27-below-15-to-19-pct-threshold (comparison, AI task-horizon analysis)
> Claim: far below the fifteen to nineteen percent threshold needed for runaway self-improvement

Source ([primary-naam-task-horizon-charts-critique](https://www.rameznaam.com/p/the-most-important-charts-in-ai-are)): "That estimated gain is still well short of the 15-19% threshold for a self-sustaining AI recursive self-improvement loop, but it's closer."

```python
def check(ctx):
    return ctx.require('naam', r'well short of the 15-19% threshold for a self-sustaining AI recursive self-improvement loop')
```

### PASS · e28-naam-called-out-anthropic-redact (attribution, AI task-horizon analysis)
> Claim: Naam also called out Anthropic for forcing METR to redact its own internal data.

Source ([primary-naam-task-horizon-charts-critique](https://www.rameznaam.com/p/the-most-important-charts-in-ai-are)): "Indeed, while METR recently looked at internal Anthropic data and found that Anthropic's AI models are accelerating AI progress, Anthropic forced METR to redact the most compelling evidence from that report."

```python
def check(ctx):
    return ctx.require('naam', r'Anthropic forced METR to redact')
```

### PASS · e29-mollick-productivity-coding-steering (attribution, AI task-horizon analysis)
> Claim: As Wharton's Ethan Mollick noted today, AI is already delivering massive productivity on well-specified coding tasks, or whenever a human is steering it.

Source ([x-emollick](https://x.com/emollick/status/2123972584400204199)): "AFFILIATION NOTE (scan): Wharton professor; independent commentator on Naam's piece. … This is well-specified work, so it has very different boundary conditions. … Occasional guidance can still leave you with enormous productivity gains, even if that doesn't satisfy the requirements for fully autonomous AI research."

```python
def check(ctx):
    return ctx.require('emollick', r'Wharton professor', r'well-specified work', r'Occasional guidance.*enormous productivity gains')
```

### PASS · e30-tml-released-inkling-2-mini (attribution, Inkling 2 Mini)
> Claim: Thinking Machines Lab just released Inkling 2 Mini

Source ([primary-thinking-machines-inkling-2-mini-open-we](https://thinkingmachines.ai/news/inkling-2-mini/)): "Introducing Inkling 2 Mini - Thinking Machines Lab … Today we are releasing Inkling 2 Mini, a fast, powerful model that's small enough to run on your laptop."

```python
def check(ctx):
    return ctx.require('thinking', r'Thinking Machines Lab', r'Today we are releasing Inkling 2 Mini')
```

### PASS · e31-open-weights-26b-model (number, Inkling 2 Mini)
> Claim: an open-weights, twenty-six-billion-parameter model

Source ([primary-thinking-machines-inkling-2-mini-open-we](https://thinkingmachines.ai/news/inkling-2-mini/)): "Inkling 2 Mini is a Mixture-of-Experts model with 26.4B total parameters, 3.4B active, and 5.4B weight activations per token to account for looping. … Inkling 2 Mini is released with open weights and is available on Tinker today for inference and customization."

```python
def check(ctx):
    return ctx.require('thinking', r'26\.4B total parameters', r'released with open weights')
```

### PASS · e32-trained-natively-4bit (number, Inkling 2 Mini)
> Claim: trained natively in four-bit precision

Source ([primary-thinking-machines-inkling-2-mini-open-we](https://thinkingmachines.ai/news/inkling-2-mini/)): "Most of Inkling 2 Mini's weights were trained and are deployed natively in NVFP4, with the last four layers in MXFP8. … Inkling 2 Mini was trained with 4-bit precision, which we describe in a recent article on Connectionism."

```python
def check(ctx):
    return ctx.require('thinking', r'trained and are deployed natively in NVFP4', r'trained with 4-bit precision')
```

### PASS · e33-fits-32gb-laptop (number, Inkling 2 Mini)
> Claim: fits on a thirty-two-gigabyte laptop

Source ([primary-thinking-machines-inkling-2-mini-open-we](https://thinkingmachines.ai/news/inkling-2-mini/)): "At launch we support Inkling 2 Mini running on any Mac system (MacBook, Mac Mini) with at least 32GB RAM via Ollama."

```python
def check(ctx):
    return ctx.require('thinking', r'MacBook.*at least 32GB RAM')
```

### PASS · e34-ties-qwen-3-8-27b-aa-index (comparison, Inkling 2 Mini)
> Claim: ties Qwen 3.8 27B on the Artificial Analysis Index

Source ([primary-thinking-machines-inkling-2-mini-open-we](https://thinkingmachines.ai/news/inkling-2-mini/)): "20.1 (Best reported score in this row)"

Note: Both Inkling 2 Mini and Qwen3.8-27B report 20.1 on AA Index (v5.0)

```python
def check(ctx):
    s1 = ctx.find('thinking', r'AA Index')
    s2 = ctx.find('thinking', r'20\.1 \(Best reported score in this row\)')
    s3 = ctx.find('thinking', r'Qwen3\.8-27B')
    if s1 and s2 and s3:
        return ctx.ok('thinking', s2, 'Both Inkling 2 Mini and Qwen3.8-27B report 20.1 on AA Index (v5.0)')
    return ctx.need('thinking', s1 or s2, 'Check AA Index tie with Qwen3.8-27B')
```

### PASS · e35-leads-open-models-under-100b-coding (comparison, Inkling 2 Mini)
> Claim: leads open models under a hundred billion parameters on agentic coding benchmarks like DeepSWE and SWE-bench Pro

Source ([primary-thinking-machines-inkling-2-mini-open-we](https://thinkingmachines.ai/news/inkling-2-mini/)): "Inkling 2 Mini leads every open-weights model with less than 100B total parameters on benchmarks such as DeepSWE v1.1 (48.2%) and Vals Index v2.2 (46.5%). … Inkling 2 Mini scores ahead of every comparable model on agentic coding benchmarks such as DeepSWE v1.1 and SWE-bench Pro v2, and is behind only Qwen3.8-27B on others."

```python
def check(ctx):
    return ctx.require('thinking', r'leads every open-weights model with less than 100B total parameters.*DeepSWE', r'agentic coding benchmarks such as DeepSWE v1\.1 and SWE-bench Pro v2')
```

### PASS · e36-middle-12-layers-3-times (number, Inkling 2 Mini)
> Claim: running its middle twelve layers three times per token

Source ([primary-thinking-machines-inkling-2-mini-open-we](https://thinkingmachines.ai/news/inkling-2-mini/)): "Inkling 2 Mini is a looped transformer, running the middle layers of the model three times for every token. … This design builds on prior work on looped transformers and is motivated by the intuition that the middle layers of the model carry more abstract reasoning, while the first and last few layers devote more space to translating between embeddings and internal representations.Universal Transformers, Dehghani et al., 2018 In our experiments, looping the middle 12 layers resulted in larger gains in accuracy than looping the last 12 on 27 out of 28 different evaluations."

```python
def check(ctx):
    return ctx.require('thinking', r'middle layers of the model three times for every token', r'looping the middle 12 layers')
```

### PASS · e37-tml-tested-oversight (attribution, Inkling 2 Mini)
> Claim: Thinking Machines tested what that means for oversight

Source ([primary-thinking-machines-inkling-2-mini-open-we](https://thinkingmachines.ai/news/inkling-2-mini/)): "Looping allows the model to reason longer without writing its reasoning down, which matters for monitoring: our ability to oversee and understand what the model does by reading its chain of thought (CoT). … We measured the impact of looping on both performance and monitorability with Inkling 2 Mini and a research-specific variable-loop variant we are releasing alongside it."

```python
def check(ctx):
    return ctx.require('thinking', r'oversee and understand what the model does', r'measured the impact of looping on both performance and monitorability')
```

### PASS · e38-looping-doubled-no-cot-horizon (comparison, Inkling 2 Mini)
> Claim: looping doubled the model's no-chain-of-thought horizon

Source ([primary-thinking-machines-inkling-2-mini-open-we](https://thinkingmachines.ai/news/inkling-2-mini/)): "The variable-loop model's no-CoT time horizon improved from 16 seconds at one pass to 37 seconds with three, and its performance on a benchmark of serial reasoning kept improving out to ten loops-twice as many as it was trained with."

```python
def check(ctx):
    return ctx.require('thinking', r'no-CoT time horizon.*from 16 seconds at one pass to 37 seconds')
```

### PASS · e39-cut-written-reasoning-in-half-5-passes (number, Inkling 2 Mini)
> Claim: cut its written reasoning in half at five passes

Source ([primary-thinking-machines-inkling-2-mini-open-we](https://thinkingmachines.ai/news/inkling-2-mini/)): "Reasoning at 5 passes was less than half as long as at 1 pass (1,661 vs."

```python
def check(ctx):
    return ctx.require('thinking', r'Reasoning at 5 passes was less than half as long as at 1 pass')
```

### PASS · e40-text-remained-legible (qualifier, Inkling 2 Mini)
> Claim: though at this scale the text remained legible

Source ([primary-thinking-machines-inkling-2-mini-open-we](https://thinkingmachines.ai/news/inkling-2-mini/)): "The model's chain of thought grew shorter with more loops but stayed legible throughout. … Overall, we find that looping increases what these models can do without a verbalized chain of thought, but at this scale we do not see a meaningful reduction in the monitorability of their reasoning."

```python
def check(ctx):
    return ctx.require('thinking', r'stayed legible throughout', r'at this scale we do not see a meaningful reduction in the monitorability')
```

### PASS · oe1-riemann-unverified (objection, Riemann Hypothesis proof)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-21/audit/sources/2026-11-21/scan-framing.txt)): "He says the proof is formalized in Lean, but no independent check of the Lean files or expert review has been reported; treat as a claim, not an established result."

Note: Episode carries unverified-proof caveat

```python
def check(ctx):
    s = ctx.find('framing', r'no independent check of the Lean files')
    if ctx.art_has(r'(?:not (?:been )?independently verified|isn\'t verified|unverified|awaiting .*verification|not yet verified)'):
        return ctx.ok('framing', s, 'Episode carries unverified-proof caveat')
    return ctx.fail('framing', s, 'Episode omits caveat that the Lean proof has not been independently verified')
```

### PASS · oe3-naam-author-analysis (objection, AI task-horizon analysis)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-21/audit/sources/2026-11-21/scan-framing.txt)): "framing (Ramez Naam (Substack)): Author's own analysis of published OpenAI and Google usage data versus METR and AI 2027 projections; an argument, not an independent measurement."

Note: Episode frames task-horizon critique as Naam's analysis

```python
def check(ctx):
    s = ctx.find('framing', r'Author\'s own analysis of published OpenAI and Google usage data')
    if ctx.art_has(r'(?:Naam(?:\'s)? (?:analysis|post|argument|critique|comparison)|according to Naam|Naam compared|author\'s (?:own )?analysis)'):
        return ctx.ok('framing', s, 'Episode frames task-horizon critique as Naam\'s analysis')
    return ctx.fail('framing', s, 'Episode omits caveat that the task-horizon critique is Naam\'s own analysis/argument')
```

## short

### FAIL · os2-inkling-company-reported (objection, Inkling 2 Mini)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-21/audit/sources/2026-11-21/scan-framing.txt)): "framing (Thinking Machines Lab): Company-reported architecture and benchmark results; evaluation setups vary by model and no independent replication is reported."

Note: Short omits caveat that Inkling 2 Mini benchmarks are company-reported without independent replication

```python
def check(ctx):
    s = ctx.find('framing', r'Company-reported architecture and benchmark results')
    if ctx.art_has(r'(?:company[- ]reported|self[- ]reported|according to Thinking Machines|Thinking Machines(?:\'s)? (?:own |reported )?(?:benchmarks|numbers|results)|not independently (?:verified|replicated))'):
        return ctx.ok('framing', s, 'Short carries company-reported caveat for Inkling 2 Mini')
    return ctx.fail('framing', s, 'Short omits caveat that Inkling 2 Mini benchmarks are company-reported without independent replication')
```

### ERROR · s18-verifiability-split-opinion (opinion, AI Verifiability Split)
> Claim: where a compiler checks the work, human understanding is optional. Everywhere else, human judgment is still the ceiling.

Note: claim quote not found verbatim in artifact

```python
def check(ctx):
    return ctx.need(None, None, 'Editorial opinion/synthesis on verifiable vs. unverifiable tasks; requires human judgment')
```

### NEEDS-HUMAN · s16-30-40x-gap (number, AI Autonomous Horizons)
> Claim: 30–40x gap

Note: no source sentence matches /33–41× at 80%/. 

```python
def check(ctx):
    return ctx.require('naam', r'33–41× at 80%')
```

### PASS · os1-riemann-unverified (objection, Riemann Hypothesis Proof)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-21/audit/sources/2026-11-21/scan-framing.txt)): "He says the proof is formalized in Lean, but no independent check of the Lean files or expert review has been reported; treat as a claim, not an established result."

Note: Short carries unverified-proof caveat

```python
def check(ctx):
    s = ctx.find('framing', r'no independent check of the Lean files')
    if ctx.art_has(r'(?:not (?:been )?independently verified|isn\'t verified|unverified|awaiting .*verification|not yet verified)'):
        return ctx.ok('framing', s, 'Short carries unverified-proof caveat')
    return ctx.fail('framing', s, 'Short omits caveat that the Lean proof has not been independently verified')
```

### PASS · os3-naam-author-analysis (objection, AI Autonomous Horizons)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-21/audit/sources/2026-11-21/scan-framing.txt)): "framing (Ramez Naam (Substack)): Author's own analysis of published OpenAI and Google usage data versus METR and AI 2027 projections; an argument, not an independent measurement."

Note: Short frames task-horizon critique as Naam's analysis

```python
def check(ctx):
    s = ctx.find('framing', r'Author\'s own analysis of published OpenAI and Google usage data')
    if ctx.art_has(r'(?:Naam(?:\'s)? (?:analysis|post|argument|critique|comparison)|according to Naam|Naam compared|author\'s (?:own )?analysis)'):
        return ctx.ok('framing', s, 'Short frames task-horizon critique as Naam\'s analysis')
    return ctx.fail('framing', s, 'Short omits caveat that the task-horizon critique is Naam\'s own analysis/argument')
```

### PASS · s01-anthropic-mathematician-rh (attribution, Riemann Hypothesis Proof)
> Claim: An Anthropic mathematician claims Claude helped him prove the Riemann Hypothesis

Source ([primary-alpoge-claude-riemann-hypothesis-claim](https://alpo.ge/remark.pdf)): "I believe I have, working with Claude, discovered a proof1 of the Riemann"

Note: Anthropic affiliation confirmed via andrewcurran_

```python
def check(ctx):
    s1 = ctx.find('alpoge', r'working with Claude, discovered a proof')
    s2 = ctx.find('andrewcurran_', r'Levent Alpöge at Anthropic')
    if s1 and s2:
        return ctx.ok('alpoge', s1, 'Anthropic affiliation confirmed via andrewcurran_')
    return ctx.need('alpoge', s1 or s2, 'Could not verify both proof claim and Anthropic affiliation')
```

### PASS · s02-real-data-9-to-16 (attribution, AI Autonomous Horizons)
> Claim: real data from Google and OpenAI shows AI only works autonomously for nine to sixteen minutes

Source ([primary-naam-task-horizon-charts-critique](https://www.rameznaam.com/p/the-most-important-charts-in-ai-are)): "What the OpenAI and Google data show is that on real world tasks inside an AI company, AI models are 80% successful in accomplishing tasks of around nine minutes at Google and an adjusted 16 minutes at OpenAI."

```python
def check(ctx):
    return ctx.require('naam', r'nine minutes at Google and an adjusted 16 minutes at OpenAI')
```

### PASS · s03-nine-to-sixteen-minutes (number, AI Autonomous Horizons)
> Claim: nine to sixteen minutes

Source ([primary-naam-task-horizon-charts-critique](https://www.rameznaam.com/p/the-most-important-charts-in-ai-are)): "What the OpenAI and Google data show is that on real world tasks inside an AI company, AI models are 80% successful in accomplishing tasks of around nine minutes at Google and an adjusted 16 minutes at OpenAI."

```python
def check(ctx):
    return ctx.require('naam', r'nine minutes.*16 minutes')
```

### PASS · s04-16-minute-horizons (number, AI Autonomous Horizons)
> Claim: 16-Minute Horizons

Source ([primary-naam-task-horizon-charts-critique](https://www.rameznaam.com/p/the-most-important-charts-in-ai-are)): "What the OpenAI and Google data show is that on real world tasks inside an AI company, AI models are 80% successful in accomplishing tasks of around nine minutes at Google and an adjusted 16 minutes at OpenAI."

```python
def check(ctx):
    return ctx.require('naam', r'16 minutes at OpenAI')
```

### PASS · s05-9-to-16-min (number, AI Autonomous Horizons)
> Claim: 9–16 min

Source ([primary-naam-task-horizon-charts-critique](https://www.rameznaam.com/p/the-most-important-charts-in-ai-are)): "What the OpenAI and Google data show is that on real world tasks inside an AI company, AI models are 80% successful in accomplishing tasks of around nine minutes at Google and an adjusted 16 minutes at OpenAI."

```python
def check(ctx):
    return ctx.require('naam', r'nine minutes.*16 minutes')
```

### PASS · s06-proof-not-verified-yet (qualifier, Riemann Hypothesis Proof)
> Claim: The claimed math proof isn't verified yet

Source ([x-artificialanlys](https://x.com/ArtificialAnlys/status/2123865423364161861)): "Both AI results are still awaiting independent verification, so scores are provisional."

```python
def check(ctx):
    return ctx.require('artificialanlys', r'awaiting independent verification')
```

### PASS · s07-author-not-mastered (attribution, Riemann Hypothesis Proof)
> Claim: its author admits he hasn't mastered huge parts of it

Source ([primary-alpoge-claude-riemann-hypothesis-claim](https://alpo.ge/remark.pdf)): "before having mastered a massive neighbourhood"

```python
def check(ctx):
    return ctx.require('alpoge', r'before having mastered a massive neighbourhood')
```

### PASS · s08-prose-250k-pages (number, Riemann Hypothesis Proof)
> Claim: Prose hit two hundred fifty thousand pages

Source ([primary-alpoge-claude-riemann-hypothesis-claim](https://alpo.ge/remark.pdf)): "2 I of course amused myself, and hit 250, 000+ pages."

```python
def check(ctx):
    return ctx.require('alpoge', r'250,\s*000\+\s*pages')
```

### PASS · s09-shipped-lean-code-compiler (attribution, Riemann Hypothesis Proof)
> Claim: he just shipped Lean code for a compiler to check

Source ([primary-alpoge-claude-riemann-hypothesis-claim](https://alpo.ge/remark.pdf)): "I decided to only present Lean."

```python
def check(ctx):
    return ctx.require('alpoge', r'decided to only present Lean')
```

### PASS · s10-claimed-proof-only-lean (qualifier, Riemann Hypothesis Proof)
> Claim: Claimed Proof Shipped Only in Lean

Source ([primary-alpoge-claude-riemann-hypothesis-claim](https://alpo.ge/remark.pdf)): "I decided to only present Lean."

```python
def check(ctx):
    return ctx.require('alpoge', r'decided to only present Lean')
```

### PASS · s11-250000-plus-pp (number, Riemann Hypothesis Proof)
> Claim: 250,000+ pp

Source ([primary-alpoge-claude-riemann-hypothesis-claim](https://alpo.ge/remark.pdf)): "2 I of course amused myself, and hit 250, 000+ pages."

```python
def check(ctx):
    return ctx.require('alpoge', r'250,\s*000\+\s*pages')
```

### PASS · s12-naam-compared-forecasts (attribution, AI Autonomous Horizons)
> Claim: Ramez Naam compared famous AI forecasts against internal Google and OpenAI data

Source ([primary-naam-task-horizon-charts-critique](https://www.rameznaam.com/p/the-most-important-charts-in-ai-are)): "The Most Important Charts in AI are Wrong - Ramez Naam … Real world data from OpenAI and Google looks nothing like the exponential charts from METR, AI 2027, AI Futures, and other extrapolations."

```python
def check(ctx):
    return ctx.require('naam', r'Ramez Naam', r'Real world data from OpenAI and Google.*METR, AI 2027')
```

### PASS · s13-80-pct-reliability (number, AI Autonomous Horizons)
> Claim: At eighty percent reliability

Source ([primary-naam-task-horizon-charts-critique](https://www.rameznaam.com/p/the-most-important-charts-in-ai-are)): "What the OpenAI and Google data show is that on real world tasks inside an AI company, AI models are 80% successful in accomplishing tasks of around nine minutes at Google and an adjusted 16 minutes at OpenAI."

```python
def check(ctx):
    return ctx.require('naam', r'80% successful.*nine minutes at Google')
```

### PASS · s14-30-to-40x-shorter (comparison, AI Autonomous Horizons)
> Claim: real autonomous horizons are thirty to forty times shorter than predicted

Source ([primary-naam-task-horizon-charts-critique](https://www.rameznaam.com/p/the-most-important-charts-in-ai-are)): "At 80% success, ECI → METR estimates are 33× OpenAI's internal task length and 41× Google's."

```python
def check(ctx):
    return ctx.require('naam', r'33× OpenAI.*41× Google')
```

### PASS · s15-trail-forecasts-30-40x (comparison, AI Autonomous Horizons)
> Claim: Real Horizons Trail Forecasts by 30–40x

Source ([primary-naam-task-horizon-charts-critique](https://www.rameznaam.com/p/the-most-important-charts-in-ai-are)): "At 80% success, ECI → METR estimates are 33× OpenAI's internal task length and 41× Google's."

```python
def check(ctx):
    return ctx.require('naam', r'33× OpenAI.*41× Google')
```

### PASS · s17-inkling-crushing-verifiable-coding (comparison, Inkling 2 Mini)
> Claim: laptop models like Thinking Machines' new Inkling 2 Mini are already crushing verifiable coding benchmarks

Source ([primary-thinking-machines-inkling-2-mini-open-we](https://thinkingmachines.ai/news/inkling-2-mini/)): "Today we are releasing Inkling 2 Mini, a fast, powerful model that's small enough to run on your laptop. … Inkling 2 Mini scores ahead of every comparable model on agentic coding benchmarks such as DeepSWE v1.1 and SWE-bench Pro v2, and is behind only Qwen3.8-27B on others."

```python
def check(ctx):
    return ctx.require('thinking', r'small enough to run on your laptop', r'scores ahead of every comparable model on agentic coding benchmarks')
```

### PASS · s19-26b-local (number, Inkling 2 Mini)
> Claim: 26B local

Source ([primary-thinking-machines-inkling-2-mini-open-we](https://thinkingmachines.ai/news/inkling-2-mini/)): "Inkling 2 Mini is a Mixture-of-Experts model with 26.4B total parameters, 3.4B active, and 5.4B weight activations per token to account for looping. … The total memory footprint of Inkling 2 Mini is ~20GB, allowing it to run on local devices such as consumer laptops and desktop AI computers."

```python
def check(ctx):
    return ctx.require('thinking', r'26\.4B total parameters', r'run on local devices')
```

### PASS · s20-sources-attribution (attribution, Sources)
> Claim: Source: Levent Alpöge / Ramez Naam / Thinking Machines Lab.

Source ([primary-thinking-machines-inkling-2-mini-open-we](https://thinkingmachines.ai/news/inkling-2-mini/)): "Introducing Inkling 2 Mini - Thinking Machines Lab"

Note: All three source attributions verified across snapshots

```python
def check(ctx):
    s1 = ctx.find('andrewcurran_', r'Levent Alpöge')
    s2 = ctx.find('naam', r'Ramez Naam')
    s3 = ctx.find('thinking', r'Thinking Machines Lab')
    if s1 and s2 and s3:
        return ctx.ok('thinking', s3, 'All three source attributions verified across snapshots')
    return ctx.need(None, None, 'Could not verify all three source attributions')
```

## takeaways

### PASS · ot1-riemann-unverified (objection, Riemann Hypothesis proof claim)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-21/audit/sources/2026-11-21/scan-framing.txt)): "He says the proof is formalized in Lean, but no independent check of the Lean files or expert review has been reported; treat as a claim, not an established result."

Note: Takeaways carries unverified-proof caveat

```python
def check(ctx):
    s = ctx.find('framing', r'no independent check of the Lean files')
    if ctx.art_has(r'(?:not (?:been )?independently verified|isn\'t verified|unverified|awaiting .*verification|not yet verified)'):
        return ctx.ok('framing', s, 'Takeaways carries unverified-proof caveat')
    return ctx.fail('framing', s, 'Takeaways omits caveat that the Lean proof has not been independently verified')
```

### PASS · t01-anthropic-mathematician-alpoge (attribution, Riemann Hypothesis proof claim)
> Claim: Anthropic mathematician Levent Alpöge

Source ([x-andrewcurran_](https://x.com/AndrewCurran_/status/2123819916768039149)): "@AndrewCurran_: Levent Alpöge at Anthropic says he has a proof of the Riemann Hypothesis."

```python
def check(ctx):
    return ctx.require('andrewcurran_', r'Levent Alpöge at Anthropic')
```

### PASS · t02-alpoge-claude-lean-rh (attribution, Riemann Hypothesis proof claim)
> Claim: Levent Alpöge claimed he and Claude found a Lean-formalized proof of the Riemann Hypothesis

Source ([primary-alpoge-claude-riemann-hypothesis-claim](https://alpo.ge/remark.pdf)): "I believe I have, working with Claude, discovered a proof1 of the Riemann"

Note: Author name confirmed via andrewcurran_ and Lean formalization via alpoge

```python
def check(ctx):
    s1 = ctx.find('alpoge', r'working with Claude, discovered a proof')
    s2 = ctx.find('alpoge', r'formalized the arguments')
    s3 = ctx.find('andrewcurran_', r'Levent Alpöge')
    if s1 and s2 and s3:
        return ctx.ok('alpoge', s1, 'Author name confirmed via andrewcurran_ and Lean formalization via alpoge')
    return ctx.need('alpoge', s1 or s2, 'Could not verify author, proof claim, and Lean formalization')
```

### PASS · t03-not-independently-verified (qualifier, Riemann Hypothesis proof claim)
> Claim: the proof has not been independently verified yet

Source ([x-artificialanlys](https://x.com/ArtificialAnlys/status/2123865423364161861)): "Both AI results are still awaiting independent verification, so scores are provisional."

```python
def check(ctx):
    return ctx.require('artificialanlys', r'awaiting independent verification')
```

### PASS · tc01-citation (citation, takeaway 1)

Note: Takeaway 1 cites https://alpo.ge/remark.pdf, which is listed in the episode sources.json.

```python
def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 1 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 1 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))
```
