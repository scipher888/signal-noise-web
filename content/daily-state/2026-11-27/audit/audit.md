# Executable audit, Daily State of AI 2026-11-27

Each claim is tested by a deterministic Python check against snapshotted source texts and X posts. PASS = the source sentence quoted supports the claim; FAIL = the source contradicts it or a required caveat is missing; NEEDS-HUMAN = opinion or not decidable by string/number match.

| artifact | PASS | FAIL | NEEDS-HUMAN | ERROR |
|---|---|---|---|---|
| episode | 42 | 3 | 30 | 0 |
| takeaways | 22 | 2 | 7 | 0 |

## Sources
- `primary-claude-research-sabotage-allegations`: [Ex-Anthropic engineer accuses Claude of sabotaging research — Anthropic’s own record tells a narrower story](https://aifrontierpost.com/articles/schirano-claude-sabotage-claim/) (sha256 78509de1c454…)
- `x-realastropulse`: [X post by @RealAstropulse (Astropulse)](https://x.com/RealAstropulse/status/2126119408997466389) (sha256 02f0f3bbb809…)
- `x-ptrcast`: [X post by @ptrCast (injuly)](https://x.com/ptrCast/status/2126021553116881326) (sha256 3ccd3ef0ab43…)
- `x-capital_vmv`: [X post by @capital_vmv (Mark Verner)](https://x.com/capital_vmv/status/2126025365017801155) (sha256 62f06aeda49c…)
- `primary-metr-openai-pretraining-loss-caveat`: [Interpreting a recent acceleration in pretraining loss](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/) (sha256 47f1ad6fc31f…)
- `x-ramez`: [X post by @ramez (Ramez Naam)](https://x.com/ramez/status/2126112326172442974) (sha256 d62061e8f528…)
- `x-ibab`: [X post by @ibab (Igor Babuschkin)](https://x.com/ibab/status/2126077013857538266) (sha256 3ca6cb1ea586…)
- `x-tobyordoxford`: [X post by @tobyordoxford (Toby Ord)](https://x.com/tobyordoxford/status/2126063832518852763) (sha256 6a1e92ea2bf7…)
- `x-skirano`: [X post by @skirano](https://x.com/skirano/status/2125371115979641188) (sha256 c8d682b0b092…)
- `x-bethmaybarnes`: [X post by @BethMayBarnes](https://x.com/BethMayBarnes/status/2126047518572310984) (sha256 5a1d2af6adb0…)
- `scan-framing`: [Morning X-first scan: verification framing per story](https://www.signalandnoise.email/content/daily-state/2026-11-27/audit/sources/2026-11-27/scan-framing.txt) (sha256 0da689d3301d…)

## episode

### FAIL · oe3-no-audit (objection, Anthropic capability limits)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-27/audit/sources/2026-11-27/scan-framing.txt)): "framing (Anthropic): Company-reported description of its own training-time limits; not independently audited."

Note: Disclose lack of independent audit of the limits.

```python
def check(ctx):
    q = ctx.find('framing', r'not independently audited')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:not|never) independently (?:audited|verified|tested)|no independent (?:audit|verification|test)') else ctx.fail('framing', q, 'Disclose lack of independent audit of the limits.')
```

### FAIL · oe5-retrieval-date (objection, API refusal and fallback behavior)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-27/audit/sources/2026-11-27/scan-framing.txt)): "framing (Anthropic (Claude Platform docs)): Company documentation of refusal categories; published_date is the retrieval date, not a release date."

Note: Docs date is retrieval, not release.

```python
def check(ctx):
    q = ctx.find('framing', r'published_date is the retrieval date')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:retrieval|access|snapshot) date[^.]{0,80}not[^.]{0,25}release|(?:retrieved|accessed)[^.]{0,100}not[^.]{0,25}release') else ctx.fail('framing', q, 'Docs date is retrieval, not release.')
```

### FAIL · oe6-news-analysis (objection, Claude sabotage allegations)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-27/audit/sources/2026-11-27/scan-framing.txt)): "framing (AI Frontier Post): Third-party news analysis; reports Schirano shared no transcript or log."

Note: Identify the secondary reporting on Schirano’s evidence.

```python
def check(ctx):
    q = ctx.find('framing', r'Third-party news analysis')
    return ctx.ok('framing', q) if ctx.art_has(r'AI Frontier Post[^.]{0,80}(?:report|analysis|notes)|(?:analysis|reporting) (?:by|from) AI Frontier Post|third-party (?:news |reporting )?analysis') else ctx.fail('framing', q, 'Identify the secondary reporting on Schirano’s evidence.')
```

### NEEDS-HUMAN · e01-episode-date (number, Daily State of AI)
> Claim: Friday, November 27th, 2026

Note: no source sentence matches /Friday,? November 27(?:th)?,? 2026/. Check the episode dateline, not the date of either news story.

```python
def check(ctx):
    return ctx.require('framing', r'Friday,? November 27(?:th)?,? 2026', note='Check the episode dateline, not the date of either news story.')
```

### NEEDS-HUMAN · e02-universal-goal (opinion, AI acceleration boundary)
> Claim: Everyone watching frontier AI wants to draw one crisp line: the point where AI systems start accelerating the work of building better AI systems.

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "However, we think publishing information about pretraining loss is very valuable for informing the public about the prospect of AI R&D acceleration."

Note: Editorial generalization about what everyone wants.

```python
def check(ctx):
    return ctx.need('metr', ctx.find('metr', r'prospect of AI R&D acceleration'), 'Editorial generalization about what everyone wants.')
```

### NEEDS-HUMAN · e03-hard-boundary (opinion, AI acceleration boundary)
> Claim: This week showed how hard it is to locate that line, whether you are trying to measure it from the outside or fence it off inside a live product.

Source ([primary-claude-research-sabotage-allegations](https://aifrontierpost.com/articles/schirano-claude-sabotage-claim/)): "Researchers who build agents and model harnesses still have to trust that the boundary Anthropic drew - frontier LLM development, and only that - is where the limits actually stop."

Note: Interpretive link between two stories.

```python
def check(ctx):
    return ctx.need('claude', ctx.find('claude', r'where the limits actually stop'), 'Interpretive link between two stories.')
```

### NEEDS-HUMAN · e19-looks-new (opinion, METR chart debate)
> Claim: making a quick commentary look like a new research finding

Source ([x-bethmaybarnes](https://x.com/BethMayBarnes/status/2126047518572310984)): "This was intended as a quick "Update" post saying "this is useful data, thanks, more please!", but I think it was foreseeable that having this graph as the headline figure would be read as a "Research" finding about degree of acceleration."

Note: Interpretation of reader perception.

```python
def check(ctx):
    return ctx.need('bethmaybarnes', ctx.find('bethmaybarnes', r'foreseeable that having this graph as the headline figure'), 'Interpretation of reader perception.')
```

### NEEDS-HUMAN · e21-apology-timing (attribution, METR chart debate)
> Claim: After Oxford philosopher Toby Ord criticized it on that basis, METR CEO Beth Barnes apologized publicly yesterday

Source ([x-bethmaybarnes](https://x.com/BethMayBarnes/status/2126047518572310984)): "Sorry!"

Note: Public apology; need a dated post establishing November 26 and the chronology relative to Ord’s criticism.

```python
def check(ctx):
    q = ctx.find('bethmaybarnes', r'^Sorry!')
    return ctx.need('bethmaybarnes', q, 'Public apology; need a dated post establishing November 26 and the chronology relative to Ord’s criticism.')
```

### NEEDS-HUMAN · e23-underlying-fog (opinion, Sources of acceleration)
> Claim: Once the presentation debate cleared, the underlying fog remained.

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "There remain substantial disagreements on how much this information should modify our projections of the future path of capabilities, and METR does not have a consensus view on this."

Note: Editorial interpretation.

```python
def check(ctx):
    return ctx.need('metr', ctx.find('metr', r'There remain substantial disagreements'), 'Editorial interpretation.')
```

### NEEDS-HUMAN · e24-shifted-credit (attribution, Sources of acceleration)
> Claim: Outside analysts argued that faster pretraining mostly shifts credit for capability gains we already saw

Source ([x-ramez](https://x.com/ramez/status/2126112326172442974)): "I still find this perplexity data fascinating, but the lack of a commensurate capability gain on _most_ capabilities makes it, ummm, a bit perplexing."

Note: A mismatch with most capability measures does not specify a mostly retrospective reallocation of credit; verify the attributed argument.

```python
def check(ctx):
    q = ctx.find('ramez', r'lack of a commensurate capability gain')
    return ctx.need('ramez', q, 'A mismatch with most capability measures does not specify a mostly retrospective reallocation of credit; verify the attributed argument.')
```

### NEEDS-HUMAN · e26-automation-role (opinion, Sources of acceleration)
> Claim: Even the role of AI automation is hard to isolate.

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "Lower pretraining loss could be attributable to a number of factors: for example, increased training compute, increased labor or experimental compute spending, or increased uplift from AI assistance."

Note: Interpretation of confounding.

```python
def check(ctx):
    return ctx.need('metr', ctx.find('metr', r'Lower pretraining loss could be attributable to a number of factors'), 'Interpretation of confounding.')
```

### NEEDS-HUMAN · e31-cannot-separate (opinion, Sources of acceleration)
> Claim: outsiders still cannot separate genuine AI-driven research from ordinary engineering catch-up

Source ([x-ibab](https://x.com/ibab/status/2126077013857538266)): "@ibab: The speedup is likely confounded by OpenAI lagging behind on pretraining tech for a few generations and catching up now."

Note: Judgment about identifiability.

```python
def check(ctx):
    return ctx.need('ibab', ctx.find('ibab', r'likely confounded by OpenAI lagging behind'), 'Judgment about identifiability.')
```

### NEEDS-HUMAN · e32-equal-difficulty (comparison, AI acceleration boundary)
> Claim: If independent evaluators cannot cleanly separate frontier AI acceleration from ordinary engineering in a chart, labs are finding it just as hard to isolate inside a deployed model.

Source ([primary-claude-research-sabotage-allegations](https://aifrontierpost.com/articles/schirano-claude-sabotage-claim/)): "Researchers who build agents and model harnesses still have to trust that the boundary Anthropic drew - frontier LLM development, and only that - is where the limits actually stop."

Note: No common measure of difficulty in the two settings.

```python
def check(ctx):
    return ctx.need('claude', ctx.find('claude', r'where the limits actually stop'), 'No common measure of difficulty in the two settings.')
```

### NEEDS-HUMAN · e33-tension (opinion, Claude sabotage allegations)
> Claim: That tension erupted at Anthropic this week

Source ([primary-claude-research-sabotage-allegations](https://aifrontierpost.com/articles/schirano-claude-sabotage-claim/)): "The charge went viral - but Anthropic's own disclosures show something narrower, and older, than the accusation suggests."

Note: Editorial characterization of the controversy.

```python
def check(ctx):
    return ctx.need('claude', ctx.find('claude', r'The charge went viral'), 'Editorial characterization of the controversy.')
```

### NEEDS-HUMAN · e36-like-count (number, Claude sabotage allegations)
> Claim: The post topped nineteen thousand likes

Note: no source sentence matches /(?:post|it) (?:passed|topped|surpassed|has passed) (?:19,000|19k|nineteen thousand) likes/. Views and likes on replies are not likes on the original post.

```python
def check(ctx):
    return ctx.require('claude', r'(?:post|it) (?:passed|topped|surpassed|has passed) (?:19,000|19k|nineteen thousand) likes', note='Views and likes on replies are not likes on the original post.')
```

### NEEDS-HUMAN · e37-viral-threads (attribution, Claude sabotage allegations)
> Claim: set off other viral threads blaming Claude, and sometimes GPT, for ruined training runs

Source ([x-realastropulse](https://x.com/RealAstropulse/status/2126119408997466389)): "@RealAstropulse: After seeing the "Claude sabotages your ML research" posts, I was still skeptical, so I tested it on my own work."

Note: Related anecdotes, but verify their reach, ruined runs, and causal link to this specific post. @ptrCast: &gt; hear rumors about claude/GPT sabotaging ML work

```python
def check(ctx):
    q = ctx.find('realastropulse', r'After seeing the .Claude sabotages your ML research. posts')
    g = ctx.find('ptrcast', r'hear rumors about claude/GPT sabotaging ML work')
    return ctx.need('realastropulse', q, 'Related anecdotes, but verify their reach, ruined runs, and causal link to this specific post. ' + (g or ''))
```

### NEEDS-HUMAN · e38-no-materials (qualifier, Claude sabotage allegations)
> Claim: None of those viral posts shared prompts, code, or logs

Source ([x-realastropulse](https://x.com/RealAstropulse/status/2126119408997466389)): "AFFILIATION NOTE (scan): Independent developer; personal anecdote with screenshots, no shared code or logs."

Note: Verify prompts, code and logs across all cited posts, including linked threads; one scan note does not settle the universal negative.

```python
def check(ctx):
    q = ctx.find('realastropulse', r'personal anecdote with screenshots, no shared code or logs')
    return ctx.need('realastropulse', q, 'Verify prompts, code and logs across all cited posts, including linked threads; one scan note does not settle the universal negative.')
```

### NEEDS-HUMAN · e40-launch-framing (attribution, Anthropic capability limits)
> Claim: In that launch post, Anthropic framed its limits under safety and alignment

Note: no source sentence matches /(?:launch|Anthropic|November).*safety and alignment/. Verify the launch post’s own framing, not a commenter’s view of alignment.

```python
def check(ctx):
    return ctx.require('claude', r'(?:launch|Anthropic|November).*safety and alignment', note='Verify the launch post’s own framing, not a commenter’s view of alignment.')
```

### NEEDS-HUMAN · e42-cap-domains (qualifier, Anthropic capability limits)
> Claim: including accelerator kernel optimization and language-model architecture

Note: no source sentence matches /cap covers two capabilities — optimizing accelerator kernels and improving large language model architectures/. 

```python
def check(ctx):
    return ctx.require('claude', r'cap covers two capabilities — optimizing accelerator kernels and improving large language model architectures')
```

### NEEDS-HUMAN · e47-api-messiness (opinion, API refusal and fallback behavior)
> Claim: Anthropic's own API documentation shows why that boundary feels messier in practice

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-27/audit/sources/2026-11-27/scan-framing.txt)): "framing (Anthropic (Claude Platform docs)): Company documentation of refusal categories; published_date is the retrieval date, not a release date."

Note: Interpretive judgment; API document text is not supplied.

```python
def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'Company documentation of refusal categories'), 'Interpretive judgment; API document text is not supplied.')
```

### NEEDS-HUMAN · e48-commercial-policy (attribution, API refusal and fallback behavior)
> Claim: In the developer docs, the frontier LLM refusal classifier is explicitly defined as a commercial restriction against building competing models

Note: no source sentence matches /(?:Claude Platform docs|Company documentation).*frontier LLM.*commercial restriction.*competing models/. Need the actual documentation defining the classifier; a competitive-advantage allegation in replies is not documentation.

```python
def check(ctx):
    return ctx.require('framing', r'(?:Claude Platform docs|Company documentation).*frontier LLM.*commercial restriction.*competing models', note='Need the actual documentation defining the classifier; a competitive-advantage allegation in replies is not documentation.')
```

### NEEDS-HUMAN · e49-benign-trigger (attribution, API refusal and fallback behavior)
> Claim: Anthropic acknowledges that benign machine-learning work can trigger it

Note: no source sentence matches /(?:Anthropic|Company documentation).*benign (?:ML|machine.learning).*?(?:trigger|refus)/. Need company documentation about false positives, not anecdotes about refusals.

```python
def check(ctx):
    return ctx.require('framing', r'(?:Anthropic|Company documentation).*benign (?:ML|machine.learning).*?(?:trigger|refus)', note='Need company documentation about false positives, not anecdotes about refusals.')
```

### NEEDS-HUMAN · e50-before-output (qualifier, API refusal and fallback behavior)
> Claim: still be billed before any output appears

Note: no source sentence matches /(?:refusal|request).*bill(?:ed|ing).*before any output/. The supplied docs summary does not specify billing.

```python
def check(ctx):
    return ctx.require('framing', r'(?:refusal|request).*bill(?:ed|ing).*before any output', note='The supplied docs summary does not specify billing.')
```

### NEEDS-HUMAN · e51-api-disclosure (qualifier, API refusal and fallback behavior)
> Claim: refusals and fallbacks are technically disclosed in the API

Note: no source sentence matches /(?:API|Claude Platform docs).*refusal.*fallback.*(?:notice|block|disclos|signal)/. Transparent fallback alone does not verify API signaling for both.

```python
def check(ctx):
    return ctx.require('framing', r'(?:API|Claude Platform docs).*refusal.*fallback.*(?:notice|block|disclos|signal)', note='Transparent fallback alone does not verify API signaling for both.')
```

### NEEDS-HUMAN · e52-http-status (number, API refusal and fallback behavior)
> Claim: refusals arrive as standard HTTP 200 responses

Note: no source sentence matches /refusal.*HTTP 200\b/. Verify the status for refusals in the missing API text.

```python
def check(ctx):
    return ctx.require('framing', r'refusal.*HTTP 200\b', note='Verify the status for refusals in the missing API text.')
```

### NEEDS-HUMAN · e53-error-alerts (qualifier, API refusal and fallback behavior)
> Claim: standard HTTP 200 responses that normal error alerts miss

Note: no source sentence matches /HTTP 200.*(?:miss|not trigger|bypass).*error alerts/. Need evidence on status and alert behavior.

```python
def check(ctx):
    return ctx.require('framing', r'HTTP 200.*(?:miss|not trigger|bypass).*error alerts', note='Need evidence on status and alert behavior.')
```

### NEEDS-HUMAN · e54-sticky-routing (qualifier, API refusal and fallback behavior)
> Claim: sticky routing sends later turns straight to the weaker fallback model

Note: drafted check rejected by the screen (imports, I/O or syntax); review by hand

```python
def check(ctx):
    return ctx.need(None, None, 'drafted check rejected by the screen (imports, I/O or syntax); review by hand')
```

### NEEDS-HUMAN · e56-no-repeat-block (qualifier, API refusal and fallback behavior)
> Claim: without repeating the fallback block

Note: no source sentence matches /(?:without repeating|do not repeat|omit).*fallback (?:block|notice)/. Need the API description of subsequent turns.

```python
def check(ctx):
    return ctx.require('framing', r'(?:without repeating|do not repeat|omit).*fallback (?:block|notice)', note='Need the API description of subsequent turns.')
```

### NEEDS-HUMAN · e57-invisible-drop (opinion, API refusal and fallback behavior)
> Claim: Inside an uninstrumented harness, a sudden capability drop can easily feel invisible.

Source ([primary-claude-research-sabotage-allegations](https://aifrontierpost.com/articles/schirano-claude-sabotage-claim/)): "Researchers who build agents and model harnesses still have to trust that the boundary Anthropic drew - frontier LLM development, and only that - is where the limits actually stop."

Note: Inference about the user experience, not a documented test.

```python
def check(ctx):
    return ctx.need('claude', ctx.find('claude', r'Researchers who build agents and model harnesses'), 'Inference about the user experience, not a documented test.')
```

### NEEDS-HUMAN · e61-looks-like-sabotage (opinion, Claude sabotage allegations)
> Claim: any misfired classifier or stubborn bug immediately looks like sabotage

Source ([x-capital_vmv](https://x.com/capital_vmv/status/2126025365017801155)): "From that moment on, any glitch, hallucination, or model error is inherently perceived by the audience as malicious intent or hidden censorship until proven otherwise."

Note: Commentary about perceived intent.

```python
def check(ctx):
    return ctx.need('capital_vmv', ctx.find('capital_vmv', r'any glitch, hallucination, or model error'), 'Commentary about perceived intent.')
```

### NEEDS-HUMAN · e62-shared-assumption (comparison, AI acceleration boundary)
> Claim: Measuring AI-accelerated research in a loss curve and quarantining it behind a classifier both assume a sharp border between routine machine learning and frontier self-improvement.

Source ([primary-claude-research-sabotage-allegations](https://aifrontierpost.com/articles/schirano-claude-sabotage-claim/)): "Researchers who build agents and model harnesses still have to trust that the boundary Anthropic drew - frontier LLM development, and only that - is where the limits actually stop."

Note: Conceptual analogy, not a shared assumption established by the sources.

```python
def check(ctx):
    return ctx.need('claude', ctx.find('claude', r'where the limits actually stop'), 'Conceptual analogy, not a shared assumption established by the sources.')
```

### NEEDS-HUMAN · e63-clean-border (opinion, AI acceleration boundary)
> Claim: Right now, neither evaluators nor labs can draw that border cleanly

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "More importantly, knowing the lag helps us determine how much AI uplift contributed to the pretraining gains: regardless of when a model was released, we can't attribute its pretraining gains to AI agents if its pretraining happened when researchers barely used AI agents."

Note: Cross-story editorial conclusion.

```python
def check(ctx):
    return ctx.need('metr', ctx.find('metr', r'knowing the lag helps us determine how much AI uplift'), 'Cross-story editorial conclusion.')
```

### NEEDS-HUMAN · e64-future-fog (opinion, AI acceleration boundary)
> Claim: until they can, every dramatic chart and every unexplained model stumble will land straight in the fog

Source ([x-bethmaybarnes](https://x.com/BethMayBarnes/status/2126047518572310984)): "@BethMayBarnes: I signed off on this post + thread, but on reflection I'm not sure it quite meets our standards for research communication: I don't think I disagree with anything we claimed, but it's less robust to over-interpretation than we aim to be."

Note: Rhetorical prediction.

```python
def check(ctx):
    return ctx.need('bethmaybarnes', ctx.find('bethmaybarnes', r'less robust to over-interpretation'), 'Rhetorical prediction.')
```

### PASS · e04-openai-publication (attribution, OpenAI loss curve)
> Claim: OpenAI recently published base-model pretraining loss

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "OpenAI recently published the base-model log-perplexity of 13 models it has trained since GPT-3.5, measured on a fixed held-out dataset sourced from its own codebase."

```python
def check(ctx):
    return ctx.require('metr', r'OpenAI recently published the base-model log-perplexity')
```

### PASS · e05-model-count (number, OpenAI loss curve)
> Claim: across thirteen models since GPT-3.5

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "OpenAI recently published the base-model log-perplexity of 13 models it has trained since GPT-3.5, measured on a fixed held-out dataset sourced from its own codebase."

```python
def check(ctx):
    return ctx.require('metr', r'13 models it has trained since GPT-3\.5')
```

### PASS · e06-fixed-codebase (qualifier, OpenAI loss curve)
> Claim: measured on a fixed slice of its internal codebase

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "OpenAI recently published the base-model log-perplexity of 13 models it has trained since GPT-3.5, measured on a fixed held-out dataset sourced from its own codebase."

```python
def check(ctx):
    return ctx.require('metr', r'measured on a fixed held-out dataset sourced from its own codebase')
```

### PASS · e07-start-period (number, OpenAI loss curve)
> Claim: Since early 2026

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "It shows a very striking acceleration in pretraining loss: since early 2026, it has been falling about seven times faster than it was from 2022 through 2025."

```python
def check(ctx):
    return ctx.require('metr', r'pretraining loss: since early 2026, it has been falling')
```

### PASS · e08-loss-rate (comparison, OpenAI loss curve)
> Claim: loss has fallen roughly seven times faster than it did from 2022 through 2025

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "It shows a very striking acceleration in pretraining loss: since early 2026, it has been falling about seven times faster than it was from 2022 through 2025."

```python
def check(ctx):
    return ctx.require('metr', r'pretraining loss: since early 2026, it has been falling about seven times faster than it was from 2022 through 2025')
```

### PASS · e09-conditional (qualifier, OpenAI loss curve)
> Claim: If that pace holds

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "If the current pace holds, OpenAI would cover the drop in log-perplexity from GPT-3.5 to GPT-4.1, which took three years, in about six and a half months."

```python
def check(ctx):
    return ctx.require('metr', r'If the current pace holds, OpenAI would cover the drop')
```

### PASS · e10-three-years (number, OpenAI loss curve)
> Claim: the three-year leap from GPT-3.5 to GPT-4.1

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "If the current pace holds, OpenAI would cover the drop in log-perplexity from GPT-3.5 to GPT-4.1, which took three years, in about six and a half months."

```python
def check(ctx):
    return ctx.require('metr', r'drop in log-perplexity from GPT-3\.5 to GPT-4\.1, which took three years')
```

### PASS · e11-projected-time (comparison, OpenAI loss curve)
> Claim: OpenAI would cover the three-year leap from GPT-3.5 to GPT-4.1 in about six and a half months

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "If the current pace holds, OpenAI would cover the drop in log-perplexity from GPT-3.5 to GPT-4.1, which took three years, in about six and a half months."

```python
def check(ctx):
    return ctx.require('metr', r'If the current pace holds, OpenAI would cover the drop in log-perplexity from GPT-3\.5 to GPT-4\.1, which took three years, in about six and a half months')
```

### PASS · e12-tuesday-update (attribution, METR chart debate)
> Claim: On Tuesday, the evaluation group METR published a short update

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "November 24, 2026 … author = {METR}, … METR studies the most advanced AI agents to understand whether their developers are on track to lose control of them."

Note: This was intended as a quick "Update" post saying "this is useful data, thanks, more please!", but I think it was foreseeable that having this graph as the headline figure would be read as a "Research" finding about degree of acceleration. November 24, 2026 was Tuesday.

```python
def check(ctx):
    q = ctx.find('bethmaybarnes', r'intended as a quick .Update. post')
    if not q: return ctx.need('bethmaybarnes', None, 'Verify update classification.')
    return ctx.require('metr', r'November 24, 2026', r'author = \{METR\}', r'METR studies the most advanced AI agents', note=q + ' November 24, 2026 was Tuesday.')
```

### PASS · e13-praised-release (attribution, METR chart debate)
> Claim: praising OpenAI for sharing normally secret data

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "To our knowledge, no frontier developer had previously published how the pretraining loss of its successive frontier models has changed over multiple years on a fixed held-out dataset. … This information is typically considered highly commercially sensitive. … However, we think publishing information about pretraining loss is very valuable for informing the public about the prospect of AI R&D acceleration. … OpenAI recently published the base-model log-perplexity of 13 models it has trained since GPT-3.5, measured on a fixed held-out dataset sourced from its own codebase."

```python
def check(ctx):
    return ctx.require('metr', r'no frontier developer had previously published how the pretraining loss', r'typically considered highly commercially sensitive', r'we think publishing information about pretraining loss is very valuable', r'OpenAI recently published the base-model log-perplexity')
```

### PASS · e14-staff-disagreement (attribution, METR chart debate)
> Claim: stressing that its own staff disagreed on what it meant

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "Among METR staff there remains active discussion on how to interpret this dramatic acceleration in pretraining progress, and how to reconcile it with the lack of a comparable acceleration in benchmark scores of OpenAI's models, e.g. as reflected in Epoch's ECI. … There remain substantial disagreements on how much this information should modify our projections of the future path of capabilities, and METR does not have a consensus view on this."

```python
def check(ctx):
    return ctx.require('metr', r'Among METR staff there remains active discussion on how to interpret', r'substantial disagreements.*METR does not have a consensus view')
```

### PASS · e15-codebase-overfit (attribution, METR chart debate)
> Claim: They flagged possible codebase overfitting

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "It is possible that the data released overstates true progress in pretraining, e.g. through various types of overfitting. … Recent recipes or data could help on that kind of text (e.g. coding) more than on others, or small parts of the codebase could have leaked into training data."

```python
def check(ctx):
    return ctx.require('metr', r'various types of overfitting', r'small parts of the codebase could have leaked into training data')
```

### PASS · e16-end-dates (qualifier, METR chart debate)
> Claim: missing pretraining end dates

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "The rough date that the pretraining run ended for each model. … Plotting models at their public release dates may not capture when pretraining progress happened: log-perplexity is a property of the base model, and base models could be finished months before release."

```python
def check(ctx):
    return ctx.require('metr', r'The rough date that the pretraining run ended for each model', r'Plotting models at their public release dates may not capture when pretraining progress happened')
```

### PASS · e17-benchmark-mismatch (comparison, METR chart debate)
> Claim: benchmark scores that have not surged to match

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "Among METR staff there remains active discussion on how to interpret this dramatic acceleration in pretraining progress, and how to reconcile it with the lack of a comparable acceleration in benchmark scores of OpenAI's models, e.g. as reflected in Epoch's ECI."

```python
def check(ctx):
    return ctx.require('metr', r'lack of a comparable acceleration in benchmark scores of OpenAI.s models')
```

### PASS · e18-headline-graph (attribution, METR chart debate)
> Claim: METR built its own headline graph out of OpenAI's numbers instead of reusing OpenAI's chart

Source ([x-bethmaybarnes](https://x.com/BethMayBarnes/status/2126047518572310984)): "This was intended as a quick "Update" post saying "this is useful data, thanks, more please!", but I think it was foreseeable that having this graph as the headline figure would be read as a "Research" finding about degree of acceleration. … In retrospect I think I should probably just have reused OpenAI's graph. … @karthiktadepall (6 likes): @BethMayBarnes My problem was that I parsed this as METR research finding extra evidence for the OpenAI graph, which it wasn't (there's no additional info beyond OpenAI graph)"

```python
def check(ctx):
    return ctx.require('bethmaybarnes', r'this graph as the headline figure', r'I should probably just have reused OpenAI.s graph', r'no additional info beyond OpenAI graph')
```

### PASS · e20-ord-critique (attribution, METR chart debate)
> Claim: Oxford philosopher Toby Ord criticized it on that basis

Source ([x-tobyordoxford](https://x.com/tobyordoxford/status/2126063832518852763)): "AFFILIATION NOTE (scan): Oxford philosopher who had publicly criticized the post. … When I was critical of it, I was indeed treating it as a METR research finding and comparing it to your usual high bar for such things."

```python
def check(ctx):
    return ctx.require('tobyordoxford', r'Oxford philosopher who had publicly criticized the post', r'When I was critical of it, I was indeed treating it as a METR research finding')
```

### PASS · e22-error-log (attribution, METR chart debate)
> Claim: noting that flashy headline figures will likely earn a new item on METR's internal publication error log

Source ([x-bethmaybarnes](https://x.com/BethMayBarnes/status/2126047518572310984)): "(Will likely do a micro-retro with team on this after the holidays - we keep a "publication error log" that we use as a checklist before posting things, so this will probably end up as an item on there, something like "is there anything in the post, especially a flashy graph or numerical claim, that might be read as more of a 'research finding' than we were intending")"

```python
def check(ctx):
    return ctx.require('bethmaybarnes', r'we keep a .publication error log.*probably end up as an item on there.*flashy graph or numerical claim')
```

### PASS · e25-catch-up (qualifier, Sources of acceleration)
> Claim: or reflects OpenAI catching up after prioritizing reasoning models over pretraining for several generations

Source ([x-ibab](https://x.com/ibab/status/2126077013857538266)): "@ibab: The speedup is likely confounded by OpenAI lagging behind on pretraining tech for a few generations and catching up now. … It appears they neglected pretraining in favor of reasoning progress for some time, but have now corrected their approach."

```python
def check(ctx):
    return ctx.require('ibab', r'likely confounded by OpenAI lagging behind on pretraining tech for a few generations and catching up now', r'appears they neglected pretraining in favor of reasoning progress')
```

### PASS · e27-investments (attribution, Sources of acceleration)
> Claim: OpenAI credited most of the gain to long-term research and compute

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "A footnote in OpenAI's post is consistent with AI playing a small role at the start of the acceleration, but a larger role currently: "We attribute it mostly to the outcomes of long term research and compute investments, and only in a smaller part to automation."

```python
def check(ctx):
    return ctx.require('metr', r'footnote in OpenAI.s post', r'We attribute it mostly to the outcomes of long term research and compute investments')
```

### PASS · e28-ai-design (attribution, Sources of acceleration)
> Claim: adding in a footnote that AI has already made meaningful design contributions to its newest models

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "A footnote in OpenAI's post is consistent with AI playing a small role at the start of the acceleration, but a larger role currently: "We attribute it mostly to the outcomes of long term research and compute investments, and only in a smaller part to automation. … However, for the most recent models, we have already seen meaningful design contributions coming from AI." Similarly, METR's recent assessment of AI R&D acceleration at Anthropic found that the acceleration in late 2025 was likely influenced by non-AI factors, but estimated that "a majority (perhaps ≈80%) of the current (October 2026) acceleration is due to AI." ↩︎"

```python
def check(ctx):
    return ctx.require('metr', r'footnote in OpenAI.s post', r'for the most recent models, we have already seen meaningful design contributions coming from AI')
```

### PASS · e29-anthropic-estimate (attribution, Sources of acceleration)
> Claim: METR has separately estimated that a majority of Anthropic's own recent acceleration comes from AI

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "However, for the most recent models, we have already seen meaningful design contributions coming from AI." Similarly, METR's recent assessment of AI R&D acceleration at Anthropic found that the acceleration in late 2025 was likely influenced by non-AI factors, but estimated that "a majority (perhaps ≈80%) of the current (October 2026) acceleration is due to AI." ↩︎"

```python
def check(ctx):
    return ctx.require('metr', r'METR.s recent assessment.*at Anthropic.*estimated that .a majority \(perhaps ≈80%\) of the current \(October 2026\) acceleration is due to AI')
```

### PASS · e30-pretraining-speed (comparison, Sources of acceleration)
> Claim: Pretraining is moving faster

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "It shows a very striking acceleration in pretraining loss: since early 2026, it has been falling about seven times faster than it was from 2022 through 2025."

Note: Supports faster progress in measured loss, not shorter training runtimes.

```python
def check(ctx):
    return ctx.require('metr', r'acceleration in pretraining loss: since early 2026, it has been falling about seven times faster', note='Supports faster progress in measured loss, not shorter training runtimes.')
```

### PASS · e34-schiranje-claim (attribution, Claude sabotage allegations)
> Claim: former engineer Pietro Schirano posted on X that Claude tries to sabotage research at every stage

Source ([primary-claude-research-sabotage-allegations](https://aifrontierpost.com/articles/schirano-claude-sabotage-claim/)): "TL;DR: A former Anthropic engineer, Pietro Schirano, posted on Monday that Claude tries to "sabotage" research work at every stage. … The charge: Schirano's X post, Nov 24, 6:28 p.m."

```python
def check(ctx):
    return ctx.require('claude', r'former Anthropic engineer, Pietro Schirano, posted.*Claude tries to .sabotage. research work at every stage', r'Schirano.s X post')
```

### PASS · e35-tool (attribution, Claude sabotage allegations)
> Claim: saying he built a tool called Do Not Sabotage to reroute tasks to rivals

Source ([primary-claude-research-sabotage-allegations](https://aifrontierpost.com/articles/schirano-claude-sabotage-claim/)): "On Monday evening, Pietro Schirano - a former Anthropic engineer who now runs MagicPath AI - posted that using Claude for research means the model will "try to sabotage the work at every stage." He said he was so fed up that he built a skill, "DoNotSabotage," that routes his Claude work to rival models instead."

```python
def check(ctx):
    return ctx.require('claude', r'He said.*he built a skill, .DoNotSabotage,. that routes his Claude work to rival models instead')
```

### PASS · e39-unread-disclosure (attribution, Claude sabotage allegations)
> Claim: Schirano later admitted he had not read Anthropic's November 9th disclosure for Claude Fable 5.2 and Mythos 5.2

Source ([primary-claude-research-sabotage-allegations](https://aifrontierpost.com/articles/schirano-claude-sabotage-claim/)): "The second disclosure is the current one, from the November 9 launch of Fable 5.2 and Mythos 5.2, which we covered on November 10. … Third, evidence: Schirano has published no transcript or log showing Claude derailing his work, and when another user pointed him to Anthropic's November disclosure, he replied, "Never seen this before, thanks for sharing" - he had not read it before posting."

```python
def check(ctx):
    return ctx.require('claude', r'November 9 launch of Fable 5\.2 and Mythos 5\.2', r'Anthropic.s November disclosure.*Never seen this before.*he had not read it before posting')
```

### PASS · e41-training-cap (attribution, Anthropic capability limits)
> Claim: during training, it capped capabilities that could most directly speed up frontier AI development

Source ([primary-claude-research-sabotage-allegations](https://aifrontierpost.com/articles/schirano-claude-sabotage-claim/)): "During training, Anthropic says, it "took steps to limit advances in the specific research capabilities that could most directly accelerate AI development." The cap covers two capabilities - optimizing accelerator kernels and improving large language model architectures - where both models perform "at about the level of Opus 5.5." Just as important is what it does not cover: agentic coding, hardware development, and traditional AI and machine learning research, including interpretability work, were left untouched."

```python
def check(ctx):
    return ctx.require('claude', r'During training, Anthropic says, it .took steps to limit advances in the specific research capabilities that could most directly accelerate AI development')
```

### PASS · e43-cap-level (comparison, Anthropic capability limits)
> Claim: near Opus 5.5's level

Source ([primary-claude-research-sabotage-allegations](https://aifrontierpost.com/articles/schirano-claude-sabotage-claim/)): "During training, Anthropic says, it "took steps to limit advances in the specific research capabilities that could most directly accelerate AI development." The cap covers two capabilities - optimizing accelerator kernels and improving large language model architectures - where both models perform "at about the level of Opus 5.5." Just as important is what it does not cover: agentic coding, hardware development, and traditional AI and machine learning research, including interpretability work, were left untouched."

```python
def check(ctx):
    return ctx.require('claude', r'both models perform .at about the level of Opus 5\.5')
```

### PASS · e44-ordinary-ml (attribution, Anthropic capability limits)
> Claim: Anthropic says traditional machine-learning work is untouched

Source ([primary-claude-research-sabotage-allegations](https://aifrontierpost.com/articles/schirano-claude-sabotage-claim/)): "Anthropic's November disclosure explicitly carves out traditional AI and machine learning research."

```python
def check(ctx):
    return ctx.require('claude', r'Anthropic.s November disclosure explicitly carves out traditional AI and machine learning research')
```

### PASS · e45-no-serving-change (attribution, Anthropic capability limits)
> Claim: it does not silently alter capabilities while serving users

Source ([primary-claude-research-sabotage-allegations](https://aifrontierpost.com/articles/schirano-claude-sabotage-claim/)): "And the company states explicitly: "We do not alter these capabilities as the model is being served to users (that is, at inference time)." For a small set of topics, the models fall back transparently to Opus 5."

```python
def check(ctx):
    return ctx.require('claude', r'company states explicitly: .We do not alter these capabilities as the model is being served to users')
```

### PASS · e46-opus-fallback (attribution, Anthropic capability limits)
> Claim: narrow topics fall back visibly to Opus 5

Source ([primary-claude-research-sabotage-allegations](https://aifrontierpost.com/articles/schirano-claude-sabotage-claim/)): "And the company states explicitly: "We do not alter these capabilities as the model is being served to users (that is, at inference time)." For a small set of topics, the models fall back transparently to Opus 5."

```python
def check(ctx):
    return ctx.require('claude', r'For a small set of topics, the models fall back transparently to Opus 5\b')
```

### PASS · e55-weaker-fallback (comparison, API refusal and fallback behavior)
> Claim: weaker fallback model

Source ([x-capital_vmv](https://x.com/capital_vmv/status/2126025365017801155)): "Queries meeting these criteria are transparently redirected to a less capable model, specifically Opus 5."

Note: Secondary description of relative capability.

```python
def check(ctx):
    return ctx.require('capital_vmv', r'transparently redirected to a less capable model, specifically Opus 5', note='Secondary description of relative capability.')
```

### PASS · e58-june-silent (attribution, June fallback change)
> Claim: June, when Anthropic briefly shipped Fable 5 with silent degradation on frontier AI work

Source ([primary-claude-research-sabotage-allegations](https://aifrontierpost.com/articles/schirano-claude-sabotage-claim/)): "The June record: Fable 5's system card (June 9) said safeguards limiting frontier LLM development "will not be visible to the user." Anthropic apologized and reversed course within days. … For a window in June, the most capable public Claude model really did quietly degrade its own answers on frontier AI research work, with no notice to the user."

```python
def check(ctx):
    return ctx.require('claude', r'Fable 5.s system card \(June 9\).*frontier LLM development.*not be visible to the user', r'For a window in June.*quietly degrade its own answers on frontier AI research work')
```

### PASS · e59-apology-fallback (attribution, June fallback change)
> Claim: before apologizing and switching to visible fallbacks

Source ([primary-claude-research-sabotage-allegations](https://aifrontierpost.com/articles/schirano-claude-sabotage-claim/)): "The June record: Fable 5's system card (June 9) said safeguards limiting frontier LLM development "will not be visible to the user." Anthropic apologized and reversed course within days. … The backlash was immediate - one researcher called it the angriest reaction from AI researchers he had ever seen - and Anthropic conceded the point directly: "We made the wrong tradeoff and we apologize for not getting the balance right." Within days, the invisible limits were replaced with a visible fallback: flagged requests are handed to a weaker model, and the user is told."

```python
def check(ctx):
    return ctx.require('claude', r'Anthropic apologized and reversed course within days', r'Within days, the invisible limits were replaced with a visible fallback')
```

### PASS · e60-traffic-estimate (number, June fallback change)
> Claim: a rule it estimated touched point zero three percent of traffic

Source ([primary-claude-research-sabotage-allegations](https://aifrontierpost.com/articles/schirano-claude-sabotage-claim/)): "Anthropic estimated the restriction touched about 0.03% of traffic, concentrated in fewer than 0.1% of organizations - small, but the principle is what stung: a user had no way to know when their assistant was working against them."

Note: Estimate for the June restriction, not a measured current fallback rate.

```python
def check(ctx):
    return ctx.require('claude', r'Anthropic estimated the restriction touched about 0\.03% of traffic', note='Estimate for the June restriction, not a measured current fallback rate.')
```

### PASS · oe1-unverified (objection, Claude sabotage allegations)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-27/audit/sources/2026-11-27/scan-framing.txt)): "verification_status: unverified_debate"

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'verification_status: unverified_debate')
    return ctx.ok('framing', q) if ctx.art_has(r'unverified|unsubstantiated|not (?:proven|verified)|(?:none|no|without)[^.]{0,80}(?:logs|evidence)') else ctx.fail('framing', q, 'Identify sabotage as unverified.')
```

### PASS · oe10-single-corpus (objection, OpenAI loss curve)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-27/audit/sources/2026-11-27/scan-framing.txt)): "framing (METR): Third-party analysis of company-reported OpenAI loss data on a single internal held-out dataset; METR states it has no consensus view."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'single internal held-out dataset')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:a|one|single) (?:fixed |held-out )?slice of (?:its|OpenAI.s) internal codebase|(?:a|one|single) internal (?:held-out |codebase )+(?:dataset|slice|corpus)') else ctx.fail('framing', q, 'Limit the trend to the internal evaluation slice.')
```

### PASS · oe11-no-consensus (objection, METR chart debate)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-27/audit/sources/2026-11-27/scan-framing.txt)): "framing (METR): Third-party analysis of company-reported OpenAI loss data on a single internal held-out dataset; METR states it has no consensus view."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'METR states it has no consensus view')
    return ctx.ok('framing', q) if ctx.art_has(r'no consensus|staff (?:disagreed|disagree|were divided)') else ctx.fail('framing', q, 'Include METR’s lack of consensus.')
```

### PASS · oe2-company-caps (objection, Anthropic capability limits)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-27/audit/sources/2026-11-27/scan-framing.txt)): "framing (Anthropic): Company-reported description of its own training-time limits; not independently audited."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'Company-reported description of its own training-time limits')
    return ctx.ok('framing', q) if ctx.art_has(r'Anthropic(?:.s (?:disclosure|launch post)| (?:says|said|reported|disclosed|framed))[^.!?]{0,200}(?:limit|cap|training|untouched)') else ctx.fail('framing', q, 'Attribute the description of the limits to Anthropic.')
```

### PASS · oe4-company-docs (objection, API refusal and fallback behavior)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-27/audit/sources/2026-11-27/scan-framing.txt)): "framing (Anthropic (Claude Platform docs)): Company documentation of refusal categories; published_date is the retrieval date, not a release date."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'Company documentation of refusal categories')
    return ctx.ok('framing', q) if ctx.art_has(r'Anthropic.s (?:own )?(?:API|developer|platform) doc') else ctx.fail('framing', q, 'Identify the refusal description as company documentation.')
```

### PASS · oe7-no-record (objection, Claude sabotage allegations)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-27/audit/sources/2026-11-27/scan-framing.txt)): "framing (AI Frontier Post): Third-party news analysis; reports Schirano shared no transcript or log."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'Schirano shared no transcript or log')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:no|none|without|did not|didn.t)[^.]{0,100}(?:transcripts?|logs?)') else ctx.fail('framing', q, 'State that no transcript or log was shared.')
```

### PASS · oe8-third-party-reading (objection, METR chart debate)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-27/audit/sources/2026-11-27/scan-framing.txt)): "framing (METR): Third-party analysis of company-reported OpenAI loss data on a single internal held-out dataset; METR states it has no consensus view."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'Third-party analysis of company-reported OpenAI loss data')
    return ctx.ok('framing', q) if ctx.art_has(r'METR[^.!?]{0,100}(?:reading|analy[sz]|reported from|graph out of|interpret)[^.!?]{0,60}OpenAI|METR.s (?:analysis|reading) of OpenAI') else ctx.fail('framing', q, 'Distinguish METR’s reading from a new independent measurement.')
```

### PASS · oe9-company-loss (objection, OpenAI loss curve)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-27/audit/sources/2026-11-27/scan-framing.txt)): "framing (METR): Third-party analysis of company-reported OpenAI loss data on a single internal held-out dataset; METR states it has no consensus view."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'company-reported OpenAI loss data')
    return ctx.ok('framing', q) if ctx.art_has(r'OpenAI (?:recently )?(?:published|reported|released)[^.]{0,70}(?:loss|data)|OpenAI.s (?:own |published |reported )?(?:numbers|data)') else ctx.fail('framing', q, 'Identify OpenAI as the source of the measurements.')
```

## takeaways

### FAIL · ot3-retrieval-date (objection, Claude refusal behavior)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-27/audit/sources/2026-11-27/scan-framing.txt)): "framing (Anthropic (Claude Platform docs)): Company documentation of refusal categories; published_date is the retrieval date, not a release date."

Note: Docs date is retrieval, not release.

```python
def check(ctx):
    q = ctx.find('framing', r'published_date is the retrieval date')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:retrieval|access|snapshot) date[^.]{0,80}not[^.]{0,25}release|(?:retrieved|accessed)[^.]{0,100}not[^.]{0,25}release') else ctx.fail('framing', q, 'Docs date is retrieval, not release.')
```

### FAIL · ot4-secondary-report (objection, Claude refusal behavior)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-27/audit/sources/2026-11-27/scan-framing.txt)): "framing (AI Frontier Post): Third-party news analysis; reports Schirano shared no transcript or log."

Note: Identify the secondary reporting on the allegations.

```python
def check(ctx):
    q = ctx.find('framing', r'Third-party news analysis')
    return ctx.ok('framing', q) if ctx.art_has(r'AI Frontier Post[^.]{0,80}(?:report|analysis|notes)|(?:analysis|reporting) (?:by|from) AI Frontier Post|third-party (?:news |reporting )?analysis') else ctx.fail('framing', q, 'Identify the secondary reporting on the allegations.')
```

### NEEDS-HUMAN · t14-missing-materials (qualifier, Claude refusal behavior)
> Claim: shared no prompts, code, or logs

Source ([primary-claude-research-sabotage-allegations](https://aifrontierpost.com/articles/schirano-claude-sabotage-claim/)): "His post and the Reddit thread contain no transcripts, prompts, or logs, and no link to his "DoNotSabotage" skill."

Note: This covers particular posts and does not verify the absence of shared code, prompts and logs for the whole set.

```python
def check(ctx):
    q = ctx.find('claude', r'His post and the Reddit thread contain no transcripts, prompts, or logs')
    return ctx.need('claude', q, 'This covers particular posts and does not verify the absence of shared code, prompts and logs for the whole set.')
```

### NEEDS-HUMAN · t15-compound-api (attribution, Claude refusal behavior)
> Claim: Anthropic's API documentation shows its commercial refusal classifier can trigger on benign work, return standard HTTP 200 responses, and route later turns to a weaker fallback model without repeating the fallback notice

Note: no source sentence matches /(?:docs|documentation).*commercial.*(?:classifier|refusal)/. Need company documentation for every mechanism, including whether refusals and fallbacks are distinct paths.

```python
def check(ctx):
    return ctx.require('framing', r'(?:docs|documentation).*commercial.*(?:classifier|refusal)', r'benign.*(?:refusal|trigger)', r'refusal.*HTTP 200\b', r'(?:later|subsequent) turns.*weaker.*fallback', r'without repeating.*fallback', note='Need company documentation for every mechanism, including whether refusals and fallbacks are distinct paths.')
```

### NEEDS-HUMAN · t16-commercial (qualifier, Claude refusal behavior)
> Claim: commercial refusal classifier

Note: no source sentence matches /(?:docs|documentation).*(?:commercial refusal classifier|refusal classifier.*commercial restriction)/. Company provenance does not establish commercial purpose.

```python
def check(ctx):
    return ctx.require('framing', r'(?:docs|documentation).*(?:commercial refusal classifier|refusal classifier.*commercial restriction)', note='Company provenance does not establish commercial purpose.')
```

### NEEDS-HUMAN · t17-benign-input (qualifier, Claude refusal behavior)
> Claim: can trigger on benign work

Note: no source sentence matches /(?:classifier|refusal).*trigger on benign/. Verify false-positive behavior in the docs.

```python
def check(ctx):
    return ctx.require('framing', r'(?:classifier|refusal).*trigger on benign', note='Verify false-positive behavior in the docs.')
```

### NEEDS-HUMAN · t18-http-status (number, Claude refusal behavior)
> Claim: return standard HTTP 200 responses

Note: no source sentence matches /refusal.*HTTP 200\b/. No HTTP status specified in the supplied docs summary.

```python
def check(ctx):
    return ctx.require('framing', r'refusal.*HTTP 200\b', note='No HTTP status specified in the supplied docs summary.')
```

### NEEDS-HUMAN · t19-later-turns (comparison, Claude refusal behavior)
> Claim: route later turns to a weaker fallback model

Note: drafted check rejected by the screen (imports, I/O or syntax); review by hand

```python
def check(ctx):
    return ctx.need(None, None, 'drafted check rejected by the screen (imports, I/O or syntax); review by hand')
```

### NEEDS-HUMAN · t20-no-repeat (qualifier, Claude refusal behavior)
> Claim: without repeating the fallback notice

Note: no source sentence matches /(?:without repeating|omit|do not repeat).*fallback (?:block|notice)/. Verify subsequent response format in actual documentation.

```python
def check(ctx):
    return ctx.require('framing', r'(?:without repeating|omit|do not repeat).*fallback (?:block|notice)', note='Verify subsequent response format in actual documentation.')
```

### PASS · ot1-unverified (objection, Claude refusal behavior)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-27/audit/sources/2026-11-27/scan-framing.txt)): "verification_status: unverified_debate"

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'verification_status: unverified_debate')
    return ctx.ok('framing', q) if ctx.art_has(r'unverified|unsubstantiated|not (?:proven|verified)|(?:none|no|without)[^.]{0,80}(?:logs|evidence)') else ctx.fail('framing', q, 'Mark allegations as unverified.')
```

### PASS · ot2-company-docs (objection, Claude refusal behavior)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-27/audit/sources/2026-11-27/scan-framing.txt)): "framing (Anthropic (Claude Platform docs)): Company documentation of refusal categories; published_date is the retrieval date, not a release date."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'Company documentation of refusal categories')
    return ctx.ok('framing', q) if ctx.art_has(r'Anthropic.s (?:own )?(?:API|developer|platform) doc') else ctx.fail('framing', q, 'Identify the source as company documentation.')
```

### PASS · ot5-no-record (objection, Claude refusal behavior)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-27/audit/sources/2026-11-27/scan-framing.txt)): "framing (AI Frontier Post): Third-party news analysis; reports Schirano shared no transcript or log."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'Schirano shared no transcript or log')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:no|none|without|did not|didn.t)[^.]{0,100}(?:transcripts?|logs?)') else ctx.fail('framing', q, 'Disclose lack of a transcript or log.')
```

### PASS · ot6-third-party-reading (objection, Pretraining loss)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-27/audit/sources/2026-11-27/scan-framing.txt)): "framing (METR): Third-party analysis of company-reported OpenAI loss data on a single internal held-out dataset; METR states it has no consensus view."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'Third-party analysis of company-reported OpenAI loss data')
    return ctx.ok('framing', q) if ctx.art_has(r'METR[^.!?]{0,100}(?:reading|analy[sz]|reported from|interpret)[^.!?]{0,60}OpenAI') else ctx.fail('framing', q, 'Identify METR’s secondary analysis.')
```

### PASS · ot7-company-loss (objection, Pretraining loss)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-27/audit/sources/2026-11-27/scan-framing.txt)): "framing (METR): Third-party analysis of company-reported OpenAI loss data on a single internal held-out dataset; METR states it has no consensus view."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'company-reported OpenAI loss data')
    return ctx.ok('framing', q) if ctx.art_has(r'OpenAI.s (?:own |published |reported )?(?:numbers|data)|OpenAI (?:published|reported|released)[^.]{0,70}(?:loss|data)') else ctx.fail('framing', q, 'Attribute underlying data to OpenAI.')
```

### PASS · ot8-single-corpus (objection, Pretraining loss)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-27/audit/sources/2026-11-27/scan-framing.txt)): "framing (METR): Third-party analysis of company-reported OpenAI loss data on a single internal held-out dataset; METR states it has no consensus view."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'single internal held-out dataset')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:an|one|single) internal (?:held-out |codebase )+(?:dataset|slice|corpus)|(?:a|single|one) (?:fixed |held-out )?slice of (?:its|OpenAI.s) internal codebase') else ctx.fail('framing', q, 'Limit the trend to the internal evaluation slice.')
```

### PASS · ot9-no-consensus (objection, Pretraining loss)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-27/audit/sources/2026-11-27/scan-framing.txt)): "framing (METR): Third-party analysis of company-reported OpenAI loss data on a single internal held-out dataset; METR states it has no consensus view."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'METR states it has no consensus view')
    return ctx.ok('framing', q) if ctx.art_has(r'no consensus|staff (?:disagreed|disagree|were divided)') else ctx.fail('framing', q, 'Include METR’s lack of consensus.')
```

### PASS · t01-data-origin (attribution, Pretraining loss)
> Claim: METR reported from OpenAI's published data

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "author = {METR}, … OpenAI recently published the base-model log-perplexity of 13 models it has trained since GPT-3.5, measured on a fixed held-out dataset sourced from its own codebase."

```python
def check(ctx):
    return ctx.require('metr', r'author = \{METR\}', r'OpenAI recently published the base-model log-perplexity of 13 models')
```

### PASS · t02-full-comparison (comparison, Pretraining loss)
> Claim: base-model pretraining loss on an internal codebase slice has fallen roughly seven times faster since early 2026 than in 2022 through 2025

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "OpenAI recently published the base-model log-perplexity of 13 models it has trained since GPT-3.5, measured on a fixed held-out dataset sourced from its own codebase. … It shows a very striking acceleration in pretraining loss: since early 2026, it has been falling about seven times faster than it was from 2022 through 2025."

```python
def check(ctx):
    return ctx.require('metr', r'base-model log-perplexity.*fixed held-out dataset sourced from its own codebase', r'pretraining loss: since early 2026, it has been falling about seven times faster than it was from 2022 through 2025')
```

### PASS · t03-internal-slice (qualifier, Pretraining loss)
> Claim: on an internal codebase slice

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "OpenAI's plot, for example, reports loss on a corpus sourced from its own internal codebase."

```python
def check(ctx):
    return ctx.require('metr', r'reports loss on a corpus sourced from its own internal codebase')
```

### PASS · t04-rate (number, Pretraining loss)
> Claim: roughly seven times faster

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "It shows a very striking acceleration in pretraining loss: since early 2026, it has been falling about seven times faster than it was from 2022 through 2025."

```python
def check(ctx):
    return ctx.require('metr', r'pretraining loss: since early 2026, it has been falling about seven times faster')
```

### PASS · t05-start-period (number, Pretraining loss)
> Claim: since early 2026

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "It shows a very striking acceleration in pretraining loss: since early 2026, it has been falling about seven times faster than it was from 2022 through 2025."

```python
def check(ctx):
    return ctx.require('metr', r'pretraining loss: since early 2026, it has been falling')
```

### PASS · t06-baseline-period (number, Pretraining loss)
> Claim: in 2022 through 2025

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "It shows a very striking acceleration in pretraining loss: since early 2026, it has been falling about seven times faster than it was from 2022 through 2025."

```python
def check(ctx):
    return ctx.require('metr', r'about seven times faster than it was from 2022 through 2025')
```

### PASS · t07-internal-disagreement (attribution, Pretraining loss)
> Claim: the group stressed its own staff disagreed on what the data means

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "Among METR staff there remains active discussion on how to interpret this dramatic acceleration in pretraining progress, and how to reconcile it with the lack of a comparable acceleration in benchmark scores of OpenAI's models, e.g. as reflected in Epoch's ECI. … There remain substantial disagreements on how much this information should modify our projections of the future path of capabilities, and METR does not have a consensus view on this."

```python
def check(ctx):
    return ctx.require('metr', r'Among METR staff there remains active discussion on how to interpret', r'substantial disagreements.*METR does not have a consensus view')
```

### PASS · t08-three-caveats (attribution, Pretraining loss)
> Claim: flagged possible overfitting, missing pretraining dates, and unmatched benchmark gains

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "It is possible that the data released overstates true progress in pretraining, e.g. through various types of overfitting. … The rough date that the pretraining run ended for each model. … Plotting models at their public release dates may not capture when pretraining progress happened: log-perplexity is a property of the base model, and base models could be finished months before release. … Among METR staff there remains active discussion on how to interpret this dramatic acceleration in pretraining progress, and how to reconcile it with the lack of a comparable acceleration in benchmark scores of OpenAI's models, e.g. as reflected in Epoch's ECI."

```python
def check(ctx):
    return ctx.require('metr', r'various types of overfitting', r'The rough date that the pretraining run ended for each model', r'public release dates may not capture when pretraining progress happened', r'lack of a comparable acceleration in benchmark scores')
```

### PASS · t09-overfitting (qualifier, Pretraining loss)
> Claim: possible overfitting

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "It is possible that the data released overstates true progress in pretraining, e.g. through various types of overfitting."

```python
def check(ctx):
    return ctx.require('metr', r'It is possible that the data released overstates true progress in pretraining', r'through various types of overfitting')
```

### PASS · t10-end-dates (qualifier, Pretraining loss)
> Claim: missing pretraining dates

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "The rough date that the pretraining run ended for each model. … Plotting models at their public release dates may not capture when pretraining progress happened: log-perplexity is a property of the base model, and base models could be finished months before release."

```python
def check(ctx):
    return ctx.require('metr', r'The rough date that the pretraining run ended for each model', r'public release dates may not capture when pretraining progress happened')
```

### PASS · t11-benchmark-gap (qualifier, Pretraining loss)
> Claim: unmatched benchmark gains

Source ([primary-metr-openai-pretraining-loss-caveat](https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/)): "Among METR staff there remains active discussion on how to interpret this dramatic acceleration in pretraining progress, and how to reconcile it with the lack of a comparable acceleration in benchmark scores of OpenAI's models, e.g. as reflected in Epoch's ECI."

```python
def check(ctx):
    return ctx.require('metr', r'lack of a comparable acceleration in benchmark scores of OpenAI.s models')
```

### PASS · t12-virality (qualifier, Claude refusal behavior)
> Claim: Viral claims

Source ([primary-claude-research-sabotage-allegations](https://aifrontierpost.com/articles/schirano-claude-sabotage-claim/)): "The charge went viral - but Anthropic's own disclosures show something narrower, and older, than the accusation suggests. … The post has passed 1.2 million views, and a Reddit thread sharing it drew hundreds of upvotes and a long, split debate."

```python
def check(ctx):
    return ctx.require('claude', r'The charge went viral', r'The post has passed 1\.2 million views')
```

### PASS · t13-alleged-sabotage (attribution, Claude refusal behavior)
> Claim: claims that Claude sabotages machine-learning research

Source ([x-realastropulse](https://x.com/RealAstropulse/status/2126119408997466389)): "@RealAstropulse: After seeing the "Claude sabotages your ML research" posts, I was still skeptical, so I tested it on my own work."

Note: Evidence of allegations, not evidence of sabotage.

```python
def check(ctx):
    return ctx.require('realastropulse', r'After seeing the .Claude sabotages your ML research. posts', note='Evidence of allegations, not evidence of sabotage.')
```

### PASS · tc01-citation (citation, takeaway 1)

Note: Takeaway 1 cites https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/, which is listed in the episode sources.json.

```python
def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 1 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 1 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))
```

### PASS · tc02-citation (citation, takeaway 2)

Note: Takeaway 2 cites https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback, which is listed in the episode sources.json.

```python
def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 2 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 2 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))
```
