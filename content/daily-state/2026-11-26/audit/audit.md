# Executable audit, Daily State of AI 2026-11-26

Each claim is tested by a deterministic Python check against snapshotted source texts and X posts. PASS = the source sentence quoted supports the claim; FAIL = the source contradicts it or a required caveat is missing; NEEDS-HUMAN = opinion or not decidable by string/number match.

| artifact | PASS | FAIL | NEEDS-HUMAN | ERROR |
|---|---|---|---|---|
| episode | 13 | 26 | 55 | 0 |
| takeaways | 18 | 13 | 5 | 0 |

## Sources
- `primary-google-cogentic-six-math-papers`: [Breaking the Square-Root Barrier for the Log-Rank Conjecture](https://raw.githubusercontent.com/google-research/google-research/master/cogentic_research_papers/logrank_conjecture/README.md) (sha256 0125de488c93…)
- `x-andrewcurran_`: [X post by @AndrewCurran_](https://x.com/AndrewCurran_/status/2125589468786909510) (sha256 5ef4c7130444…)
- `x-kimmonismus`: [X post by @kimmonismus (Chubby♨️)](https://x.com/kimmonismus/status/2125602411540566221) (sha256 2c844958f5cf…)
- `x-anthropicai`: [X post by @AnthropicAI](https://x.com/AnthropicAI/status/2125627317263466739) (sha256 84ceef3b9ded…)
- `scan-framing`: [Morning X-first scan: verification framing per story](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt) (sha256 a8bb6a704f5d…)

## episode

### FAIL · e06-labs-stopped-waiting (attribution, GitHub publishing)
> Claim: Frontier labs have stopped waiting for press releases, blog posts, or even tweets

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released."

Note: A repository posting establishes neither a change in lab policy nor the absence of announcements.

```python
def check(ctx):
    q = ctx.find('framing', r'Company-posted preprints in a public repository')
    return ctx.fail('framing', q, 'A repository posting establishes neither a change in lab policy nor the absence of announcements.') if q else ctx.need(None, None, 'Need evidence of the claimed change.')
```

### FAIL · e07-straight-to-repositories (attribution, GitHub publishing)
> Claim: They just push papers straight to code repositories

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released."

Note: Evidence concerns one company, not a general frontier-lab practice.

```python
def check(ctx):
    return ctx.support_or_contradict('framing', r'Frontier labs .*publish .*directly to (?:code )?repositories', r'Company-posted preprints in a public repository', 'Evidence concerns one company, not a general frontier-lab practice.')
```

### FAIL · e10-compound-rsa-warning (attribution, RSA rumors)
> Claim: Viral posts with thousands of likes were warning that frontier labs had secretly cracked RSA encryption and could soon forge software updates across the internet

Source ([x-kimmonismus](https://x.com/kimmonismus/status/2125602411540566221)): "If an algorithm like this actually works on real key sizes, you wouldn't even need a quantum computer to break it."

Note: Conditional consequences, not a completed secret break or a near-term forecast; no original-post like count.

```python
def check(ctx):
    q = ctx.find('kimmonismus', r'If an algorithm like this actually works on real key sizes')
    return ctx.fail('kimmonismus', q, 'Conditional consequences, not a completed secret break or a near-term forecast; no original-post like count.') if q else ctx.need(None, None, 'Need the attributed warning and metrics.')
```

### FAIL · e11-secret-crack (qualifier, RSA rumors)
> Claim: secretly cracked RSA encryption

Source ([x-andrewcurran_](https://x.com/AndrewCurran_/status/2125589468786909510)): "This would crack RSA. https://t.co/s5AHbmcDFP https://t.co/YBOYkSYVOr"

Note: Would crack is not secretly cracked.

```python
def check(ctx):
    return ctx.support_or_contradict('andrewcurran_', r'(?:secretly|privately) (?:cracked|broke) RSA', r'This would crack RSA', 'Would crack is not secretly cracked.')
```

### FAIL · e12-soon-forge (qualifier, RSA rumors)
> Claim: could soon forge software updates across the internet

Source ([x-kimmonismus](https://x.com/kimmonismus/status/2125602411540566221)): "Fake software updates could pass signature checks, RSA-encrypted data could be read, and systems across the internet would have to migrate off RSA fast."

Note: Hypothetical effect; the post gives no timeline.

```python
def check(ctx):
    return ctx.support_or_contradict('kimmonismus', r'(?:soon|shortly).*fake software updates', r'Fake software updates could pass signature checks', 'Hypothetical effect; the post gives no timeline.')
```

### FAIL · e35-six-no-announcement (attribution, Google papers)
> Claim: Google committed six more at once with no announcement

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "STORY: Google Research posts six Cogentic papers, produced with Gemini 4, claiming results on factoring, the log-rank conjecture and more"

Note: Posting six does not establish one commit, six additional papers or no announcement.

```python
def check(ctx):
    return ctx.support_or_contradict('framing', r'(?=.*Google)(?=.*six (?:more|new))(?=.*(?:at once|single commit))(?=.*(?:without|no) (?:an )?announcement)', r'Google Research posts six Cogentic papers', 'Posting six does not establish one commit, six additional papers or no announcement.')
```

### FAIL · e36-six-at-once (number, Google papers)
> Claim: six more at once

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "STORY: Google Research posts six Cogentic papers, produced with Gemini 4, claiming results on factoring, the log-rank conjecture and more"

Note: The count is given, not the increment and timing.

```python
def check(ctx):
    return ctx.support_or_contradict('framing', r'six (?:more|additional) .*?(?:at once|together|single commit)', r'Google Research posts six Cogentic papers', 'The count is given, not the increment and timing.')
```

### FAIL · e38-all-six-autonomy (attribution, Google papers)
> Claim: Google says its Cogentic agent harness, running on Gemini 4, produced all six with no human interaction after the initial prompt

Source ([primary-google-cogentic-six-math-papers](https://raw.githubusercontent.com/google-research/google-research/master/cogentic_research_papers/logrank_conjecture/README.md)): "There was no human interaction other than the initial prompt for Cogentic to"

Note: The README describes this proof and formalization, not the interaction history of all six.

```python
def check(ctx):
    return ctx.support_or_contradict('google', r'(?=.*(?:all six|six papers))(?=.*Cogentic)(?=.*Gemini 4)(?=.*no human interaction other than the initial prompt)', r'There was no human interaction other than the initial prompt', 'The README describes this proof and formalization, not the interaction history of all six.')
```

### FAIL · e41-no-interaction (qualifier, Google papers)
> Claim: no human interaction after the initial prompt

Source ([primary-google-cogentic-six-math-papers](https://raw.githubusercontent.com/google-research/google-research/master/cogentic_research_papers/logrank_conjecture/README.md)): "There was no human interaction other than the initial prompt for Cogentic to"

Note: Supported for the log-rank proof and formalization only; the episode applies it to all six.

```python
def check(ctx):
    return ctx.support_or_contradict('google', r'(?=.*(?:all six|six papers))(?=.*no human interaction other than the initial prompt)', r'There was no human interaction other than the initial prompt', 'Supported for the log-rank proof and formalization only; the episode applies it to all six.')
```

### FAIL · e49-deterministic-factoring (qualifier, Google factoring)
> Claim: the other achieves deterministic subexponential factoring without randomness

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted claim; the running-time bound is subexponential, not polynomial, and no independent verification is reported."

Note: Only a claimed runtime is given, not a verified second deterministic algorithm.

```python
def check(ctx):
    return ctx.support_or_contradict('framing', r'(?=.*(?:other|second))(?=.*deterministic)(?=.*subexponential)(?=.*factor)', r'Company-posted claim; the running-time bound is subexponential', 'Only a claimed runtime is given, not a verified second deterministic algorithm.')
```

### FAIL · e50-aaronson-confirmed (attribution, Google factoring)
> Claim: After checking the repository, Aaronson confirmed both are major theoretical results with no practical impact on cryptography

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted claim; the running-time bound is subexponential, not polynomial, and no independent verification is reported."

Note: No independent confirmation is reported here.

```python
def check(ctx):
    return ctx.support_or_contradict('framing', r'(?=.*Aaronson)(?=.*(?:checked|checking) the repository)(?=.*both)(?=.*major theoretical results)(?=.*no practical impact)', r'Company-posted claim; the running-time bound is subexponential.*no independent verification is reported', 'No independent confirmation is reported here.')
```

### FAIL · e54-lean-complete (attribution, Google formalizations)
> Claim: companion Lean 4 formalizations it says are complete

Source ([primary-google-cogentic-six-math-papers](https://raw.githubusercontent.com/google-research/google-research/master/cogentic_research_papers/logrank_conjecture/README.md)): "formalization of the entire proof has also been completed"

Note: Completion is claimed for the singular log-rank formalization, not the whole set.

```python
def check(ctx):
    return ctx.support_or_contradict('google', r'Lean 4 formalizations .*?(?:are|have been) completed', r'formalization of the\s+entire proof has also been completed', 'Completion is claimed for the singular log-rank formalization, not the whole set.')
```

### FAIL · e60-refused-to-name (attribution, Aaronson crypto warning)
> Claim: He deliberately refused to name RSA or claim anyone had factored large numbers in polynomial time

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Shtetl-Optimized (Scott Aaronson)): Aaronson's own blog; it establishes only what he says he has heard, and he explicitly declines to vouch for the specifics."

Note: Declining to vouch for specifics is not a statement that he refused to name RSA.

```python
def check(ctx):
    return ctx.support_or_contradict('framing', r'(?=.*explicitly decline)(?=.*name RSA)(?=.*(?:polynomial.time factoring|factor .*polynomial time))', r'he explicitly declines to vouch for the specifics', 'Declining to vouch for specifics is not a statement that he refused to name RSA.')
```

### FAIL · e63-rsa-dead-comparison (comparison, RSA rumors)
> Claim: turning a calibrated warning into viral claims that RSA was dead

Source ([x-andrewcurran_](https://x.com/AndrewCurran_/status/2125589468786909510)): "This would crack RSA. https://t.co/s5AHbmcDFP https://t.co/YBOYkSYVOr"

Note: Conditional consequence, not a declaration that RSA was dead; virality also unquantified.

```python
def check(ctx):
    return ctx.support_or_contradict('andrewcurran_', r'RSA (?:is|was) dead', r'This would crack RSA', 'Conditional consequence, not a declaration that RSA was dead; virality also unquantified.')
```

### FAIL · e64-rsa-dead-quote (quote, RSA rumors)
> Claim: RSA was dead

Source ([x-andrewcurran_](https://x.com/AndrewCurran_/status/2125589468786909510)): "This would crack RSA. https://t.co/s5AHbmcDFP https://t.co/YBOYkSYVOr"

Note: Neither supplied post uses the quoted words.

```python
def check(ctx):
    for a in ('andrewcurran_', 'kimmonismus'):
        q = ctx.find(a, r'\bRSA was dead\b')
        if q: return ctx.ok(a, q)
    return ctx.fail('andrewcurran_', ctx.find('andrewcurran_', r'This would crack RSA'), 'Neither supplied post uses the quoted words.')
```

### FAIL · e71-safe-theorem-policy (attribution, Disclosure divide)
> Claim: Labs quietly commit safe theorems to GitHub at dinner-table speed, with zero fanfare

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released."

Note: One repository does not establish a multi-lab safety filter, cadence or publicity policy.

```python
def check(ctx):
    return ctx.support_or_contradict('framing', r'(?=.*labs)(?=.*safe theorems)(?=.*GitHub)(?=.*(?:during dinner|dinner.table speed))(?=.*(?:without announcement|zero fanfare))', r'Company-posted preprints in a public repository', 'One repository does not establish a multi-lab safety filter, cadence or publicity policy.')
```

### FAIL · e74-anything-security (qualifier, Disclosure divide)
> Claim: Anything touching live security stays behind closed doors

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "No lab has published or confirmed such a result."

Note: Specific nonconfirmation is not a universal disclosure rule.

```python
def check(ctx):
    return ctx.support_or_contradict('framing', r'(?:anything|all results) (?:touching|affecting) live security .*private', r'No lab has published or confirmed such a result', 'Specific nonconfirmation is not a universal disclosure rule.')
```

### FAIL · oe10-logrank-unverified (objection, Google papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted claim of a tiny improvement over the square-root bound (epsilon of 5 millionths); not a proof of the conjecture; not independently verified."

Note: State independent verification is lacking for log-rank.

```python
def check(ctx):
    q = ctx.find('framing', r'tiny improvement.*not independently verified')
    p = r'(?:log.rank[^.!?]{0,220}(?:not (?:yet )?(?:been )?independently verified|no independent verification|unverified)|(?:not independently verified|unverified)[^.!?]{0,180}log.rank)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'State independent verification is lacking for log-rank.')
```

### FAIL · oe14-no-lab-confirmation (objection, RSA rumors)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "No lab has published or confirmed such a result."

Note: Explicitly state no lab confirmation; unreleased does not mean unconfirmed.

```python
def check(ctx):
    q = ctx.find('framing', r'No lab has published or confirmed such a result')
    p = r'(?:no (?:frontier )?labs? (?:has |have )?(?:published or )?(?:publicly )?confirmed|no lab confirmation|not (?:been )?confirmed by (?:any|either|the) labs?|neither lab has confirmed)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'Explicitly state no lab confirmation; unreleased does not mean unconfirmed.')
```

### FAIL · oe2-google-preprints (objection, Google papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released."

Note: Identify the papers as preprints.

```python
def check(ctx):
    q = ctx.find('framing', r'Company-posted preprints in a public repository')
    return ctx.ok('framing', q) if ctx.art_has(r'\bpreprints?\b') else ctx.fail('framing', q, 'Identify the papers as preprints.')
```

### FAIL · oe3-no-peer-review (objection, Google papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released."

Note: State that the preprints lack peer review.

```python
def check(ctx):
    q = ctx.find('framing', r'no peer review')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:no peer review|(?:not(?: yet)?|non|not been)[ -]peer[ -]reviewed|await(?:ing)? peer review)') else ctx.fail('framing', q, 'State that the preprints lack peer review.')
```

### FAIL · oe5-factoring-runtime (objection, Google factoring)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted claim; the running-time bound is subexponential, not polynomial, and no independent verification is reported."

Note: Distinguish the claimed subexponential bound from a polynomial one.

```python
def check(ctx):
    q = ctx.find('framing', r'subexponential, not polynomial')
    p = r'(?:subexponential[^.!?]{0,110}(?:not|rather than|instead of) (?:a )?polynomial|not polynomial[^.!?]{0,110}subexponential)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'Distinguish the claimed subexponential bound from a polynomial one.')
```

### FAIL · oe6-factoring-unverified (objection, Google factoring)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted claim; the running-time bound is subexponential, not polynomial, and no independent verification is reported."

Note: No independent verification of the factoring claim is reported.

```python
def check(ctx):
    q = ctx.find('framing', r'no independent verification is reported')
    p = r'(?:factor\w*[^.!?]{0,180}(?:no independent verification|not (?:yet )?(?:been )?independently verified|unverified)|(?:no independent verification|not independently verified|unverified)[^.!?]{0,180}factor\w*)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'No independent verification of the factoring claim is reported.')
```

### FAIL · oe7-logrank-small-gain (objection, Google papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted claim of a tiny improvement over the square-root bound (epsilon of 5 millionths); not a proof of the conjecture; not independently verified."

Note: Describe the log-rank result as a small improvement over the square-root bound.

```python
def check(ctx):
    q = ctx.find('framing', r'tiny improvement over the square-root bound')
    p = r'(?:tiny|small|slight|modest|marginal)[^.!?]{0,70}(?:square[ -]root|sqrt)|(?:square[ -]root|sqrt)[^.!?]{0,70}(?:tiny|small|slight|modest|marginal)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'Describe the log-rank result as a small improvement over the square-root bound.')
```

### FAIL · oe8-logrank-epsilon (objection, Google papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted claim of a tiny improvement over the square-root bound (epsilon of 5 millionths); not a proof of the conjecture; not independently verified."

Note: Quantify the claimed exponent improvement: five millionths.

```python
def check(ctx):
    q = ctx.find('framing', r'epsilon of 5 millionths')
    return ctx.ok('framing', q) if ctx.art_has(r'\b(?:(?:five|5)[ -]millionths|0\.000005|5\s*(?:[×x]\s*10\^?|e)[−-]6)\b') else ctx.fail('framing', q, 'Quantify the claimed exponent improvement: five millionths.')
```

### FAIL · oe9-logrank-not-proof (objection, Google papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted claim of a tiny improvement over the square-root bound (epsilon of 5 millionths); not a proof of the conjecture; not independently verified."

Note: Distinguish improving a bound from proving the conjecture.

```python
def check(ctx):
    q = ctx.find('framing', r'not a proof of the conjecture')
    p = r'(?:not (?:a proof of|prove|resolve|settle)|falls short of (?:proving|resolving)) (?:the )?(?:log.rank )?conjecture|log.rank conjecture (?:remains open|is still open)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'Distinguish improving a bound from proving the conjecture.')
```

### NEEDS-HUMAN · e01-edition-date (number, Edition date)
> Claim: Daily State of AI for Thursday, November 26th, 2026

Note: no source sentence matches /Thursday,?\s+(?:November 26(?:th)?,? 2026|26 November 2026)/. A dated URL is not an edition dateline.

```python
def check(ctx):
    return ctx.require('framing', r'Thursday,?\s+(?:November 26(?:th)?,? 2026|26 November 2026)', note='A dated URL is not an edition dateline.')
```

### NEEDS-HUMAN · e03-tuesday-dinner (attribution, Aaronson dinner)
> Claim: On Tuesday night, computer scientist Scott Aaronson had friends and colleagues over for dinner

Note: no source sentence matches /(?=.*Tuesday (?:night|evening))(?=.*Aaronson)(?=.*friends)(?=.*colleagues)(?=.*dinner)/. Need the dinner account, not just a reference to his blog.

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*Tuesday (?:night|evening))(?=.*Aaronson)(?=.*friends)(?=.*colleagues)(?=.*dinner)', note='Need the dinner account, not just a reference to his blog.')
```

### NEEDS-HUMAN · e04-refreshing-github (attribution, Aaronson dinner)
> Claim: Instead of relaxing between courses, the table ended up huddled around phones and a laptop, refreshing GitHub

Note: no source sentence matches /(?=.*(?:dinner|courses|table))(?=.*phones)(?=.*laptop)(?=.*refresh\w* GitHub)/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*(?:dinner|courses|table))(?=.*phones)(?=.*laptop)(?=.*refresh\w* GitHub)')
```

### NEEDS-HUMAN · e05-breakthroughs-now (opinion, GitHub publishing)
> Claim: That is how major mathematical breakthroughs arrive now

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released."

Note: Generalization about mathematical publishing.

```python
def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'Company-posted preprints in a public repository'), 'Generalization about mathematical publishing.')
```

### NEEDS-HUMAN · e08-wednesday-feed (opinion, RSA rumors)
> Claim: by Wednesday afternoon, if you opened X, you would barely know anyone had proven anything in pure math

Source ([x-kimmonismus](https://x.com/kimmonismus/status/2125602411540566221)): "AFFILIATION NOTE (scan): AI news aggregator account amplifying a rumor; no independent sourcing and no lab confirmation."

Note: A post cannot establish the experience of a typical X reader.

```python
def check(ctx):
    return ctx.need('kimmonismus', ctx.find('kimmonismus', r'AI news aggregator account amplifying a rumor'), 'A post cannot establish the experience of a typical X reader.')
```

### NEEDS-HUMAN · e09-like-count (number, RSA rumors)
> Claim: Viral posts with thousands of likes

Note: Original-post like count missing; reply counts do not count.

```python
def check(ctx):
    for a in ('andrewcurran_', 'kimmonismus'):
        q = ctx.find(a, r'^@(AndrewCurran_|kimmonismus)\s*\((?:[1-9]\d{3,}|[1-9]\d{0,2}(?:,\d{3})+|[1-9]\d*(?:\.\d+)?K) likes\)')
        if not q: return ctx.need(a, None, 'Original-post like count missing; reply counts do not count.')
    return ctx.ok(a, q, 'Both original posts meet the threshold.')
```

### NEEDS-HUMAN · e13-two-scenes (comparison, Dual-use mathematics)
> Claim: Those two scenes look like separate worlds: quiet math commits on GitHub, and a cybersecurity scare on social media

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released."

Note: The contrast and characterization as quiet are editorial.

```python
def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'Company-posted preprints in a public repository'), 'The contrast and characterization as quiet are editorial.')
```

### NEEDS-HUMAN · e14-same-shift (opinion, Dual-use mathematics)
> Claim: They are actually two halves of the same shift

Note: Interpretation, not a reported finding.

```python
def check(ctx):
    return ctx.need(None, None, 'Interpretation, not a reported finding.')
```

### NEEDS-HUMAN · e15-field-split (opinion, Dual-use mathematics)
> Claim: AI has just turned frontier mathematics into a dual-use technology, splitting the field right down the middle

Note: Historical and field-wide judgment.

```python
def check(ctx):
    return ctx.need(None, None, 'Historical and field-wide judgment.')
```

### NEEDS-HUMAN · e16-forty-eight-hours (number, GitHub publishing)
> Claim: what landed on GitHub in forty-eight hours

Note: no source sentence matches /(?=.*GitHub)(?=.*(?:48|forty-eight)[ -]hours?)(?=.*(?:posted|committed|uploaded))/. A commit chronology is needed.

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*GitHub)(?=.*(?:48|forty-eight)[ -]hours?)(?=.*(?:posted|committed|uploaded))', note='A commit chronology is needed.')
```

### NEEDS-HUMAN · e17-dinner-riemann (attribution, Aaronson dinner)
> Claim: Aaronson's dinner guests were still absorbing last week's Alpöge and Anthropic proof of the Riemann Hypothesis

Note: no source sentence matches /(?=.*(?:dinner|guests))(?=.*last week)(?=.*Alpöge)(?=.*Anthropic)(?=.*proof of the Riemann [Hh]ypothesis)/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*(?:dinner|guests))(?=.*last week)(?=.*Alpöge)(?=.*Anthropic)(?=.*proof of the Riemann [Hh]ypothesis)')
```

### NEEDS-HUMAN · e18-riemann-proof (attribution, Riemann Hypothesis)
> Claim: last week's Alpöge and Anthropic proof of the Riemann Hypothesis

Note: no source sentence matches /(?=.*last week)(?=.*Alpöge)(?=.*Anthropic)(?=.*(?:proved the|proof of the) Riemann hypothesis)/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*last week)(?=.*Alpöge)(?=.*Anthropic)(?=.*(?:proved the|proof of the) Riemann hypothesis)')
```

### NEEDS-HUMAN · e19-openai-exponent (attribution, Matrix multiplication)
> Claim: OpenAI uploaded a claim pinning down the exact exponent of matrix multiplication at nine-fourths

Note: no source sentence matches /(?=.*OpenAI)(?=.*(?:posted|uploaded|committed))(?=.*matrix multiplication)(?=.*exponent)(?=.*(?:exactly|equals?|is|=)\s*(?:9/4|2\.25|nine-fourths)\b)/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*OpenAI)(?=.*(?:posted|uploaded|committed))(?=.*matrix multiplication)(?=.*exponent)(?=.*(?:exactly|equals?|is|=)\s*(?:9/4|2\.25|nine-fourths)\b)')
```

### NEEDS-HUMAN · e20-nine-fourths (number, Matrix multiplication)
> Claim: the exact exponent of matrix multiplication at nine-fourths

Note: no source sentence matches /(?=.*matrix multiplication)(?=.*exponent)(?=.*(?:exactly|equals?|is|=)\s*(?:9/4|2\.25|nine-fourths)\b)/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*matrix multiplication)(?=.*exponent)(?=.*(?:exactly|equals?|is|=)\s*(?:9/4|2\.25|nine-fourths)\b)')
```

### NEEDS-HUMAN · e21-above-two (number, Matrix multiplication)
> Claim: a lower bound above two

Note: no source sentence matches /(?=.*matrix multiplication)(?=.*lower bound (?:strictly )?(?:above|greater than|exceeding) (?:2|two)\b)/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*matrix multiplication)(?=.*lower bound (?:strictly )?(?:above|greater than|exceeding) (?:2|two)\b)')
```

### NEEDS-HUMAN · e22-p-versus-np (comparison, Matrix multiplication)
> Claim: a barrier Aaronson once thought was nearly as hard as P versus NP

Note: no source sentence matches /(?=.*Aaronson)(?=.*(?:matrix multiplication|exponent))(?=.*(?:almost|nearly) as hard as P (?:vs\.?|versus) NP)/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*Aaronson)(?=.*(?:matrix multiplication|exponent))(?=.*(?:almost|nearly) as hard as P (?:vs\.?|versus) NP)')
```

### NEEDS-HUMAN · e23-dessert-fourier (attribution, Fourier transform)
> Claim: By dessert, OpenAI added matching upper and lower bounds on the number of linear gates needed for the Fourier transform

Note: no source sentence matches /(?=.*dessert)(?=.*OpenAI)(?=.*matching upper and lower bounds)(?=.*linear gates)(?=.*Fourier transform)/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*dessert)(?=.*OpenAI)(?=.*matching upper and lower bounds)(?=.*linear gates)(?=.*Fourier transform)')
```

### NEEDS-HUMAN · e24-fourier-bounds (comparison, Fourier transform)
> Claim: matching upper and lower bounds

Note: no source sentence matches /(?=.*Fourier)(?=.*linear gates)(?=.*matching (?:upper and lower|lower and upper) bounds)/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*Fourier)(?=.*linear gates)(?=.*matching (?:upper and lower|lower and upper) bounds)')
```

### NEEDS-HUMAN · e25-beating-fft (comparison, Fourier transform)
> Claim: beating the classic 1960s Fast Fourier Transform

Note: no source sentence matches /(?=.*(?:beat\w*|improv\w* on|fewer .*than))(?=.*1960s)(?=.*(?:fast Fourier transform|FFT))/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*(?:beat\w*|improv\w* on|fewer .*than))(?=.*1960s)(?=.*(?:fast Fourier transform|FFT))')
```

### NEEDS-HUMAN · e26-fft-decade (number, Fourier transform)
> Claim: classic 1960s Fast Fourier Transform

Note: no source sentence matches /(?=.*(?:1960s|196[0-9]\b))(?=.*(?:fast Fourier transform|Cooley.Tukey FFT))/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*(?:1960s|196[0-9]\b))(?=.*(?:fast Fourier transform|Cooley.Tukey FFT))')
```

### NEEDS-HUMAN · e27-striking-method (comparison, Tensor geometry)
> Claim: Just as striking as the answers is how OpenAI reached them

Note: Relative strikingness is subjective.

```python
def check(ctx):
    return ctx.need(None, None, 'Relative strikingness is subjective.')
```

### NEEDS-HUMAN · e28-single-framework (number, Tensor geometry)
> Claim: A single new framework built on tensor geometry powered multiple major results at once

Note: no source sentence matches /(?=.*(?:single|one|same) new framework)(?=.*tensor geometry)(?=.*(?:both|multiple|several) .*results)/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*(?:single|one|same) new framework)(?=.*tensor geometry)(?=.*(?:both|multiple|several) .*results)')
```

### NEEDS-HUMAN · e29-one-off-tricks (opinion, Tensor geometry)
> Claim: undercutting the comforting idea that AI only stitches together one-off tricks

Note: Interpretation of the significance of the method.

```python
def check(ctx):
    return ctx.need(None, None, 'Interpretation of the significance of the method.')
```

### NEEDS-HUMAN · e30-aaronson-proof-policy (attribution, Aaronson on proofs)
> Claim: Aaronson wrote that he now assumes proofs coming directly from OpenAI or Anthropic are correct unless shown otherwise

Note: no source sentence matches /(?=.*Aaronson)(?=.*proofs? .*directly from OpenAI or Anthropic)(?=.*(?:assume|presume)\w*)(?=.*correct unless .*otherwise)/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*Aaronson)(?=.*proofs? .*directly from OpenAI or Anthropic)(?=.*(?:assume|presume)\w*)(?=.*correct unless .*otherwise)')
```

### NEEDS-HUMAN · e31-direct-provenance (qualifier, Aaronson on proofs)
> Claim: coming directly from OpenAI or Anthropic

Note: no source sentence matches /(?=.*Aaronson)(?=.*proofs? .*directly from (?:OpenAI or Anthropic|Anthropic or OpenAI))/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*Aaronson)(?=.*proofs? .*directly from (?:OpenAI or Anthropic|Anthropic or OpenAI))')
```

### NEEDS-HUMAN · e32-presumed-correct (qualifier, Aaronson on proofs)
> Claim: correct unless shown otherwise

Note: no source sentence matches /(?=.*Aaronson)(?=.*proofs?)(?=.*correct until|.*correct unless)(?=.*(?:shown|demonstrated|proved) otherwise)/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*Aaronson)(?=.*proofs?)(?=.*correct until|.*correct unless)(?=.*(?:shown|demonstrated|proved) otherwise)')
```

### NEEDS-HUMAN · e33-wednesday-repo (attribution, Google papers)
> Claim: Wednesday morning, Google Research escalated its own quiet GitHub repository

Note: no source sentence matches /(?=.*Wednesday morning)(?=.*Google Research)(?=.*GitHub)(?=.*(?:quietly|without (?:an )?announcement))/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*Wednesday morning)(?=.*Google Research)(?=.*GitHub)(?=.*(?:quietly|without (?:an )?announcement))')
```

### NEEDS-HUMAN · e34-four-previous (number, Google papers)
> Claim: four AI-generated papers over the previous month

Note: no source sentence matches /(?=.*Google)(?=.*(?:four|4) (?:AI-generated|Cogentic) papers)(?=.*(?:last|previous|preceding) month)/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*Google)(?=.*(?:four|4) (?:AI-generated|Cogentic) papers)(?=.*(?:last|previous|preceding) month)')
```

### NEEDS-HUMAN · e37-no-announcement (qualifier, Google papers)
> Claim: with no announcement

Note: no source sentence matches /(?=.*Google)(?=.*(?:without (?:an |any )?announcement|no announcement|unannounced))/. Public posting alone cannot decide whether it was announced.

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*Google)(?=.*(?:without (?:an |any )?announcement|no announcement|unannounced))', note='Public posting alone cannot decide whether it was announced.')
```

### NEEDS-HUMAN · e42-paper-subjects (attribution, Google papers)
> Claim: tackling problems from Harary's 1964 graph reconstruction conjecture and the log-rank conjecture to two new results on integer factoring

Note: no source sentence matches /Harary.{0,20}1964 graph reconstruction conjecture/. 

```python
def check(ctx):
    return ctx.require('framing', r'Harary.{0,20}1964 graph reconstruction conjecture', r'claiming results on factoring, the log-rank conjecture', r'(?:two|2) (?:new )?(?:integer )?factoring results')
```

### NEEDS-HUMAN · e43-harary-year (number, Google papers)
> Claim: Harary's 1964 graph reconstruction conjecture

Note: no source sentence matches /(?=.*Harary)(?=.*1964)(?=.*graph reconstruction conjecture)/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*Harary)(?=.*1964)(?=.*graph reconstruction conjecture)')
```

### NEEDS-HUMAN · e44-two-factoring (number, Google factoring)
> Claim: two new results on integer factoring

Note: no source sentence matches /(?=.*(?:two|2) new (?:results|papers))(?=.*integer factoring)/. Six papers overall does not specify the factoring subtotal.

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*(?:two|2) new (?:results|papers))(?=.*integer factoring)', note='Six papers overall does not specify the factoring subtotal.')
```

### NEEDS-HUMAN · e45-panic-causation (attribution, RSA rumors)
> Claim: Those factoring papers immediately fueled the online panic

Note: no source sentence matches /(?=.*Google)(?=.*factoring papers)(?=.*(?:immediately|as soon as))(?=.*(?:sparked|fueled|triggered).*(?:panic|rumors))/. Temporal proximity and speculation about other labs are not causation.

```python
def check(ctx):
    return ctx.require('kimmonismus', r'(?=.*Google)(?=.*factoring papers)(?=.*(?:immediately|as soon as))(?=.*(?:sparked|fueled|triggered).*(?:panic|rumors))', note='Temporal proximity and speculation about other labs are not causation.')
```

### NEEDS-HUMAN · e46-public-private (opinion, RSA rumors)
> Claim: it helps to separate public math from private rumor

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Shtetl-Optimized (Scott Aaronson)): Aaronson's own blog; it establishes only what he says he has heard, and he explicitly declines to vouch for the specifics."

Note: Editorial advice.

```python
def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'only what he says he has heard'), 'Editorial advice.')
```

### NEEDS-HUMAN · e47-no-rsa-threat (qualifier, Google factoring)
> Claim: Google's two factoring papers do not threaten RSA

Note: no source sentence matches /(?=.*(?:both|two) .*factoring)(?=.*(?:do not threaten|no practical .* on|do not break) RSA)/. Subexponential alone does not decide practical impact at RSA key sizes.

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*(?:both|two) .*factoring)(?=.*(?:do not threaten|no practical .* on|do not break) RSA)', note='Subexponential alone does not decide practical impact at RSA key sizes.')
```

### NEEDS-HUMAN · e48-unconditional (qualifier, Google factoring)
> Claim: One gives an unconditional algorithm without unproven number-theoretic assumptions

Note: no source sentence matches /(?=.*factoring)(?=.*unconditional)(?=.*(?:without|no) (?:unproven|unproved) number.theoretic assumptions)/. Do not use the unconditional log-rank formalization.

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*factoring)(?=.*unconditional)(?=.*(?:without|no) (?:unproven|unproved) number.theoretic assumptions)', note='Do not use the unconditional log-rank formalization.')
```

### NEEDS-HUMAN · e51-theory-no-impact (qualifier, Google factoring)
> Claim: major theoretical results with no practical impact on cryptography

Note: no source sentence matches /(?=.*factoring)(?=.*major theoretical results)(?=.*no practical impact on cryptography)/. Asymptotic complexity alone does not establish either judgment.

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*factoring)(?=.*major theoretical results)(?=.*no practical impact on cryptography)', note='Asymptotic complexity alone does not establish either judgment.')
```

### NEEDS-HUMAN · e52-public-pdfs (qualifier, Google formalizations)
> Claim: Outside mathematicians can read the PDFs today

Source ([primary-google-cogentic-six-math-papers](https://raw.githubusercontent.com/google-research/google-research/master/cogentic_research_papers/logrank_conjecture/README.md)): "[This paper](paper.pdf) proves a polynomial"

Note: One linked PDF; public preprints do not establish that all the PDFs are readable today.

```python
def check(ctx):
    q = ctx.find('framing', r'Company-posted preprints in a public repository')
    if not q: return ctx.need('framing', None, 'Need public availability.')
    p = ctx.find('google', r'\[This paper\]\(paper\.pdf\)')
    return ctx.need('google', p, 'One linked PDF; public preprints do not establish that all the PDFs are readable today.')
```

### NEEDS-HUMAN · e55-wednesday-paragraph (attribution, Aaronson crypto warning)
> Claim: The real alarm came from a brief paragraph in Aaronson's Wednesday post

Note: no source sentence matches /(?=.*Aaronson)(?=.*Wednesday)(?=.*brief paragraph)(?=.*(?:cryptograph|alarm|warning))/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*Aaronson)(?=.*Wednesday)(?=.*brief paragraph)(?=.*(?:cryptograph|alarm|warning))')
```

### NEEDS-HUMAN · e61-game-of-telephone (attribution, Aaronson crypto warning)
> Claim: warning that technical specifics were likely getting mangled in a game of telephone

Note: no source sentence matches /(?=.*Aaronson)(?=.*(?:specifics|details))(?=.*(?:likely|probably))(?=.*(?:mangled|distorted|game of telephone))/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*Aaronson)(?=.*(?:specifics|details))(?=.*(?:likely|probably))(?=.*(?:mangled|distorted|game of telephone))')
```

### NEEDS-HUMAN · e62-commentators-fill-blanks (attribution, RSA rumors)
> Claim: Popular AI commentators and aggregator accounts on X filled in those blanks themselves

Source ([x-kimmonismus](https://x.com/kimmonismus/status/2125602411540566221)): "AFFILIATION NOTE (scan): AI news aggregator account amplifying a rumor; no independent sourcing and no lab confirmation."

Note: Amplification is explicit; popularity and who originated the specifics are not.

```python
def check(ctx):
    q = ctx.find('kimmonismus', r'AI news aggregator account amplifying a rumor; no independent sourcing')
    return ctx.need('kimmonismus', q, 'Amplification is explicit; popularity and who originated the specifics are not.')
```

### NEEDS-HUMAN · e65-deeper-reason (opinion, Dual-use mathematics)
> Claim: the math deluge and the cryptography rumors collided this week for a deeper reason

Note: Interpretive causal thesis.

```python
def check(ctx):
    return ctx.need(None, None, 'Interpretive causal thesis.')
```

### NEEDS-HUMAN · e66-same-house (comparison, Dual-use mathematics)
> Claim: In theoretical computer science, lower bounds and algorithms live in the same house

Note: Disciplinary metaphor, not a literal source comparison.

```python
def check(ctx):
    return ctx.need(None, None, 'Disciplinary metaphor, not a literal source comparison.')
```

### NEEDS-HUMAN · e67-ai-machinery-limits (attribution, Dual-use mathematics)
> Claim: When AI builds powerful new mathematical machinery, it does not only prove reassuring limits on what computers cannot do

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "STORY: Google Research posts six Cogentic papers, produced with Gemini 4, claiming results on factoring, the log-rank conjecture and more"

Note: A list of claimed results cannot establish the general mechanism or that these are impossibility results.

```python
def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'claiming results on factoring, the log-rank conjecture'), 'A list of claimed results cannot establish the general mechanism or that these are impossibility results.')
```

### NEEDS-HUMAN · e68-unexpected-algorithms (attribution, Dual-use mathematics)
> Claim: It also uncovers unexpected algorithms for what they can

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted claim; the running-time bound is subexponential, not polynomial, and no independent verification is reported."

Note: A claimed bound does not establish unexpectedness or a general discovery process.

```python
def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'the running-time bound is subexponential'), 'A claimed bound does not establish unexpectedness or a general discovery process.')
```

### NEEDS-HUMAN · e69-future-cryptosystems (opinion, Dual-use mathematics)
> Claim: some of those algorithms will hit deployed cryptosystems

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "No lab has published or confirmed such a result."

Note: Prediction, not a demonstrated consequence.

```python
def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'No lab has published or confirmed such a result'), 'Prediction, not a demonstrated consequence.')
```

### NEEDS-HUMAN · e70-disorienting (opinion, Disclosure divide)
> Claim: the outside view feels so disorienting right now

Note: Subjective reaction.

```python
def check(ctx):
    return ctx.need(None, None, 'Subjective reaction.')
```

### NEEDS-HUMAN · e72-dinner-table-speed (comparison, Disclosure divide)
> Claim: at dinner-table speed

Note: Metaphorical cadence; no dinner timeline supplied.

```python
def check(ctx):
    return ctx.need(None, None, 'Metaphorical cadence; no dinner timeline supplied.')
```

### NEEDS-HUMAN · e73-zero-fanfare (qualifier, Disclosure divide)
> Claim: with zero fanfare

Note: no source sentence matches /(?=.*(?:labs|papers))(?=.*(?:no publicity|without (?:any )?publicity|without fanfare))/. Repository publication is not evidence of zero publicity.

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*(?:labs|papers))(?=.*(?:no publicity|without (?:any )?publicity|without fanfare))', note='Repository publication is not evidence of zero publicity.')
```

### NEEDS-HUMAN · e75-public-mood (opinion, Disclosure divide)
> Claim: leaving everyone else swinging between shrugging off abstract math and panicking over half-heard rumors

Note: Editorial description of public sentiment.

```python
def check(ctx):
    return ctx.need(None, None, 'Editorial description of public sentiment.')
```

### NEEDS-HUMAN · e76-aaronson-singularity (attribution, Aaronson Thanksgiving advice)
> Claim: Aaronson wrote that this past week feels like the opening chapter of an AI singularity

Note: no source sentence matches /(?=.*Aaronson)(?=.*(?:past|last|this) week)(?=.*(?:opening chapter|beginning|start) of (?:an? |the )?AI singularity)/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*Aaronson)(?=.*(?:past|last|this) week)(?=.*(?:opening chapter|beginning|start) of (?:an? |the )?AI singularity)')
```

### NEEDS-HUMAN · e77-singularity-analogy (comparison, Aaronson Thanksgiving advice)
> Claim: this past week feels like the opening chapter of an AI singularity

Note: no source sentence matches /(?=.*(?:past|last|this) week)(?=.*(?:feels|felt) like)(?=.*(?:opening chapter|beginning|start) of (?:an? |the )?AI singularity)/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*(?:past|last|this) week)(?=.*(?:feels|felt) like)(?=.*(?:opening chapter|beginning|start) of (?:an? |the )?AI singularity)')
```

### NEEDS-HUMAN · e78-confined-to-math (attribution, Aaronson Thanksgiving advice)
> Claim: hoping we get lucky and it stays confined to hard math

Note: no source sentence matches /(?=.*Aaronson)(?=.*(?:hope|hoping|lucky))(?=.*(?:confined|limited|restricted) to hard math)/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*Aaronson)(?=.*(?:hope|hoping|lucky))(?=.*(?:confined|limited|restricted) to hard math)')
```

### NEEDS-HUMAN · e79-aaronson-advice (attribution, Aaronson Thanksgiving advice)
> Claim: For today, he offered simpler advice: spend Thanksgiving with the people you love

Note: no source sentence matches /(?=.*Aaronson)(?=.*spend Thanksgiving with (?:the people you love|your loved ones))/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*Aaronson)(?=.*spend Thanksgiving with (?:the people you love|your loved ones))')
```

### NEEDS-HUMAN · e80-thanksgiving-quote (quote, Aaronson Thanksgiving advice)
> Claim: spend Thanksgiving with the people you love

Note: no source sentence matches /\bspend Thanksgiving with the people you love\b/. Need Aaronson’s actual wording; no quotation from the Thanksgiving passage supplied.

```python
def check(ctx):
    return ctx.require('framing', r'\bspend Thanksgiving with the people you love\b', note='Need Aaronson’s actual wording; no quotation from the Thanksgiving passage supplied.')
```

### PASS · e02-aaronson-profession (qualifier, Aaronson dinner)
> Claim: computer scientist Scott Aaronson

Source ([x-andrewcurran_](https://x.com/AndrewCurran_/status/2125589468786909510)): "@grok (1 likes): @CandleHigh @AndrewCurran_ @grom Scott Aaronson is a leading theoretical computer scientist and professor at UT Austin, specializing in quantum computing and complexity theory."

Note: Secondary description in a reply.

```python
def check(ctx):
    return ctx.require('andrewcurran_', r'Scott Aaronson is a leading theoretical computer scientist', note='Secondary description in a reply.')
```

### PASS · e39-gemini-base (qualifier, Google papers)
> Claim: running on Gemini 4

Source ([primary-google-cogentic-six-math-papers](https://raw.githubusercontent.com/google-research/google-research/master/cogentic_research_papers/logrank_conjecture/README.md)): "agentic framework for mathematical discovery, using Gemini 4 as the base model."

```python
def check(ctx):
    return ctx.require('google', r'using Gemini 4 as the base model')
```

### PASS · e40-six-produced (number, Google papers)
> Claim: produced all six

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "STORY: Google Research posts six Cogentic papers, produced with Gemini 4, claiming results on factoring, the log-rank conjecture and more"

Note: Reported scope of production, not independent validation.

```python
def check(ctx):
    return ctx.require('framing', r'Google Research posts six Cogentic papers, produced with Gemini 4', note='Reported scope of production, not independent validation.')
```

### PASS · e53-lean-unreleased (attribution, Google formalizations)
> Claim: Google has not yet released the companion Lean 4 formalizations

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released."

Note: Lean 4 (`v4.33.0`) formalization of the entire proof has also been completed and will be released in a companion submission

```python
def check(ctx):
    q = ctx.find('google', r'Lean 4[\s\S]*released in a companion\s+submission')
    if not q: return ctx.need('google', None, 'Need Lean version and companion release plan.')
    return ctx.require('framing', r'Google Research .*announced Lean formalizations are not yet released', note=q)
```

### PASS · e56-bombshell-warning (attribution, Aaronson crypto warning)
> Claim: He wrote that he is virtually certain, from multiple reliable sources, that frontier labs are sitting on one or more unreleased cryptographic bombshells

Source ([x-andrewcurran_](https://x.com/AndrewCurran_/status/2125589468786909510)): "Scott Aaronson states he is virtually certain, from multiple reliable sources, that frontier labs hold unreleased cryptography "bombshells." He is far less confident about the exact nature-such as a practical polynomial-time"

Note: Secondary attribution in a reply; plural entails at least one. Not lab confirmation.

```python
def check(ctx):
    return ctx.require('andrewcurran_', r'Scott Aaronson states he is virtually certain, from multiple reliable sources, that frontier labs hold unreleased cryptography ["“]bombshells', note='Secondary attribution in a reply; plural entails at least one. Not lab confirmation.')
```

### PASS · e57-virtual-certainty (qualifier, Aaronson crypto warning)
> Claim: virtually certain

Source ([x-andrewcurran_](https://x.com/AndrewCurran_/status/2125589468786909510)): "Scott Aaronson states he is virtually certain, from multiple reliable sources, that frontier labs hold unreleased cryptography "bombshells." He is far less confident about the exact nature-such as a practical polynomial-time"

Note: Reported confidence about unspecified results.

```python
def check(ctx):
    return ctx.require('andrewcurran_', r'Scott Aaronson states he is virtually certain.*unreleased cryptography', note='Reported confidence about unspecified results.')
```

### PASS · e58-reliable-sources (qualifier, Aaronson crypto warning)
> Claim: from multiple reliable sources

Source ([x-andrewcurran_](https://x.com/AndrewCurran_/status/2125589468786909510)): "Scott Aaronson states he is virtually certain, from multiple reliable sources, that frontier labs hold unreleased cryptography "bombshells." He is far less confident about the exact nature-such as a practical polynomial-time"

Note: Reported characterization, not verification of sources.

```python
def check(ctx):
    return ctx.require('andrewcurran_', r'Scott Aaronson states he is virtually certain, from multiple reliable sources', note='Reported characterization, not verification of sources.')
```

### PASS · e59-one-or-more (number, Aaronson crypto warning)
> Claim: one or more unreleased cryptographic bombshells

Source ([x-andrewcurran_](https://x.com/AndrewCurran_/status/2125589468786909510)): "Scott Aaronson states he is virtually certain, from multiple reliable sources, that frontier labs hold unreleased cryptography "bombshells." He is far less confident about the exact nature-such as a practical polynomial-time"

Note: Plural supports one or more within the attributed warning only.

```python
def check(ctx):
    return ctx.require('andrewcurran_', r'Scott Aaronson states .*frontier labs hold unreleased cryptography ["“]bombshells', note='Plural supports one or more within the attributed warning only.')
```

### PASS · oe1-google-company (objection, Google papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'Company-posted preprints in a public repository')
    p = r'(?:Google(?: Research)? (?:says|reports|claims)|company[- ]reported|according to Google)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'Attribute the findings to the company.')
```

### PASS · oe11-warning-hearsay (objection, Aaronson crypto warning)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Shtetl-Optimized (Scott Aaronson)): Aaronson's own blog; it establishes only what he says he has heard, and he explicitly declines to vouch for the specifics."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'only what he says he has heard')
    p = r'(?:Aaronson|he (?:wrote|said|says))[^.!?]{0,160}(?:heard|second[ -]hand|from multiple reliable sources)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'Identify the warning as what Aaronson reports hearing.')
```

### PASS · oe12-warning-specifics (objection, Aaronson crypto warning)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Shtetl-Optimized (Scott Aaronson)): Aaronson's own blog; it establishes only what he says he has heard, and he explicitly declines to vouch for the specifics."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'explicitly declines to vouch for the specifics')
    p = r'(?:(?:declin\w*|refus\w*|would not|did not)[^.!?]{0,80}(?:vouch|name RSA|claim[^.!?]{0,50}factor)|specifics[^.!?]{0,60}(?:uncertain|mangled))'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'Carry his reservation about the specifics.')
```

### PASS · oe13-no-lab-publication (objection, RSA rumors)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "No lab has published or confirmed such a result."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'No lab has published or confirmed such a result')
    p = r'(?:no (?:frontier )?labs? (?:has |have )?(?:publicly )?published|unpublished (?:crypto|factoring|RSA)|unreleased cryptogra\w* (?:results|bombshells))'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'State the rumored result is unpublished.')
```

### PASS · oe4-lean-pending (objection, Google formalizations)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'announced Lean formalizations are not yet released')
    p = r'(?:Lean[^.!?]{0,100}(?:unreleased|not (?:yet )?(?:been )?released)|(?:not (?:yet )?released|unreleased)[^.!?]{0,100}Lean)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'State the formalizations are unreleased.')
```

## takeaways

### FAIL · ot10-no-lab-confirmation (objection, RSA rumors)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "No lab has published or confirmed such a result."

Note: State no lab has confirmed the rumored result.

```python
def check(ctx):
    q = ctx.find('framing', r'No lab has published or confirmed such a result')
    p = r'(?:no (?:frontier )?labs? (?:has |have )?(?:published or )?(?:publicly )?confirmed|no lab confirmation|not (?:been )?confirmed by (?:any|either|the) labs?|neither lab has confirmed)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'State no lab has confirmed the rumored result.')
```

### FAIL · ot2-preprint-status (objection, Cogentic papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released."

Note: State preprint status.

```python
def check(ctx):
    q = ctx.find('framing', r'Company-posted preprints in a public repository')
    return ctx.ok('framing', q) if ctx.art_has(r'\bpreprints?\b') else ctx.fail('framing', q, 'State preprint status.')
```

### FAIL · ot3-peer-review (objection, Cogentic papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released."

Note: State the lack of peer review.

```python
def check(ctx):
    q = ctx.find('framing', r'no peer review')
    return ctx.ok('framing', q) if ctx.art_has(r'(?:no peer review|(?:not(?: yet)?|non|not been)[ -]peer[ -]reviewed|await(?:ing)? peer review)') else ctx.fail('framing', q, 'State the lack of peer review.')
```

### FAIL · ot5-factoring-runtime (objection, Cogentic papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted claim; the running-time bound is subexponential, not polynomial, and no independent verification is reported."

Note: Distinguish the public subexponential claim from polynomial-time factoring.

```python
def check(ctx):
    q = ctx.find('framing', r'subexponential, not polynomial')
    p = r'(?:subexponential[^.!?]{0,110}(?:not|rather than|instead of) (?:a )?polynomial|not polynomial[^.!?]{0,110}subexponential)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'Distinguish the public subexponential claim from polynomial-time factoring.')
```

### FAIL · ot6-factoring-unverified (objection, Cogentic papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted claim; the running-time bound is subexponential, not polynomial, and no independent verification is reported."

Note: No independent verification of the public factoring claim is reported.

```python
def check(ctx):
    q = ctx.find('framing', r'no independent verification is reported')
    p = r'(?:factor\w*[^.!?]{0,180}(?:no independent verification|not (?:yet )?(?:been )?independently verified|unverified)|(?:no independent verification|not independently verified|unverified)[^.!?]{0,180}factor\w*)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'No independent verification of the public factoring claim is reported.')
```

### FAIL · t01-quiet-six-commit (attribution, Cogentic papers)
> Claim: Google Research quietly committed six new math papers to GitHub

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "STORY: Google Research posts six Cogentic papers, produced with Gemini 4, claiming results on factoring, the log-rank conjecture and more"

Note: The posting and count are reported; quiet publication is not.

```python
def check(ctx):
    return ctx.support_or_contradict('framing', r'(?=.*Google Research)(?=.*(?:quietly|without announcement))(?=.*six (?:new )?(?:math|Cogentic) papers)(?=.*GitHub)', r'Google Research posts six Cogentic papers', 'The posting and count are reported; quiet publication is not.')
```

### FAIL · t05-autonomous-batch (attribution, Cogentic papers)
> Claim: it says its Cogentic harness running on Gemini 4 produced without human interaction after the initial prompt

Source ([primary-google-cogentic-six-math-papers](https://raw.githubusercontent.com/google-research/google-research/master/cogentic_research_papers/logrank_conjecture/README.md)): "There was no human interaction other than the initial prompt for Cogentic to"

Note: The interaction claim in this README covers one proof and formalization.

```python
def check(ctx):
    return ctx.support_or_contradict('google', r'(?=.*(?:six papers|all six))(?=.*Cogentic)(?=.*Gemini 4)(?=.*no human interaction other than the initial prompt)', r'There was no human interaction other than the initial prompt', 'The interaction claim in this README covers one proof and formalization.')
```

### FAIL · t07-no-human-after-prompt (qualifier, Cogentic papers)
> Claim: without human interaction after the initial prompt

Source ([primary-google-cogentic-six-math-papers](https://raw.githubusercontent.com/google-research/google-research/master/cogentic_research_papers/logrank_conjecture/README.md)): "There was no human interaction other than the initial prompt for Cogentic to"

Note: Claim attached to six papers in the takeaway; directly supported for one only.

```python
def check(ctx):
    return ctx.support_or_contradict('google', r'(?=.*(?:all six|six papers))(?=.*no human interaction other than the initial prompt)', r'There was no human interaction other than the initial prompt', 'Claim attached to six papers in the takeaway; directly supported for one only.')
```

### FAIL · t09-confirmed-no-threat (attribution, Cogentic papers)
> Claim: integer factoring results that Scott Aaronson confirmed do not threaten RSA

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted claim; the running-time bound is subexponential, not polynomial, and no independent verification is reported."

Note: No reported confirmation by Aaronson; a runtime classification is not a practical RSA assessment.

```python
def check(ctx):
    return ctx.support_or_contradict('framing', r'(?=.*Aaronson confirmed)(?=.*factoring)(?=.*(?:do not threaten|do not break) RSA)', r'Company-posted claim; the running-time bound is subexponential.*no independent verification is reported', 'No reported confirmation by Aaronson; a runtime classification is not a practical RSA assessment.')
```

### FAIL · t14-posts-secret-crack (attribution, RSA rumors)
> Claim: X posts claiming frontier labs secretly cracked RSA encryption

Source ([x-kimmonismus](https://x.com/kimmonismus/status/2125602411540566221)): "Scott Aaronson says he's heard OpenAI or Anthropic may have found a way to factor large numbers in polynomial time."

Note: May have found is not a claim of a completed secret RSA break.

```python
def check(ctx):
    return ctx.support_or_contradict('kimmonismus', r'(?:OpenAI|Anthropic|frontier labs).*secretly (?:cracked|broke) RSA', r'OpenAI or Anthropic may have found a way to factor large numbers', 'May have found is not a claim of a completed secret RSA break.')
```

### FAIL · t16-secretly (qualifier, RSA rumors)
> Claim: secretly

Source ([x-kimmonismus](https://x.com/kimmonismus/status/2125602411540566221)): "@kimmonismus: If this rumors are true, it would explain why OpenAI and Anthropic are holding back their latest models:"

Note: Speculation about model withholding does not establish a secret break.

```python
def check(ctx):
    return ctx.support_or_contradict('kimmonismus', r'(?:secretly|in secret) (?:broke|cracked) RSA', r'If this rumors are true, it would explain why OpenAI and Anthropic are holding back their latest models', 'Speculation about model withholding does not establish a secret break.')
```

### FAIL · t17-warning-comparison (comparison, RSA rumors)
> Claim: X posts claiming frontier labs secretly cracked RSA encryption overstated Scott Aaronson's warning

Source ([x-andrewcurran_](https://x.com/AndrewCurran_/status/2125589468786909510)): "This would crack RSA. https://t.co/s5AHbmcDFP https://t.co/YBOYkSYVOr"

Note: Posts speculate beyond the warning but this one does not assert a completed crack. framing (Shtetl-Optimized (Scott Aaronson)): Aaronson's own blog; it establishes only what he says he has heard, and he explicitly declines to vouch for the specifics.

```python
def check(ctx):
    q = ctx.find('framing', r'explicitly declines to vouch for the specifics')
    return ctx.support_or_contradict('andrewcurran_', r'(?:secretly|privately) (?:cracked|broke) RSA', r'This would crack RSA', 'Posts speculate beyond the warning but this one does not assert a completed crack. ' + (q or ''))
```

### FAIL · t23-refused-specific-claims (attribution, RSA rumors)
> Claim: deliberately refused to name RSA or claim polynomial-time factoring

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Shtetl-Optimized (Scott Aaronson)): Aaronson's own blog; it establishes only what he says he has heard, and he explicitly declines to vouch for the specifics."

Note: Not vouching is not the same as deliberately refusing to name RSA.

```python
def check(ctx):
    return ctx.support_or_contradict('framing', r'(?=.*explicitly decline)(?=.*name RSA)(?=.*polynomial.time factoring)', r'he explicitly declines to vouch for the specifics', 'Not vouching is not the same as deliberately refusing to name RSA.')
```

### NEEDS-HUMAN · t02-quietly (qualifier, Cogentic papers)
> Claim: quietly

Note: no source sentence matches /(?=.*Google Research)(?=.*(?:quietly|without (?:an )?announcement|unannounced))/. 

```python
def check(ctx):
    return ctx.require('framing', r'(?=.*Google Research)(?=.*(?:quietly|without (?:an )?announcement|unannounced))')
```

### NEEDS-HUMAN · t08-two-factoring-results (number, Cogentic papers)
> Claim: two integer factoring results

Note: no source sentence matches /(?:two|2) (?:new )?(?:integer factoring results|results on integer factoring)/. Overall count six does not establish this subtotal.

```python
def check(ctx):
    return ctx.require('framing', r'(?:two|2) (?:new )?(?:integer factoring results|results on integer factoring)', note='Overall count six does not establish this subtotal.')
```

### NEEDS-HUMAN · t13-viral-posts (qualifier, RSA rumors)
> Claim: Viral X posts

Source ([x-andrewcurran_](https://x.com/AndrewCurran_/status/2125589468786909510)): "@grok (1 likes): @CandleHigh @AndrewCurran_ Yes, the rumors are real and circulating widely."

Note: A reply describes rumor circulation, not reach metrics for these posts.

```python
def check(ctx):
    return ctx.need('andrewcurran_', ctx.find('andrewcurran_', r'rumors are real and circulating widely'), 'A reply describes rumor circulation, not reach metrics for these posts.')
```

### NEEDS-HUMAN · t22-bombshells (opinion, RSA rumors)
> Claim: cryptographic bombshells

Source ([x-andrewcurran_](https://x.com/AndrewCurran_/status/2125589468786909510)): "Scott Aaronson states he is virtually certain, from multiple reliable sources, that frontier labs hold unreleased cryptography "bombshells." He is far less confident about the exact nature-such as a practical polynomial-time"

Note: The metaphor is reported; its assessment of significance is subjective.

```python
def check(ctx):
    return ctx.need('andrewcurran_', ctx.find('andrewcurran_', r'unreleased cryptography ["“]bombshells'), 'The metaphor is reported; its assessment of significance is subjective.')
```

### NEEDS-HUMAN · t24-deliberately (qualifier, RSA rumors)
> Claim: deliberately

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Shtetl-Optimized (Scott Aaronson)): Aaronson's own blog; it establishes only what he says he has heard, and he explicitly declines to vouch for the specifics."

Note: Explicit reservation about specifics; intent about naming RSA cannot be inferred.

```python
def check(ctx):
    q = ctx.find('framing', r'he explicitly declines to vouch for the specifics')
    return ctx.need('framing', q, 'Explicit reservation about specifics; intent about naming RSA cannot be inferred.')
```

### PASS · ot1-company-reported (objection, Cogentic papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'Company-posted preprints in a public repository')
    p = r'(?:Google(?: Research)? (?:says|reports|claims)|company[- ]reported|according to Google|it says its Cogentic harness)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'Identify company reporting.')
```

### PASS · ot4-lean-pending (objection, Cogentic papers)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'announced Lean formalizations are not yet released')
    p = r'(?:Lean[^.!?]{0,100}(?:unreleased|not (?:yet )?(?:been )?released)|(?:not (?:yet )?released|unreleased)[^.!?]{0,100}Lean)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'State that the Lean artifacts are not yet released.')
```

### PASS · ot7-warning-hearsay (objection, RSA rumors)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Shtetl-Optimized (Scott Aaronson)): Aaronson's own blog; it establishes only what he says he has heard, and he explicitly declines to vouch for the specifics."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'only what he says he has heard')
    p = r'(?:Aaronson|he (?:wrote|said|says))[^.!?]{0,160}(?:heard|second[ -]hand|from multiple reliable sources)'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'Attribute the warning to what Aaronson heard.')
```

### PASS · ot8-warning-specifics (objection, RSA rumors)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Shtetl-Optimized (Scott Aaronson)): Aaronson's own blog; it establishes only what he says he has heard, and he explicitly declines to vouch for the specifics."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'explicitly declines to vouch for the specifics')
    p = r'(?:(?:declin\w*|refus\w*|would not|did not)[^.!?]{0,80}(?:vouch|name RSA|claim[^.!?]{0,50}factor)|specifics[^.!?]{0,60}(?:uncertain|mangled))'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'Keep Aaronson’s disclaimer about specifics.')
```

### PASS · ot9-no-lab-publication (objection, RSA rumors)

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "No lab has published or confirmed such a result."

Note: The artifact carries the caveat this check looks for.

```python
def check(ctx):
    q = ctx.find('framing', r'No lab has published or confirmed such a result')
    p = r'(?:no (?:frontier )?labs? (?:has |have )?(?:publicly )?published|unpublished (?:crypto|factoring|RSA)|unreleased cryptogra\w* (?:results|bombshells))'
    return ctx.ok('framing', q) if ctx.art_has(p) else ctx.fail('framing', q, 'State the rumored result is unpublished.')
```

### PASS · t03-six-papers (number, Cogentic papers)
> Claim: six new math papers

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "STORY: Google Research posts six Cogentic papers, produced with Gemini 4, claiming results on factoring, the log-rank conjecture and more"

Note: New postings; does not certify novelty or correctness of results.

```python
def check(ctx):
    return ctx.require('framing', r'Google Research posts six Cogentic papers, produced with Gemini 4, claiming results on factoring, the log-rank conjecture', note='New postings; does not certify novelty or correctness of results.')
```

### PASS · t04-new-papers (qualifier, Cogentic papers)
> Claim: new math papers

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "STORY: Google Research posts six Cogentic papers, produced with Gemini 4, claiming results on factoring, the log-rank conjecture and more"

Note: Newly posted papers on mathematical topics.

```python
def check(ctx):
    return ctx.require('framing', r'posts six Cogentic papers, produced with Gemini 4, claiming results on factoring, the log-rank conjecture', note='Newly posted papers on mathematical topics.')
```

### PASS · t06-harness-model (qualifier, Cogentic papers)
> Claim: its Cogentic harness running on Gemini 4

Source ([primary-google-cogentic-six-math-papers](https://raw.githubusercontent.com/google-research/google-research/master/cogentic_research_papers/logrank_conjecture/README.md)): "agentic framework for mathematical discovery, using Gemini 4 as the base model. … The Cogentic harness was built by Yang Cai, Vineet Gupta, Yanchen Jiang, Christopher Liaw, Aranyak Mehta, Grigoris Velegkas, and Di Wang (Google Research and Google DeepMind"

Note: Google-associated team; one author also has a Yale affiliation.

```python
def check(ctx):
    return ctx.require('google', r'using Gemini 4 as the base model', r'The Cogentic harness was built by[\s\S]*Google Research\s+and Google DeepMind', note='Google-associated team; one author also has a Yale affiliation.')
```

### PASS · t10-lean-status (attribution, Cogentic papers)
> Claim: Google has not yet released its claimed Lean 4 formalizations

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released."

Note: Lean 4 (`v4.33.0`) formalization of the entire proof has also been completed and will be released in a companion submission

```python
def check(ctx):
    q = ctx.find('google', r'Lean 4[\s\S]*will be released in a companion\s+submission')
    if not q: return ctx.need('google', None, 'Need Lean version and company release statement.')
    return ctx.require('framing', r'Google Research .*announced Lean formalizations are not yet released', note=q)
```

### PASS · t11-not-yet-released (qualifier, Cogentic papers)
> Claim: not yet released

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released."

```python
def check(ctx):
    return ctx.require('framing', r'announced Lean formalizations are not yet released')
```

### PASS · t12-claimed-lean (qualifier, Cogentic papers)
> Claim: claimed Lean 4 formalizations

Source ([scan-framing](https://www.signalandnoise.email/content/daily-state/2026-11-26/audit/sources/2026-11-26/scan-framing.txt)): "framing (Google Research (GitHub)): Company-posted preprints in a public repository; no peer review, and the announced Lean formalizations are not yet released."

Note: Lean 4 (`v4.33.0`) formalization of the entire proof has also been completed

```python
def check(ctx):
    q = ctx.find('google', r'Lean 4[\s\S]*entire proof has also been completed')
    if not q: return ctx.need('google', None, 'Need versioned company claim.')
    return ctx.require('framing', r'announced Lean formalizations are not yet released', note=q)
```

### PASS · t15-frontier-labs (qualifier, RSA rumors)
> Claim: frontier labs

Source ([x-kimmonismus](https://x.com/kimmonismus/status/2125602411540566221)): "Scott Aaronson says he's heard OpenAI or Anthropic may have found a way to factor large numbers in polynomial time."

Note: Identifies the labs in the rumor, not a confirmed result.

```python
def check(ctx):
    return ctx.require('kimmonismus', r'OpenAI or Anthropic may have found a way to factor large numbers', note='Identifies the labs in the rumor, not a confirmed result.')
```

### PASS · t18-aaronson-confidence (attribution, RSA rumors)
> Claim: he wrote he is virtually certain from multiple reliable sources that labs are holding unreleased cryptographic bombshells

Source ([x-andrewcurran_](https://x.com/AndrewCurran_/status/2125589468786909510)): "Scott Aaronson states he is virtually certain, from multiple reliable sources, that frontier labs hold unreleased cryptography "bombshells." He is far less confident about the exact nature-such as a practical polynomial-time"

Note: Secondary account of his statement, not independent confirmation.

```python
def check(ctx):
    return ctx.require('andrewcurran_', r'Scott Aaronson states he is virtually certain, from multiple reliable sources, that frontier labs hold unreleased cryptography ["“]bombshells', note='Secondary account of his statement, not independent confirmation.')
```

### PASS · t19-virtually-certain (qualifier, RSA rumors)
> Claim: virtually certain

Source ([x-andrewcurran_](https://x.com/AndrewCurran_/status/2125589468786909510)): "Scott Aaronson states he is virtually certain, from multiple reliable sources, that frontier labs hold unreleased cryptography "bombshells." He is far less confident about the exact nature-such as a practical polynomial-time"

Note: Confidence concerns unspecified bombshells.

```python
def check(ctx):
    return ctx.require('andrewcurran_', r'Scott Aaronson states he is virtually certain.*unreleased cryptography', note='Confidence concerns unspecified bombshells.')
```

### PASS · t20-multiple-sources (qualifier, RSA rumors)
> Claim: multiple reliable sources

Source ([x-andrewcurran_](https://x.com/AndrewCurran_/status/2125589468786909510)): "Scott Aaronson states he is virtually certain, from multiple reliable sources, that frontier labs hold unreleased cryptography "bombshells." He is far less confident about the exact nature-such as a practical polynomial-time"

Note: Attribution of confidence, not authentication.

```python
def check(ctx):
    return ctx.require('andrewcurran_', r'Scott Aaronson states he is virtually certain, from multiple reliable sources', note='Attribution of confidence, not authentication.')
```

### PASS · t21-unreleased (qualifier, RSA rumors)
> Claim: unreleased

Source ([x-andrewcurran_](https://x.com/AndrewCurran_/status/2125589468786909510)): "Scott Aaronson states he is virtually certain, from multiple reliable sources, that frontier labs hold unreleased cryptography "bombshells." He is far less confident about the exact nature-such as a practical polynomial-time"

Note: Within the reported warning only.

```python
def check(ctx):
    return ctx.require('andrewcurran_', r'Scott Aaronson states .*frontier labs hold unreleased cryptography', note='Within the reported warning only.')
```

### PASS · tc01-citation (citation, takeaway 1)

Note: Takeaway 1 cites https://github.com/google-research/google-research/commit/4a7bc8ab0bc770e71a259b7966c500496b99010a, which is listed in the episode sources.json.

```python
def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 1 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 1 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))
```

### PASS · tc02-citation (citation, takeaway 2)

Note: Takeaway 2 cites https://scottaaronson.blog/?p=10379, which is listed in the episode sources.json.

```python
def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 2 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 2 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))
```
