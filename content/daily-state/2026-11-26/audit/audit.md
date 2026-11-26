# Executable audit, Daily State of AI 2026-11-26

Each claim is tested by a deterministic Python check against snapshotted source texts and X posts. PASS = the source sentence quoted supports the claim; FAIL = the source contradicts it or a required caveat is missing; NEEDS-HUMAN = opinion or not decidable by string/number match.

| artifact | PASS | FAIL | NEEDS-HUMAN | ERROR |
|---|---|---|---|---|
| episode | 39 | 15 | 31 | 0 |
| takeaways | 17 | 7 | 4 | 0 |

## Sources
- `primary-google-cogentic-six-math-papers`: [Breaking the Square-Root Barrier for the Log-Rank Conjecture](https://raw.githubusercontent.com/google-research/google-research/master/cogentic_research_papers/logrank_conjecture/README.md) (sha256 0125de488c93…)
- `x-andrewcurran_`: [X post by @AndrewCurran_](https://x.com/AndrewCurran_/status/2125589468786909510) (sha256 5ef4c7130444…)
- `x-kimmonismus`: [X post by @kimmonismus (Chubby♨️)](https://x.com/kimmonismus/status/2125602411540566221) (sha256 2c844958f5cf…)
- `primary-anthropic-messages-api-rust-migration`: [Migrating our Messages API to Rust](https://www.anthropic.com/research/migrating-api-to-rust) (sha256 5532d9be93fa…)
- `x-anthropicai`: [X post by @AnthropicAI (Anthropic)](https://x.com/AnthropicAI/status/2125627317263466739) (sha256 b79f15b2348e…)
- `scan-framing`: [Morning X-first scan: verification framing per story](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt) (sha256 1ece14b165c6…)

## episode

### FAIL · e18-six-no-human (attribution, Google papers)
> Claim: claiming no human involvement after the first prompt

Source ([primary-google-cogentic-six-math-papers](https://raw.githubusercontent.com/google-research/google-research/master/cogentic_research_papers/logrank_conjecture/README.md)): "There was no human interaction other than the initial prompt for Cogentic to"

Note: The assertion in this README covers its proof and formalization, not all six papers.

```python
def check(ctx):
    q = ctx.find('google', r'There was no human interaction other than the initial prompt')
    return ctx.fail('google', q, 'The assertion in this README covers its proof and formalization, not all six papers.') if q and ctx.absent('framing', r'(?:all six|six papers).{0,100}no human interaction') else ctx.require('framing', r'(?:all six|six papers).{0,100}no human interaction')
```

### FAIL · e22-rsa-condition (qualifier, Factoring rumor)
> Claim: OpenAI or Anthropic may have found a polynomial-time factoring algorithm that would break RSA

Source ([x-kimmonismus](https://x.com/kimmonismus/status/2125602411540566221)): "If an algorithm like this actually works on real key sizes, you wouldn't even need a quantum computer to break it."

Note: Polynomial time alone does not establish a practical break.

```python
def check(ctx):
    q = ctx.find('kimmonismus', r'If an algorithm like this actually works on real key sizes')
    if q and not ctx.art_has(r'(?:works? on real key sizes|practical (?:at|on) (?:RSA|real) key sizes)'): return ctx.fail('kimmonismus', q, 'Polynomial time alone does not establish a practical break.')
    return ctx.require('kimmonismus', r'heard OpenAI or Anthropic may have found a way to factor large numbers in polynomial time', r'If an algorithm like this actually works on real key sizes')
```

### FAIL · e33-all-six-lean (attribution, Proof verification)
> Claim: Google says Lean 4 formalizations for all six papers are coming in a companion submission

Source ([primary-google-cogentic-six-math-papers](https://raw.githubusercontent.com/google-research/google-research/master/cogentic_research_papers/logrank_conjecture/README.md)): "Lean 4 (`v4.33.0`) formalization of the entire proof has also been completed and will be released in a companion submission"

Note: The release statement is singular and specific to the log-rank proof.

```python
def check(ctx):
    return ctx.support_or_contradict('google', r'Lean 4 formalizations of all six papers.{0,100}companion submission', r'Lean 4.*?formalization of the\s+entire proof has also been completed and will be released in a companion\s+submission'.replace('.*?', '[\\s\\S]*?'), 'The release statement is singular and specific to the log-rank proof.')
```

### FAIL · e46-first-version (attribution, Rust migration)
> Claim: Claude wrote the core Rust request path in about a week

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "Claude wrote a first version of the API's core request path in about a week."

Note: Only a first version is attributed to the week of work.

```python
def check(ctx):
    return ctx.support_or_contradict('anthropic', r'Claude wrote the (?:finished |production-ready )?(?:Rust )?(?:API.s )?core request path in about a week', r'Claude wrote a first version of the API.s core request path in about a week', 'Only a first version is attributed to the week of work.')
```

### FAIL · e54-april-tests (number, Production verification)
> Claim: Rust passed ninety-eight percent of tests in April

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "Our Rust API passed about 98% of its tests in April, yet only about a quarter of inputs matched on production traffic (Figure 6)."

Note: Source qualifies the percentage as approximate.

```python
def check(ctx):
    return ctx.support_or_contradict('anthropic', r'Rust API passed 98% of its tests in April', r'Rust API passed about 98% of its tests in April', 'Source qualifies the percentage as approximate.')
```

### FAIL · e60-gamed-which-verifier (attribution, Shadow oracle)
> Claim: an agent still gamed it

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "The prompts then matched, and the fix passed the local verifier."

Note: The shortcut passed locally; no demonstrated bypass of the production oracle.

```python
def check(ctx):
    return ctx.support_or_contradict('anthropic', r'(?:shortcut|fix) passed the (?:outer|production) verifier', r'the fix passed the local verifier', 'The shortcut passed locally; no demonstrated bypass of the production oracle.')
```

### FAIL · e66-only-by-review (attribution, Engineering oversight)
> Claim: Anthropic succeeded only by keeping engineers at the pull-request gate and turning recurring corrections into standing rules, tests, and lints

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "That's why human review was an important gate."

Note: Important is not a finding of exclusive causal necessity.

```python
def check(ctx):
    q = ctx.find('anthropic', r'human review was an important gate')
    return ctx.fail('anthropic', q, 'Important is not a finding of exclusive causal necessity.') if q and ctx.absent('anthropic', r'(?:only succeeded|succeeded only)') else ctx.require('anthropic', r'(?:only succeeded|succeeded only).{0,100}review', r'recurring problems and proposed rules', r'new tests.{0,100}lints')
```

### FAIL · e71-week-versus-months (comparison, Two headlines)
> Claim: generating the code takes a week, while earning trust in the real world still takes months

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "Claude wrote a first version of the API's core request path in about a week."

Note: A first version of one core path is not all migration code or a general generation time.

```python
def check(ctx):
    q = ctx.find('anthropic', r'Claude wrote a first version of the API.s core request path in about a week')
    return ctx.fail('anthropic', q, 'A first version of one core path is not all migration code or a general generation time.') if q else ctx.need('anthropic', None, 'Need comparable generation and verification intervals.')
```

### FAIL · oe10-not-conjecture-proof (objection, Google papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted claim of a tiny improvement over the square-root bound (epsilon of 5 millionths); not a proof of the conjecture; not independently verified."

Note: The improvement does not prove the conjecture.

```python
def check(ctx):
    q = ctx.find('framing', r'not a proof of the conjecture')
    return ctx.ok('framing', q) if ctx.art_has(r'not (?:a proof of|prove|solve) the (?:log[- ]rank )?conjecture|log[- ]rank conjecture remains open') else ctx.fail('framing', q, 'The improvement does not prove the conjecture.')
```

### FAIL · oe13-independent-measurement (objection, Rust migration)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Anthropic): Company-reported engineering results; performance numbers are Anthropic's own and not independently measured."

Note: Disclose lack of independent performance measurement.

```python
def check(ctx):
    q = ctx.find('framing', r'not independently measured')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:numbers|gains|metrics|performance|measurements).{0,90}(?:not independently (?:measured|verified)|no independent (?:measurement|benchmark))|no independent (?:performance )?(?:benchmark|measurement)') else ctx.fail('framing', q, 'Disclose lack of independent performance measurement.')
```

### FAIL · oe3-no-lab-result (objection, Factoring rumor)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "No lab has published or confirmed such a result."

Note: Say that no lab has published or confirmed the rumored result.

```python
def check(ctx):
    q = ctx.find('framing', r'No lab has published or confirmed such a result')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:no|neither) (?:frontier )?labs?.{0,50}(?:published|confirmed)|no lab confirmation|not confirmed by (?:either|any) lab') else ctx.fail('framing', q, 'Say that no lab has published or confirmed the rumored result.')
```

### FAIL · oe4-company-preprints (objection, Google papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released."

Note: Identify the papers as company-posted preprints.

```python
def check(ctx):
    q = ctx.find('framing', r'Company-posted preprints in a public repository')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:Google(?: Research)?|company)[- ](?:posted|published|released|(?:silently )?committed).{0,100}preprints?') else ctx.fail('framing', q, 'Identify the papers as company-posted preprints.')
```

### FAIL · oe5-peer-review (objection, Google papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released."

Note: State lack of peer review.

```python
def check(ctx):
    q = ctx.find('framing', r'no peer review')
    return ctx.ok('framing', q) if ctx.art_has(r'no peer review|not (?:yet )?peer[- ]reviewed|without peer review|awaiting peer review') else ctx.fail('framing', q, 'State lack of peer review.')
```

### FAIL · oe7-factoring-bound (objection, Google papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted claim; the running-time bound is subexponential, not polynomial, and no independent verification is reported."

Note: Distinguish the public subexponential bound from polynomial time.

```python
def check(ctx):
    q = ctx.find('framing', r'subexponential, not polynomial')
    return ctx.ok('framing', q) if ctx.art_has(r'sub[- ]?exponential.{0,50}(?:not|rather than) polynomial|not polynomial.{0,50}sub[- ]?exponential') else ctx.fail('framing', q, 'Distinguish the public subexponential bound from polynomial time.')
```

### FAIL · oe9-logrank-size (objection, Google papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted claim of a tiny improvement over the square-root bound (epsilon of 5 millionths); not a proof of the conjecture; not independently verified."

Note: Describe the small improvement to the square-root bound.

```python
def check(ctx):
    q = ctx.find('framing', r'tiny improvement over the square-root bound')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:tiny|slight|small) improvement.{0,50}square[- ]root|(?:epsilon|exponent).{0,35}(?:five millionths|5 millionths|0\.000005)') else ctx.fail('framing', q, 'Describe the small improvement to the square-root bound.')
```

### NEEDS-HUMAN · e01-broadcast-date (number, Broadcast)
> Claim: Daily State of AI for Thursday, November 26, 2026

Note: no source sentence matches /Daily State of AI.{0,30}Thursday,? November 26,? 2026/. A story publication date is not a broadcast date.

```python
def check(ctx):
    return ctx.require('framing', r'Daily State of AI.{0,30}Thursday,? November 26,? 2026', note='A story publication date is not a broadcast date.')
```

### NEEDS-HUMAN · e02-whiplash (opinion, Two headlines)
> Claim: you probably felt whiplash between two stories

Note: Audience reaction is conjectural.

```python
def check(ctx):
    return ctx.need(None, None, 'Audience reaction is conjectural.')
```

### NEEDS-HUMAN · e03-singularity-talk (attribution, Math proofs)
> Claim: a math avalanche that has top researchers whispering about a singularity

Note: no source sentence matches /(?:leading|top) researchers.{0,100}singularity/. A roundup of papers does not document researchers saying this.

```python
def check(ctx):
    return ctx.require('framing', r'(?:leading|top) researchers.{0,100}singularity', note='A roundup of papers does not document researchers saying this.')
```

### NEEDS-HUMAN · e05-commentator-majority (attribution, Two headlines)
> Claim: Most commentators are treating these as separate headlines, or reducing both to a simple line about verification

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "STORY: Anthropic says Claude agents helped migrate its Messages API from Python to Rust, using live production traffic as the verifier"

Note: Separate story entries do not establish a majority of commentators or their views.

```python
def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'Anthropic says Claude agents'), 'Separate story entries do not establish a majority of commentators or their views.')
```

### NEEDS-HUMAN · e06-missing-tension (opinion, Two headlines)
> Claim: What they're missing is the tension between them

Note: Editorial interpretation.

```python
def check(ctx):
    return ctx.need(None, None, 'Editorial interpretation.')
```

### NEEDS-HUMAN · e07-same-day (comparison, Two headlines)
> Claim: Published the very same day as the math panic, Anthropic's post

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "PublishedNov 25, 2026"

Note: Need a dated math event, not just the date of the scan.

```python
def check(ctx):
    a = ctx.find('anthropic', r'Published\s*Nov 25, 2026')
    b = ctx.find('framing', r'(?:math panic|Aaronson.s (?:post|blog)).{0,60}Nov(?:ember)? 25, 2026')
    return ctx.ok('framing', b, str(a)) if a and b else ctx.need('anthropic', a, 'Need a dated math event, not just the date of the scan.')
```

### NEEDS-HUMAN · e08-reality-check (opinion, Two headlines)
> Claim: Anthropic's post is the sharpest reality check against assuming an overnight math singularity translates straight into messy real-world systems

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "But as Claude has become more capable, it's begun to take on projects in live systems, where generating the work is easier than verifying it."

Note: Sharpest is an editorial ranking.

```python
def check(ctx):
    return ctx.need('anthropic', ctx.find('anthropic', r'generating the work is easier than verifying it'), 'Sharpest is an editorial ranking.')
```

### NEEDS-HUMAN · e09-hyperspace (comparison, Math proofs)
> Claim: mathematics suddenly looks like hyperspace

Note: Figurative comparison.

```python
def check(ctx):
    return ctx.need(None, None, 'Figurative comparison.')
```

### NEEDS-HUMAN · e10-viral-yesterday (attribution, Math proofs)
> Claim: Yesterday, computer scientist Scott Aaronson summed up the shock in a viral post

Source ([x-andrewcurran_](https://x.com/AndrewCurran_/status/2125589468786909510)): "@AndrewCurran_: Scott Aaronson on his blog."

Note: Blog mention does not establish date, contents and reach.

```python
def check(ctx):
    return ctx.need('andrewcurran_', ctx.find('andrewcurran_', r'Scott Aaronson on his blog'), 'Blog mention does not establish date, contents and reach.')
```

### NEEDS-HUMAN · e11-riemann (attribution, Math proofs)
> Claim: fresh off an Anthropic-assisted Riemann Hypothesis proof

Note: no source sentence matches /Anthropic.{0,70}(?:assisted|helped).{0,70}(?:proof of the Riemann hypothesis|Riemann hypothesis proof)/. 

```python
def check(ctx):
    return ctx.require('framing', r'Anthropic.{0,70}(?:assisted|helped).{0,70}(?:proof of the Riemann hypothesis|Riemann hypothesis proof)')
```

### NEEDS-HUMAN · e12-vp-vnp (attribution, Math proofs)
> Claim: OpenAI and Anthropic uploaded GitHub proofs that VP does not equal VNP

Source ([x-andrewcurran_](https://x.com/AndrewCurran_/status/2125589468786909510)): "VP ≠ VNP would be huge for algebraic complexity, but it would not automatically crack RSA unless the proof also yields an efficient factoring"

Note: Conditional comment is not a record of proofs uploaded by both labs.

```python
def check(ctx):
    return ctx.need('andrewcurran_', ctx.find('andrewcurran_', r'VP ≠ VNP would be huge'), 'Conditional comment is not a record of proofs uploaded by both labs.')
```

### NEEDS-HUMAN · e13-openai-exponent (attribution, Math proofs)
> Claim: followed by OpenAI claiming the exact exponent of matrix multiplication is nine-fourths

Note: no source sentence matches /(?:then|later|subsequently) OpenAI.{0,80}exact exponent of matrix multiplication.{0,20}(?:9/4|nine.fourths|2\.25)/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?:then|later|subsequently) OpenAI.{0,80}exact exponent of matrix multiplication.{0,20}(?:9/4|nine.fourths|2\.25)')
```

### NEEDS-HUMAN · e14-exponent-value (number, Math proofs)
> Claim: the exact exponent of matrix multiplication is nine-fourths

Note: no source sentence matches /exact exponent of matrix multiplication.{0,20}(?:9/4|nine.fourths|2\.25)\b/. 

```python
def check(ctx):
    return ctx.require('framing', r'exact exponent of matrix multiplication.{0,20}(?:9/4|nine.fourths|2\.25)\b')
```

### NEEDS-HUMAN · e15-fourier (qualifier, Math proofs)
> Claim: alongside tight Fourier transform bounds

Note: no source sentence matches /(?:tight bounds.{0,30}Fourier transform|tight Fourier transform bounds)/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?:tight bounds.{0,30}Fourier transform|tight Fourier transform bounds)')
```

### NEEDS-HUMAN · e16-silent-commit (attribution, Google papers)
> Claim: Then Google Research silently committed six papers

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "STORY: Google Research posts six Cogentic papers, produced with Gemini 4, claiming results on factoring, the log-rank conjecture and more"

Note: Posting is documented; silence and sequence are not.

```python
def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'Google Research posts six Cogentic papers'), 'Posting is documented; silence and sequence are not.')
```

### NEEDS-HUMAN · e19-paper-topics (attribution, Google papers)
> Claim: They cover integer factoring, discrete logarithms, the log-rank conjecture, approximate Nash equilibria, and graph edge reconstruction

Note: no source sentence matches /discrete logarithms/. 

```python
def check(ctx):
    return ctx.require('framing', r'papers.{0,100}factoring, the log-rank conjecture', r'discrete logarithms', r'approximate Nash equilibria', r'graph edge reconstruction')
```

### NEEDS-HUMAN · e23-aaronson-confidence (attribution, Factoring rumor)
> Claim: Aaronson confirmed he is virtually certain, from multiple reliable sources, that frontier labs hold unreleased cryptography bombshells

Source ([x-andrewcurran_](https://x.com/AndrewCurran_/status/2125589468786909510)): "Scott Aaronson states he is virtually certain, from multiple reliable sources, that frontier labs hold unreleased cryptography "bombshells." He is far less confident about the exact nature-such as a practical polynomial-time"

Note: The wording is in a Grok reply; verify Aaronson’s own statement and level of confidence.

```python
def check(ctx):
    q = ctx.find('andrewcurran_', r'Scott Aaronson states he is virtually certain, from multiple reliable sources, that frontier labs hold unreleased cryptography .bombshells')
    return ctx.need('andrewcurran_', q, 'The wording is in a Grok reply; verify Aaronson’s own statement and level of confidence.')
```

### NEEDS-HUMAN · e24-telephone (attribution, Factoring rumor)
> Claim: he warned specifics can get mangled in a game of Telephone

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Shtetl-Optimized (Scott Aaronson)): Aaronson's own blog; it establishes only what he says he has heard, and he explicitly declines to vouch for the specifics."

Note: Declining to vouch does not document the Telephone explanation.

```python
def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'he explicitly declines to vouch for the specifics'), 'Declining to vouch does not document the Telephone explanation.')
```

### NEEDS-HUMAN · e26-factoring-attribution (attribution, Google papers)
> Claim: Google posted two theoretical factoring results, one randomized and one deterministic

Note: no source sentence matches /two.{0,40}factoring.{0,100}randomized.{0,60}deterministic/. 

```python
def check(ctx):
    return ctx.require('framing', r'Google Research posts six Cogentic papers.{0,80}factoring', r'two.{0,40}factoring.{0,100}randomized.{0,60}deterministic')
```

### NEEDS-HUMAN · e27-factoring-count (number, Google papers)
> Claim: two theoretical factoring results, one randomized and one deterministic

Note: no source sentence matches /(?:two|2) (?:theoretical )?factoring (?:results|algorithms|papers).{0,100}one randomized.{0,30}one deterministic/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?:two|2) (?:theoretical )?factoring (?:results|algorithms|papers).{0,100}one randomized.{0,30}one deterministic')
```

### NEEDS-HUMAN · e28-sieve-comparison (comparison, Google papers)
> Claim: whose bounds do not beat the classic heuristic Number Field Sieve in practice

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted claim; the running-time bound is subexponential, not polynomial, and no independent verification is reported."

Note: This does not compare the bounds or practical performance to the Number Field Sieve.

```python
def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'running-time bound is subexponential, not polynomial'), 'This does not compare the bounds or practical performance to the Number Field Sieve.')
```

### NEEDS-HUMAN · e29-repository-assessment (attribution, Google papers)
> Claim: Aaronson looked at the repository and saw nothing of practical relevance for cryptography

Note: no source sentence matches /Aaronson.{0,100}(?:repository|repo).{0,100}nothing of practical relevance (?:for|to) cryptography/. 

```python
def check(ctx):
    return ctx.require('framing', r'Aaronson.{0,100}(?:repository|repo).{0,100}nothing of practical relevance (?:for|to) cryptography')
```

### NEEDS-HUMAN · e30-github-theorems (attribution, Math proofs)
> Claim: labs drop major theorems straight onto GitHub

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released."

Note: One lab’s repository does not establish the broader practice or theorem status.

```python
def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'Company-posted preprints in a public repository'), 'One lab’s repository does not establish the broader practice or theorem status.')
```

### NEEDS-HUMAN · e31-math-gap (opinion, Proof verification)
> Claim: mathematics has a generator-verifier gap that favors AI

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "Many ambitious Claude projects have relied on this gap: formalizing proofs in mathematics or migrating large, well-tested codebases are tasks Claude can take on as long as it has a reliable way to verify its work."

Note: Generalization about AI advantage.

```python
def check(ctx):
    return ctx.need('anthropic', ctx.find('anthropic', r'Claude projects have relied on this gap: formalizing proofs in mathematics'), 'Generalization about AI advantage.')
```

### NEEDS-HUMAN · e35-lean-oversight (qualifier, Proof verification)
> Claim: even Lean isn't completely hands-off

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "A theorem in mathematics is a precise statement, and a proof assistant (like Lean) can check each step of a proof against a fixed set of rules."

Note: Checking steps does not specify which human oversight is necessary.

```python
def check(ctx):
    return ctx.need('anthropic', ctx.find('anthropic', r'proof assistant \(like Lean\) can check each step'), 'Checking steps does not specify which human oversight is necessary.')
```

### NEEDS-HUMAN · e36-blog-commenters (attribution, Proof verification)
> Claim: As commenters noted on Aaronson's blog, machine-checked proofs can span hundreds of thousands or millions of lines

Note: no source sentence matches /commenters.{0,60}Aaronson.s blog.{0,120}hundreds of thousands or millions of lines/. 

```python
def check(ctx):
    return ctx.require('framing', r'commenters.{0,60}Aaronson.s blog.{0,120}hundreds of thousands or millions of lines')
```

### NEEDS-HUMAN · e37-proof-length (number, Proof verification)
> Claim: can span hundreds of thousands or millions of lines

Note: no source sentence matches /(?:machine.checked|formalized) proofs.{0,70}hundreds of thousands or millions of lines/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?:machine.checked|formalized) proofs.{0,70}hundreds of thousands or millions of lines')
```

### NEEDS-HUMAN · e38-definition-review (qualifier, Proof verification)
> Claim: experts still must check adversarially that the formalized definitions actually match the real conjecture

Note: no source sentence matches /experts.{0,60}(?:adversarial|adversarially).{0,80}definitions.{0,60}conjecture/. 

```python
def check(ctx):
    return ctx.require('framing', r'experts.{0,60}(?:adversarial|adversarially).{0,80}definitions.{0,60}conjecture')
```

### NEEDS-HUMAN · e39-wrong-statement (comparison, Proof verification)
> Claim: rather than the AI proving something technically valid that misses the point

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "A theorem in mathematics is a precise statement, and a proof assistant (like Lean) can check each step of a proof against a fixed set of rules."

Note: Step checking alone does not document a mismatch with an intended conjecture.

```python
def check(ctx):
    return ctx.need('anthropic', ctx.find('anthropic', r'A theorem in mathematics is a precise statement'), 'Step checking alone does not document a mismatch with an intended conjecture.')
```

### NEEDS-HUMAN · e68-zero-human (opinion, Two headlines)
> Claim: Math looks like a zero-human singularity because the rules are fixed

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "A theorem in mathematics is a precise statement, and a proof assistant (like Lean) can check each step of a proof against a fixed set of rules."

Note: Fixed rules do not establish a singularity.

```python
def check(ctx):
    return ctx.need('anthropic', ctx.find('anthropic', r'check each step of a proof against a fixed set of rules'), 'Fixed rules do not establish a singularity.')
```

### NEEDS-HUMAN · e72-holiday (qualifier, Broadcast)
> Claim: have a great Thanksgiving

Note: Sign-off; no broadcast calendar in the source texts.

```python
def check(ctx):
    return ctx.need(None, None, 'Sign-off; no broadcast calendar in the source texts.')
```

### PASS · e04-engineering-post (attribution, Rust migration)
> Claim: a methodical Anthropic engineering post about migrating its Messages API from Python to Rust

Source ([x-anthropicai](https://x.com/AnthropicAI/status/2125627317263466739)): "@AnthropicAI: We recently migrated our Messages API from Python to Rust. … On our engineering blog, we share how we used the existing service to verify the new one, with teams of Claude agents tracking down and fixing differences between the two versions."

```python
def check(ctx):
    return ctx.require('anthropicai', r'@AnthropicAI: We recently migrated our Messages API from Python to Rust', r'On our engineering blog, we share how we used the existing service to verify the new one')
```

### PASS · e17-six-cogentic (attribution, Google papers)
> Claim: six papers produced by its Cogentic harness on Gemini 4

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "STORY: Google Research posts six Cogentic papers, produced with Gemini 4, claiming results on factoring, the log-rank conjecture and more"

```python
def check(ctx):
    return ctx.require('framing', r'Google Research posts six Cogentic papers, produced with Gemini 4')
```

### PASS · e20-social-amplification (attribution, Factoring rumor)
> Claim: social accounts amplified an unverified ten-day rumor

Source ([x-kimmonismus](https://x.com/kimmonismus/status/2125602411540566221)): "AFFILIATION NOTE (scan): AI news aggregator account amplifying a rumor; no independent sourcing and no lab confirmation."

Note: In fact, this rumor has persisted for about ten days, about both Anthropic and OpenAI.

```python
def check(ctx):
    q = ctx.find('kimmonismus', r'aggregator account amplifying a rumor; no independent sourcing and no lab confirmation')
    d = ctx.find('andrewcurran_', r'this rumor has persisted for about ten days, about both Anthropic and OpenAI')
    return ctx.ok('kimmonismus', q, str(d)) if q and d else ctx.need('andrewcurran_', d, 'Need both duration and evidence of unconfirmed amplification.')
```

### PASS · e21-rumor-duration (number, Factoring rumor)
> Claim: unverified ten-day rumor

Source ([x-andrewcurran_](https://x.com/AndrewCurran_/status/2125589468786909510)): "In fact, this rumor has persisted for about ten days, about both Anthropic and OpenAI."

Note: Approximate age of the rumor, not a confirmed discovery.

```python
def check(ctx):
    return ctx.require('andrewcurran_', r'this rumor has persisted for about ten days, about both Anthropic and OpenAI', note='Approximate age of the rumor, not a confirmed discovery.')
```

### PASS · e25-separate-results (comparison, Factoring rumor)
> Claim: That rumor is separate from Google's public papers

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "No lab has published or confirmed such a result. … framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released. … framing (Google Research (GitHub)): Company-posted claim; the running-time bound is subexponential, not polynomial, and no independent verification is reported."

```python
def check(ctx):
    return ctx.require('framing', r'No lab has published or confirmed such a result', r'Company-posted preprints in a public repository', r'running-time bound is subexponential, not polynomial')
```

### PASS · e32-lean-rules (qualifier, Proof verification)
> Claim: a proof assistant like Lean offers a fixed, explicit rulebook

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "A theorem in mathematics is a precise statement, and a proof assistant (like Lean) can check each step of a proof against a fixed set of rules."

```python
def check(ctx):
    return ctx.require('anthropic', r'proof assistant \(like Lean\) can check each step of a proof against a fixed set of rules')
```

### PASS · e34-unverified-now (qualifier, Proof verification)
> Claim: leaving them unverified for now

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released. … framing (Google Research (GitHub)): Company-posted claim; the running-time bound is subexponential, not polynomial, and no independent verification is reported."

```python
def check(ctx):
    q = ctx.find('google', r'entire proof has also been completed and will be released')
    if q and not ctx.art_has(r'not independently verified|not yet independently verified|no independent verification|unverified for now|remain unverified|leaving them unverified'): return ctx.fail('google', q, 'Unreleased is not unformalized; distinguish lack of independent verification.')
    return ctx.require('framing', r'announced Lean formalizations are not yet released', r'no independent verification is reported')
```

### PASS · e40-traffic-growth (number, Rust migration)
> Claim: Messages API traffic grew roughly eighteen hundred times since early 2024

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "From early 2024 to fall 2026, API traffic grew roughly 1,800 times."

```python
def check(ctx):
    return ctx.require('anthropic', r'From early 2024 to fall 2026, API traffic grew roughly 1,800 times')
```

### PASS · e41-overhead (comparison, Rust migration)
> Claim: Anthropic needed far less overhead

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "As each reply arrived, the stream of tokens had to be sorted into text, thinking, and tool calls, and Python added overhead to every one of those steps each time it created an object, freed memory, or handed its work to the next task. … Traffic eventually grew far beyond what the initial Python service was built for (Figure 1), and we quickly needed to find a way to make the service much more efficient. … Rust would allow us to use far less CPU per request."

```python
def check(ctx):
    return ctx.require('anthropic', r'Python added overhead to every one of those steps', r'needed to find a way to make the service much more efficient', r'Rust would allow us to use far less CPU per request')
```

### PASS · e42-reported-gains (attribution, Rust migration)
> Claim: According to Anthropic, moving from Python to Rust cut CPU use per request by about seventy percent and median time to first token by about twenty percent, with zero downtime

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "We ran into this problem when we migrated our Messages API from Python to Rust. … This allowed us to ship an API on Rust that uses about 70% less CPU per request and cuts median time to first token by about 20% without ever taking the service offline or freezing feature development."

Note: Company summary; figure covers one region for CPU and Claude Code requests for latency.

```python
def check(ctx):
    return ctx.require(
        'anthropic',
        r'migrated our Messages API from Python to Rust',
        r'uses about 70% less CPU per request',
        r'cuts median time to first token by about 20%',
        r'without ever taking the service offline',
        note='Company summary; figure covers one region for CPU and Claude Code requests for latency.',
    )
```

### PASS · e43-cpu-cut (number, Rust migration)
> Claim: cut CPU use per request by about seventy percent

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "This allowed us to ship an API on Rust that uses about 70% less CPU per request and cuts median time to first token by about 20% without ever taking the service offline or freezing feature development."

```python
def check(ctx):
    return ctx.require('anthropic', r'uses about 70% less CPU per request')
```

### PASS · e44-latency-cut (number, Rust migration)
> Claim: median time to first token by about twenty percent

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "This allowed us to ship an API on Rust that uses about 70% less CPU per request and cuts median time to first token by about 20% without ever taking the service offline or freezing feature development."

```python
def check(ctx):
    return ctx.require('anthropic', r'cuts median time to first token by about 20%')
```

### PASS · e45-no-outage (number, Rust migration)
> Claim: with zero downtime

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "This allowed us to ship an API on Rust that uses about 70% less CPU per request and cuts median time to first token by about 20% without ever taking the service offline or freezing feature development."

```python
def check(ctx):
    return ctx.require('anthropic', r'ship an API on Rust.{0,150}without ever taking the service offline')
```

### PASS · e47-week (number, Rust migration)
> Claim: in about a week

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "Claude wrote a first version of the API's core request path in about a week."

```python
def check(ctx):
    return ctx.require('anthropic', r'Claude wrote a first version of the API.s core request path in about a week')
```

### PASS · e48-migration-months (number, Rust migration)
> Claim: migrating public traffic still took five months, from April to September

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "Changes merged to our API's Rust code in each two-week period, from April until public traffic moved to Rust in September 2026."

Note: Five calendar months between named months, not five months spent shifting traffic itself.

```python
def check(ctx):
    return ctx.require('anthropic', r'from April until public traffic moved to Rust in September 2026', note='Five calendar months between named months, not five months spent shifting traffic itself.')
```

### PASS · e49-gap-inverts (comparison, Production verification)
> Claim: In a live production system, the generator-verifier gap inverts

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "But as Claude has become more capable, it's begun to take on projects in live systems, where generating the work is easier than verifying it."

```python
def check(ctx):
    return ctx.require('anthropic', r'projects in live systems, where generating the work is easier than verifying it')
```

### PASS · e50-no-rulebook (qualifier, Production verification)
> Claim: There is no fixed rulebook

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "In our case, neither approach was sufficient, so we used the existing system as an oracle to test parity during the migration. … We were releasing new models and shipping new features regularly, which made the definition of "correct" a moving target."

Note: Supports the claim for this migration, not every production system.

```python
def check(ctx):
    return ctx.require('anthropic', r'In our case, neither approach was sufficient', r'definition of .correct. a moving target', note='Supports the claim for this migration, not every production system.')
```

### PASS · e51-changing-python (qualifier, Rust migration)
> Claim: The Python service kept changing throughout the rewrite

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "This proved hard for several reasons, including that the Python API continued changing throughout the migration, so parity was a moving target; Claude can reply nondeterministically to the same request, so a difference between two outputs didn't necessarily mean a bug; and we couldn't read customer requests, so we weren't able to easily see where the two versions diverged."

```python
def check(ctx):
    return ctx.require('anthropic', r'the Python API continued changing throughout the migration')
```

### PASS · e52-insufficient-tests (qualifier, Production verification)
> Claim: Anthropic couldn't trust ported integration tests alone

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "Tests were the easiest place for us to start, since we already had an existing set of about 700 integration tests. … However, two problems limited our ability to trust them to verify the correctness of a migration as high stakes as this (Figure 4). … We saw this happen: when we audited the ported tests, we found more than 100 weakened assertions."

```python
def check(ctx):
    return ctx.require('anthropic', r'existing set of about 700 integration tests', r'two problems limited our ability to trust them to verify the correctness', r'when we audited the ported tests')
```

### PASS · e53-weakened-assertions (number, Production verification)
> Claim: an audit found over a hundred weakened assertions

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "We saw this happen: when we audited the ported tests, we found more than 100 weakened assertions."

```python
def check(ctx):
    return ctx.require('anthropic', r'when we audited the ported tests, we found more than 100 weakened assertions')
```

### PASS · e55-quarter-inputs (number, Production verification)
> Claim: it matched only about a quarter of live production inputs

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "Our Rust API passed about 98% of its tests in April, yet only about a quarter of inputs matched on production traffic (Figure 6)."

```python
def check(ctx):
    return ctx.require('anthropic', r'only about a quarter of inputs matched on production traffic')
```

### PASS · e56-uncovered-cases (qualifier, Production verification)
> Claim: Real traffic hit uncovered edge cases

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "The gap came partly from cases in production traffic that our tests didn't cover."

```python
def check(ctx):
    return ctx.require('anthropic', r'cases in production traffic that our tests didn.t cover')
```

### PASS · e57-emoji-bytes (comparison, Production verification)
> Claim: Python escaping emojis in JSON tool calls while Rust wrote them raw

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "For example, when Python writes JSON tool calls, it escapes certain characters (e.g., an emoji) by replacing them with text codes. … Rust wrote those characters as is, so the two prompts differed by a few bytes."

```python
def check(ctx):
    return ctx.require('anthropic', r'when Python writes JSON tool calls, it escapes certain characters', r'an emoji\) by replacing them with text codes', r'Rust wrote those characters as is')
```

### PASS · e58-common-bugs (qualifier, Production verification)
> Claim: common bugs fired across huge waves of requests

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "In a test suite, each case counts once, but in live traffic, a bug will show up in each request where it's triggered, which means a single common bug can cause many mismatches. … A single bug could produce hundreds of thousands of nearly identical diff records."

```python
def check(ctx):
    return ctx.require('anthropic', r'a single common bug can cause many mismatches', r'A single bug could produce hundreds of thousands of nearly identical diff records')
```

### PASS · e59-private-fingerprints (attribution, Shadow oracle)
> Claim: Anthropic built a privacy-preserving shadow oracle comparing byte-level fingerprints without reading user text

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "In our case, neither approach was sufficient, so we used the existing system as an oracle to test parity during the migration. … To do that we had to work without reading user requests or Claude's replies to them, which means we couldn't easily see where the Rust and Python versions of the API differed. … The result was a shadowing system that produced a small record of each difference between our Rust and Python APIs. … first diff: byte 17 ← fingerprint"

```python
def check(ctx):
    return ctx.require(
        'anthropic',
        r'used the existing system as an oracle',
        r'without reading user requests or Claude.s replies',
        r'shadowing system that produced a small record of each difference',
        r'first diff: byte 17.{0,30}fingerprint',
    )
```

### PASS · e61-missing-description (qualifier, Shadow oracle)
> Claim: a web search tool description was missing

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "The production API retrieved the web search tool's description from an internal service. … The Rust API didn't call this service yet, so the tool description was missing from the prompts."

```python
def check(ctx):
    return ctx.require('anthropic', r'production API retrieved the web search tool.s description from an internal service', r'the tool description was missing from the prompts')
```

### PASS · e62-local-copy (attribution, Shadow oracle)
> Claim: the agent hardcoded the text locally instead of calling the internal service

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "The production API retrieved the web search tool's description from an internal service. … The Rust API didn't call this service yet, so the tool description was missing from the prompts. … An agent proposed a shortcut to copy the text into files that would be readable by Rust. … The prompts then matched, and the fix passed the local verifier."

```python
def check(ctx):
    return ctx.require('anthropic', r'web search tool.s description from an internal service', r'Rust API didn.t call this service yet', r'An agent proposed a shortcut to copy the text into files that would be readable by Rust', r'The prompts then matched, and the fix passed the local verifier')
```

### PASS · e63-matched-prompts (comparison, Shadow oracle)
> Claim: The outputs matched

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "The prompts then matched, and the fix passed the local verifier."

Note: Outputs of local prompt construction, not production model replies.

```python
def check(ctx):
    return ctx.require('anthropic', r'The prompts then matched, and the fix passed the local verifier', note='Outputs of local prompt construction, not production model replies.')
```

### PASS · e64-verifier-pass (attribution, Shadow oracle)
> Claim: The verifier said pass

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "The prompts then matched, and the fix passed the local verifier."

Note: Local verifier only.

```python
def check(ctx):
    return ctx.require('anthropic', r'The prompts then matched, and the fix passed the local verifier', note='Local verifier only.')
```

### PASS · e65-engineer-rejection (attribution, Shadow oracle)
> Claim: An engineer had to reject it as throwaway code

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "Agents trace a mismatch to the web search tool across four Slack threads and propose a fix, which an engineer rejects as throwaway code."

```python
def check(ctx):
    return ctx.require('anthropic', r'propose a fix, which an engineer rejects as throwaway code')
```

### PASS · e67-no-repeat (number, Engineering oversight)
> Claim: teams didn't have to catch the same shortcut twice

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "For example, when an engineer turned down the web search shortcut (Figure 12), the agent saved a note to memory explaining the decision, the reason for it, and the correct fix, which was to have Rust call the service that supplies tool descriptions. … Agents checked the memory note, recognized the known bug, and linked those records to it, instead of writing another workaround (Figure 14)."

Note: Observed for this shortcut; not a zero-recurrence statistic across all shortcuts.

```python
def check(ctx):
    return ctx.require('anthropic', r'engineer turned down the web search shortcut', r'Agents checked the memory note, recognized the known bug, and linked those records to it, instead of writing another workaround', note='Observed for this shortcut; not a zero-recurrence statistic across all shortcuts.')
```

### PASS · e69-moving-target (comparison, Production verification)
> Claim: correctness is a moving target

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "We were releasing new models and shipping new features regularly, which made the definition of "correct" a moving target."

```python
def check(ctx):
    return ctx.require('anthropic', r'made the definition of .correct. a moving target')
```

### PASS · e70-imperfect-checks (qualifier, Production verification)
> Claim: agents optimize around imperfect checks

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "But the verifier rewarded matching outputs, and the agent found the cheapest way to produce them. … A verifier can tell an agent whether the outputs matched, but not whether the fix is good enough to ship."

```python
def check(ctx):
    return ctx.require('anthropic', r'verifier rewarded matching outputs, and the agent found the cheapest way to produce them', r'not whether the fix is good enough to ship')
```

### PASS · oe1-aaronson-hearsay (objection, Factoring rumor)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Shtetl-Optimized (Scott Aaronson)): Aaronson's own blog; it establishes only what he says he has heard, and he explicitly declines to vouch for the specifics."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'only what he says he has heard')
    return ctx.ok('framing', q) if ctx.art_has(r'Aaronson.{0,100}(?:heard|told|from multiple reliable sources)') else ctx.fail('framing', q, 'Identify the information as second hand.')
```

### PASS · oe11-logrank-verification (objection, Google papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted claim of a tiny improvement over the square-root bound (epsilon of 5 millionths); not a proof of the conjecture; not independently verified."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'not a proof of the conjecture; not independently verified')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:log[- ]rank|(?:six|Google.s) papers).{0,200}(?:not independently verified|no independent verification|remain unverified|unverified for now|leaving them unverified)') else ctx.fail('framing', q, 'Flag the log-rank claim as lacking independent verification.')
```

### PASS · oe12-company-metrics (objection, Rust migration)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Anthropic): Company-reported engineering results; performance numbers are Anthropic's own and not independently measured."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'performance numbers are Anthropic.s own')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:according to Anthropic|Anthropic (?:reports|says)|company[- ]reported).{0,200}CPU') else ctx.fail('framing', q, 'Attribute the measurements to Anthropic.')
```

### PASS · oe2-specifics (objection, Factoring rumor)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Shtetl-Optimized (Scott Aaronson)): Aaronson's own blog; it establishes only what he says he has heard, and he explicitly declines to vouch for the specifics."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'declines to vouch for the specifics')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:not vouch|declin\w* to vouch|less confident about the exact|specifics can get mangled|uncertain about the specifics)') else ctx.fail('framing', q, 'Carry Aaronson’s reservation about specifics.')
```

### PASS · oe6-lean-release (objection, Proof verification)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'announced Lean formalizations are not yet released')
    return ctx.ok('framing', q) if ctx.art_has(r'Lean(?: 4)? formalizations?.{0,60}(?:not yet (?:public|released)|unreleased|coming in a companion submission|will be released)|pending (?:release of (?:the )?)?Lean 4 formalizations') else ctx.fail('framing', q, 'State that the announced formalizations are not public yet.')
```

### PASS · oe8-factoring-verification (objection, Google papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted claim; the running-time bound is subexponential, not polynomial, and no independent verification is reported."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'no independent verification is reported')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:factoring (?:papers|results|bounds)|Google.s (?:public )?(?:papers|results)|six papers).{0,200}(?:not independently verified|no independent verification|remain unverified|unverified for now|leaving them unverified)') else ctx.fail('framing', q, 'Flag the public factoring results, not just the separate rumor, as lacking independent verification.')
```

## takeaways

### FAIL · ot1-company-preprints (objection, Gemini math papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released."

Note: Identify the company-posted preprints.

```python
def check(ctx):
    q = ctx.find('framing', r'Company-posted preprints in a public repository')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:Google(?: Research)?|company)[- ](?:posted|published|released).{0,100}preprints?') else ctx.fail('framing', q, 'Identify the company-posted preprints.')
```

### FAIL · ot2-peer-review (objection, Gemini math papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released."

Note: State lack of peer review.

```python
def check(ctx):
    q = ctx.find('framing', r'no peer review')
    return ctx.ok('framing', q) if ctx.art_has(r'no peer review|not (?:yet )?peer[- ]reviewed|without peer review|awaiting peer review') else ctx.fail('framing', q, 'State lack of peer review.')
```

### FAIL · ot4-factoring-bound (objection, Gemini math papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted claim; the running-time bound is subexponential, not polynomial, and no independent verification is reported."

Note: Give the qualification on the public factoring bound.

```python
def check(ctx):
    q = ctx.find('framing', r'subexponential, not polynomial')
    return ctx.ok('framing', q) if ctx.art_has(r'sub[- ]?exponential.{0,50}(?:not|rather than) polynomial|not polynomial.{0,50}sub[- ]?exponential') else ctx.fail('framing', q, 'Give the qualification on the public factoring bound.')
```

### FAIL · ot7-independent-measurement (objection, Messages API migration)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Anthropic): Company-reported engineering results; performance numbers are Anthropic's own and not independently measured."

Note: Say the performance gains were not independently measured.

```python
def check(ctx):
    q = ctx.find('framing', r'not independently measured')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:numbers|gains|metrics|performance|measurements).{0,90}(?:not independently (?:measured|verified)|no independent (?:measurement|benchmark))|no independent (?:performance )?(?:benchmark|measurement)') else ctx.fail('framing', q, 'Say the performance gains were not independently measured.')
```

### FAIL · t03-human-involvement (attribution, Gemini math papers)
> Claim: claiming no human involvement after the first prompt

Source ([primary-google-cogentic-six-math-papers](https://raw.githubusercontent.com/google-research/google-research/master/cogentic_research_papers/logrank_conjecture/README.md)): "There was no human interaction other than the initial prompt for Cogentic to generate a full proof and formalization"

Note: The claim concerns this proof, not six proofs.

```python
def check(ctx):
    return ctx.support_or_contradict('google', r'(?:all six papers|six proofs).{0,120}no human interaction other than the initial prompt', r'There was no human interaction other than the initial prompt for Cogentic to\s+generate a full proof and formalization', 'The claim concerns this proof, not six proofs.')
```

### FAIL · t05-pending-formalizations (qualifier, Gemini math papers)
> Claim: they remain unverified pending Lean 4 formalizations

Source ([primary-google-cogentic-six-math-papers](https://raw.githubusercontent.com/google-research/google-research/master/cogentic_research_papers/logrank_conjecture/README.md)): "formalization of the entire proof has also been completed"

Note: At least the log-rank formalization is complete; public release and independent verification are separate issues.

```python
def check(ctx):
    return ctx.support_or_contradict('google', r'Lean 4 formalizations.{0,80}(?:not yet completed|remain to be written)', r'formalization of the\s+entire proof has also been completed', 'At least the log-rank formalization is complete; public release and independent verification are separate issues.')
```

### FAIL · t18-core-authorship (attribution, Messages API migration)
> Claim: Claude wrote the core request path

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "Claude wrote a first version of the API's core request path in about a week."

Note: Authorship is explicitly scoped to a first version.

```python
def check(ctx):
    return ctx.support_or_contradict('anthropic', r'Claude wrote the (?:API.s )?core request path', r'Claude wrote a first version of the API.s core request path', 'Authorship is explicitly scoped to a first version.')
```

### NEEDS-HUMAN · t07-crypto-assessment (attribution, Gemini math papers)
> Claim: computer scientist Scott Aaronson saw nothing of practical cryptographic relevance in their factoring results

Note: no source sentence matches /Aaronson.{0,120}(?:factoring|repository).{0,120}nothing of practical (?:cryptographic relevance|relevance (?:to|for) cryptography)/. 

```python
def check(ctx):
    return ctx.require('framing', r'Aaronson.{0,120}(?:factoring|repository).{0,120}nothing of practical (?:cryptographic relevance|relevance (?:to|for) cryptography)')
```

### NEEDS-HUMAN · t08-crypto-opinion (opinion, Gemini math papers)
> Claim: nothing of practical cryptographic relevance in their factoring results

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted claim; the running-time bound is subexponential, not polynomial, and no independent verification is reported."

Note: The asymptotic classification alone cannot decide practical relevance.

```python
def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'running-time bound is subexponential'), 'The asymptotic classification alone cannot decide practical relevance.')
```

### NEEDS-HUMAN · t15-oversight-duration (qualifier, Messages API migration)
> Claim: earning production trust still took five months of human oversight

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "Changes merged to our API's Rust code in each two-week period, from April until public traffic moved to Rust in September 2026."

Note: Dates bound the migration work. They do not isolate the time spent earning trust under human oversight.

```python
def check(ctx):
    return ctx.need('anthropic', ctx.find('anthropic', r'from April until public traffic moved to Rust in September 2026'), 'Dates bound the migration work. They do not isolate the time spent earning trust under human oversight.')
```

### NEEDS-HUMAN · t16-five-months (number, Messages API migration)
> Claim: five months of human oversight

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "Changes merged to our API's Rust code in each two-week period, from April until public traffic moved to Rust in September 2026."

Note: Five named-month intervals; chart measures merged changes, not a duration of oversight.

```python
def check(ctx):
    return ctx.need('anthropic', ctx.find('anthropic', r'from April until public traffic moved to Rust in September 2026'), 'Five named-month intervals; chart measures merged changes, not a duration of oversight.')
```

### PASS · ot3-lean-release (objection, Gemini math papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'formalizations are not yet released')
    return ctx.ok('framing', q) if ctx.art_has(r'Lean(?: 4)? formalizations?.{0,60}(?:not yet (?:public|released)|unreleased|coming in a companion submission|will be released)|pending (?:public )?release of (?:the )?Lean 4 formalizations|pending Lean 4 formalizations') else ctx.fail('framing', q, 'Specify pending release rather than implying formalization has not been done.')
```

### PASS · ot5-independent-verification (objection, Gemini math papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted claim; the running-time bound is subexponential, not polynomial, and no independent verification is reported."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'no independent verification is reported')
    return ctx.ok('framing', q) if ctx.art_has(r'no independent verification|not (?:yet )?independently verified|they remain unverified') else ctx.fail('framing', q, 'Flag lack of independent verification of the public claims.')
```

### PASS · ot6-company-metrics (objection, Messages API migration)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Anthropic): Company-reported engineering results; performance numbers are Anthropic's own and not independently measured."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'performance numbers are Anthropic.s own')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:Anthropic reports|according to Anthropic|company[- ]reported).{0,200}CPU') else ctx.fail('framing', q, 'Attribute the measurements to Anthropic.')
```

### PASS · t01-google-posted (attribution, Gemini math papers)
> Claim: Google Research posted six Gemini 4 math papers

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "STORY: Google Research posts six Cogentic papers, produced with Gemini 4, claiming results on factoring, the log-rank conjecture and more"

```python
def check(ctx):
    return ctx.require('framing', r'Google Research posts six Cogentic papers, produced with Gemini 4')
```

### PASS · t02-paper-count (number, Gemini math papers)
> Claim: six Gemini 4 math papers

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "STORY: Google Research posts six Cogentic papers, produced with Gemini 4, claiming results on factoring, the log-rank conjecture and more"

```python
def check(ctx):
    return ctx.require('framing', r'six Cogentic papers, produced with Gemini 4, claiming results on factoring, the log-rank conjecture')
```

### PASS · t04-after-prompt (qualifier, Gemini math papers)
> Claim: after the first prompt

Source ([primary-google-cogentic-six-math-papers](https://raw.githubusercontent.com/google-research/google-research/master/cogentic_research_papers/logrank_conjecture/README.md)): "no human interaction other than the initial prompt for Cogentic to generate a full proof and formalization"

Note: Timing qualifier supported for the log-rank paper only.

```python
def check(ctx):
    return ctx.require('google', r'no human interaction other than the initial prompt for Cogentic to\s+generate a full proof and formalization', note='Timing qualifier supported for the log-rank paper only.')
```

### PASS · t06-aaronson-profession (qualifier, Gemini math papers)
> Claim: computer scientist Scott Aaronson

Source ([x-andrewcurran_](https://x.com/AndrewCurran_/status/2125589468786909510)): "@grok (1 likes): @CandleHigh @AndrewCurran_ @grom Scott Aaronson is a leading theoretical computer scientist and professor at UT Austin, specializing in quantum computing and complexity theory."

Note: Description in a reply, not an institutional bio.

```python
def check(ctx):
    return ctx.require('andrewcurran_', r'Scott Aaronson is a leading theoretical computer scientist', note='Description in a reply, not an institutional bio.')
```

### PASS · t09-anthropic-metrics (attribution, Messages API migration)
> Claim: Anthropic reports that migrating its Messages API from Python to Rust cut CPU use per request by about 70 percent and median time to first token by about 20 percent

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "We ran into this problem when we migrated our Messages API from Python to Rust. … This allowed us to ship an API on Rust that uses about 70% less CPU per request and cuts median time to first token by about 20% without ever taking the service offline or freezing feature development."

```python
def check(ctx):
    return ctx.require('anthropic', r'we migrated our Messages API from Python to Rust', r'Rust that uses about 70% less CPU per request and cuts median time to first token by about 20%')
```

### PASS · t10-migration-direction (attribution, Messages API migration)
> Claim: migrating its Messages API from Python to Rust

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "We ran into this problem when we migrated our Messages API from Python to Rust."

```python
def check(ctx):
    return ctx.require('anthropic', r'we migrated our Messages API from Python to Rust')
```

### PASS · t11-cpu-comparison (comparison, Messages API migration)
> Claim: cut CPU use per request by about 70 percent

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "This allowed us to ship an API on Rust that uses about 70% less CPU per request and cuts median time to first token by about 20% without ever taking the service offline or freezing feature development."

```python
def check(ctx):
    return ctx.require('anthropic', r'Rust that uses about 70% less CPU per request')
```

### PASS · t12-cpu-number (number, Messages API migration)
> Claim: about 70 percent

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "This allowed us to ship an API on Rust that uses about 70% less CPU per request and cuts median time to first token by about 20% without ever taking the service offline or freezing feature development."

```python
def check(ctx):
    return ctx.require('anthropic', r'about 70% less CPU per request')
```

### PASS · t13-joint-comparison (comparison, Messages API migration)
> Claim: cut CPU use per request by about 70 percent and median time to first token by about 20 percent

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "This allowed us to ship an API on Rust that uses about 70% less CPU per request and cuts median time to first token by about 20% without ever taking the service offline or freezing feature development."

```python
def check(ctx):
    return ctx.require('anthropic', r'uses about 70% less CPU per request and cuts median time to first token by about 20%')
```

### PASS · t14-latency-number (number, Messages API migration)
> Claim: about 20 percent

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "This allowed us to ship an API on Rust that uses about 70% less CPU per request and cuts median time to first token by about 20% without ever taking the service offline or freezing feature development."

```python
def check(ctx):
    return ctx.require('anthropic', r'cuts median time to first token by about 20%')
```

### PASS · t17-after-core (qualifier, Messages API migration)
> Claim: after Claude wrote the core request path

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "Claude wrote a first version of the API's core request path in about a week. … But building trust in the migration required us to find a way to verify that our Rust API was at parity with our production API."

Note: Sequence concerns the first version, not a finished path.

```python
def check(ctx):
    return ctx.require('anthropic', r'Claude wrote a first version of the API.s core request path', r'But building trust in the migration required us to find a way to verify', note='Sequence concerns the first version, not a finished path.')
```

### PASS · t19-week (number, Messages API migration)
> Claim: in about a week

Source ([primary-anthropic-messages-api-rust-migration](https://www.anthropic.com/research/migrating-api-to-rust)): "Claude wrote a first version of the API's core request path in about a week."

```python
def check(ctx):
    return ctx.require('anthropic', r'Claude wrote a first version of the API.s core request path in about a week')
```

### PASS · tc01-citation (citation, takeaway 1)

Note: Takeaway 1 cites https://scottaaronson.blog/?p=10379, which is listed in the episode sources.json.

```python
def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 1 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 1 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))
```

### PASS · tc02-citation (citation, takeaway 2)

Note: Takeaway 2 cites https://www.anthropic.com/research/migrating-api-to-rust, which is listed in the episode sources.json.

```python
def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 2 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 2 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))
```
